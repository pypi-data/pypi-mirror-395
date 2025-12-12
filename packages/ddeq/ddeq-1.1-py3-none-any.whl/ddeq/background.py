import numpy as np
import scipy.ndimage
import skimage.morphology
import xarray as xr

import ddeq


"""\
The background module can be used to estimate the background field from the
results of the plume detection algorithm.
"""


def create_gaussian_kernel(sigma):
    """
    Create a Gaussian kernel with standard deviation `sigma` pixels. The shape
    of the kernel is at least (11,11) and at most (5*sigma, 5*sigma).
    """
    # size should be odd and at least 11 pixels
    size = max(11, int(5 * sigma))
    if size % 2 == 0:
        size += 1

    kernel = np.zeros((size, size))
    kernel[size // 2, size // 2] = 1.0
    kernel = scipy.ndimage.gaussian_filter(kernel, sigma=sigma)

    return kernel


def estimate(data, variable, sigma=10.0, mask_hits=True, extra_dilation=None):
    """\
    Estimate smooth varible background using normalized convolution. Returns
    data with added dataarray '{variable}_estimated_background'.

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing data containg `variable` as well as `is_hit` and
        `plume_area`.

    variable : str
        Name of variable for background calculation.

    sigma : number, optional
        Size of Gaussian kernel used for normalized convolution in pixels
        (default: 10 pixels).

    mask_hits : boolean, optional
        If True, all significantly enhanced values found by the plume detection
        algoritm are masked otherwise only the plume area is masked.

    extra_dilation : number, optional
        If not None add extra dilation of masked pixels using a disk with
        given radius given by `extra_dilation`.

    Returns
    -------
    xr.Dataset
        Remote sensing dataset with added estimated background field.
    """
    c = np.array(data[variable])

    # only use pixels that are in plume area around plume without enhanced values
    if mask_hits:
        valids = np.array(~data.is_hit)
    else:
        if "source" in data.plume_area.dims:
            valids = np.logical_not(np.array(data.plume_area.any("source")))
        else:
            valids = np.logical_not(np.array(data.plume_area))

    valids[~np.isfinite(c)] = False

    if extra_dilation is not None:
        disk = skimage.morphology.disk(extra_dilation)
        valids = ~skimage.morphology.dilation(~valids, disk)

    kernel = create_gaussian_kernel(sigma)

    c[~valids] = np.nan
    bg_est = ddeq.misc.normalized_convolution(c, kernel, mask=~valids)
    bg_est = xr.DataArray(
        bg_est, name=f"{variable}_estimated_background", dims=data[variable].dims
    )
    attrs_dict = {
        "units": data[variable].attrs.get("units", None),
        "long name": f"estimated {variable} background",
        "method": f"normalized convolution (sigma = {sigma:.1f} px)",
    }
    bg_est.attrs.update(attrs_dict)

    data[f"{variable}_estimated_background"] = bg_est

    return data
