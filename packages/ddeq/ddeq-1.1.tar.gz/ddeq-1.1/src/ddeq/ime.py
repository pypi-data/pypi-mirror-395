import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import xarray as xr

import ddeq


def estimate_emissions(
    data: xr.Dataset,
    winds: xr.Dataset,
    sources: xr.Dataset,
    gas: str,
    variable: str = "{gas}_minus_estimated_background_mass",
    L_min: float = 0,
    L_max: float = None,
    A_std: float = 0,
    decay_time: float = np.nan,
    min_pixel_number: int = 10,
    allowed_upstream_detected: int = 5,
    return_uncertainty_contributions: bool = False,
    quiet: bool = True,
):
    """
    Estimate emissions using the integrated mass enhancement (IME) method.

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing data from pre-processing.

    winds : xr.Dataset
        Wind for each source.

    sources : xr.Dataset
        Source dataset for which emissions will be estimated.

    gas : str
        Gas for which emissions will be estimated.

    variable : str, optional
        Name of variable in `data` with gas enhancement above background in mass
        columns (units: kg m-2).

    L_min : float, optional
        Along-plume distance where mass integration starts. Default is the
        source location, i.e. L_min = 0.0.

    L_max : float, optional
        Along-plume distance where mass integration ends. Default is the plume
        length minus 10 km, but at least 10 km.

    decay_time : float, optional
        The decay time of the gas in seconds. If np.nan, no decay time is used.

    min_pixel_number : int, optional
        Minimum number of pixels needed for estimating emissions.

    allowed_upstream_detected : int, optional
        Maximum number of pixels detected upstream of the source.

    Returns
    -------
    xr.Dataset
        Results dataset with estimated emissions for each source with additional
        parameters.
    """

    results = {}
    uncertainty_contributions = {}

    extra_variables = {
        "A_std": {"units": "m2"},
        "VCD_std": {"units": "kg m-2"},
        "L_min": {"units": "m"},
        "L_max": {"units": "m"},
        "L_std": {"units": "m"},
        "pixel_nr": {"description": "number of pixels used for IME"},
        "wind_speed": {"units": "m s-1", "method": winds.attrs.get("method", "-")},
        "wind_speed_precision": {"units": "m s-1"},
        "wind_direction": {"units": "°"},
        "angle_between_curve_and_wind": {"units": "°"},
        "emissions_scaling_factor": {"units": "1"},
        "integrated_{gas}_mass": {"units": "kg"},
        "integrated_{gas}_mass_precision": {"units": "kg"},
    }
    if not np.isnan(decay_time):
        extra_variables[f"{gas}_decay_time"] = {"units": "s"}

    if "time" in winds.dims:
        winds = winds.sel(time=data.time, method="nearest")

    for name, source in sources.groupby("source", squeeze=False):

        global_attrs = {"method": "integrated mass enhancement"}
        wind_method = winds.attrs.get("METHOD", None)

        if wind_method is not None:
            global_attrs["wind method"] = wind_method

        results[name] = ddeq.misc.init_results_dataset(
            source, [gas], extra_vars=extra_variables, global_attrs=global_attrs
        )
        uncertainty_contributions[name] = xr.Dataset(
            source,
            attrs={
                "description": "Contribution of different variables to the overall uncertainty of emission estimations. Calculated by setting the given uncertainty to 0."
            },
        )

        if name not in data.source:
            if not quiet:
                print(f"'{name}' does not exist in data. Skipping...")
            continue

        this = ddeq.misc.select_source(data, source=name)

        # minimum number of detected pixles for IME approach
        if this["detected_plume"].sum() <= min_pixel_number:
            print(
                f"Plume of '{name}' is smaller than {min_pixel_number} pixels. Skipping..."
            )
            continue

        # no multiple sources
        if ddeq.misc.has_multiple_sources(data, name):
            if not quiet:
                print(f"Plume of '{name}' overlaps with other sources. Skipping...")
            continue

        # no upstream detections for area sources
        pixel_size = np.sqrt(np.nanmean(this.pixel_area))
        upstream_detected = sum(this.xp.values[this.detected_plume] < -pixel_size)
        if (
            pixel_size > this["diameter_source"].values
            and upstream_detected > allowed_upstream_detected
        ):
            if not quiet:
                print(
                    f"'{name}' has {upstream_detected} detected pixels upstream of the source. Skipping..."
                )
            continue

        # plume area
        area = this["plume_area"].values

        # interpolate missing data
        VCD = this[variable.format(gas=gas)].values
        missing_data = np.isfinite(VCD)

        # fill cloud- and data-gaps
        kernel = ddeq.dplume.gaussian_kernel(sigma=2)
        VCD = np.where(
            np.isfinite(VCD), VCD, ddeq.misc.normalized_convolution(VCD, kernel)
        )

        # fraction of missing pixels in plume area
        fraction = np.sum(missing_data[area]) / np.sum(area)
        if fraction < 0.75:
            if not quiet:
                print(
                    f"'{name}' contains too many missing values ({int(fraction*100)}). Skipping..."
                )
            continue

        # plume length 10 km shorter than most distance detected pixel
        # but at least 10 km
        plume_length = np.max(this["xp"].values[area])

        if L_max is None:
            L_max = plume_length

            if L_max >= 20e3:
                L_max -= 10e3

        # reduce L_max if plume length is given and larger than detected plume
        elif L_max > plume_length:
            L_max = plume_length

        L = L_max - L_min

        # any missing values remain in detected plume
        if (
            np.sum(
                np.isnan(
                    VCD[
                        this["detected_plume"].values
                        & (L_min <= this.xp)
                        & (this.xp <= L_max)
                    ]
                )
            )
            > 0
        ):
            if not quiet:
                print(f"'{name}' contains missing values. Skipping...")
            continue

        # wind speed and its uncertainty
        wind = winds.sel(source=name)
        U = float(wind["speed"])
        D = float(wind["direction"])
        U_std = float(wind["speed_precision"])

        # compute integrated mass enhancement
        integration_area = area & (L_min <= this["xp"]) & (this["xp"] <= L_max)
        A = data["pixel_area"].values
        IME = np.nansum(VCD[integration_area] * A[integration_area])

        # 10% but at least half a pixel
        pixel_length = float(np.sqrt(np.mean(A[integration_area])))
        L_std = max(0.1 * L, 0.5 * pixel_length)
        VCD_std = this[f"{gas}_mass"].attrs.get("noise_level", np.nan)

        # Calculate flux
        flux = calculate_flux(IME, U, L, decay_time, L_min, L_max)

        # Calculate uncertainties
        uncertainties = {
            "A_std": (0, VCD_std, U_std, L_std),
            "VCD_std": (A_std, 0, U_std, L_std),
            "U_std": (A_std, VCD_std, 0, L_std),
            "L_std": (A_std, VCD_std, U_std, 0),
            "total_std": (A_std, VCD_std, U_std, L_std),
        }

        for key, (
            A_std_temp,
            VCD_std_temp,
            U_std_temp,
            L_std_temp,
        ) in uncertainties.items():

            IME_std, flux_std = calculate_uncertainties(
                A=A[integration_area],
                VCD=VCD[integration_area],
                U=U,
                L=L,
                A_std=A_std_temp,
                VCD_std=VCD_std_temp,
                U_std=U_std_temp,
                L_std=L_std_temp,
            )

            uncertainty_contributions[name] = uncertainty_contributions[name].assign(
                **{key: (("source"), [flux_std], {"units": "kg s-1"})}
            )

        variables_to_assign = {
            "A_std": A_std,
            "VCD_std": VCD_std,
            "L_min": L_min,
            "L_max": L_max,
            "L_std": L_std,
            "pixel_nr": integration_area.values.sum(),
            "wind_speed": U,
            "wind_speed_precision": U_std,
            "wind_direction": D,
            f"integrated_{gas}_mass": IME,
            f"integrated_{gas}_mass_precision": IME_std,
            f"{gas}_emissions": flux,
            f"{gas}_emissions_precision": flux_std,
        }
        if not np.isnan(decay_time):
            variables_to_assign[f"{gas}_decay_time"] = decay_time

        for var_name, value in variables_to_assign.items():
            attrs = results[name][var_name].attrs if var_name in results[name] else {}
            results[name] = results[name].assign(
                **{var_name: (("source"), [value], attrs)}
            )

    estimated_emissions = xr.concat(results.values(), dim="source")
    uncertainties = xr.concat(uncertainty_contributions.values(), dim="source")

    if return_uncertainty_contributions:
        return estimated_emissions, uncertainties
    else:
        return estimated_emissions


def calculate_flux(IME, U, L, decay_time=np.nan, L_min=0, L_max=None):
    """
    Calculate emission flux with or without decay time.
    """
    if np.isnan(decay_time):
        return U / L * IME
    else:
        L0 = U * decay_time
        c = decay_time * (np.exp(-L_min / L0) - np.exp(-L_max / L0))
        return IME / c


def calculate_uncertainties(A, VCD, U, L, A_std, VCD_std, U_std, L_std):
    """
    Calculate uncertainties in the flux estimation.
    """
    IME = np.nansum(VCD * A)

    IME_std = np.sqrt(A_std**2 * np.nansum(VCD**2) + VCD_std**2 * np.nansum(A**2))

    flux_std = (
        1.0
        / L
        * np.sqrt(
            U**2 * IME_std**2 + IME**2 * U_std**2 + U**2 * IME**2 / L**2 * L_std**2
        )
    )

    return IME_std, flux_std
