import re
import cdsapi
import ddeq.wind
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


################################ DOWNLOAD FILES ################################

# Download reanalysis files


# Download model spread


################################# MODIFY FILES #################################
def rename_era5_dims(data: xr.Dataset) -> xr.Dataset:
    """
    Rename dimensions of an ERA5 dataset for consistency.
    """
    data = data.rename(
        {
            "valid_time": "time",
            "latitude": "lat",
            "longitude": "lon",
        }
    )

    return data


def rename_era5_wind_vars(data: xr.Dataset) -> xr.Dataset:
    """
    Rename ERA5 variables to standardized names (U, V).
    """
    rename_dict = {}
    for var in data.variables:
        if var in ["u", "u10", "u100"]:
            rename_dict[var] = "U"
        elif var in ["v", "v10", "v100"]:
            rename_dict[var] = "V"

    return data.rename(rename_dict)


def drop_era5_vars(data: xr.Dataset) -> xr.Dataset:
    """
    Drop unwanted coordinates (e.g., 'number', 'expver') from an ERA5 dataset.
    Should not be applied to ERA5 ensemble members.
    """
    for var in ["number", "expver"]:
        if var in data.coords:
            data = data.drop_vars(var)

    return data


################################## READ FILES ##################################
def prepare_gnfra(
    era5_filename_lvl: Union[str, Path], era5_filename_sfc: Union[str, Path]
) -> xr.Dataset:
    """
    Prepare GNFR-A weighted wind dataset using ERA5 input files.
    """

    weighted_wind = ddeq.wind.calculate_gnfra_weighted_winds(
        era5_filename_lvl, era5_filename_sfc
    )
    weighted_wind = weighted_wind[["u", "v"]]
    wind = ddeq.wind.prepare_era5_data(wind_data=weighted_wind)

    method = "GNFR-A weighted vertical mean"
    description = (
        "U- and V-wind component vertically weighted for GNFR-A "
        "emission profile (Brunner et al. 2019)"
    )
    wind = ddeq.wind.calc_wind_speed(wind, method, description)

    return wind


def prepare_pbl_mean(
    era5_filename_lvl: Union[str, Path],
    era5_filename_sfc: Union[str, Path],
    era5_filename_pbl: Union[str, Path],
    min_pbl_height: float = 400,
) -> xr.Dataset:
    """
    Prepare planetary boundary layer (PBL) mean wind dataset using ERA5 input files.
    """

    era5_pbl = xr.open_dataset(era5_filename_pbl)
    wind_height = compute_height_levels(era5_filename_lvl, era5_filename_sfc)

    wind_data = xr.merge([wind_height, era5_pbl[["blh"]]])

    # select data below pbl
    wind_pbl = wind.where(wind_data.h <= wind_data.blh)
    wind_pbl["blh"] = wind_pbl.blh.mean(dim="model_level", keep_attrs=True)

    # only use values where the blh is higher than 400m (based on GNFR-A profile)
    wind_pbl = wind_pbl.mean("model_level", keep_attrs=True)
    wind_pbl = wind_pbl.where(wind_pbl.blh > min_pbl_height)
    wind_pbl = wind_pbl[["u", "v", "blh"]]

    wind = ddeq.wind.prepare_era5_data(wind_data=wind_pbl)

    method = "pbl mean"
    description = (
        "Vertical mean of U- and V-wind component inside the planetary "
        "boundary layer"
    )
    wind = ddeq.wind.calc_wind_speed(wind, method, description)

    return wind


def prepare_pressure_lvl_mean(era5_filename_lvl: Union[str, Path]) -> xr.Dataset:
    """
    Prepare unweighted vertical mean wind dataset for pressure levels using ERA5 input file.
    """
    era5_lvl = xr.open_dataset(era5_filename_lvl)
    wind = ddeq.wind.prepare_era5_data(wind_data=era5_lvl)

    pres_lvls = wind.pressure_level.values.astype(int).tolist()
    wind = wind.mean("pressure_level", keep_attrs=True)

    method = "unweighted vertical mean"
    description = (
        f"Unweighted mean of U- and V-wind component of the pressure levels {pres_lvls}"
    )
    wind = ddeq.wind.calc_wind_speed(wind, method, description)

    return wind


def prepare_single_lvl(era5_filename_sfc: Union[str, Path]) -> xr.Dataset:
    """
    Prepare wind data for a single level (e.g., surface) using ERA5 input file.
    """
    era5_sfc = xr.open_dataset(era5_filename_sfc)
    height = _get_era5_wind_height(era5_sfc)
    wind = ddeq.wind.prepare_era5_data(wind_data=era5_sfc)

    method = f"{height} m wind"
    description = f"U- and V-wind component at {height} m"
    wind = ddeq.wind.calc_wind_speed(wind, method, description)

    return wind


def _get_era5_wind_height(wind_data: xr.Dataset) -> int:
    """
    Extract height information from the wind data variable name.
    """
    for var in wind_data.data_vars:
        # Check if the variable is named "uXX" or "vXX"
        match = re.match(r"[uv](\d+)", var)
        if match:
            return int(match.group(1))



