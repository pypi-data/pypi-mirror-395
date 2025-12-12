from pathlib import Path
import calendar

import numpy as np
import onnxruntime as rt
import pandas as pd
import xarray as xr

import ddeq
import ucat

PATH = Path("/input/CORSO/NOX_Models/")

from scipy.constants import g as G
R = 287.052874  # specific gas constant for dry air


def read_no2_profile(data, lvl):
    aux = ddeq.amf.read_aux_on_swath(data)
    pressure_mid = aux.hyam + aux.hybm * aux.ps
    pressure_int = aux.hyai + aux.hybi * aux.ps

    dh = R * aux.t / G * np.log(pressure_int[:-1].values / pressure_int[1:].values)
    dh = xr.where(np.isfinite(dh), dh, 0.0)
    h = dh.cumsum(dim='layer') - 0.5 * dh

    # add and invert height levels to match ERA-5
    aux["h"] = xr.DataArray(h)
    aux = aux.sel(layer=aux.layer[::-1]).copy()

    aux["p"] = xr.DataArray(pressure_mid)

    lvl["no2"] = ddeq.era5.interp_heights(lvl.h, aux, ['no2'], vcoord="layer")["NO2"].transpose(*lvl.h.dims)
    lvl["p"] = ddeq.era5.interp_heights(lvl.h, aux, ['p'], vcoord="layer")["P"].transpose(*lvl.h.dims)

    return lvl


def _quick_interp(values, time, lon, lat):
    value = np.interp(time.to_datetime64(), values.time, np.arange(values.time.size))
    index = int(value)
    weight = value % 1
    values = (1.0 - weight) * values.isel(time=index).interp(lon=lon, lat=lat) \
              + weight * values.isel(time=index+1).interp(lon=lon, lat=lat)
    return values


def predict_nox_chemistry(data, model="Europe"):
    """
    Test implementation for using ML models developed by Schooling et al. for
    computing NOx:NO2 ratio and NOx lifetime on TROPOMI swath over Europe
    (https://doi.org/10.5194/egusphere-2024-3949).
    """
    time = pd.Timestamp(data.attrs["time"])

    # Load ML models
    if model == "Europe":
        month = ["Jan", "Apr", "Jul", "Oct"][(time.month % 12) // 3]
        rate_model = rt.InferenceSession(PATH / "UEDIN-Europe" / f"FINALPredRate_{month}.onnx")
        ratio_model = rt.InferenceSession(PATH / "UEDIN-Europe" / f"FINALPredRatio_{month}.onnx")
    elif model == "global-with-coords":
        month = calendar.month_abbr[time.month]
        path = PATH / Path("UEDIN-global")
        rate_model = rt.InferenceSession(path / 'Rate_Apr_9P.onnx')
        ratio_model = rt.InferenceSession(path / 'Ratio_Apr_8P.onnx')

    elif model == "global-without-coords":
        month = calendar.month_abbr[time.month]
        path = PATH / Path("UEDIN-global")
        rate_model = joblib.load(path / 'Rate_Apr_7P.onnx')
        ratio_model = joblib.load(path / 'Ratio_Apr_6P.onnx')

    # Get parameters
    lvl_filename = time.strftime('/input/ERA5/CORSO/raw/ERA5-lvl-%Y%m%dt0000.nc')
    sng_filename = time.strftime('/input/ERA5/CORSO/raw/ERA5-sng-%Y%m%dt0000.nc')

    sza = data["solar_zenith_angle"]  #   0...90
    lon = data.lon                    # -15...40
    lat = data.lat                    # ...

    # Read TROPOMI AUX file (only 10 lowest layer, i.e. < 5 km)
    aux = ddeq.amf.read_aux_on_swath(data)
    aux = aux.isel(layer=slice(10))

    # Read ERA-5 on pressure levels and interpolate on AUX layers
    with ddeq.era5.open(lvl_filename) as nc:
        lvl = nc[["t", "q", "u", "v", "z"]]
        lvl = _quick_interp(lvl, time, lon, lat)
        lvl["h"] = lvl["z"] / G

    lvl = ddeq.era5.interp_heights(aux.h, lvl, vars=["t", "q", "u", "v"])

    # Read radiation at the surface
    with ddeq.era5.open("/input/ERA5/CORSO/ERA5-sng-2021-radiation.nc") as nc:
        rad = nc["avg_sdswrf"]
        rad = _quick_interp(rad, time, lon, lat)

    # NO2 to NOx conversion
    elev = aux["h"] # FIXME: Is this above model surface or sea surface?
    temp = aux["t"]
    humid = ucat.convert_points(lvl["Q"], "kg/kg", "m3/m3", molar_mass="H2O")
    wind = np.sqrt(lvl["U"]**2 + lvl["V"]**2) # in m/s

    # Model parameters
    if model in ["Europe", "global-with-coords"]:
        p = np.array([
            sza.expand_dims({"layer": aux.layer.size}, axis=-1),
            lon.expand_dims({"layer": aux.layer.size}, axis=-1),
            lat.expand_dims({"layer": aux.layer.size}, axis=-1),
            elev,
            rad.expand_dims({"layer": aux.layer.size}, axis=-1),
            temp,
            humid,
            wind
        ], dtype=np.float32)
    else:
        p = np.array([
            sza.expand_dims({"layer": aux.layer.size}, axis=-1),
            elev,
            rad.expand_dims({"layer": aux.layer.size}, axis=-1),
            temp,
            humid,
            wind
        ], dtype=np.float32)

    p = p.transpose(1,2,3,0)
    ratio = ratio_model.run(None, {'float_input': p.reshape(-1, 8)})[0]
    ratio = 1.0 / ratio.reshape(p.shape[:3])

    # Convert NO2 to NOx
    no2 = ucat.convert_points(aux.no2, "mol/mol", "cm-3", T=aux.t, p=aux.p, molar_mass="NO2")
    nox = ratio * no2

    # Model parameters
    if model in ["Europe", "global-with-coords"]:
        p = np.array([
            nox,
            sza.expand_dims({"layer": aux.layer.size}, axis=-1),
            lon.expand_dims({"layer": aux.layer.size}, axis=-1),
            lat.expand_dims({"layer": aux.layer.size}, axis=-1),
            elev,
            rad.expand_dims({"layer": aux.layer.size}, axis=-1),
            temp,
            humid,
            wind
        ], dtype=np.float32)
    else:
        p = np.array([
            nox,
            sza.expand_dims({"layer": aux.layer.size}, axis=-1),
            elev,
            rad.expand_dims({"layer": aux.layer.size}, axis=-1),
            temp,
            humid,
            wind
        ], dtype=np.float32)

    p = p.transpose(1,2,3,0)
    rate = rate_model.run(None, {'float_input': p.reshape(-1, 9)})[0]
    rate = rate.reshape(p.shape[:3])

    # mask outside training area (only geographical)
    if model == "Europe":
        mask = (data.lon.values < -15.0) | (data.lon.values > 40.0) \
             | (data.lat.values < 32.75) | (data.lat.values > 61.25)

        ratio[mask,:] = np.nan
        rate[mask,:] = np.nan

    # Compute lifetime
    lifetime = -1.0 * nox.values / rate

    # Create results dataset
    dims = data.lon.dims + ("layer", )
    d = xr.Dataset()
    d["h"] = xr.DataArray(elev.values, dims=dims)
    d["ratio"] = xr.DataArray(ratio, dims=dims)
    d["lifetime"] = xr.DataArray(lifetime, dims=dims)
    d["nox"] = xr.DataArray(nox.values, dims=dims)

    # Compute columns
    ratio_column = ddeq.era5.vertically_weighted_mean(d["h"], d["ratio"], "layer")
    lifetime_column = ddeq.era5.vertically_weighted_mean(d["h"], d["lifetime"], "layer")

    if model == "Europe":
        ratio_column.values[mask] = np.nan
        lifetime_column.values[mask] = np.nan

    d["NOx_NO2_column_ratio"] = xr.DataArray(ratio_column, dims=data.lon.dims)
    d["NOx_column_lifetime"] = xr.DataArray(lifetime_column, dims=data.lon.dims)

    return d

