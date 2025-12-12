import warnings

import cartopy.crs as ccrs
import numpy as np
import scipy.ndimage
import scipy.stats
import shapely
import skimage.measure
import xarray as xr
import ddeq
from typing import Union, Tuple

# --- Load diplib quietly, so as to not crowd the std out
import contextlib

with contextlib.redirect_stdout(None):
    import diplib as dip

# ignore warnings
warnings.filterwarnings("ignore", r"All-NaN (slice|axis) encountered")
np.seterr(divide="ignore", invalid="ignore")


def find_plume_by_labels(
    data: xr.DataArray,
    labels: np.ndarray,
    lon_o: Union[float, xr.DataArray],
    lat_o: Union[float, xr.DataArray],
    radius: int,
) -> np.ndarray:
    """
    Find plume by using `labels` that are within `radius` (in pixels)  around
    (`lon_o`, `lat_o`).

    Args:
        data (xr.DataArray):
            Dataset which contains the coordinates.
        labels (np.ndarray):
            Array containing the labelled plumes.
        lon_o (float):
            Longitude of the source.
        lat_o (float):
            Latitude of the source.
        radius (int):
            Radius around the source in pixels.

    Returns:
        np.ndarray:
            Array containing only the pixels which are assigned to the source.
    """
    lon_o = lon_o.values if isinstance(lon_o, xr.DataArray) else lon_o
    lat_o = lat_o.values if isinstance(lat_o, xr.DataArray) else lat_o
    radius = radius.values if isinstance(radius, xr.DataArray) else radius

    # get the pixel which contains the source
    lat_i, lon_i, dist = ddeq.misc.find_closest(data, ("lon", "lat"), (lon_o, lat_o))

    # create empty field containing the source
    source_field = np.zeros_like(labels)
    source_field[lat_i, lon_i] = 1

    # add buffer around the source with radius in pixels
    # FIXME: Generates a memory error if the source diameter has a similar size as the source_field
    footprint = skimage.morphology.disk(radius)
    dilated_source = skimage.morphology.binary_dilation(
        source_field, footprint=footprint
    )

    numbers = []
    for l in set(labels.flatten()) - {0}:
        hit = np.any(np.logical_and(dilated_source, np.where(labels == l, 1, 0)))

        if hit:
            numbers.append(l)

    if numbers:
        return np.any([labels == i for i in numbers], axis=0)
    else:
        return np.zeros(labels.shape, bool)



def label_plumes(d: np.ndarray, n_min: int = 0) -> np.ndarray:
    """\
    Label detected plume pixels. Regions with less than n_min are removed.
    """
    d[np.isnan(d)] = 0
    labels = skimage.measure.label(d, background=0)

    i = 1
    final = np.zeros_like(labels)

    for l in set(labels.flatten()):
        if l != 0 and np.sum(labels == l) >= n_min:
            final[labels == l] = i
            i += 1

    return final


def do_test(mean_s, mean_b, var_rand, var_sys, size, q, variance=None, dtype="f4"):
    """
    mean_s:    mean of sample
    mean_b:    mean of background
    variance:  estimated local variance

    var_rand:  random variance of sample
    var_sys:   systematic variance of sample
    size:      size of sample
    q:         threshold

                 mean_s - mean_bg
    SNR = ----------------------------- > z_q
           np.sqrt(var_rand + var_sys)
    """
    mean_s = np.array(mean_s)
    size = np.array(size)

    if np.ndim(mean_b) == 0:
        mean_b = np.full(mean_s.shape, mean_b)

    if variance is None:
        z_values = np.full(mean_s.shape, np.nan)
        m = size > 0

        z_values[m] = mean_s[m] - mean_b[m]
        z_values[m] /= np.sqrt(var_rand / size[m] + var_sys)
    else:
        z_values = (mean_s - mean_b) / np.sqrt(variance)

    return z_values.astype(dtype), z_values > scipy.stats.norm.ppf(q)


def weighted_mean(x, kernel):
    """
    Computed weighted mean.
    """
    valids = np.isfinite(x)

    if np.any(valids):
        kernel = kernel[valids]
        kernel = kernel / kernel.sum()

        return np.sum(x[valids] * kernel)
    else:
        return np.nan


def weighted_mean_var(x, kernel, variance):
    """
    Compute variance reduction of weighted mean.
    """
    valids = np.isfinite(x)

    if np.any(valids):
        kernel = kernel[valids]
        kernel = kernel / kernel.sum()

        return variance * np.sum(kernel**2)
    else:
        return np.nan


def gaussian_kernel(sigma, size=11):
    """
    Create a gaussian kernel.
    """
    if size % 2 == 0:
        raise ValueError("kernel size needs to be an odd integer")

    f = np.zeros([size, size])
    f[size // 2, size // 2] = 1.0
    g = scipy.ndimage.gaussian_filter(f, sigma=sigma)
    return g


def local_mean(
    img: xr.DataArray,
    size: int,
    kernel_type: str = "gaussian",
    var_rand: Union[int, float] = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute local mean, variance reduction and number of valid pixels using
    different kernel_types:

    Args:
        img (xr.DataArray):
            Field from which local means have to be calculated.
        size (int):
            Size of the kernel.
            - neighborhood: radius
            - gaussian: standard deviation
            - uniform: width
        kernel_type (str, optional):
            Type of kernel to be applied. 'gaussian', 'uniform', 'neighborhood'
        var_rand (Union[int, float], optional):
            Variance due to random errors.

    Raises:
        ValueError: Raise error if 'kernel_type' is not implemented

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: mean, variance, n
    """

    if kernel_type == "uniform" and size == 1:
        mean = img.copy()
        var = var_rand * np.ones_like(mean)
        n = np.isfinite(mean).astype(int)
        return mean, var, n

    if kernel_type == "gaussian":
        footprint = gaussian_kernel(sigma=size)

    elif kernel_type == "uniform":
        footprint = np.ones((size, size))

    elif kernel_type == "neighborhood":
        footprint = skimage.morphology.disk(size)

    else:
        raise ValueError(
            '"kernel_type" needs to be "gaussian", "uniform" or "neighborhood"'
        )

    # only compute if any values in across-track direction
    domain = np.any(img, axis=1)

    # normalize footprint
    footprint = footprint / footprint.sum()

    # keep dtype of image
    footprint = footprint.astype(img.dtype)

    # compute mean, variance and number of valid pixels
    mean = np.full(img.shape, np.nan, dtype=img.dtype)
    var = np.full(img.shape, np.nan, dtype=img.dtype)
    n = np.full(img.shape, np.nan, dtype=int)

    mean[domain, :] = scipy.ndimage.generic_filter(
        img[domain, :],
        function=weighted_mean,
        size=footprint.shape,
        mode="constant",
        cval=np.nan,
        extra_arguments=(footprint.flatten(),),
    )
    var[domain, :] = scipy.ndimage.generic_filter(
        img[domain, :],
        function=weighted_mean_var,
        size=footprint.shape,
        mode="constant",
        cval=np.nan,
        extra_arguments=(footprint.flatten(), var_rand),
    )
    n[domain, :] = scipy.ndimage.generic_filter(
        np.isfinite(img).astype(int)[domain, :],
        np.count_nonzero,
        footprint=(footprint != 0),
        mode="constant",
        cval=0,
    )

    return mean, var, n


def local_median(img, size):
    """
    Compute local median for image.
    """
    #return scipy.ndimage.generic_filter(img, np.nanmedian, size)
    bg = ddeq.misc.normalized_convolution(
        img.values,
        np.ones((size,size)) / size**2
    )
    return scipy.ndimage.median_filter(bg, size)


def overlaps_with_sources(lon, lat, lon_source, lat_source, diameters):
    """
    lon, lat      longitude and latitude of satellite pixels
    lon_source, lat_source  longitudes and latitudes of point sources
    diameters     diameters of sources (in meters)

    """
    # use only valid longitudes and latitudes
    mask = np.isfinite(lon) & np.isfinite(lat)
    lon = np.ma.array(lon, mask=~mask)
    lat = np.ma.array(lat, mask=~mask)

    # Make a polygon for each scanline
    polygons = []
    for i in range(lon.shape[0] - 1):
        # If there is a jump about the antimeridian, split the scanline
        jumps = np.abs(np.diff(lon[i])) > 100
        split_indices = np.where(jumps)[0] + 1
        split_indices = np.concatenate(([0], split_indices, [lon.shape[1]]))

        for j in range(len(split_indices) - 1):
            start, end = split_indices[j], split_indices[j+1]
            if end - start < 2:
                continue  # not enough points to make a polygon

            lon_block = lon[i:i+2, start:end]
            lat_block = lat[i:i+2, start:end]

            # Skip if any values are masked
            if np.ma.any(lon_block.mask) or np.ma.any(lat_block.mask):
                continue

            # Build polygon: follow edges clockwise
            coords = np.transpose([
                np.concatenate([lon_block[0], lon_block[1][::-1], [lon_block[0][0]]]),
                np.concatenate([lat_block[0], lat_block[1][::-1], [lat_block[0][0]]]),
            ])

            poly = shapely.geometry.Polygon(coords)
            poly = poly.buffer(0)  # fix potential invalid polygons
            # Could be plotted as such
            # shapely.plotting.plot_polygon(poly)
            # plt.show()

            if poly.is_valid:
                polygons.append(poly)

    # Merge all scanlines (allowing for some imprecision)
    buffer_size = min(2.0 * np.nanmedian(np.diff(lon.data)), 2) # in degrees
    merged = shapely.ops.unary_union([p.buffer(buffer_size) for p in polygons])
    merged = merged.buffer(-buffer_size)
    # Could be plotted as such
    # shapely.plotting.plot_polygon(merged)
    # plt.show()

    # create area around source
    overlaps = []

    for lon0, lat0, diameter in zip(lon_source, lat_source, diameters):
        point = shapely.geometry.Point(lon0, lat0)
        area = ddeq.sources.buffer_point(point, 0.5 * diameter)
        overlaps.append(merged.intersects(area))

    return np.array(overlaps, dtype="bool")


def generate_downstream_masks(data, wind_dir_at_source, source, cost_image):
    """
    This finds the cost of moving from the source to any other
    point in an image. Moving downwind is cheap (where np.cos(0°)=1),
    and moving backwards is not allowed.
    This allows us to select purely the downstream portion of any
    detected plume, disregarding any upstream data.

    data                xr dataframe
    wind_dir_at_source  wind direction at the source (0 degrees is wind from the North)
    source              xr dataset of source
    cost_image          numpy array (=1/is_hit)
    """
    # Find the indices on the grid closest to the source
    lon_s, lat_s, _ = ddeq.sources.get_location(source)
    dist = (data.lon - lon_s).values ** 2 + (data.lat - lat_s).values ** 2
    idx, idy = np.unravel_index(dist.argmin(), dist.shape)

    # Correct for the difference between grid "up" and North direction
    delta = (
        np.rad2deg(
            np.arctan2(np.gradient(data.lat, axis=0), -np.gradient(data.lon, axis=0))
        )
        + 90
    )[
        idx, idy
    ]  # (this field...
    #    delta=0    means the track goes north,
    #    delta=pi/2 means the track goes east, etc.

    angle_matrix = np.array(
        [[+225, +180, +135], [+270, np.nan, +90], [+315, +0, +45]]
    )  # The range [0, 45, ..., 360] degrees layed around this matrix

    metric = 1 - np.cos(np.deg2rad(float(wind_dir_at_source) - delta + angle_matrix))
    metric[metric > 1] = -1
    metric[1, 1] = 0

    # Perform a weighted distance walk.
    binimg = np.zeros_like(cost_image)
    binimg[idx, idy] = 1
    out = dip.GreyWeightedDistanceTransform(
        cost_image, dip.Image(binimg) == 0, metric=metric, mode="chamfer"
    )
    mask = out < 10
    return mask


def unmix_plumes(data, sources, winds, pixel_size, min_plume_size=0):
    """
    After running the plume detection algorithm, overlapping plumes
    are discarded. This function recovers the portions of the plume
    prior to mixing (i.e., from the source, downstream to the place
    where the plumes overlap).

    data                xarray dataset with observations etc.
    sources             xarray dataset with source locations
    winds               xarray dataset with wind directions
    pixel_size          pixel size in meters
    """
    # Preserve the originally detected plumes
    data["detected_plume_orig"] = data.detected_plume.copy(deep=True)

    # Copy the Boolean 'is_hit' field into an image field
    # (1 where is_hit=True, 1e5 otherwise)
    cost_image = dip.Image(1 / (data.is_hit.values + 1e-5))

    # Loop through all sources a second time, checking for overlaps
    for source in data.source:
        # Returns, e.g., [True, False, False, True]
        # if source[0] and source[3] overlap.

        list_of_overlaps = (
            data.detected_plume_orig.sel(source=source) * data.detected_plume_orig
        ).any(dim=data.is_hit.dims)

        # Default: no overlap, nothing to do
        if list_of_overlaps.sum() <= 1:
            continue

        # Get list of overlapping sources
        names_of_overlaps = data.source[list_of_overlaps].values

        # Get corresponding wind directions
        wind_direction = [
            winds.direction.sel(source=name).values for name in names_of_overlaps
        ]

        # Compute directional (downstream) plume masks
        masks = []
        for i, name in enumerate(data.source[list_of_overlaps]):
            mask = generate_downstream_masks(
                data, wind_direction[i], sources.sel(source=name), cost_image
            )
            masks.append(mask)

        # Fix the mask belonging to the source
        source_idx = np.where(data.source[list_of_overlaps] == source)[0][0]

        mask_source = masks[source_idx]
        masks.pop(source_idx)

        # Remove masks if they are downstream
        for mask in masks:
            mask_source -= mask

        # Relabel the detected plumes
        labels = label_plumes(data.is_hit.values * mask_source, min_plume_size)

        lon_source, lat_source, diameter = ddeq.sources.get_location(sources, source)
        data.detected_plume.loc[dict(source=source)] = find_plume_by_labels(
            data,
            labels,
            lon_source,
            lat_source,
            max(0.5 * float(diameter) / pixel_size, 3.0),
        )

    return data


def detect_plumes(
    data: xr.Dataset,
    sources: xr.Dataset,
    variable: str,
    variable_std: str,
    var_sys: float = 0.0,
    filter_type: str = "gaussian",
    filter_size: float = 0.5,
    q: float = 0.99,
    thr: float = None,
    min_plume_size: float = 0,
    background: str = "median",
    crs=None,
):
    """
    Detects plumes inside remote sensing `data` and assigns them to given
    `sources`.

    Parameters
    ----------
    data : xr.Dataset
        Dataset of remote sensing data read, for example, by
        `ddeq.smartcarb.read_level2`

    sources : xr.Dataset
        Dataset with source locations read, for example, by
        `ddeq.misc.read_point_sources`.

    variable : str, optional
        Name of data array in `data` with the trace gas columns that is used
        for plume detection.

    variable_str : str, optional
        Name of data array in `data` with the uncertainty of the trace gas
        columns.

    var_sys : float, optional
        Systematic uncertainty of the trace gas field that is not reduced by
        spatial averaging. Standard values used in the SMARTCARB and CoCO2
        project were (0.2 ppm)**2 for CO2 and (0.5e15 cm-2 = 8.3e-6 mol/m²)**2
        for NO2.

    filter_type : str, optional
        Name of filter used for computing the local mean can be "gaussian"
        (default), "uniform" or "neighborhood" (see `ddeq.dplume.local_mean` for
        details).

    filter_size : number, optional
        Size of filter user for computing the locam mean in pixels. Needs to be
        an integer for "uniform" and "neighborhood".

    q : float, optional
        probability for threshold z(q) that a pixel is significantly enhanced
        above the background used for the statistical z-test.

    thr : float, optional
        Threshold for plume segmention in gas units. If provided the threshold
        will be applied to the local enhancement instead of using the z-test
        on the signal-to-noise ratio.

    min_plume_size : integer, optional
        Minimum size of connected pixels that are considered a plume (default:
        0).

    background : np.array, float or string, optional
        If number, the background used for the plume detection. The default
        value is "median", which computes the background field using a median
        filter of 100 by 100 pixels.

    Returns
    -------
    xr.Dataset
        Returns `data` with added variables (e.g., `detected_plumes`) that
        contain the results from the plume detection algorithm.

    """
    # Avoid running expensive plume detection when no sources in swath
    if "chunk_center" in data:
        overlaps = overlaps_with_sources(
            data.lon.where(data["chunk_center"]),
            data.lat.where(data["chunk_center"]),
            *ddeq.sources.get_location(sources),
        )
    else:
        overlaps = overlaps_with_sources(
            data.lon,
            data.lat,
            *ddeq.sources.get_location(sources),
        )

    # Add overlapping sources to dataset
    sources = sources.where(xr.DataArray(overlaps, dims="source"), drop=True)
    data["source"] = sources["source"].copy()
    data["label_source"] = sources["label"].copy()
    data["lon_source"], data["lat_source"], data["diameter_source"] = (
        ddeq.sources.get_location(sources)
    )

    # Compute easting and northing and pixel areas
    data = ddeq.plume_coords.compute_xy_coords(data, crs)
    data = ddeq.plume_coords.compute_pixel_areas(data)
    pixel_size = float(np.sqrt(np.mean(data["pixel_area"])))

    # Return dataset if no sources in dataset
    if not np.any(overlaps):
        return data

    # Detect plume
    # Estimate background mean
    if isinstance(background, str) and background == "median":
        mean_bg = local_median(data[variable], 50)
    else:
        mean_bg = background

    # Estimate random and systematic error of observations
    # Random noise (use scalar)
    var_rand = np.nanmean(data[variable_std].values) ** 2

    # TODO: estimate systemtic error from data (?)

    # Local mean, variance and number of valid pixels
    mean_s, variance, n_s = local_mean(
        data[variable], size=filter_size, kernel_type=filter_type, var_rand=var_rand
    )

    variance = variance + var_sys
    n_s = np.array(n_s, dtype="f4")

    # Z-test
    detected_plume = np.zeros(data[variable].shape + data["source"].shape, dtype=bool)
    if thr is None:
        z_values, is_hit = do_test(
            mean_s, mean_bg, None, None, n_s, q, variance=variance
        )
    else:
        is_hit = np.array(mean_s - mean_bg) > thr
        z_values = np.full(is_hit.shape, np.nan)

    # Label plumes
    labels = label_plumes(is_hit, min_plume_size)

    # Identify plumes intersecting with sources
    for j, name in enumerate(data["source"]):
        lon_s, lat_s, diameter = ddeq.sources.get_location(sources, name)
        detected_plume[:, :, j] = find_plume_by_labels(
            data, labels, lon_s, lat_s, max(0.5 * float(diameter) / pixel_size, 3.0)
        )

    # Dict with some additional info used for visualizing results
    if thr is None:
        attrs = {
            "trace_gas": variable,
            "probability for z-value": q,
            "filter_type": filter_type,
            "filter_size": filter_size,
            "trace_gas_uncertainty (random)": np.sqrt(var_rand),
            "trace_gas_uncertainty (systematic)": np.sqrt(var_sys),
        }
    else:
        attrs = {
            "trace_gas": variable,
            "threshold": thr,
            "filter_type": filter_type,
            "filter_size": filter_size,
        }

    data.attrs.update(attrs)

    dims = data[variable].dims

    data[f"{variable}_local_median"] = xr.DataArray(
        mean_bg,
        dims=dims,
        attrs={
            "description": f"Local median of {variable}",
            "units": data[variable].attrs.get("units", None),
        },
    )
    data["z_values"] = xr.DataArray(
        z_values,
        dims=dims,
        attrs={"description": "z-values calculated from the plume detection"},
    )
    data["is_hit"] = xr.DataArray(
        is_hit, dims=dims, attrs={"description": "pixel is part of a detected plume"}
    )
    data["labels"] = xr.DataArray(
        labels, dims=dims, attrs={"description": "Labels assigned to detected plumes"}
    )
    data[f"local_{variable}_mean"] = xr.DataArray(
        mean_s,
        dims=dims,
        attrs={
            "description": f"Local mean of {variable}",
            "units": data[variable].attrs.get("units", None),
        },
    )

    if n_s is not None:
        data[f"local_{variable}_pixels"] = xr.DataArray(n_s, dims=dims)

    data["detected_plume"] = xr.DataArray(detected_plume, dims=dims + ("source",))

    return data



def detect_from_wind(
    data: xr.Dataset,
    sources: xr.Dataset,
    winds: xr.Dataset,
    dmax: float,
    crs,

):
    """\
    Detect plume locations from wind directions assuming plumes are downstream of
    sources.

    Parameters
    ----------
    data : xr.Dataset
        Dataset of remote sensing data read, for example, by
        `ddeq.smartcarb.read_level2`

    sources : xr.Dataset
        Dataset with source locations read, for example, by
        `ddeq.misc.read_point_sources`.

    winds : xr.Dataset
        Dataset with wind at sources.

    pixel_size : float
        Size of pixel (in meters)
    """
    # Avoid running plume detection when no sources in swath
    # FIXME: this does not work on the date line
    if "chunk_center" in data:
        overlaps = overlaps_with_sources(
            data.lon.where(data["chunk_center"]),
            data.lat.where(data["chunk_center"]),
            *ddeq.sources.get_location(sources),
        )
    else:
        overlaps = overlaps_with_sources(
            data.lon,
            data.lat,
            *ddeq.sources.get_location(sources),
        )

    # Return dataset if no sources in dataset
    if not np.any(overlaps):
        return data

    # Add overlapping sources to dataset
    sources = sources.where(xr.DataArray(overlaps, dims="source"), drop=True)
    data["source"] = sources["source"].copy()
    data["label_source"] = sources["label"].copy()
    data["lon_source"], data["lat_source"], data["diameter_source"] = (
        ddeq.sources.get_location(sources)
    )

    # Compute easting and northing and pixel areas
    data = ddeq.plume_coords.compute_xy_coords(data, crs)
    data = ddeq.plume_coords.compute_pixel_areas(data)

    # Init nodes
    n_nodes = 2
    data["x_nodes"] = xr.DataArray(
        np.full((n_nodes, data.source.size), np.nan),
        dims=("nodes", "source"),
        attrs={"epsg": data.x.attrs["epsg"]}
    )
    data["y_nodes"] = xr.DataArray(
        np.full((n_nodes, data.source.size), np.nan),
        dims=("nodes", "source"),
        attrs={"epsg": data.x.attrs["epsg"]}
    )

    for name, source in sources.groupby("source", squeeze=False):

        this = data.sel(source=name)
        x0 = float(data.x_source.sel(source=name))
        y0 = float(data.y_source.sel(source=name))

        # detect plume using wind vector
        U = float(winds.U.sel(source=name)[0])
        V = float(winds.V.sel(source=name)[0])

        u0 = U / np.sqrt(U**2 + V**2)
        v0 = V / np.sqrt(U**2 + V**2)

        lon0 = float(data.lon_source.sel(source=name))
        lat0 = float(data.lat_source.sel(source=name))

        # scaling
        s = dmax / ddeq.misc.distance_between_coordinates(lon0, lat0, lon0 + u0, lat0 + v0)

        lon1 = lon0 + s * u0
        lat1 = lat0 + s * v0

        x1, y1 = crs.transform_point(lon1, lat1, ccrs.PlateCarree())

        # Add nodes to dataset
        this["x_nodes"][:] = np.array([x0, x1])
        this["y_nodes"][:] = np.array([y0, y1])

    return data





