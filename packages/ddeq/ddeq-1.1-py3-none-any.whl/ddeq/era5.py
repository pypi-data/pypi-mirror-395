import itertools
import os

import cdsapi
import numpy as np
import pandas as pd
import scipy
import scipy.interpolate
import xarray as xr

import ddeq

from typing import Tuple, Union, List
from pathlib import Path

g = scipy.constants.g
R = 287.058

# define some variables for the calculation of the weighted wind profile
lower_bounds = np.array([170, 310, 470, 710])  # height bound of GNFR-A weights in m
upper_bounds = np.array([310, 470, 710, 990])  # height bound of GNFR-A weights in m
values = np.array([0.08, 0.46, 0.29, 0.17])  # relative GNFR-A weights
bounds = np.append(lower_bounds, upper_bounds[-1])
width = np.diff(bounds)


def open(filename):
    """
    Open ERA5 file (sng, lvl or pres) and prepare for computing effective
    wind speed.
    """
    # Read single layer and change longitude from [0,360] to [-180,+180]
    file = xr.open_dataset(filename)
    file = file.assign_coords(longitude=(file.longitude + 180) % 360 - 180)
    file = file.sortby("longitude")

    # Rename variables
    file = file.rename_dims(longitude="lon", latitude="lat")
    file = file.rename_vars(longitude="lon", latitude="lat")

    if "valid_time" in file.dims:
        file = file.rename_dims(valid_time="time")
        file = file.rename_vars(valid_time="time")

    # Rename "level" to "model_level" or "pressure_level" for old ERA-5 files
    if "level" in file.dims:
        new_name = file["level"].attrs["long_name"]
        if new_name == "model_level_number":
            new_name = "model_level"
        assert new_name in ["model_level", "pressure_level"]
        file = file.rename_dims(level=new_name)
        file = file.rename_vars(level=new_name)

    return file


def read_blh(filename, extent=None):
    sng = open(filename)

    if extent is not None:
        north, west, south, east = [extent[s] for s in ["north", "west", "south", "east"]]
        west_east = (west <= sng.lon) & (sng.lon < east)
        south_north = (south <= sng.lat) & (sng.lat < north)
        sng = sng.sel(lon=west_east, lat=south_north)

    return sng[["blh"]]


def read(
    sng_filename=None,
    lvl_filename=None,
    method=None,
    levels=None,
    heights=None,
    weights=None,
    level_units="",
    times=None,
    extent=None,
    sources=None,
    lons=None,
    lats=None,
    height_offset=None,
):
    """\
    Read and prepare ERA-5 data using different methods.

    Parameters
    ----------
    sng_filename : str
        Filename to ERA-5 data on single model level with the following
        variables:
        - lon: longitude
        - lat: latitude
        - sp: surface pressure
        - z: geopotential
        - u10: u-wind at 10 m
        - v10: v-wind at 10 m
        - u100: u-wind at 100 m
        - v100: v-wind at 100 m
        - blh: boundary layer height

    lvl_filename : str, optional
        Filename of ERA-5 data on model or pressure levels with the
        following variables:
        - z: geopotential (only pressure levels)
        - u: u-wind
        - v: v-wind
        - t: temperature (only model levels)
        - q: specific humidity (only model levels)

    method : str
        Method used to compute the effective wind speed:
        - "10m"      Wind speed at 10 meters
        - "100m"     Wind speed at 100 meters
        - "levels"   Average of model/pressure levels that are provided by
                     the `levels` parameter. If `level_units` is "index",
                     levels are selected using the "isel" method, while
                     otherwise the sel method is used.
        - "heights"  Wind for heights given by `heights` parameter.
        - "pbl-mean" Mean wind in the planetary boundary layer.
        - "pbl-mid"  Wind at the middle of planetary boundary layer.
        - "GNFR-A"   Wind weighted by emission profile for the
                     public power sector (i.e. GNFR category A).

    levels : int, float
        Model/pressure levels used with "levels" method (see method
        description).

    level_units : str,
        Units of values provided by `levels` parameter (see method
        description).

    heights : number
        Heights used for interpolation with "heights" method.

    times : pd.Timestamp
        Select times from ERA5 nearest to the provided times.

    extent : dict
        Clip ERA5 field to provided extent using -180,+180 for longitude
        using dict with "north", "west", "south", "east".

    sources : xr.Dataset
        Source dataset with longitude and latitude of sources. If provided,
        winds will be interpolated to source locations.

    lons : xr.DataArray
        Longitude on which model fields are interpolated.

    lats : xr.DataArray
        Latitude on which model fields are interpolated.

    height_offset : xr.DataArray
        Offset for height (TODO).

    Return
    ------
    xr.Dataset (dims: time, lon, lat) or (time, source)
        Dataset of effective wind speed either on a longitude-latitude grid
        or for each source.
    """

    # Open files
    sng = None if sng_filename is None else open(sng_filename)
    if lvl_filename is None:
        lvl = None
    else:
        lvl = open(lvl_filename)
        vcoord = "pressure_level" if "pressure_level" in lvl.dims else "model_level"

    # Depending on method only keep variables that are necessary
    # (for quicker interpolation).
    if method == "10m":
        sng = sng[["u10", "v10"]]
        lvl = None
    elif method == "100m":
        sng = sng[["u100", "v100"]]
        lvl = None
    elif method == "levels":
        sng = None
        if "z" in lvl:
            lvl = lvl[["u", "v", "z"]]
        else:
            lvl = lvl[["u", "v"]]

    elif method == "level-mean":
        sng = None
        lvl = lvl[["u", "v"]]
    elif method in ["blh-mean", "pbl-mean"]:
        if vcoord == "model_level":
            pass # TODO
        else:
            sng = sng[["blh", "z", "u10", "v10", "u100", "v100"]]
            lvl = lvl[["u", "v", "z"]]
    else:
        pass

    # crop to extent (makes pre-processing faster)
    if extent is not None:
        sng = None if sng is None else crop_extent(sng, extent)
        lvl = None if lvl is None else crop_extent(lvl, extent)

    # Interpolate time (TODO: add option for linear interpolation that
    # supports extrapolation)
    if times is not None:
        times = xr.DataArray(np.atleast_1d(times), dims="time")

        if sng is not None:
            sng = sng.interp(time=times, method="nearest")
        if lvl is not None:
            lvl = lvl.interp(time=times, method="nearest")

    # Interpolate to source locations
    if sources is not None:
        lons = sources["lon"]
        lats = sources["lat"]

        if extent is not None:
            north, west, south, east = [extent[s] for s in ["north", "west", "south", "east"]]
            inside = (west <= lons) & (lons < east) & (south <= lats) & (lats < north)
            lons, lats = lons[inside], lats[inside]

        if len(lons) == 0 or len(lats) == 0:
            return None

    if lons is not None and lats is not None:
        if sng is not None:
            sng = sng.interp(lon=lons, lat=lats)

        if lvl is not None:
            lvl = lvl.interp(lon=lons, lat=lats)

    # effective wind speed
    if method in ["10m", "100m"]:
        wind = sng.rename({f"u{method[:-1]}": "U", f"v{method[:-1]}": "V"})
        description = f"U- and V-wind component at {method}"

    elif method == "levels":
        if level_units == "index":
            wind = lvl.isel({vcoord: levels})
        else:
            wind = lvl.sel({vcoord: levels})

        if vcoord in wind.dims:
            wind = wind.mean(vcoord)

        wind = wind.rename_vars({"u": "U", "v": "V"})
        description = f"U- and V-wind average for levels {levels}."

    elif method in ["pbl-mean", "blh-mean"]:
        if vcoord == "model_level":
            lvl, sng = compute_height_levels(lvl, sng, height_offset)
        else:
            lvl = stack_pressure_and_single_levels(lvl, sng, height_offset)

        # Oversample from ground to PBL height and average
        heights = sng.blh * xr.DataArray(np.linspace(0,1,21), dims="height_index")
        wind = interp_heights(heights, lvl).mean("height_index")

        wind["blh"] = sng["blh"].copy()
        description = f"Average U- and V-wind below boundary layer height."

    elif method.lower() in ["gnfra", "gnfr-a", "gnfr_a"]:
        if "model_level" in lvl:
            lvl, sng = compute_height_levels(lvl, sng, height_offset)
        else:
            lvl = stack_pressure_and_single_levels(lvl, sng, height_offset)

        wind = calculate_gnfra_weighted_winds(lvl, sng)
        description = "Weighted average for U- and V-wind using GNFR-A emission profile."

    elif method.lower() in ["height", "heights", "pbl-mid", "blh-mid"]:
        if method.lower() in ["pbl-mid", "blh-mid"]:
            heights = sng["blh"] / 2.0
            description = "U- and V-wind at middle of planet boundary layer."
        else:
            description = f"U- and V-wind at a height of {heights} m."

        # compute height levels
        if vcoord == "model_level":
            lvl, sng = compute_height_levels(lvl, sng, height_offset)
        else:
            lvl = stack_pressure_and_single_levels(lvl, sng, height_offset)

        wind = interp_heights(heights, lvl)

    else:
        raise NotImplementedError

    # Add wind speed
    wind = _add_wind_speed(wind, method, description)

    return wind


def crop_extent(lvl, extent):
    north, west, south, east = [extent[s] for s in ["north", "west", "south", "east"]]
    west_east = (west <= lvl.lon) & (lvl.lon < east)
    south_north = (south <= lvl.lat) & (lvl.lat < north)
    return lvl.sel(lon=west_east, lat=south_north)


def _convert_time(time: Union[np.datetime64, xr.DataArray]) -> pd.Timestamp:
    """Convert time to pandas timestamp format."""
    if isinstance(time, xr.DataArray):
        return pd.Timestamp(time.to_pandas())
    elif isinstance(time, np.datetime64):
        return pd.Timestamp(time)
    return time


def _set_area(coords: Union[str, Tuple[float, float]]) -> List[float]:
    """Set area based on global or specific coordinates."""
    if coords == "global":
        return [90, -180, -90, 180]
    elif isinstance(coords, tuple):
        lon, lat = coords
        return [lat - 0.251, lon - 0.251, lat + 0.251, lon + 0.251]
    raise ValueError(
        "Coordinates should either be 'global' or a tuple of (longitude, latitude)"
    )



def _add_wind_speed(wind: xr.Dataset, method: str, description: str):
    """Add wind speed and direction attributes to the dataset."""

    attrs = {
        "CREATOR": "ddeq.era5",
        "DATE_CREATED": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        "ORIGIN": "ERA-5",
        "METHOD": method,
        "DESCRIPTION": description,
    }

    wind.attrs.update(attrs)

    wind["speed"] = xr.DataArray(
        np.sqrt(wind.U**2 + wind.V**2), attrs={"units": "m s-1"}
    )

    if "U_precision" in wind.data_vars and "V_precision" in wind.data_vars:
        wind["speed_precision"] = xr.DataArray(
            np.sqrt(wind.U_precision**2 + wind.V_precision**2), attrs={"units": "m s-1"}
        )
    else:
        wind["speed_precision"] = xr.DataArray(
            np.full_like(wind.U, 1.0), dims=wind.speed.dims, attrs={"units": "m s-1"}
        )
    wind["direction"] = xr.DataArray(
        ddeq.wind.calculate_wind_direction(wind.U, wind.V), attrs={"units": "°"}
    )

    return wind


def get_gnfra_profile(
    heights: xr.DataArray,
    lower_bounds: Union[list, np.ndarray] = [170, 310, 470, 710],
    upper_bounds: Union[list, np.ndarray] = [310, 470, 710, 990],
    weights: Union[list, np.ndarray] = [0.08, 0.46, 0.29, 0.17],
):
    lower_bounds = np.array(lower_bounds)
    upper_bounds = np.array(upper_bounds)
    weights = np.array(weights)

    bounds = np.append(lower_bounds, upper_bounds[-1])

    def func(s):
        # get values on model level boundaries
        if bounds[0] <= s < bounds[-1]:
            i = np.searchsorted(bounds, s, side="right")
            return weights[i - 1]
        else:
            return 0.0

    func_vec = np.vectorize(func)

    return func_vec(heights)



def vertically_weighted_mean(
    heights: xr.DataArray,
    values: xr.DataArray,
    vcoord: str,
    lower_bounds: Union[list, np.ndarray] = [170, 310, 470, 710],
    upper_bounds: Union[list, np.ndarray] = [310, 470, 710, 990],
    weights: Union[list, np.ndarray] = [0.08, 0.46, 0.29, 0.17],
):
    """
    Compute vertically weighted mean `values` on `height` levels. Weights are
    given by `lower_bound`, `upper_bounds` and `weights`, where default is the
    GNFR-A emissions profile.
    """
    # define some variables for the calculation of the weighted wind profile
    lower_bounds = np.array(lower_bounds)
    upper_bounds = np.array(upper_bounds)
    weights = np.array(weights)

    # compute weights (by quick interpolation)
    z2 = np.linspace(0, 1000, 501)
    w2 = get_gnfra_profile(z2, lower_bounds, upper_bounds, weights)

    ifunc = scipy.interpolate.interp1d(z2, w2, bounds_error=False, fill_value=0.0)
    w2 = ifunc(heights)

    weights = xr.DataArray(
        w2,
        dims=heights.dims,
        attrs={"description": "relative GNFR-A weights"}
    )
    weights = weights / weights.sum(dim=vcoord, keep_attrs=True)

    values = (values * weights).sum(
        dim=vcoord, keep_attrs=True
    ) / weights.sum(dim=vcoord, keep_attrs=True)

    return values


def calculate_gnfra_weighted_winds(
    lvl, sng,
    lower_bounds: Union[list, np.ndarray] = [170, 310, 470, 710],
    upper_bounds: Union[list, np.ndarray] = [310, 470, 710, 990],
    weights: Union[list, np.ndarray] = [0.08, 0.46, 0.29, 0.17],
) -> xr.Dataset:
    """
    Compute a vertically averaged wind speed based on a GNFR-A weighted wind.

    lower_bounds:
        height of lower bound of GNFR-A weights in m
    upper_bounds:
        height of upper bound of GNFR-A weights in m
    weights:
        relative GNFR-A weights [-]

    Note that the current implementation is quite slow and thus only recommended
    for small regions.
    """
    # vertical coordindate in dataset
    vcoord = "pressure_level" if "pressure_level" in lvl.dims else "model_level"

    u_attrs = lvl.u.attrs
    v_attrs = lvl.v.attrs

    # computed vertically-weighted winds
    wind = xr.Dataset()
    wind["U"] = vertically_weighted_mean(lvl.h, lvl.u, vcoord)
    wind["V"] = vertically_weighted_mean(lvl.h, lvl.v, vcoord)

    wind["U"].attrs.update(u_attrs)
    wind["U"].attrs.update({"units": "m s-1", "description": "GNFR-A weighted u-wind"})

    wind["V"].attrs.update(v_attrs)
    wind["V"].attrs.update({"units": "m s-1", "description": "GNFR-A weighted v-wind"})

    return wind


def compute_height_levels(
    lvl: xr.Dataset, sng: xr.Dataset, height_offset: xr.DataArray = 0.0
) -> xr.Dataset:
    """
    Compute the geometric height of the ERA5 model levels using the hypsometric equation

    lvl : xr.Dataset
        ERA5 data on model levels
    sng : xr.Dataset
        ERA5 data on the surface
    Returns
    -------
    xr.Dataset
        Dataset containing computed heights of model levels.
    """
    if "sp" not in sng:
        sng["sp"] = np.exp(sng["lnsp"])

    a, b = read_l137_a_and_b_parameter()

    lower_value = np.nanmin(lvl.model_level.values.astype(int)) - 1
    level_bound = np.insert(lvl.model_level.values.astype(int), 0, lower_value)

    lvl["a"] = xr.DataArray(
        a[level_bound], dims=["level_bound"], attrs={"units": "Pa"}
    )
    lvl["b"] = xr.DataArray(b[level_bound], dims=["level_bound"], attrs={"units": 1})

    # calculate pressure
    lvl["p_bound"] = lvl.a + lvl.b * sng.sp
    lvl["p_bound"].attrs = {"units": "Pa", "long_name": "pressure at level boundary"}
    lvl["p_bound"] = lvl["p_bound"].transpose(
        *["level_bound" if d == "model_level" else d for d in lvl.t.dims]
    )
    lvl["p_mid"] = xr.DataArray(
        data=0.5
        * (
            lvl["p_bound"].isel(level_bound=slice(1, None))
            + lvl["p_bound"].isel(level_bound=slice(None, -1))
        ),
        dims=lvl.t.dims,
        attrs={"units": "Pa", "long_name": "pressure at level middle"},
    )

    # calculate virtual temperature
    lvl["t_v"] = lvl.t * (1.0 + 0.609133 * lvl.q)
    lvl["t_v"].attrs = {"units": "K", "long_name": "virtual_temperature"}

    # calculate thickness of layer with hypsometric equation
    lvl["dh"] = (
        R
        * lvl.t_v
        / g
        * np.log(lvl.p_bound).diff("level_bound").values
    )
    lvl["dh"].attrs = {"units": "m", "long_name": "thickness_of_model_level"}

    # height at upper boundary of level
    lvl["h"] = (
        lvl["dh"].isel(model_level=slice(None, None, -1)).cumsum(dim="model_level")
    )
    lvl["h"] = lvl.h - lvl.dh / 2  # height at the middle of the level
    lvl["h"].attrs = {"units": "m", "long_name": "height_of_model_level"}

    # height offset
    if height_offset is not None:
        lvl["h"] -= height_offset

    return lvl, sng


def read_l137_a_and_b_parameter(
    filename: Union[str, Path] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Read ERA5 model level definitions and return 'a' and 'b' parameters for
    computing vertical levels of ERA5 model:
        ph = a + b * surface_pressure

    Parameters
    ----------
    filename : Union[str, Path], optional
        File name of the CSV containing level definitions. Default is a predefined path.
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Arrays of 'a' and 'b' coefficients for computing vertical levels.
    """
    if filename is None:
        filename = Path(ddeq.DATA_PATH) / "ERA5_L137_model_level_definitions.csv"
    level_definitions = pd.read_csv(filename, index_col=0)
    a = np.array(level_definitions["a [Pa]"])
    b = np.array(level_definitions["b"])
    return a, b


def interp_heights(heights, lvl, vars=("u", "v"), sfc=None, vcoord=None):
    """
    Quick linear interpolation of u and v-wind on heights. Extrapolation is used for heights
    below lowest level.

    The function requires more testing.
    """
    results = xr.Dataset(attrs=lvl.attrs)

    if vcoord is None:
        vcoord = "model_level" if "model_level" in lvl.h.dims else "pressure_level"

    if np.any(np.diff(lvl.h[dict((d, 0) for d in lvl.h.dims if d != vcoord)]) >= 0):
        raise ValueError("Height needs to decrease with index.")

    i = ((lvl.h - heights) < 0).argmax(vcoord)

    ha = lvl.h.isel({vcoord: i-1})
    hb = lvl.h.isel({vcoord: i})

    for v in vars:
        ua = lvl[v].isel({vcoord: i-1})
        ub = lvl[v].isel({vcoord: i})
        uh = ua + (ub - ua) / (hb - ha) * (heights - ha)

        results[v.upper()] = xr.DataArray(uh)

    return results

    # extrapolation where index 0
    #uh.values[i==0] = lvl.u.isel({vcoord: -1}).values[i==0]
    #vh.values[i==0] = lvl.v.isel({vcoord: -1}).values[i==0]

    return xr.Dataset({"U": uh, "V": vh}, attrs=lvl.attrs)


def stack_pressure_and_single_levels(lvl, sng, height_offset=0.0):
    """
    Stack winds on pressure levels and 10/100m wind fields. Since wind on
    pressure level can be below 100 m for high surface elevation, this
    requires resorting all variables. The ERA5 product on pressure level
    provides values below the surface, which are set to nan here.
    """
    # Invert pressure levels from top to bottom
    lvl = lvl.isel(pressure_level=slice(None,None,-1)).copy()

    # Compute height above surface (which for some reason can be negative)
    lvl["h"] = (lvl["z"] - sng["z"]) / ddeq.era5.g
    axis = lvl.h.dims.index("pressure_level")

    # compute 10-m winds
    u10 = sng[["u10", "v10"]].rename_vars(u10="u", v10="v").copy()
    u10["pressure_level"] = 1012.0
    u10 = u10.set_coords('pressure_level').expand_dims("pressure_level", axis)
    u10["h"] = xr.DataArray(10.0)

    # compute 100-m winds
    u100 = sng[["u100", "v100"]].rename_vars(u100="u", v100="v").copy()
    u100["pressure_level"] = 1001.0
    u100 = u100.set_coords('pressure_level').expand_dims("pressure_level", axis)
    u100["h"] = xr.DataArray(100.0)

    # concatenate
    lvl = lvl.assign_coords(pressure_level=lvl.pressure_level)
    lvl = xr.concat([lvl, u100, u10], dim="pressure_level")

    # sort to have monotone decreasing height
    indices = np.flip(lvl.h.argsort(axis=axis).values, axis=axis)

    elements = [range(n) if i != axis else [Ellipsis]
                for i,n in enumerate(lvl.h.shape)]

    for i in itertools.product(*elements):
        m = indices[i]
        j = tuple(k if j != axis else m for j,k in enumerate(i))

        for var in "ztuvh":
            if var in lvl:
                lvl[var].values[i] = lvl[var].values[j]

    # 
    if height_offset is not None:
        lvl["h"] = lvl["h"] - height_offset
    # set values below surface to nan
    #for var in "ztuv":
    #    if var in lvl:
    #        lvl[var].values[lvl.h.values <= 0] = np.nan

    return lvl

