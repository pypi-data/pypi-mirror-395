
import glob
import os

import numpy as np
import pandas as pd
import ucat
import xarray as xr

import ddeq

from scipy.constants import g as GACC
R = 287.052874  # specific gas constant for dry air
GAMMA = -0.0065 # lapse rate


def read_aux_on_swath(data, path="/input/CORSO/TROPOMI/aux/"):
    """\
    Read AUX file and interpolate to time, longitude and latitude in data.

    TODO:
    - Correct for height difference between AUX and data.
    - Add ERA-5 data
    """
    time = pd.Timestamp(data.attrs['time'])
    pattern = time.strftime(
        'S5P_OPER_AUX_CTMANA_%Y%m%dT000000_????????T000000_????????T??????.nc'
    )
    # TODO: check if taken last makes sense
    try:
        aux_filename = sorted(glob.glob(os.path.join(path, pattern)))[-1]
    except IndexError:
        raise IndexError(f'No AUX file for "{pattern}" in "{path}".')

    # open aux filename and interpolate to remote sensing image
    aux = xr.open_dataset(aux_filename)
    aux = aux.interp(lon=data.lon, lat=data.lat,
                     time=pd.Timestamp(data.attrs['time']),
                     method='linear')

    # re-arange to make compatible with data
    aux = aux.rename(lev='layer')
    aux = aux.assign_coords({"layer": data.layer})
    aux = aux.transpose(Ellipsis, *data.averaging_kernel.dims)

    del aux["time"]

    # TOPOGRAPHY CORRECTION (Zhou et al. 2009)

    # pressure levels in middle and at interface
    pressure_mid = aux.hyam + aux.hybm * aux.ps
    pressure_int = data.tm5_constant_a + data.tm5_constant_b * aux.ps

    # correct surface pressure for topography (Zhou et al. 2009)
    # (TODO: update temperature profile)
    ps_eff = aux.ps * (aux.t[0] / (aux.t[0] + GAMMA * (aux.surface_altitude - data.surface_altitude))) ** (-GACC / R / GAMMA)

    # effective pressure levels in middle and at interface
    pressure_mid_eff = aux.hyam + aux.hybm * ps_eff
    pressure_int_eff = data.tm5_constant_a + data.tm5_constant_b * ps_eff

    # layer thickness and mid height (TODO: use virtual temperature)
    dh = R * aux.t / GACC * np.log(pressure_int_eff.sel(vertices=0) / pressure_int_eff.sel(vertices=1))
    dh = xr.where(np.isfinite(dh), dh, 0.0)
    h = dh.cumsum(dim='layer') - 0.5 * dh

    aux["dh"] = dh
    aux["h"] = h
    aux["p"] = pressure_mid_eff


    # profile correction for topography
    for gas in ["so2", "no2", "ch2o"]:
        topo_correction = (
            (pressure_int_eff.sel(vertices=0) - pressure_int_eff.sel(vertices=1))
            / (pressure_int.sel(vertices=0) - pressure_int.sel(vertices=1))
        )

        values = ucat.convert_points(
            aux[gas] * topo_correction,
            "mol mol-1",
            "mol m-3",
            p=pressure_mid_eff,
            T=aux.t,
            molar_mass=aux[gas].attrs["moleweight_tracer"],
        )
        attrs = {
            "standard_name": aux[gas].attrs['standard_name'].replace("mole_fraction", "molar_concentration"),
            "long_name": aux[gas].attrs['long_name'].replace("volume mixing ratio", "molar concentration"),
            "units": "mol m-3"
        }
        aux[f"{gas}_model"] = xr.DataArray(values, dims=aux[gas].dims, attrs=attrs)

        #
        aux[f"{gas}_raw"] = ucat.convert_points(
            aux[gas],
            "mol mol-1",
            "mol m-3",
            p=pressure_mid_eff,
            T=aux.t,
            molar_mass=aux[gas].attrs["moleweight_tracer"],
        )

    return aux


def compute_gnfra_weights_on_aux(aux):
    """
    Compute GNFR-A weights on aux file. This is slow for large datasets.
    """
    # GNFR-A profile
    h_gnfra = np.linspace(100,1000,501)
    w_gnfra = ddeq.era5.get_gnfra_profile(h_gnfra)

    profile = xr.Dataset()
    profile["h"] = xr.DataArray(h_gnfra, dims="z")
    profile["w"] = xr.DataArray(w_gnfra, dims="z")
    profile = profile.set_coords("h")

    # Top and bottom of TM5 layers
    index = (aux.h + 0.5 * aux.dh > 1000).argmax("layer").max() + 1
    pbl = dict(layer=range(int(index)))
    bottom = aux.h.sel(pbl) - 0.5 * aux.dh.sel(pbl)
    top = aux.h.sel(pbl) + 0.5 * aux.dh.sel(pbl)

    # Integrate within intervals to get weights
    mask = (bottom <= profile.z) & (profile.z < top)

    weights = xr.zeros_like(aux.h)
    weights.loc[pbl] = profile.w.where(mask, 0.0).sum("z")
    weights /= weights.sum("layer")

    return weights


def correct_amf_from_csf_method(data, emissions, source_name):
    """
    Air mass factor correction for TROPOMI NO2 product using TROPOMI NO2 and AUX
    dataset and emission estimated by CSF method.

    AMF correction assumes that NO2 enhancement (above background) described by
    Gaussian curve in CSF method adds an NO2 enhancement to the low-resolution
    AUX NO2 profile with the shape of the GNFR-A profile. The new NO2 profile is
    used with the averaging kernels to apply the AMF correction. The correction
    is only applied to the polygon in the plume area used for fitting the Gaussian
    curve.

    Returns `data` with added "NO2_amf" and "NO2_amf_mass" data arrays with the
    vertical column densities after AMF correction.
    """
    # get data for given source and only first polygon (FIXME)
    this = data.sel(source=[source_name])
    polygon = emissions.sel(source=source_name, polygon=0)
    mask = (polygon.xa <= this.xp ) & (this.xp <= this.xp) & (polygon.ya <= this.yp) & (this.yp <= polygon.yb)

    if emissions.polygon.size > 1:
        print("Warning: AMF correction only applied to first polygon in CSF results.")

    # Read AUX on TROPOMI Level 1 in polygon area
    this = this.where(mask, drop=True).squeeze()
    aux = ddeq.amf.read_aux_on_swath(this)

    # Add GNFR-A weights to AUX dataset
    weights = compute_gnfra_weights_on_aux(aux)

    # Compute NO2 enhancement from Gaussian curve
    no2_enhancement = ddeq.functions.gauss(this.yp, *[float(polygon[name]) for name in ["NO2_line_density", "NO2_standard_width", "NO2_shift"]])
    no2_enhancement = ucat.convert_columns(no2_enhancement, "kg m-2", "mol m-2", molar_mass="NO2")

    # Calculate layer VCDs from AUX NO2 profile and NO2 enhancement
    layer_vcd = aux.no2_model * aux.dh + no2_enhancement * weights

    # Compute new AMF (FIXME: tropopause cutoff not fully consistent with standard product)
    trop_mask = (this.averaging_kernel.layer <= aux.tropopause_layer_index - 1).astype(float)
    layer_amfs = this.air_mass_factor_total * this.averaging_kernel
    M_new = (trop_mask * layer_amfs * layer_vcd ).sum("layer") / (trop_mask * layer_vcd).sum("layer")

    # Apply AMF correction
    loc = dict(scanline=this.scanline, ground_pixel=this.ground_pixel)
    data["NO2_amf"] = data.NO2.copy()
    data["NO2_amf"].loc[loc] = this.NO2 * this.air_mass_factor_troposphere / M_new

    ddeq.emissions.convert_units(data, "NO2", "NO2_amf")

    return data


def update_vcds(data, path, gas='NO2', max_iter=10):
    """
    Update vertical column densities (VCD) of `gas` by recomputing air mass
    factors (AMF) for Sentinel-5P/TROPOMI data. The method computes
    the mean concentration in the boundary layer from ERA-5 boundary layer
    height and TROPOMI `gas` enhancement above the background
    (i.e. `gas` - `gas`_estimated_background).

    The mean concentration is used to update the TM5 a priori profiles in
    the boundary layer and to compute the air mass factor using the
    averaging kernels. Since updating the AMFs will increase the enhancement,
    iteration is used till convergence.

    The method will only update AMFs for pixels that have been detected as
    enhanced above the background by the plume detection algorithm.

    The function will recompute {gas}_minus_estimated_background and the mass
    columns from the updated `gas` VCDS.
    """

    # if not valid data at detected pixels do not update
    if np.all(np.isnan(data[gas].values[data.is_hit])):
        return data

    # read AUX file and interpolate to dataset
    aux = read_aux_on_data(data, path=path)

    # Averaging kernels above tropopause to zero for tropospheric AMF
    if gas == 'NO2':
        amf_varname = 'air_mass_factor_troposphere'
        AK = xr.where(data.averaging_kernel.layer >= aux.tropopause_layer_index,
                      data.averaging_kernel, data.averaging_kernel)
    else:
        amf_varname = 'air_mass_factor'
        AK = data.averaging_kernel.copy()

    AMF = data[amf_varname].copy()

    # Convert TM5 to molar concentration (TODO: account for humidity)
    TM5_profiles = ucat.convert_points(values, 'mol mol-1', 'mol m-3',
                                       p=pressure_mid_eff, T=aux.t)

    data = data.rename(**{gas: f'{gas}_standard',
                          amf_varname: f'{amf_varname}_standard'})

    # Iterative update AMFs and VCDs
    VCD_current = data[f'{gas}_standard'].copy()

    for i in range(max_iter):

        # Compute concentration in boundary layer (mol / m³)
        inside_blh = (VCD_current - data[f'{gas}_estimated_background']) / data.blh

        profile = xr.where((h <= data.blh) & data.is_hit,
                           inside_blh, TM5_profiles)

        # Update AMFs and VCDs
        AMF_update = AMF * (AK * profile * dh).sum('layer') / (profile * dh).sum('layer')
        VCD_update = AMF * data[f'{gas}_standard'] / AMF_update

        change = np.nanmean(
            np.abs(VCD_update.values[data.is_hit] - VCD_current.values[data.is_hit])
            / VCD_current.values[data.is_hit]
        )
        if change <= 0.01:
            break

        VCD_current, VCD_update = VCD_update, None

    else:
        raise ValueError(f'Maximum number of iterations ({max_iter}) without convergence.')

    # Add updated VCDs and AMFs to remote sensing dataset
    data[gas] = xr.DataArray(
        VCD_update,
        dims=data[f'{gas}_standard'].dims,
        attrs=data[f'{gas}_standard'].attrs
    )
    data[gas].attrs['comment'] = 'AMF correction applied assuming well-mixed profile for pixels with enhanced columns.'

    data[amf_varname] = xr.DataArray(
        AMF_update,
        dims=data[f'{amf_varname}_standard'].dims,
        attrs=data[f'{amf_varname}_standard'].attrs
    )
    data[amf_varname].attrs['comment'] = 'AMF correction applied assuming well-mixed profile for pixels with enhanced columns.'


    # Update fields from plume detection and pre-processing
    # (i.e. {gas}_minus_estimated_background and *_mass)
    data[f'{gas}_minus_estimated_background'] = data[gas] - data[f'{gas}_estimated_background']

    data[f'{gas}_mass'] = xr.DataArray(
            ucat.convert_columns(data[gas], 'mol m-2', 'kg m-2', molar_mass=gas),
            dims=data[f'{gas}_mass'].dims, attrs=data[f'{gas}_mass'].attrs
    )
    data[f'{gas}_minus_estimated_background_mass'] = xr.DataArray(
            ucat.convert_columns(data[f'{gas}_minus_estimated_background'],
                                 'mol m-2', 'kg m-2', molar_mass=gas),
            dims=data[f'{gas}_minus_estimated_background_mass'].dims,
            attrs=data[f'{gas}_minus_estimated_background_mass'].attrs
    )

    return data