
import numpy as np
import scipy.optimize
import scipy.spatial
import skimage.morphology
import xarray as xr

import ddeq


class BezierCurve:
    def __init__(self, x_nodes, y_nodes, x_source, y_source):
        self.x_nodes = np.asarray(x_nodes)
        self.y_nodes = np.asarray(y_nodes)
        self.x_source = float(x_source)
        self.y_source = float(y_source)

    @classmethod
    def from_data(cls, data, name):
        """
        Create curve from source "name" in data.
        """
        this = data.sel(source=name)
        return cls(
            this["x_nodes"],
            this["y_nodes"],
            this["x_source"],
            this["y_source"]
        )

    def __call__(self, t):
        return bezier_curve(
            t,
            x_nodes=self.x_nodes,
            y_nodes=self.y_nodes
        )

    def compute_parameter(self, x, y, npts=1000):
        x = float(x)
        y = float(y)
        t = np.linspace(0.0, 1.0, npts)
        xp, yp = self(t)
        return t[np.argmin((xp - x)**2 + (yp - y)**2)]

    def compute_natural_coords(self, x, y, npts=100):

        # Evaluate points along the parametric curve
        t = np.linspace(0.0, 1.0, npts)
        xp, yp = self(t)

        if np.sum(np.isfinite(xp)) == 0 or np.sum(np.isfinite(yp)) == 0:
            return None, None

        # Establish shortest Euclidean distance (automatically corresponds to
        # shortest perpendicular distance between any point vs. the curve!)
        grid_coords = np.nan_to_num(np.vstack((x.ravel(), y.ravel())).T)
        curve_coords = np.vstack((xp.ravel(), yp.ravel())).T
        kdtree = scipy.spatial.KDTree(curve_coords)
        neighbours, idx = kdtree.query(grid_coords)

        # ... so, establish the normal distance to the line
        y_min = neighbours.reshape(x.shape)
        y_min = np.where(~np.isnan(y), y_min, np.nan)

        # index of source location
        ps = np.transpose([[self.x_source], [self.y_source]])
        _, ids = kdtree.query(ps)

        # ---> Establish the corresponding length along the line
        offsets = np.sqrt(np.gradient(xp) ** 2 + np.gradient(yp) ** 2)
        x_length = np.cumsum(offsets)
        x_min = x_length[idx].reshape(x.shape) - x_length[ids]
        x_min = np.where(~np.isnan(x), x_min, np.nan)

        # compute sign
        xx, yy = self(t)
        bad = (idx == 0) | (idx == npts - 1)

        # tangent
        v0, v1 = self.compute_tangent(t[idx])

        # normal vector
        xc, yc = self(t[idx])
        n0 = np.asarray(x).flatten() - xc
        n1 = np.asarray(y).flatten() - yc

        sign = - np.sign(v0 * n1 - v1 * n0)
        sign[bad] = np.nan
        sign = sign.reshape(x.shape)

        y_min *= sign

        # mask outside [0,1]
        x_min[bad.reshape(x_min.shape)] = np.nan

        return x_min, y_min

    def compute_tangent(self, t):
        xc1, yc1 = self(t - 0.01)
        xc2, yc2 = self(t + 0.01)

        tx = xc2 - xc1
        ty = yc2 - yc1

        s = np.sqrt(tx**2 + ty**2)

        return tx / s, ty / s

    def compute_normal(self, t):
        tx, ty = self.compute_tangent(t)
        return -ty, tx



def bernstein_poly(i, n, t):
    """\
    The Bernstein polynomial of n, i as a function of t
    """
    return scipy.special.comb(n, i) * t ** i * (1 - t) ** (n - i)


def bezier_curve(t, points=None, x_nodes=None, y_nodes=None):
    """\
    Given a set of control points, return the bezier curve defined by the
    control points.
    """
    if points is not None:
        x_nodes, y_nodes = points.T
    n = x_nodes.size

    polynomial_array = np.array(
        [bernstein_poly(i, n-1, t) for i in range(n)]
    )

    xvals = np.dot(x_nodes, polynomial_array)
    yvals = np.dot(y_nodes, polynomial_array)

    return xvals, yvals


def compute_natural_coords(data, npts=1000):
    """\
    Create a quick 'natural coordinate' system w.r.t. a curve,

    IN:
      x_nodes   list of node points (in meters)
      y_nodes   list of node points (in meters)
      x         2D array of Easting coordinates (in meters)
      y         2D array of Northing coordinates (in meters)
      npts      number of points computed for curve (higher more accurate but slower)

    OUT:
      x_min     2D array of TANGENTIAL distance to the curve
      y_min     2D array of NORMAL distance to the curve
      curve     bezier.Curve object (allows for simple plotting, e.g., curve.plot())
    """
    shape = data.x.shape + (data.source.size,)
    dims = data.x.dims + ("source",)

    data["xp"] = xr.DataArray(np.full(shape, np.nan), dims=dims)
    data["yp"] = xr.DataArray(np.full(shape, np.nan), dims=dims)

    x = data.x.values
    y = data.y.values

    for name, this in data.groupby("source", squeeze=False):

        this = this.isel(source=0)
        curve = BezierCurve(
            this["x_nodes"].values,
            this["y_nodes"].values,
            this["x_source"].values,
            this["y_source"].values
        )
        x_min, y_min = curve.compute_natural_coords(x, y, npts=npts)

        data.xp.loc[dict(source=name)][:,:] = x_min
        data.yp.loc[dict(source=name)][:,:] = y_min

    return data


def cost_function(p, x, y, w, p1=None, ps=None):
    """Distance between curve and detected pixels.

    p1: is first control point upstream of source
    ps: is the source location
    """
    x_nodes, y_nodes = p.reshape(-1,2).T
    w = w / w.mean()

    if ps is not None:
        x = np.insert(x, 0, ps[0])
        y = np.insert(y, 0, ps[1])
        w = np.insert(w, 0, 10)

    if p1 is not None:
        x = np.insert(x, 0, p1[0])
        y = np.insert(y, 0, p1[1])
        w = np.insert(w, 0, 10)

    # Evaluate points along the parametric curve
    t = np.linspace(0.0, 1.0, 100)
    xp, yp = bezier_curve(t, p.reshape(-1,2))

    # Establish shortest Euclidean distance (automatically corresponds to
    # shortest perpendicular distance between any point vs. the curve!)
    grid_coords = np.nan_to_num(np.vstack((x.ravel(), y.ravel())).T)
    curve_coords = np.vstack((xp.ravel(), yp.ravel())).T
    kdtree = scipy.spatial.KDTree(curve_coords)
    neighbours, idx = kdtree.query(grid_coords)

    return w * np.abs(neighbours)



def fit_to_detections(
    data,
    n_nodes=3,
    force_origin=False,
    use_weights=False,
):
    """
    Fit a 

    n_nodes (default: 3)
        Number of nodes for curve with either 2 or 3 for a line or a curve.
        Curves with larger number of likely very unstable.

    use_weights (default: True)
        Use z-values as weights for fit.
    """
    assert n_nodes >= 2

    x_nodes = []
    y_nodes = []

    for name in data.source:

        this = data.sel(source=name)

        # location of the source
        xs, ys = float(this.x_source), float(this.y_source)
        diameter = float(this.diameter_source)

        is_plume = this["detected_plume"].values
        is_plume = skimage.morphology.convex_hull_image(is_plume)

        pixel_size = np.sqrt(np.nanmean(this.pixel_area.values[is_plume]))

        #is_plume &= np.sqrt((this.x - xs)**2 + (this.y - ys)**2) <= diameter

        # Use z-values as weights
        weights = this["z_values"].values.copy()
        weights[(weights < 0.05) | np.isnan(weights)] = 0.05

        x = np.asarray(this.x)[is_plume]
        y = np.asarray(this.y)[is_plume]

        if use_weights:
            w = np.asarray(weights)[is_plume]
        else:
            w = np.ones_like(x)

        # vector through middle point of detection
        xc = np.nanmean(x)
        yc = np.nanmean(y)

        u = (xc - xs)
        v = (yc - ys)

        # point at the beginning of plume
        x1 = xs - max(6 * pixel_size, diameter) * u / np.sqrt(u**2 + v**2)
        y1 = ys - max(6 * pixel_size, diameter) * v / np.sqrt(u**2 + v**2)

        # point at the end of plume
        x2 = xs + 2 * u
        y2 = ys + 2 * v

        # starting nodes
        p0 = np.transpose([
            np.linspace(x1, x2, n_nodes),
            np.linspace(y1, y2, n_nodes)
        ])

        if force_origin:
            args = (x, y, w, (x1,y1), (xs,ys))
        else:
            args = (x, y, w, (x1,y1))


        res = scipy.optimize.least_squares(cost_function, p0.flatten(), args=args)
        xn, yn = res["x"].reshape(-1, 2).T

        x_nodes.append(xn)
        y_nodes.append(yn)

    # Add nodes to dataset
    data["x_nodes"] = xr.DataArray(
        np.transpose(x_nodes),
        dims=("nodes", "source"),
        attrs={"epsg": data.x.attrs["epsg"]}
    )
    data["y_nodes"] = xr.DataArray(
        np.transpose(y_nodes),
        dims=("nodes", "source"),
        attrs={"epsg": data.x.attrs["epsg"]}
    )

    return data


def compute_plume_areas(data, plume_width=None):

    xmins, xmaxs = [], []
    ymins, ymaxs = [], []
    areas = []

    for name in data.source:
        this = data.sel(source=name)

        # source diameter and pixel size
        source_diameter = float(this.diameter_source)
        pixel_size = float(ddeq.misc.get_pixel_size_at_source(this))

        # plume length
        xmin = float(this.xp.min())
        xmax = float(this.xp.max())

        if plume_width is None:
            if "detected_plume" in this:
                ymin = float(np.nanmin(this.yp.where(this.detected_plume))) - 5 * pixel_size
                ymax = float(np.nanmax(this.yp.where(this.detected_plume))) + 5 * pixel_size
            else:
                raise ValueError("Provide `plume_width` or \"detected plume\" in data.")
        else:
            ymin = -1.0 * plume_width / 2.0
            ymax = plume_width / 2.0

        xmins.append(xmin)
        xmaxs.append(xmax)
        ymins.append(ymin)
        ymaxs.append(ymax)

        # plume area that is used by the emission quantification method
        areas.append(
            (xmin <= this.xp) & (this.xp <= xmax) &
            (ymin <= this.yp) & (this.yp <= ymax)
        )

    # Area used for emission quantification definied by xmin, xmax, ymin and ymax
    data["plume_area"] = xr.DataArray(np.stack(areas, axis=-1), dims=data.xp.dims)
    data["plume_xmin"] = xr.DataArray(xmins, dims=data.source.dims)
    data["plume_xmax"] = xr.DataArray(xmaxs, dims=data.source.dims)
    data["plume_ymin"] = xr.DataArray(ymins, dims=data.source.dims)
    data["plume_ymax"] = xr.DataArray(ymaxs, dims=data.source.dims)

    return data
