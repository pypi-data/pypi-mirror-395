from datetime import timedelta
import os
import netCDF4
import numpy as np
import pandas
import pyproj
import re
import scipy.ndimage
import skimage.draw
import skimage.morphology
import xarray as xr

import f90nml
import cartopy.crs as ccrs
from cartopy.geodesic import Geodesic

# Instance of Geodesic class for working in lon-lat coordinates
EARTH = Geodesic()

import ddeq


def init_results_dataset(
    source: xr.DataArray,
    gases: list,
    extra_vars: dict = {},
    units: str = "kg s-1",
    global_attrs: dict = {},
):
    """
    Initialize dataset for estimated emissions.
    """
    if isinstance(gases, str):
        gases = [gases]

    result = xr.Dataset(source, attrs=global_attrs)

    for gas in gases:
        for name, attrs in extra_vars.items():
            nan_values = np.full(np.shape(source.source), np.nan)

            result[name.format(gas=gas)] = xr.DataArray(
                nan_values, dims=source.dims, attrs=attrs
            )
        name = f"{gas}_emissions"
        name_std = f"{gas}_emissions_precision"
        result[name] = xr.DataArray(
            np.full(source["source"].size, np.nan),
            dims=["source"],
            attrs={"units": units},
        )
        result[name_std] = xr.DataArray(
            np.full(source["source"].size, np.nan),
            dims=["source"],
            attrs={"units": units},
        )

    return result


def select_source(data, source):
    """
    Select source in data but also compute new fields for other plumes and multiple sources.
    """
    this = data.sel(source=source).copy()

    if "detected_plume" in data:
        this["other_sources"] = (
            data["detected_plume"].any("source") & ~this["detected_plume"]
        )
        this["multiple_sources"] = data["detected_plume"].sum("source") > 1

    return this


class Domain:
    def __init__(
        self,
        name,
        startlon,
        startlat,
        stoplon,
        stoplat,
        ie=None,
        je=None,
        pollon=None,
        pollat=None,
    ):
        """
        to add: dlon, dlat, ie, je
        """
        self.name = name

        self.startlat = float(startlat)
        self.stoplat = float(stoplat)
        self.startlon = float(startlon)
        self.stoplon = float(stoplon)

        self.ie = ie
        self.je = je

        self.rlon = None
        self.rlat = None
        self.lon = None
        self.lat = None

        self.width = np.abs(self.stoplon - self.startlon)
        self.height = np.abs(self.stoplat - self.startlat)

        self.pollon = pollon
        self.pollat = pollat

        self.is_rotpole = pollon is not None and pollat is not None
        is_grid = self.ie is not None and self.je is not None

        if is_grid:
            self.dlon = (self.stoplon - self.startlon) / (self.ie - 1)
            self.dlat = (self.stoplat - self.startlat) / (self.je - 1)
        else:
            self.dlon, self.dlat = None, None

        if self.is_rotpole:
            self.proj = ccrs.RotatedPole(pole_latitude=pollat, pole_longitude=pollon)

            if is_grid:
                self.rlon = np.linspace(self.startlon, self.stoplon, self.ie)
                self.rlat = np.linspace(self.startlat, self.stoplat, self.je)

                rlon, rlat = np.meshgrid(self.rlon, self.rlat)

                self.lon, self.lat = transform_coords(
                    rlon, rlat, self.proj, ccrs.PlateCarree(), use_xarray=False
                )
        else:
            self.proj = ccrs.PlateCarree()

            if is_grid:
                self.lon = np.linspace(self.startlon, self.stoplon, self.ie)
                self.lat = np.linspace(self.startlat, self.stoplat, self.je)

    @property
    def extent(self):
        return {
            "north": self.stoplat,
            "west": self.startlon,
            "south": self.startlat,
            "east": self.stoplon
        }

    @property
    def shape(self):
        return self.je, self.ie

    @classmethod
    def around_source(cls, source, dlat=3.0, dlon=4.0):
        lon_s, lat_s, diameter = ddeq.sources.get_location(source)
        return cls(
            name=source.label,
            startlat=lat_s - dlat/2,
            stoplat=lat_s + dlat/2,
            startlon=lon_s - dlon/2,
            stoplon=lon_s + dlon/2
        )

    @classmethod
    def from_nml(cls, filename):
        with open(filename) as nml_file:
            nml = f90nml.read(nml_file)

        pollon = nml["lmgrid"]["pollon"]
        pollat = nml["lmgrid"]["pollat"]
        startlon = nml["lmgrid"]["startlon_tot"]
        startlat = nml["lmgrid"]["startlat_tot"]
        dlon = nml["lmgrid"]["dlon"]
        dlat = nml["lmgrid"]["dlat"]
        ie = nml["lmgrid"]["ie_tot"]
        je = nml["lmgrid"]["je_tot"]

        stoplat = startlat + (je - 1) * dlat
        stoplon = startlon + (ie - 1) * dlon

        return cls(
            filename, startlon, startlat, stoplon, stoplat, ie, je, pollon, pollat
        )

    def get_transform(self):
        import rasterio.transform

        return rasterio.transform.from_bounds(
            self.startlon, self.startlat, self.stoplon, self.stoplat, self.ie, self.je
        )


def read_point_sources(filename=None):
    """\
    Read list of point sources and converts them to format used by the
    plume detection algorithm.

    Parameters
    ----------
    filename : str, default: None
        Name of CSV file with point source information (see "sources.csv"
        in ddeq.DATA_PATH for an example).

    Returns
    -------
    xr.Dataset
        xarray dataset containing point source locations
    """
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), "data", "sources.csv")

    point_sources = pandas.read_csv(
        filename,
        index_col=0,
        names=["label", "longitude", "latitude", "diameter"],
        header=0,
    )

    sources = xr.Dataset(coords={"source": point_sources.index})
    sources["lon"] = xr.DataArray(
        point_sources["longitude"],
        dims="source",
        attrs={"name": "longitude of point source"},
    )
    sources["lat"] = xr.DataArray(
        point_sources["latitude"],
        dims="source",
        attrs={"name": "latitude of point source"},
    )
    sources["diameter"] = xr.DataArray(
        point_sources["diameter"],
        dims="source",
        attrs={"name": "source diameter", "units": "m"},
    )
    sources["label"] = xr.DataArray(point_sources["label"], dims="source")

    return sources


def transform_coords(x, y, input_crs, output_crs, use_xarray=True, names=("x", "y")):
    """
    Convert easting and northing in EPSG to WGS84.
    """
    if use_xarray:
        dims = x.dims

    x = np.asarray(x)
    y = np.asarray(y)
    shape = x.shape

    res = output_crs.transform_points(input_crs, x.flatten(), y.flatten())
    xnew, ynew = res[:, 0].reshape(shape), res[:, 1].reshape(shape)

    if use_xarray:
        xnew = xr.DataArray(xnew, name=names[0], dims=dims)
        ynew = xr.DataArray(ynew, name=names[1], dims=dims)

    return xnew, ynew

    if np.ndim(x) == 0:
        res = output_crs.transform_point(lon, lat, input_crs)
        xnew, ynew = res[0], res[1]

    elif np.ndim(x) in [1, 2]:
        res = out.transform_points(in_, lon, lat)
        xnew, ynew = res[..., 0], res[..., 1]

    else:
        shape = x.shape
        res = output_crs.transform_points(input_crs, x.flatten(), y.flatten())
        x, y = x[:, 0].reshape(shape), y[:, 1].reshape(shape)


def wgs2epsg(lon, lat, epsg, inverse=False):
    """
    Transforms lon/lat to EPSG.
    """
    if inverse:
        out = ccrs.PlateCarree()
        in_ = ccrs.epsg(epsg)
    else:
        out = ccrs.epsg(epsg)
        in_ = ccrs.PlateCarree()

    if np.ndim(lon) == 0:
        res = out.transform_point(lon, lat, in_)
        return res[0], res[1]
    elif np.ndim(lon) in [1, 2]:
        res = out.transform_points(in_, lon, lat)
        return res[..., 0], res[..., 1]
    else:
        shape = lon.shape
        res = out.transform_points(in_, lon.flatten(), lat.flatten())
        return res[:, 0].reshape(shape), res[:, 1].reshape(shape)


def has_multiple_sources(data, source):
    """
    Returns if the plume detected for "source" has also added to other
    sources in the dataset.
    """
    return bool(
        np.any(
            data["detected_plume"].sel(source=source)
            & (data["detected_plume"].sum("source") > 1)
        )
    )


def get_source_clusters(data, sources):
    """\
    Return a list of list source names that have overlapping plumes.
    """
    plumes = data["detected_plume"]

    sources_names = plumes.source.values
    names = []
    cluster = []

    for name in sources_names:
        current = plumes.sel(source=name)
        twins = []

        if name in names:
            continue

        for name in sources_names:
            if np.all(current == plumes.sel(source=name)):
                names.append(name)
                twins.append(name)

        cluster.append(twins)

    return cluster


def compute_plume_area(data, radius, units="px", pixel_size=None):
    """
    Compute plume area by increasing size of detected plume using binary
    dilation with circular kernel of `radius` either in meters (m) or
    pixels (px). In addition, a circle is drawn around the source location.

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing data with variable `detected_plume`.

    radius : number
        Radius of kernel in meters or pixels.

    units : str, optional
        Units used for radius either "m" for meters or "px" for pixels.

    pixel_size : float, optional
        Size of image pixels in meters.

    Returns
    -------
    area : np.array
        Boolean mask with area around detected plume.
    """
    if units == "m":
        r = int(np.round(radius / pixel_size))
    else:
        r = radius

    kernel = create_disk(r)

    # set pixels within distance from detected pixels to True
    if np.any(kernel):
        detected_plume = np.array(data["detected_plume"])
        area = skimage.morphology.dilation(detected_plume, kernel)
    else:
        area = np.array(data["detected_plume"]).copy()

    # set area around source to True
    x_o = float(data["x_source"])
    y_o = float(data["y_source"])
    distance = np.sqrt((data.x - x_o) ** 2 + (data.y - y_o) ** 2)
    distance = np.array(distance)

    if units == "m":
        area[distance < radius] = True
    else:
        location = np.unravel_index(np.argmin(distance), data.x.shape)
        rr, cc = skimage.draw.disk(location, r, shape=data.x.shape)
        area[rr, cc] = True

    return area


def create_disk(r):
    """Create disk kernel with radius r."""
    shape = (2 * r, 2 * r)
    kernel = np.zeros(shape, dtype=bool)
    rr, cc = skimage.draw.disk((r - 0.5, r - 0.5), r, shape=shape)
    kernel[rr, cc] = True

    return kernel


def cubic_equation(a, b, c, d):
    """
    Find roots of cubic polynomial:
        a * x**3 + b * x**2 + c * x + d = 0
    """
    try:
        dtype = np.complex256
    except AttributeError:
        dtype = np.complex128
    a = np.asarray(a).astype(dtype)
    b = np.asarray(b).astype(dtype)
    c = np.asarray(c).astype(dtype)
    d = np.asarray(d).astype(dtype)

    d0 = b**2 - 3 * a * c
    d1 = 2 * b**3 - 9 * a * b * c + 27 * a**2 * d

    C = ((d1 + np.sqrt(d1**2 - 4 * d0**3)) / 2.0) ** (1 / 3)

    xi = (-1.0 + np.sqrt(-3.0 + 0j)) / 2.0
    s = lambda k: xi**k * C

    roots = [-1.0 / (3.0 * a) * (b + s(k) + d0 / s(k)) for k in range(3)]

    return np.array(roots)


def get_plume_width(data, dy=5e3, area="detected_plume"):

    # distance from center line
    if isinstance(area, str):
        yp = data["yp"].values[data[area]]
    else:
        yp = data["yp"].values[area]

    ymin = np.floor((np.nanmin(yp) - 2 * dy) / dy) * dy
    ymax = np.ceil((np.nanmax(yp) + 2 * dy) / dy) * dy

    return ymin, ymax


def compute_polygons(
    data,
    source_diameter=0.0,
    dmin=0.0,
    dmax=np.inf,
    delta=None,
    add_upstream_box=False,
    extra_width=1,
    pixel_size=None,
):
    """
    Compute [xa,xb] and [ya,yb] intervals for polygons.
    """
    if pixel_size is None:
        raise ValueError("Pixel size is None.")

    #if dmin is None or delta is None:
    if pixel_size > source_diameter:
            dmin = 0.0 if dmin is None else dmin
            delta = 2.5 * pixel_size if delta is None else delta
    else:
            dmin = -1.0 * source_diameter if dmin is None else dmin
            delta = 5.0 * pixel_size if delta is None else delta


    dmax = min(dmax, np.nanmax(data.xp.values[data.detected_plume]))
    distances = np.arange(dmin, dmax + delta, delta)

    if add_upstream_box:  # FIXME
        xa_values = np.concatenate([[-6 * pixel_size], distances[:-1]])
        xb_values = np.concatenate([[-pixel_size], distances[1:]])
    else:
        xa_values = distances[:-1]
        xb_values = distances[1:]

    ya, yb = get_plume_width(data, dy=extra_width * pixel_size)

    return (
        xa_values,
        xb_values,
        np.full_like(xa_values, ya),
        np.full_like(xb_values, yb),
    )


def normalized_convolution(values, kernel, mask=None):

    if mask is None:
        mask = ~np.isfinite(values)

    values = values.copy()
    certainty = 1.0 - mask

    values[certainty == 0.0] = 0.0

    return scipy.ndimage.convolve(values, kernel) / scipy.ndimage.convolve(
        certainty, kernel
    )


def compute_plume_age_and_length(ld):
    """
    Estimate plume age (in seconds) and length (in meters) based on wind
    speed and arc length up to most distance detected pixel.
    """
    values = ld.x.values[ld.is_plume.values]

    if np.size(values) > 0:
        plume_length = ld.x.values[ld.is_plume.values].max()
    else:
        plume_length = 0.0

    plume_age = plume_length / np.mean(ld["wind_speed"])

    return plume_age, plume_length


def compute_angle_between_curve_and_wind(curve, wind_direction, crs):
    """
    Compute the angle between wind vector and curve tangent, which can be
    used as a warning flag for large misfits.

    Parameter:
    - source: name of point source
    - curves: dict with curves
    """

    # compute curve angle (lon-lat angle)
    t_source = curve.compute_parameter(curve.x_source, curve.y_source)
    u, v = curve.compute_tangent(t_source)

    u, v = transform_coords(
        np.array([curve.x_source, curve.x_source - u]),
        np.array([curve.y_source, curve.y_source - v]),
        crs,
        ccrs.PlateCarree(),
        use_xarray=False,
    )
    u = np.diff(u)
    v = np.diff(v)

    curve_angle = float(np.squeeze(np.rad2deg(np.arctan2(u, v))))

    return smallest_angle(wind_direction, curve_angle)


def smallest_angle(x, y):
    return min(abs(x - y), 360 - abs(x - y))


def generate_grids(center_lon, center_lat, lon_km, lat_km, grid_reso):
    """
    Generate the km and degree grids corresponding resolution grid_reso in km.
    """
    longrid_km = np.arange(-lon_km, lon_km + grid_reso, grid_reso)
    latgrid_km = np.arange(-lat_km, lat_km + grid_reso, grid_reso)[::-1]

    shape = latgrid_km.size, longrid_km.size

    lat_arr = np.asarray(
        EARTH.direct(
            np.repeat([(center_lon, center_lat)], shape[0], axis=0),
            np.zeros(shape[0]),
            1000 * latgrid_km,
        )
    )[:, 1]

    latgrid = np.repeat(np.reshape(lat_arr, (-1, 1)), shape[1], axis=1)
    longrid = np.full(shape, np.nan)

    for r in range(shape[0]):
        longrid[r, :] = np.asarray(
            EARTH.direct(
                np.repeat([(center_lon, lat_arr[r])], shape[0], axis=0),
                90 * np.ones(shape[0]),
                1000 * longrid_km,
            )
        )[:, 0]

    return longrid, latgrid, longrid_km, latgrid_km


def calculate_gaussian_curve(gas, polygon):
    """
    Calculate Gaussian curve from fit parameters for Gaussian curve in
    cross-sectional flux method.
    """
    s = np.linspace(float(polygon["ya"]), float(polygon["yb"]), 501)
    p = [
        float(polygon[name])
        for name in [
            f"{gas}_line_density",
            f"{gas}_standard_width",
            f"{gas}_shift",
            f"{gas}_slope",
            f"{gas}_intercept",
        ]
    ]
    return s, ddeq.functions.gauss(s, *p)


def distance_between_coordinates(lon1, lat1, lon2, lat2):
    """
    Distance (in meters between two lon, lat points.
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    # Radius of earth in kilometers is 6371
    distance = 6371e3 * c

    return distance


def get_data_at_location(
    data: xr.Dataset,
    lon0: float,
    lat0: float,
    lon_name: str = "lon",
    lat_name: str = "lat",
) -> xr.Dataset:
    """\
    Obtain data at the nearest neighbour of a location given by
    lon0 and lat0.
    """

    if np.ndim(data[lat_name].data) == 2:
        lon_i, lat_i, dist = ddeq.misc.find_closest(
            data=data, fld=(lon_name, lat_name), poi=(lon0, lat0)
        )
    else:
        lon_i = np.argmin(np.abs(data[lon_name].data - lon0))
        lat_i = np.argmin(np.abs(data[lat_name].data - lat0))

    isel_dict = {
        lon_name: lon_i,
        lat_name: lat_i,
    }

    return data.isel(**isel_dict)


def find_closest(data, fld, poi):
    """
    Get the index of the pixel closest to the point of interest.

    Parameters:
    ----------
    data: netCDF
        File with the coordinates to find
    fld: (str, str)
        Tuple of strings with the names of the coordinates in data (i.e 'lon', 'lat')
    poi: (float, float)
        Tuple of floats with the coordinates of the point of interest

    Returns:
    --------
    ind: (int, int)
        Indexes of the pixel closest to the point of interest.
    dist: float
        Distance of the closest pixel to the point of interest.
        In the units of the input data.
    """
    xf, yf = fld
    x, y = poi
    diff = np.sqrt((data[xf].values - x) ** 2 + (data[yf].values - y) ** 2)

    return (*np.unravel_index(np.nanargmin(diff), diff.shape), np.nanmin(diff))


def cluster_sources(sources, distance):
    """
    Cluster sources based on `distance` in meters following the example at [1].


    [1] https://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/
    """
    # TODO
    pass


def get_opt_crs(domain):
    """
    Get a coordinate reference system (crs) based on the extent of the domain.

    Parameters
    ----------
    domain : ddeq.misc.Domain
        Domain class used to define plotting area.

    Returns
    -------
    cartopy.crs.CRS
    """
    # Define the area of interest
    area_of_interest = pyproj.aoi.AreaOfInterest(
        west_lon_degree=domain.startlon,
        south_lat_degree=domain.startlat,
        east_lon_degree=domain.stoplon,
        north_lat_degree=domain.stoplat,
    )

    # query all crs which intersect with the domain
    utm_crs_list = pyproj.database.query_utm_crs_info(
        datum_name="WGS 84", area_of_interest=area_of_interest
    )

    df = pandas.DataFrame(utm_crs_list)

    return ccrs.epsg(int(df.iloc[0]["code"]))


def format_unit_superscripts(units: str):
    """
    Formats units for plotting by converting superscripts LaTeX format.

    Parameters:
        units (str): The units string to format.

    Returns:
        str: The formatted units string.
    """
    if units is None:
        return "a.u."

    # Regular expression to match numbers that should be superscripts
    pattern = r"([a-zA-Z])([-]?\d+)"

    # Replace the pattern with LaTeX superscript format
    formatted_units = re.sub(pattern, r"\1$^{\2}$", units)

    return formatted_units


def compute_pixel_area(data):
    """
    Compute pixel area from lon/lat using Haversine and Brahmagupta formula.
    """
    lonc = data["lonc"] if "lonc" in data else data["longitude_bounds"]
    latc = data["latc"] if "lonc" in data else data["latitude_bounds"]

    a,b,c,d = [
        ddeq.misc.distance_between_coordinates(
            lonc[:,:,i],
            latc[:,:,i],
            lonc[:,:,j],
            latc[:,:,j])
        for i,j in [(0,1), (1,2), (2,3), (3,0)]
    ]

    s = (a+b+c+d) / 2.0
    K = np.sqrt( (s-a) * (s-b) * (s-c) * (s-d) )

    attrs = {"long_name": "Area of pixel", "units": "m2"}
    data["pixel_area"] = xr.DataArray(K, dims=lonc.dims[:2], attrs=attrs)

    return data


def extract_gas(variable: str) -> str:
    gases = ["CH4", "CO2", "NO2", "NOx", "NO", "SO2"]
    for gas in gases:
        if gas in variable:
            return gas
    else:
        raise ValueError(f"No gas found in {variable}.")


def round_dyn(number: float, digits: int = 1) -> float:
    exponent = np.floor(np.log10(number))
    return np.round(number, -int(exponent - digits))


def get_pixel_size_at_source(data, source_name=None):

    if source_name is not None:
        data = data.sel(source=source_name)

    # source location
    lon_source = float(data.lon_source)
    lat_source = float(data.lat_source)
    source_diameter = float(data.diameter_source)

     # pixel size
    i,j,_ = ddeq.misc.find_closest(data, ("lon", "lat"), (lon_source, lat_source))
    pixel_size = np.sqrt(data.pixel_area[i,j].values)

    return pixel_size
