import cartopy.crs as ccrs
import netCDF4
import numpy as np
import scipy.optimize
import shapely
import skimage
import xarray as xr
import matplotlib.pyplot as plt

import ddeq.misc


def compute_pixel_areas(data):
    """
    Compute area of pixels (in m²).
    """
    area = np.zeros(data.xc.shape[:2])

    for j in range(data.xc.shape[1]):
        px = np.array([data.xc[:, j], data.yc[:, j]])
        px = np.transpose(px, [1, 2, 0])
        area[:, j] = [shapely.geometry.Polygon(p).area for p in px]

    data["pixel_area"] = xr.DataArray(area, dims=data.x.dims, attrs={"units": "m2"})

    return data


def compute_xy_coords(data, crs):
    """
    Compute xy coordinates (in meters) for pixel centers and corners using
    provided coordinate reference system (cartopy.crs).
    """
    wgs84 = ccrs.PlateCarree()

    data["x"], data["y"] = ddeq.misc.transform_coords(
        data.lon, data.lat, input_crs=wgs84, output_crs=crs, use_xarray=True
    )
    data["x_source"], data["y_source"] = ddeq.misc.transform_coords(
        data.lon_source, data.lat_source, input_crs=wgs84, output_crs=crs, use_xarray=True
    )
    if ("lonc" in data and "latc" in data) or (
        "longitude_bounds" in data and "latitude_bounds" in data
    ):

        lonc = data["lonc"] if "lonc" in data else data["longitude_bounds"]
        latc = data["latc"] if "latc" in data else data["latitude_bounds"]

        data["xc"], data["yc"] = ddeq.misc.transform_coords(
            lonc, latc, input_crs=wgs84, output_crs=crs, use_xarray=True
        )

    for var in ["x", "y", "x_source", "y_source", "xc", "yc"]:
        if var in data:
            data[var].attrs["epsg"] = crs.to_epsg()

    return data


def compute_plume_coords(data, curve, source, do_corners=False):
    """
    Compute plume coordinates for center and corner pixels within plume area.
    """
    index = int(np.argmax(data.source.values == source))
    source_data = data.sel(source=source)

    # center pixels in plume coords
    if "xp" not in data or "yp" not in data:
        shape = data["x"].shape + data["source"].shape
        dims = data["x"].dims + data["source"].dims

        data["xp"] = xr.DataArray(np.full(shape, np.nan), dims=dims)
        data["yp"] = xr.DataArray(np.full(shape, np.nan), dims=dims)

        data.xp.attrs["long name"] = "along plume coordinate"
        data.yp.attrs["long name"] = "across plume coordinate"

    data["xp"][:, :, index], data["yp"][:, :, index] = compute_plume_coordinates(
        source_data, curve, which="centers"
    )

    # compute for all ground pixels distance to center line
    # pixel corners
    if do_corners:
        if "xcp" not in data or "ycp" not in data:
            shape = data["xc"].shape + data["source"].shape
            dims = data["xc"].dims + data["source"].dims
            data["xcp"] = xr.DataArray(np.full(shape, np.nan), dims=dims)
            data["ycp"] = xr.DataArray(np.full(shape, np.nan), dims=dims)
            data.xcp.attrs["long name"] = "along plume corner coordinates"
            data.ycp.attrs["long name"] = "across plume corner coordinates"

        data["xcp"][:, :, :, index], data["ycp"][:, :, :, index] = (
            compute_plume_coordinates(source_data, curve, which="corners")
        )

        # check if pixels still valid polygons (can happen if curve is
        # over- or undershooting
        for i, j in np.ndindex(source_data.plume_area.shape):

            if not source_data.plume_area[i, j]:
                continue

            coords = np.transpose(
                [data["xcp"][i, j, :, index], data["ycp"][i, j, :, index]]
            )
            px = shapely.geometry.Polygon(coords)

            if (
                np.any(np.isnan(coords))
                or not px.is_valid
                or np.abs(px.area - px.convex_hull.area) > 1.0
            ):
                print("Error: Mask invalid pixel corners (%d,%d)." % (i, j))
                data["xcp"][i, j, :, index] = np.nan
                data["ycp"][i, j, :, index] = np.nan

    # update plume area by masking nans
    invalids = np.isnan(data.xp[:, :, index]) | np.isnan(data.yp[:, :, index])

    if do_corners:
        invalids |= np.any(np.isnan(data.xcp[:, :, index]), axis=2)
        invalids |= np.any(np.isnan(data.ycp[:, :, index]), axis=2)

    area = np.array(data.plume_area.sel(source=source))
    area[invalids] = False
    data["plume_area"][:, :, index] = area

    return data


class Poly2D:
    def __init__(
        self, x, y, w, degree=2, x_o=0.0, y_o=0.0, x0=0.0, y0=0.0, force_source=True
    ):
        """\
        A 2D curve fitted on the point cloud given by x and y.

        Parameters
        ----------
        x,y,w: x,y coords and weights used for fitting the data

        degree: degrees if the two polynomials x(t) and y(t)

        x_o, y_o: location of source (will be added to x,y and given
                  high weight such that curves goes through source if
                  force_origin is True)

        x0, y0: origin of coordinate system
        """
        self.x = x
        self.y = y
        self.w = w
        self.degree = degree
        self.force_source = force_source

        self.x_o = x_o
        self.y_o = y_o
        self.t_o = np.nan

        self.x0 = x0
        self.y0 = y0

        # initial coefficients
        self.c = np.zeros(2 * (degree + 1))
        self.c[2] = self.x_o
        self.c[5] = self.y_o

        self._fit()

        # arc length to origin
        self.t_o = self.get_parameter(self.x_o, self.y_o)

        #
        self.tmin = 0.0
        self.tmax = np.max(self.get_parameter(self.x, self.y))
        self.interpolator = None

    def to_file(self, filename, group=None, mode="a"):
        """
        Convert Poly2D to netCDF file.
        """
        data = xr.Dataset()

        for name in ["x", "y", "w", "degree", "x_o", "y_o", "x0", "y0"]:

            value = getattr(self, name)

            if np.ndim(value) == 0:
                data.attrs[name] = value

            else:
                data[name] = xr.DataArray(value, dims="pixels")

        try:
            data.to_netcdf(filename, mode=mode, group=group)
        except FileNotFoundError:
            data.to_netcdf(filename, mode="w", group=group)

        return data

    @classmethod
    def from_file(cls, filename, group=None):
        """
        Read curve from netCDF file.
        """
        with xr.open_dataset(filename, group=group) as data:
            args = dict((key, np.array(data[key])) for key in data)
            args.update(data.attrs)

        return cls(**args)

    def _fit(self):

        def objective(c, w, x, y):
            xt, yt = self._compute_curve(c, x, y)

            return np.concatenate([w * (xt - x), w * (yt - y)])

        # add origin
        if self.force_source:
            x = np.append(self.x, self.x_o)
            y = np.append(self.y, self.y_o)
            w = np.append(self.w, 100.0 * np.nanmax(self.w))
        else:
            x = np.append(self.x, self.x0)  # force origin of coords
            y = np.append(self.y, self.y0)
            w = np.append(self.w, 1000.0)

        # angle around origin (not used)
        # phi = np.arctan2(y - y0, x - x0)

        # curve fit
        res = scipy.optimize.leastsq(
            objective, x0=self.c, args=(w, x, y), full_output=True
        )
        self.c = res[0]
        self.cov_x = res[1]  # TODO
        ierr = res[4]

        if ierr not in [1, 2, 3, 4]:
            print("least square failed with error code: ", res)

    def arc2parameter(self, arc, pixel_size):
        if self.interpolator is None:
            ta = np.arange(
                self.tmin - 25 * pixel_size, 2 * self.tmax, 0.25 * pixel_size
            )
            la = [arc_length_of_2d_curve(self, self.t_o, v) for v in ta]
            self.interpolator = scipy.interpolate.interp1d(la, ta)

        return self.interpolator(arc)

    def get_parameter(self, x, y):
        return np.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2)

    def compute_tangent(self, t0, norm=False):
        v = np.array(self(t=t0, m=1))
        if norm:
            v /= np.linalg.norm(v, axis=0)
        return v

    def compute_angle(self, t=None):
        """
        Compute tangent angle for curve.
        """
        if t is None:
            t = self.t_o

        u, v = self.compute_tangent(t)
        return np.rad2deg(np.arctan2(u, v))

    def get_coefficients(self, c=None, m=0):

        if c is None:
            c = self.c

        k = c.size // 2
        cx = c[:k]
        cy = c[k:]

        if m != 0:
            cx = np.polyder(cx, m)
            cy = np.polyder(cy, m)

        return cx, cy

    def compute_normal(self, t0, x=None, y=None, t=None):

        x0, y0 = self(t=t0)

        # tangent vector
        v = self.compute_tangent(t0, norm=True)

        # rotate 90 degree
        n = np.dot([[0, -1], [1, 0]], v)

        cx = np.array([-n[0], x0])
        cy = np.array([-n[1], y0])

        if t is None:
            s = np.sign(v[0] * (y - y0) - v[1] * (x - x0))
            t = s * np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

        return compute_poly_curve(cx, cy, t)

    def _compute_curve(self, c, x=None, y=None, t=None, m=0):

        if t is None:
            t = self.get_parameter(x, y)
        else:
            if x is not None or y is not None:
                print("Warning: `x` and `y` will be ignored as `t` was given.")

        cx, cy = self.get_coefficients(c=c, m=m)

        x, y = compute_poly_curve(cx, cy, t)

        return x, y

    def __call__(self, x=None, y=None, t=None, m=0):
        return self._compute_curve(self.c, x, y, t, m)


def compute_poly_curve(cx, cy, t):
    """
    Compute poly curve.
    """
    return np.polyval(cx, t), np.polyval(cy, t)


def create_line(
    data,
    source,
    source_distance,
    boundary_width,
    degree=2,
    force_source=False,
    crs=None,
):
    """
    source_distance: distance of the origin from the source in reverse
                     direction of the detected plume (in pixels)
    boundary_width:  width around detected plume included in fit (in meters)
    """
    data = data.sel(source=source)

    plume = data["detected_plume"].values

    # Use z-values as weights
    weights = data["z_values"].values.copy() ** 2
    weights[(weights < 0.05) | np.isnan(weights)] = 0.05

    # get location of plume and XCO2 values (plus wind etc.)
    is_plume = ddeq.misc.compute_plume_area(data, radius=boundary_width, units="px")

    x = np.asarray(data.x)[is_plume]
    y = np.asarray(data.y)[is_plume]
    w = np.asarray(weights)[is_plume]

    # location of the source
    x_o, y_o = float(data.x_source), float(data.y_source)

    # origin of center line (50 km upstream of source)
    x0 = np.mean(data.x.values[plume])
    y0 = np.mean(data.y.values[plume])
    delta = np.sqrt((x0 - x_o) ** 2 + (y0 - y_o) ** 2)

    x1 = x_o - (x0 - x_o) / delta * source_distance
    y1 = y_o - (y0 - y_o) / delta * source_distance

    # fit 2d curve
    curve = Poly2D(
        x, y, w, degree, x_o=x_o, y_o=y_o, x0=x1, y0=y1, force_source=force_source
    )

    return curve


def read_curves(filename):
    """
    Read curves from netCDF file and return as dictionary.
    """
    with netCDF4.Dataset(filename) as nc:
        sources = nc.groups.keys()

    curves = {}
    for source in sources:
        try:
            curves[source] = Poly2D.from_file(filename, group=source)
        except OSError:
            pass

    return curves


def save_curves(curves, filename):
    """
    Save dict of curves to netCDF file.
    """
    for source, curve in curves.items():
        if curve is not None:
            curve.to_file(filename=filename, group=source)


#
# Across- and along-plume coords
#


def integral_sqrt_poly(x, a, b, c):
    """
    Integral over sqrt(a*x**2 + b*x + c)
    """
    s = np.sqrt(a * x**2 + b * x + c)

    A = (b + 2 * a * x) / (4 * a) * s
    B = (4 * a * c - b**2) / (8 * a ** (3 / 2))
    C = np.abs(2 * a * x + b + 2 * np.sqrt(a) * s)

    return A + B * np.log(C)


def compute_arc_length(curve, smin, smax):
    a, b = curve.get_coefficients()

    c0 = 4 * a[0] ** 2 + 4 * b[0] ** 2
    c1 = 4 * a[0] * a[1] + 4 * b[0] * b[1]
    c2 = a[1] ** 2 + b[1] ** 2

    smin = integral_sqrt_poly(smin, c0, c1, c2)
    smax = integral_sqrt_poly(smax, c0, c1, c2)

    return smax - smin


def arc_length_of_2d_curve(curve, a, b):

    t = np.linspace(a, b, 50001)
    xt, yt = curve(t=t, m=1)

    v = np.sqrt(xt**2 + yt**2)

    l = scipy.integrate.simpson(y=v, x=t)
    return l


def compute_plume_coordinates(data, curve, show=False, which="centers", area=None):
    """
    Computes along- and across-plume coordinates analytically
    if curve.degree == 2.

    Parameters
    ----------
    data : satellite data incl. x, y and plume_area
    curve : center curve
    which : process either pixel 'centers' or 'corners'.

    """
    if curve.degree != 2:
        raise ValueError("Degree of curve needs to be 2 not %d" % curve.degree)

    a, b = curve.get_coefficients()

    # parameter for minimum distance to curve
    if area is None:
        if "plume_area" in data:
            area = data.plume_area.values
        else:
            area = np.ones(data.x.shape, bool)

    if which == "centers":
        qx = data.x.values[area]
        qy = data.y.values[area]
    else:
        qx = data.xc.values[area].flatten()
        qy = data.yc.values[area].flatten()

    # coefficients for analytical solution
    c0 = 4 * a[0] ** 2 + 4 * b[0] ** 2
    c1 = 6 * a[0] * a[1] + 6 * b[0] * b[1]
    c2 = (
        4 * a[0] * a[2]
        - 4 * a[0] * qx
        + 2 * a[1] ** 2
        + 4 * b[0] * b[2]
        - 4 * b[0] * qy
        + 2 * b[1] ** 2
    )
    c3 = 2 * a[1] * a[2] - 2 * a[1] * qx + 2 * b[1] * b[2] - 2 * b[1] * qy

    roots = ddeq.misc.cubic_equation(c0, c1, c2, c3)
    real = np.abs(roots.imag) < 1e-6

    tmin = []
    n_no_solutions = 0
    n_multiple_solutions = 0

    for i in range(qx.size):

        n_solutions = np.sum(real[:, i])

        if n_solutions == 0:
            tmin.append(np.nan)
            n_no_solutions += 1

        elif n_solutions == 1:
            tmin.append(float(roots[:, i][real[:, i]].real[0]))

        elif n_solutions > 1:
            # use shortest arc length (which might fail for strongly bend plumes)
            # using shortest distance fails, if curve bends back to source location
            j = np.argmin(roots[:, i].real)
            tmin.append(roots[j, i].real)

            n_multiple_solutions += 1

        else:
            raise ValueError

    if n_no_solutions > 0:
        name = " ".join(
            "%s" % v
            for v in [
                data.time.values,
                getattr(data, "orbit", "none"),
                getattr(data, "lon_eq", "none"),
            ]
        )
        print('No real solution for some points in "%s"' % name)

    if n_multiple_solutions > 0:
        pass

    tmin = np.array(tmin)
    px, py = curve(t=tmin)

    # sign of distance (negative left of curve from source)
    t = curve.get_parameter(qx, qy)
    v = curve.compute_tangent(t, norm=True)
    n = np.array([px - qx, py - qy])

    # compute sign using z-element of cross product
    sign = np.sign(v[0] * n[1] - v[1] * n[0])

    if which == "centers":

        # compute distance
        distance = xr.full_like(data.x, np.nan)
        distance.values[area] = sign * np.sqrt((px - qx) ** 2 + (py - qy) ** 2)

        # arc-length
        arc = xr.full_like(data.x, np.nan)
        arc.values[area] = compute_arc_length(curve, curve.t_o, tmin)

    else:
        # distance
        d = sign * np.sqrt((px - qx) ** 2 + (py - qy) ** 2)
        distance = xr.full_like(data.xc, np.nan)
        distance.values[area] = d.reshape(d.size // 4, 4)

        # arc-length
        a = compute_arc_length(curve, curve.t_o, tmin)
        arc = xr.full_like(data.xc, np.nan)
        arc.values[area] = a.reshape(a.size // 4, 4)

    if show:
        fig = plt.figure()
        ax = plt.subplot(aspect="equal")

        for i, (x, y) in enumerate(zip(qx, qy)):
            px, py = curve(t=tmin[i])
            ax.plot([px, x], [py, y], "o-")

        ax.plot(*curve(t=np.linspace(0, tmin.max())), "k-")

    return arc, distance


def compute_plume_line_and_coords(
    data,
    crs,
    radius=None,
    radius_units="m",
    do_coords=True,
    plume_area="area",
    reject_overlapping_sources=True,
):
    """
    Compute plume center line and coordinates in the plume coordinate system
    using arc length (x-direction) and distance from center line (y-direction).

    Parameters
    ----------
    data : xr.Dataset
        Satellite data with detected plume for sources.

    crs : cartopy.crs
        Coordinate reference system used for computing local easting and
        northing from longitude and latitude.

    radius : float, optional
        Radius for an area around the detected plume that is included when fitting
        the center line used if `plume_area` == 'area'). Default: 25e3 meters.

    radius_units : str, optional
        Units used for radius either "m" for meters or "px" for pixels.

    do_coords : boolean, optional
        If True compute the plume coordinates.

    plume_area : str, optional
        if 'area' compute plume area using radius and pixel size
        if 'hull' compute plume area as convex hull of detected pixels

    reject_overlapping_sources : boolean
        Don't compute line and coords for plume detection overlapping several
        sources.

    Returns
    -------
    xr.Dataset, dict
        `data` with added variables and dictionary of curves for each source by
        name.
    """

    if "detected_plume" not in data:
        return data, {}

    # convert to coordinate system using meters
    data = compute_xy_coords(data, crs=crs)

    # compute pixel area [in m²]
    if "xc" in data and "yc" in data:
        data = compute_pixel_areas(data)

    if 'detected_plume' not in data:
        return data, {}

    # area around plume used for fitting center curve
    data["plume_area"] = xr.zeros_like(data.detected_plume)
    pixel_size = np.sqrt(np.mean(data["pixel_area"]))

    curves = {}

    for source in data.source.values:

        # select source
        source_data = data.sel(source=source)

        # area for which data are prepared for mass-balance approach
        if plume_area == "area":
            area = ddeq.misc.compute_plume_area(
                source_data, radius=radius, pixel_size=pixel_size, units=radius_units
            )
        elif plume_area == "hull":
            area = skimage.morphology.convex_hull_image(
                source_data["detected_plume"].values
            )

        else:
            raise ValueError(
                f'`plume_area` needs to be "area" or "hull" but not {plume_area}'
            )

        # use index, because sel method might fail according to documentation
        index = int(np.argmax(data.source.values == source))
        data["plume_area"][:, :, index] = area

        # compute curve
        if source_data["detected_plume"].sum() == 0 or (
            ddeq.misc.has_multiple_sources(data, source) and reject_overlapping_sources
        ):

            curves[source] = None
        else:
            # source_distance, force_source, ... should be taken from
            # source_data['type']
            if radius_units == "m":
                source_distance = float(2.0 * radius)
            else:
                source_distance = float(2.0 * radius * pixel_size)

            curves[source] = create_line(
                data,
                source=source,
                degree=2,
                source_distance=source_distance,
                boundary_width=2,  # pixels
                force_source=True,
            )

            if do_coords:
                data = compute_plume_coords(
                    data=data, curve=curves[source], source=source, do_corners=False
                )

    return data, curves
