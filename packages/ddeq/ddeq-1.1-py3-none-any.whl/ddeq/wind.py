import datetime
import os
import warnings
import ddeq.era5_v2
import ddeq.misc
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from scipy.interpolate import RectSphereBivariateSpline, SmoothSphereBivariateSpline
from typing import Union, List, Tuple, Optional
from pathlib import Path

import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import scipy
import scipy.integrate
import scipy.interpolate
import xarray as xr

from ddeq.smartcarb import DOMAIN
import ddeq


################################## READ WINDS ##################################
def read_at_sources(
    wind: xr.Dataset,
    sources: xr.Dataset,
    lat_name: str = "lat",
    lon_name: str = "lon",
    interpolation_method: str = "linear",
    interpolation_time: Optional[
        Union[
            xr.DataArray,
            pd.Timestamp,
            pd.DatetimeIndex,
            datetime.datetime,
            pd.DatetimeIndex,
        ]
    ] = None,
    time_name: str = "time",
    **interp_kwargs,
) -> xr.Dataset:
    """
    Read wind data at provided sources and optionally interpolate over time.

    Parameters
    ----------
    wind : xr.Dataset
        A dataset containing the wind field information.

    sources : xr.Dataset
        A dataset containing the source information, typically with lat and lon coordinates.

    lat_name : str, optional
        Name of the latitude coordinate in the sources dataset, by default "lat".

    lon_name : str, optional
        Name of the longitude coordinate in the sources dataset, by default "lon".

    interpolation_method : str, optional
        Method to use for interpolation (e.g., "linear", "nearest"), by default "linear".

    interpolation_time : Optional[Union[xr.DataArray, pd.Timestamp, pd.DatetimeIndex, datetime.datetime]], optional
        The time(s) to interpolate wind data to. Can be a pandas timestamp, datetime object,
        xarray DataArray, or pandas date range, by default None.

    time_name : str, optional
        Name of the time coordinate in the wind dataset, by default "time".

    **interp_kwargs
        Additional keyword arguments to pass to xarray's interp function (e.g., "fill_value").

    Returns
    -------
    xr.Dataset
        Wind dataset with the wind information interpolated at each source location.
    """

    winds = {}
    for name, source in sources.groupby("source", squeeze=False):

        lon_s, lat_s, _ = ddeq.sources.get_location(source)
        lon_s = float(lon_s[0])
        lat_s = float(lat_s[0])
        coords_to_interpolate = {lat_name: lat_s, lon_name: lon_s}
        wind_subset = wind.interp(
            coords_to_interpolate, method=interpolation_method, **interp_kwargs
        )

        winds[name] = wind_subset

        winds[name]["source"] = name
        winds[name]["lon_source"] = lon_s
        winds[name]["lat_source"] = lat_s

    wind_at_sources = xr.concat(
        [winds[name].set_coords("source") for name in sorted(winds.keys())],
        dim="source",
    )

    # If interpolation_time is provided, interpolate the dataset in time
    if interpolation_time is not None and time_name is not None:
        wind_at_sources = temporal_interpolation(
            wind_at_sources,
            interpolation_time,
            time_name,
            interpolation_method,
            **interp_kwargs,
        )

    return wind_at_sources


def read_smartcarb(
    time, lon, lat, radius=None, data_path=".", method="linear", average=False
):
    """\
    Read SMARTCARB winds at given location at given `time`. The location is
    interpolated from SMARTCARB model grid to given `lon` and `lat`. If `lon`
    and `lat` are given as scalar, it is possible to provide a radius around
    location for which are extracted.

    radius :: size of square around location given in rotated degrees used
    for averaging
    data_path :: path to SMARTCARB wind fields
    method :: interpolation method (used by xr.DataArray.interp method)
    average :: average extracted winds

    Return xr.Dataset with wind components `U` and `V` as well as `wind speed`
    and `direction`.
    """
    source = lon.source.copy()
    lon = np.atleast_1d(lon).flatten()
    lat = np.atleast_1d(lat).flatten()

    rlon, rlat, _ = np.transpose(
        DOMAIN.proj.transform_points(ccrs.PlateCarree(), lon, lat)
    )
    rlon = xr.DataArray(rlon, dims="source")
    rlat = xr.DataArray(rlat, dims="source")

    filename = time.round("h").strftime("SMARTCARB_winds_%Y%m%d%H.nc")
    filename = os.path.join(data_path, filename)

    with xr.open_dataset(filename) as nc:
        nc = nc.isel(time=0)

        if radius is not None:
            nc = nc.rolling(
                rlat=int(radius // 0.01),
                rlon=int(radius // 0.01)
            ).reduce(np.nanmean)

        u = nc["U_GNFR_A"].interp(rlon=rlon, rlat=rlat, method=method).data
        v = nc["V_GNFR_A"].interp(rlon=rlon, rlat=rlat, method=method).data


    wind = xr.Dataset()
    wind["lon"] = xr.DataArray(lon, dims="source")
    wind["lat"] = xr.DataArray(lat, dims="source")
    wind["U"] = xr.DataArray(u, dims="source")
    wind["V"] = xr.DataArray(v, dims="source")

    if average:
        u_std = wind["U"].std()
        v_std = wind["V"].std()
        wind = wind.mean("source")
        wind["U_std"] = u_std
        wind["V_std"] = v_std

    wind["speed"] = np.sqrt(wind.U**2 + wind.V**2)
    wind["speed_precision"] = 1.0  # FIXME
    wind["direction"] = ddeq.wind.calculate_wind_direction(wind.U, wind.V)

    wind["source"] = source

    # Add time dimension
    wind = wind.expand_dims(dim="time")
    wind["time"] = xr.DataArray([time], dims="time")

    return wind.where(np.isfinite(wind["U"]), drop=True)


def read_era5():
    # TODO
    pass


def read_gnfra_wind(
    folder,
    time,
    pattern="ERA5-gnfra-%Y%m%dt%H00.nc",
    latlims=None,
    lonlims=None,
    dataset="ERA5",
):
    """
    The function is called by the DIV method to obtain 2D wind fields from the
    SMARTCARB dataset or from ERA-5.

    The function will be replaced by `read_field' in future.

    Parameters
    ----------
    folder : str
        Path to folder where wind data is located.
    time : datetime object / pd.Timestamp
        time of the data.
    pattern : str (default: 'ERA5-gnfra-%Y%m%dt%H00')
        pattern of ERA5/SMARTCARB wind filename using `time.strftime(pattern)'
    latlims : tuple of float, optional
        Latitude limits to focus the data into a region. The default is None.
    lonlims : tuple of float, optional
        Latitude limits to focus the data into a region. The default is None.
    dataset : str, optional
        Dataset of wind data, choices are 'ERA5' or 'SMARTCARB'. The default is 'ERA5'.

    Returns
    -------
    ds : xarray dataset
        Wind data.
    """
    if (latlims is None and lonlims is not None) or (
        latlims is not None and lonlims is None
    ):
        raise ValueError(
            "Provide either both or neither of longitude and latitude limits"
        )

    # lims = True if both latlims and lonlims are provided
    lims = latlims is not None and lonlims is not None

    filename = os.path.join(folder, time.strftime(pattern))

    if dataset == "ERA5":
        ds = xr.open_dataset(filename)
        if lims:
            wlon, wlat = ds["longitude"][:].data, ds["latitude"][:].data
            lat_slice = (min(latlims) - 0.5 <= wlat) & (wlat <= max(latlims) + 0.5)
            lon_slice = (min(lonlims) - 0.5 <= wlon) & (wlon <= max(lonlims) + 0.5)
            ds = ds.where(
                xr.DataArray(
                    lat_slice[:, None] & lon_slice[None, :],
                    dims=["latitude", "longitude"],
                ),
                drop=True,
            )

    elif dataset == "SMARTCARB":
        # Read data
        ds = xr.open_dataset(
            filename, drop_variables=["height_10m", "U", "V", "U_10M", "V_10M", "HHL"]
        )

        # Reindex latitude into decreasing order, the highest latitude at
        # index 0 and the lowest at -1
        ds = ds.reindex(rlat=ds["rlat"][::-1].data)

        # If limits are given, slice data to the area of interest
        if lims:
            wlon, wlat = ds["lon"][:, :].data.flatten(), ds["lat"][:, :].data.flatten()
            shape = (ds["rlat"].size, ds["rlon"].size)

            top_right = np.unravel_index(
                np.argmin((wlon - max(lonlims)) ** 2 + (wlat - max(latlims)) ** 2),
                shape,
            )
            bottom_right = np.unravel_index(
                np.argmin((wlon - max(lonlims)) ** 2 + (wlat - min(latlims)) ** 2),
                shape,
            )
            bottom_left = np.unravel_index(
                np.argmin((wlon - min(lonlims)) ** 2 + (wlat - min(latlims)) ** 2),
                shape,
            )
            top_left = np.unravel_index(
                np.argmin((wlon - min(lonlims)) ** 2 + (wlat - max(latlims)) ** 2),
                shape,
            )

            row_index = np.arange(0, shape[0], 1, dtype=int)
            col_index = np.arange(0, shape[1], 1, dtype=int)

            lat_slice = (min(top_left[0], top_right[0]) - 1 <= row_index) & (
                row_index <= max(bottom_left[0], bottom_right[0]) + 1
            )
            lon_slice = (min(top_left[1], bottom_left[1]) - 1 <= col_index) & (
                col_index <= max(top_right[1], bottom_right[1]) + 1
            )

            ds = ds.where(
                xr.DataArray(
                    lat_slice[:, None] & lon_slice[None, :], dims=["rlat", "rlon"]
                ),
                drop=True,
            )

    return ds


############################## CALCULATE VARIABLES ##############################
def add_ensemble_spread(
    wind_data: xr.Dataset, wind_ensemble_spread: xr.Dataset, time_name: str = "time"
) -> xr.Dataset:
    """
    Add ensemble spread for U and V wind components to the dataset.

    Parameters:
    wind_data (xr.Dataset): Original wind data.
    wind_ensemble_spread (xr.Dataset): Ensemble spread data for wind components.

    Returns:
    xr.Dataset: Wind data with added ensemble spread.
    """
    wind_ensemble_spread_interp = temporal_interpolation(
        dataset=wind_ensemble_spread,
        interpolation_time=wind_data[time_name],
        time_name=time_name,
        fill_value="extrapolate",
    )

    wind_data["U_ensemble_spread"] = wind_ensemble_spread_interp.U
    wind_data["V_ensemble_spread"] = wind_ensemble_spread_interp.V

    return wind_data


def add_eff_wind_speed_uncertainty(wind_data: xr.Dataset, stability: str) -> xr.Dataset:
    """
    Add placeholders for method uncertainty for U and V wind components.

    Parameters:
    wind_data (xr.Dataset): Original wind data.

    stability (str):
        "stable", "neutral" or "unstable"

    Returns:
    xr.Dataset: Wind data with added method uncertainty as None.
    """
    if stability.lower == "stable":
        raise NotImplementedError(
            "Currently, only neutral and unstable cases are implemented."
        )

    for component in ["U", "V"]:
        uncertainty_var = f"{component}_eff_wind_speed_uncertainty"
        wind_data[uncertainty_var] = wind_data[component] * 0.16
        wind_data[uncertainty_var].attrs.update({
            "units": "m s-1",
            "description": (
                f"Estimated uncertainty of the effective wind speed for the {component} component. "
                "The uncertainty was obtained by assuming a 16% uncertainty relative to the original "
                f"{component} component wind speed."
            ),
            "stability": stability
        })

    return wind_data


def calc_wind_precision(
    wind_data: xr.Dataset, default_wind_speed_precision: float = 1.0
) -> xr.Dataset:
    """
    Calculate wind precision based on ensemble spread and/or method uncertainty.

    Parameters:
    wind_data (xr.Dataset): Wind data that may contain ensemble spread and/or uncertainty data.
    default_wind_speed_precision (float): Default precision value if no uncertainty or spread data available.

    Returns:
    xr.Dataset: Wind data with calculated precision for U and V components.
    """
    has_u_ensemble_spread = "U_ensemble_spread" in wind_data.data_vars
    has_v_ensemble_spread = "V_ensemble_spread" in wind_data.data_vars
    has_u_eff_wind_speed_uncertainty = (
        "U_eff_wind_speed_uncertainty" in wind_data.data_vars
    )
    has_v_eff_wind_speed_uncertainty = (
        "V_eff_wind_speed_uncertainty" in wind_data.data_vars
    )

    if has_u_ensemble_spread and has_v_ensemble_spread:
        if has_u_eff_wind_speed_uncertainty and has_v_eff_wind_speed_uncertainty:
            wind_data["U_precision"] = np.sqrt(
                wind_data["U_ensemble_spread"] ** 2
                + wind_data["U_eff_wind_speed_uncertainty"] ** 2
            )
            wind_data["V_precision"] = np.sqrt(
                wind_data["V_ensemble_spread"] ** 2
                + wind_data["V_eff_wind_speed_uncertainty"] ** 2
            )
            description = (
                "Precision based on model spread and effective wind speed uncertainty"
            )
        else:
            wind_data["U_precision"] = wind_data["U_ensemble_spread"]
            wind_data["V_precision"] = wind_data["V_ensemble_spread"]
            description = "Precision based on model spread only"
    elif has_u_eff_wind_speed_uncertainty and has_v_eff_wind_speed_uncertainty:
        wind_data["U_precision"] = wind_data["U_eff_wind_speed_uncertainty"]
        wind_data["V_precision"] = wind_data["V_eff_wind_speed_uncertainty"]
        description = "Precision based on effective wind speed uncertainty only"
    else:
        wind_data["U_precision"] = np.full(
            wind_data["U"].shape, default_wind_speed_precision
        )
        wind_data["V_precision"] = np.full(
            wind_data["U"].shape, default_wind_speed_precision
        )
        description = "Precision based on default value"

    wind_data.attrs.update({"precision_description": description})
    wind_data["U_precision"].attrs.update({"units": "m s-1"})
    wind_data["V_precision"].attrs.update({"units": "m s-1"})

    return wind_data


def calc_wind_speed(wind: xr.Dataset, method: str, description: str) -> xr.Dataset:
    """
    Calculate wind speed, precision, and direction, and add metadata.

    Parameters:
    wind (xr.Dataset): Wind data containing U and V components.
    method (str): Method used to calculate the wind speed.
    description (str): Description of the calculation method.

    Returns:
    xr.Dataset: Wind data with added speed, precision, and direction.
    """

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


def calculate_wind_direction(
    u: Union[float, np.ndarray], v: Union[float, np.ndarray]
) -> Union[float, np.ndarray]:
    return (270.0 - np.rad2deg(np.arctan2(v, u))) % 360


################################# MODIFY DATA #################################


def get_wind_at_location(winds, lon0, lat0):
    """\
    Obtain wind at location given by lon0 and lat0 in wind field (xr.Dataset)
    using nearest neighbor interpolation.
    """
    lat = winds["lat"].data
    lon = winds["lon"].data

    if np.ndim(lat) == 2:
        dist = (lat - lat0) ** 2 + (lon - lon0) ** 2
        i, j = np.unravel_index(dist.argmin(), dist.shape)
        return np.array([float(winds["U"][i, j]), float(winds["V"][i, j])])
    else:
        return np.squeeze([
            winds["U"].interp(lon=lon0, lat=lat0, method="nearest"),
            winds["V"].interp(lon=lon0, lat=lat0, method="nearest"),
        ])


def prepare_era5_data(wind_data: xr.Dataset) -> xr.Dataset:
    wind_data = ddeq.era5_v2.drop_era5_vars(data=wind_data)
    wind_data = ddeq.era5_v2.rename_era5_dims(data=wind_data)
    wind_data = ddeq.era5_v2.rename_era5_wind_vars(data=wind_data)

    return wind_data


def temporal_interpolation(
    dataset: xr.Dataset,
    interpolation_time: Union[
        xr.DataArray,
        pd.Timestamp,
        pd.DatetimeIndex,
        datetime.datetime,
        pd.DatetimeIndex,
    ],
    time_name: str,
    interpolation_method: str = "linear",
    **interp_kwargs,
) -> xr.Dataset:
    """
    Interpolate the given dataset over the specified time dimension.

    Parameters
    ----------
    dataset : xr.Dataset
        The dataset to be interpolated.

    interpolation_time : Union[xr.DataArray, pd.Timestamp, pd.DatetimeIndex, datetime.datetime, pd.DatetimeIndex]
        The time(s) to interpolate the dataset to. Can be a pandas timestamp, datetime object,
        xarray DataArray, or pandas date range.

    time_name : str
        Name of the time coordinate in the dataset.

    interpolation_method : str, optional
        Method to use for interpolation (e.g., "linear", "nearest"), by default "linear".

    **interp_kwargs
        Additional keyword arguments to pass to xarray's interp function (e.g., "fill_value").

    Returns
    -------
    xr.Dataset
        Dataset interpolated over the specified time dimension.
    """
    time_to_interpolate = {time_name: interpolation_time}
    return dataset.interp(
        time_to_interpolate, method=interpolation_method, kwargs=interp_kwargs
    )


def spatial_interpolation(data, wlon, wlat, lon, lat):
    """
    Interpolates wind in spatial dimensions to given pixels lon-lat pixels.

    Parameters
    ----------
    data : 1d-array or 2d-array
        Wind data.
    wlon : 1d-array or 2d-array
        Wind longitude coordinates.
    wlat : 1d-array or 2d-array
        Wind latitude coordinates.
    lon : 1d-array
        Longitude coordinates to be interpolated.
    lat : 1d-array
        Latitude coordinates to be interpolated.

    Returns
    -------
    interp : 1d-array
        Interpolated data values.
    """
    if wlon.ndim == 1 and wlat.ndim == 1:
        if data.ndim == 1:
            data = data.reshape((len(wlat), len(wlon)))
        # Interpolator in regular rectangular lat-lon grid
        interpolator = RectSphereBivariateSpline(
            np.deg2rad(90 - wlat), np.deg2rad(wlon), data
        )
    elif wlon.ndim == 2 and wlat.ndim == 2:
        wlon, wlat = wlon.flatten(), wlat.flatten()
        if data.ndim == 2:
            data = data.flatten()
        # Same weights for each data value, the square sum of weights is exactly one
        weights = np.ones(len(data)) / np.sqrt(len(data))
        # Interpolator on the irregular spherical lat-lon grid, requires smoothing factor s, for the chosen
        # weights the function to to optimized is the root-mean-square distance between the data and the spline
        interpolator = SmoothSphereBivariateSpline(
            np.deg2rad(90 - wlat.flatten()),
            np.deg2rad(wlon.flatten()),
            data,
            w=weights,
            s=1e-2 * len(data),
        )
    else:
        pass
    # Evaluate interpolator at requested coordinates
    interp = interpolator.ev(np.deg2rad(90 - lat), np.deg2rad(lon))
    return interp


def interpolate_to_polygons(along_distance: np.ndarray, wind: xr.Dataset) -> xr.Dataset:
    """
    Returns winds interpolated to along plume distances.

    Parameters
    ----------
    along_distance (np.array)
        distances along the plume.

    wind (xr.Dataset)
        dataset with wind speeds at different distances along the plume.
    """
    wind_at_polys = xr.Dataset()
    wind_at_polys["along"] = xr.DataArray(
        along_distance, dims="along", attrs={"units": "m"}
    )

    for name, values in wind.data_vars.items():
        wind_at_polys[name] = xr.DataArray(
            np.interp(along_distance, wind.distance, wind[name]),
            dims="along",
            attrs=wind[name].attrs,
        )

    return wind_at_polys


def integrate_along_curve(
    data: xr.Dataset, wind: xr.Dataset, source: xr.Dataset, curve=None, crs=None
) -> xr.Dataset:
    """
    Compute wind speed along curve using time series of wind speed at source.

    Parameters
    ----------
    data (xr.Dataset)
        dataset of remote sensing data

    wind (xr.Dataset)
        time series of wind speed at source

    source (xr.Dataset)
        source location

    curve (Poly2D, default: None)
        center curve (only needed for computing angle between wind vector
        and curve, which also requires to provide `crs'.

    crs (default: None)
        coordinate reference system
    """

    plume_length = np.max(data["xp"].values[data["detected_plume"]])
    earliest = pd.Timestamp(min(wind.time.values))

    # start at source in distance 0.0 at current time
    distance = 0.0
    seconds = 0.0
    current = pd.Timestamp(data.time.to_pandas())
    w = wind.sel(time=current, method="nearest")  # TODO: interpolate

    # at source location
    lon_source, lat_source, _ = ddeq.sources.get_location(source)
    seconds_since_emission = [0.0]
    lons = [float(lon_source)]
    lats = [float(lat_source)]
    distances = [0.0]
    in_plume = [True]
    wind_backwards = [w]

    angles = [
        (
            np.nan
            if curve is None
            else ddeq.misc.compute_angle_between_curve_and_wind(
                curve, w.direction, crs=crs
            ).item()
        )
    ]

    while distance < plume_length and (current - pd.Timedelta(hours=1)) > earliest:

        # next time is one hour earlier
        current -= pd.Timedelta(hours=1)

        # wind one hour earlier
        w = wind.sel(time=current, method="nearest")

        # mean wind speed between current and previous hour
        travel_speed = wind["speed"].interp(time=current + pd.Timedelta(hours=0.5))

        # distance to travel within one hour
        seconds += 3600
        distance += float(travel_speed) * 3600

        # nearest index in 2D field of satellite image
        nrow, nobs, dist = ddeq.misc.find_closest(data, ("xp", "yp"), (distance, 0))

        # add data
        lons.append(data.isel(nrows=nrow, nobs=nobs).lon.values)
        lats.append(data.isel(nrows=nrow, nobs=nobs).lat.values)

        distances.append(distance)
        seconds_since_emission.append(seconds)

        in_plume.append(distance <= plume_length)

        #  angle between curve and wind vector
        if curve is None:
            angles.append(np.nan)
        else:
            angles.append(
                ddeq.misc.compute_angle_between_curve_and_wind(
                    curve, w.direction, crs=crs
                ).item()
            )

        wind_backwards.append(w)

    # concat everything
    wind_backwards = xr.concat(wind_backwards, dim="time")
    wind_backwards["lon"] = xr.DataArray(lons, dims="time")
    wind_backwards["lat"] = xr.DataArray(lats, dims="time")
    wind_backwards["distance"] = xr.DataArray(
        distances, dims="time", attrs={"units": "m"}
    )
    wind_backwards["seconds_since_emission"] = xr.DataArray(
        seconds_since_emission, dims="time", attrs={"units": "s"}
    )
    wind_backwards["in_plume"] = xr.DataArray(in_plume, dims="time")
    wind_backwards["angle_between_curve_and_wind"] = xr.DataArray(
        angles, dims="time", attrs={"units": "degrees"}
    )

    return wind_backwards


################################## DEPRECATED ##################################
def read_coco2_era5(
    time,
    lon,
    lat,
    suffix=None,
    method="linear",
    path="/project/coco2/jupyter/WP4/ERA5/",
):
    """
    Read ERA-5 data from CoCO2 project on ICOS-CP.
    """
    warnings.warn(
        "CoCO2-specific function will be removed in future.",
        DeprecationWarning,
        stacklevel=2,
    )

    if suffix is None:
        filename = time.strftime("ERA5-gnfra-%Y%m%dt%H00.nc")
    else:
        filename = time.strftime(f"ERA5-gnfra-%Y%m%dt%H00_{suffix}.nc")
    filename = os.path.join(path, filename)

    lon = np.atleast_1d(lon)
    lat = np.atleast_1d(lat)

    with xr.open_dataset(filename) as nc:

        u = [
            float(
                nc["U_GNFR_A"].interp(longitude=lon[i], latitude=lat[i], method=method)
            )
            for i in range(lon.size)
        ]

        v = [
            float(
                nc["V_GNFR_A"].interp(longitude=lon[i], latitude=lat[i], method=method)
            )
            for i in range(lon.size)
        ]

    wind = xr.Dataset()
    wind["lon"] = xr.DataArray(lon, dims="index")
    wind["lat"] = xr.DataArray(lat, dims="index")
    wind["U"] = xr.DataArray(u, dims="index")
    wind["V"] = xr.DataArray(v, dims="index")

    wind["speed"] = np.sqrt(wind.U**2 + wind.V**2)
    wind["speed_precision"] = 1.0  # FIXME
    wind["direction"] = ddeq.wind.calculate_wind_direction(wind.U, wind.V)

    return wind


def read_wind_field(wind_data, source, lon, lat, radius):
    # TODO: combine with read_time_series & read_field
    """
    Read wind at a certain point from TROPOMI or MicroHH files.

    Parameters:
    ----------
    wind_data: netCDF
        A file containing the wind information
    source: str
        The name of the source for which the wind is read in
    lon: float
        Longitude of the source
    lat: float
        Latitude of the source
    radius: int
        Radius of pixels around the source.

    Returns:
    wind_src: netCDF
        A file with the mean wind information of the kernel with radius 'radius'
    """

    if "UM" in wind_data.data_vars:
        wind_data = wind_data.rename({"UM": "U", "VM": "V"})
    if "longitude" in wind_data.data_vars:
        wind_data = wind_data.rename({"longitude": "lon", "latitude": "lat"})

    wind_data["speed"] = np.sqrt(wind_data.U**2 + wind_data.V**2)
    wind_data["direction"] = ddeq.wind.calculate_wind_direction(
        wind_data.U, wind_data.V
    )

    lon_closest, lat_closest, dist = ddeq.misc.find_closest(
        wind_data, ("lon", "lat"), (lon, lat)
    )  # get values for closest coordinate

    wind_src = xr.Dataset(
        coords={"source": (["source"], np.array([source], dtype=object))},
        data_vars={
            "lon": (["source"], [wind_data.lon[lon_closest, lat_closest].values]),
            "lat": (["source"], [wind_data.lat[lon_closest, lat_closest].values]),
            "U": (
                ["source"],
                [
                    wind_data.U[
                        lon_closest - radius : lon_closest + radius + 1,
                        lat_closest - radius : lat_closest + radius + 1,
                    ]
                    .median()
                    .values
                ],
                {"units": "m s-1"},
            ),
            "V": (
                ["source"],
                [
                    wind_data.V[
                        lon_closest - radius : lon_closest + radius + 1,
                        lat_closest - radius : lat_closest + radius + 1,
                    ]
                    .median()
                    .values
                ],
                {"units": "m s-1"},
            ),
            "speed": (
                ["source"],
                [
                    wind_data.speed[
                        lon_closest - radius : lon_closest + radius + 1,
                        lat_closest - radius : lat_closest + radius + 1,
                    ]
                    .median()
                    .values
                ],
                {"units": "m s-1"},
            ),
            "speed_precision": (
                ["source"],
                [
                    wind_data.speed[
                        lon_closest - radius : lon_closest + radius + 1,
                        lat_closest - radius : lat_closest + radius + 1,
                    ]
                    .std()
                    .values
                ],
                {"units": "m s-1"},
            ),
            "direction": (
                ["source"],
                [
                    scipy.stats.circmean(
                        wind_data.direction[
                            lon_closest - radius : lon_closest + radius + 1,
                            lat_closest - radius : lat_closest + radius + 1,
                        ].values.flatten(),
                        high=360,
                        nan_policy="omit",
                    )
                ],
                {"units": "°"},
            ),
            "direction_precision": (
                ["source"],
                [
                    scipy.stats.circstd(
                        wind_data.direction[
                            lon_closest - radius : lon_closest + radius + 1,
                            lat_closest - radius : lat_closest + radius + 1,
                        ].values.flatten(),
                        high=360,
                        nan_policy="omit",
                    )
                ],
                {"units": "°"},
            ),
        },
        attrs=dict(radius=f"{radius} pixels around determined pixel"),
    )

    return wind_src


def read_field(filename, product="ERA5", altitude="GNFR-A", average_below=False):
    # TODO: combine with read_time_series & read_wind_field
    """\
    Return wind field from file for different products. 3D wind fields are
    taken at nearest altitude or averaged_below. If altitude is "GNFR_A", use
    vertically weighted wind field.

    Parameters
    ----------
    filename : str
        Name of file with SMARTCARB or ERA-5 wind fields.

    product: str, optional
        Either "ERA5" (default) or "SMARTCARB" product.

    altitude : str or float, optional
         The approach used for vertically averaging winds for computing the
         effective wind speed. Default is "GNFR-A" using the vertical emission
         profile for power plants. This requires that the file already includes
         the vertically averaged wind fields as "U_GNFR_A" and "V_GNFRA_A".
         Otherwise, if a number is given, the wind field is taken at the provide
         altitude or (if average_below is True) averaged below the given
         altitude.

    average_below, boolean, optional
        If True, wind fields will be averaged below given `altitude`.

    Returns
    -------
    xr.Dataset
        2D wind field on model grid.
    """
    with xr.open_dataset(filename) as rfile:

        if product == "SMARTCARB":

            lat = rfile.variables["lat"][:]
            lon = rfile.variables["lon"][:]

            if altitude == "GNFR-A":
                u = np.squeeze(rfile["U_GNFR_A"][:])
                v = np.squeeze(rfile["V_GNFR_A"][:])
            else:
                u = np.squeeze(rfile["U"][:])
                v = np.squeeze(rfile["V"][:])
                h = np.squeeze(rfile["HHL"].values[:])  # altitude in m
                h = h[:] - h[-1]  # above surface
                h = 0.5 * (h[1:] + h[:-1])  # at layer center

        elif product == "ERA5":

            lat = rfile.variables["latitude"][:]
            lon = rfile.variables["longitude"][:]

            if altitude == "GNFR-A":
                u = np.squeeze(rfile.variables["U_GNFR_A"][:])
                v = np.squeeze(rfile.variables["V_GNFR_A"][:])
            else:
                u = np.squeeze(rfile.variables["u"][:])
                v = np.squeeze(rfile.variables["v"][:])

                raise NotImplementedError
        else:
            raise ValueError(f'Unknown wind product "{product}".')

    # average wind below altitude
    if not isinstance(altitude, str):
        if average_below:
            u = np.nanmean(np.where(h < altitude, u, np.nan), axis=0)
            v = np.nanmean(np.where(h < altitude, v, np.nan), axis=0)
        else:
            # extract value at level
            k = np.argmin(np.abs(h - altitude), axis=0)

            unew = np.zeros(u.shape[1:])
            vnew = np.zeros(v.shape[1:])

            # quickest when itereating over small number of indices
            for index in set(k.flatten()):
                mask = k == index
                unew[mask] = u.values[index, mask]
                vnew[mask] = v.values[index, mask]

            u = xr.DataArray(unew, dims=u.dims[1:], attrs=u.attrs)
            v = xr.DataArray(vnew, dims=v.dims[1:], attrs=v.attrs)

    # Create wind dataset
    attrs = {}
    attrs["wind_product"] = product
    attrs["altitude"] = str(altitude)

    wind_field = xr.Dataset(attrs=attrs)

    wind_field["U"] = xr.DataArray(data=u)
    wind_field["V"] = xr.DataArray(data=v)
    wind_field["lat"] = xr.DataArray(data=lat)
    wind_field["lon"] = xr.DataArray(data=lon)

    return wind_field


def read_time_series(time, sources, query, timesteps=1, data_path=".", overwrite=False):
    # TODO: combine with read_field & read_wind_field
    """
    Read time series of ERA5 winds at given sources.

    Parameters:
    ----------
    time : datetime64 or xarray
        Time for which the wind data should be downloaded
    sources : xarray
        Dataset of sources with lat and lon
    query : str
        Indicate how the wind should be vertically averaged
            - complete: GNFR-A weighted wind on model level wind
            - pbl_mean: Mean wind in pbl
            - pressure_levels: Mean wind of pressure levels 1000 to 700 hPa
    timesteps : int
        Number of timesteps before "time" for which the data should be downloaded
        If 24, a full day will be returned.
    data_path : str
        Path to which the files should be saved
    overwrite : bool
        Indicates if the file should be overwritten if it already exists

    Returns:
    --------
    winds : netCDF
        A file containing the u and v component of the wind, total wind speed and direction.
    """

    if isinstance(time, xr.DataArray):
        time = pd.Timestamp(time.to_pandas())
    elif isinstance(time, np.datetime64):
        time = pd.Timestamp(time)

    winds = {}
    for name, source in sources.groupby("source"):

        coords = (source.latitude.values, source.longitude.values)
        prefix = name

        wind = ddeq.era5.prepare(
            time,
            coords,
            query=query,
            prefix=prefix,
            timesteps=timesteps,
            data_path=data_path,
            overwrite=overwrite,
        )

        wind = wind.reset_coords(names=["lat", "lon"])
        winds[name] = wind

    winds = xr.concat(winds.values(), dim="source")
    winds["source"] = xr.DataArray(sources.source, dims="source")

    return winds
