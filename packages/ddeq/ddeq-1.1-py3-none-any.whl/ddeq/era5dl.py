from typing import Tuple, Union, List

import os

import cdsapi
import pandas as pd

import ddeq


def _generate_time_list(timesteps: Union[int, list], time: pd.Timestamp) -> List[str]:
    # TODO: Replace with new ERA5Downloader
    """
    Generate the list of times based on timesteps.
    """
    if timesteps == 1:
        time = [time.round("h").strftime("%H:00")]
    elif timesteps == 24:
        time = [f"{hour:02d}:00" for hour in range(0, timesteps, 1)]
    else:
        time = [
            f"{hour:02d}:00"
            for hour in range(
                max(0, time.round("h").hour + 1 - timesteps),
                time.round("h").hour + 1,
                1,
            )
        ]

    return time


def _generate_era5_filename(
    data_path: str,
    prefix: str,
    timesteps: Union[int, list],
    time: pd.Timestamp,
    filename_type: str,
) -> str:
    # TODO: Replace with new ERA5Downloader
    """
    Generate the ERA5 filename based on timesteps, prefix, and code.
    """
    if prefix != "":
        prefix = prefix + "_"

    if timesteps == 24:
        era5_filename = os.path.join(
            data_path, time.strftime(f"{prefix}ERA5-{filename_type}-%Y%m%d.nc")
        )
    else:
        era5_filename = os.path.join(
            data_path, time.strftime(f"{prefix}ERA5-{filename_type}-%Y%m%dt%H00.nc")
        )

    return era5_filename


def download_pressure_lvl(
    time: pd.Timestamp,
    area: List[float],
    prefix: str = "",
    data_path: str = ".",
    overwrite: bool = False,
    timesteps: int = 1,
) -> str:
    # TODO: Replace with new ERA5Downloader
    """
    Download ERA-5 data on pressure levels of a given time step.
    Documentation: https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation

    timesteps :: number of hours to download on the given day.
        If 24, a full day will be returned.
    """
    # Extract area from dictionary providing north, west, south and east
    area = [area[s] for s in ["north", "west", "south", "east"]]

    era5_filename = _generate_era5_filename(
        data_path=data_path,
        prefix=prefix,
        timesteps=timesteps,
        time=time,
        filename_type="pl",
    )
    time_list = _generate_time_list(timesteps=timesteps, time=time)

    if os.path.exists(era5_filename) and not overwrite:
        return era5_filename

    cds = cdsapi.Client()

    query = {
        "product_type": "reanalysis",
        "date": time.strftime("%Y-%m-%d"),
        "time": time_list,
        "format": "netcdf",
        "variable": [
            "geopotential",
            "temperature",
            "u_component_of_wind",
            "v_component_of_wind",
        ],
        "pressure_level": [
            "700",
            "750",
            "775",
            "800",
            "825",
            "850",
            "875",
            "900",
            "925",
            "950",
            "975",
            "1000",
        ],
        "grid": [0.25, 0.25],
        "area": area,  # north, east, south, west
    }

    cds.retrieve("reanalysis-era5-pressure-levels", query, era5_filename)

    return era5_filename


def download_model_lvl(
    time: pd.Timestamp,
    area: List[float],
    prefix: str = "",
    data_path: str = ".",
    overwrite: bool = False,
    timesteps: int = 1,
) -> str:
    # TODO: Replace with new ERA5Downloader
    """
    Download ERA-5 data on model levels of a given time step.

    timesteps :: number of hours to download on the given day.
        If 24, a full day will be returned.
    """
    # Extract area from dictionary providing north, west, south and east
    area = [area[s] for s in ["north", "west", "south", "east"]]

    era5_filename = _generate_era5_filename(
        data_path=data_path,
        prefix=prefix,
        timesteps=timesteps,
        time=time,
        filename_type="ml",
    )
    time_list = _generate_time_list(timesteps=timesteps, time=time)

    if os.path.exists(era5_filename) and not overwrite:
        return era5_filename

    cds = cdsapi.Client()

    # data download specifications:
    cls = "ea"
    expver = "1"
    levtype = "ml"
    stream = "oper"
    tp = "an"
    date = time.strftime("%Y-%m-%d")
    grid = [0.25, 0.25]

    # model levels
    query_lvl = {
        #"class": cls,
        "date": date,
        #"expver": expver,
        # 1 is top level, 137 the lowest model level in ERA5
        "levelist": "100/to/137/by/1",
        "levtype": levtype,
        # temperature (t), u- and v-wind, and specific humidity (q)
        "param": "130/131/132/133",
        "stream": stream,
        "time": time_list,
        "type": tp,
        # Latitude/longitude grid: east-west (longitude) and north-south
        # resolution (latitude). Default: 0.25 x 0.25°
        "grid": grid,
        "area": area,  # North, West, South, East. Default: global
        "format": "netcdf",
    }

    cds.retrieve("reanalysis-era5-complete", query_lvl, era5_filename)

    return era5_filename


def download_single_lvl(
    time: pd.Timestamp,
    area: List[float],
    variables: Union[str, List[str]] = None,
    code: str = "",
    prefix: str = "",
    data_path: str = ".",
    overwrite: bool = False,
    timesteps: int = 1,
) -> str:
    # TODO: Replace with new ERA5Downloader
    """
    Download ERA-5 variables data of a given time step.

    time : pd.Timestamp,
        Time for which the pbl should be downloaded
    variables : Union[str, List[str]],
        Names of variables that will be downloaded such as
        'boundary_layer_height', '100m_u_component_of_wind',
        '100m_v_component_of_wind', '10m_u_component_of_wind' and
        '10m_v_component_of_wind'.
    area : List[float], Dict[float]
        North, West, South, East coordinates of area of interest,
        e.g [60, -10, 50, 2]
    code : str
        Code included in filename of downloaded data.
    prefix : str
        Prefix for the downloaded data
    data_path : str
        Path where to store the data
    overwrite : bool
        Indicates if the file should be overwritten if it already exists
    timesteps : int
        number of hours to download on the given day.
        If 24, a full day will be returned.

    Returns
    -------
    era5_filename_pbl : str
        Path to the downloaded ERA5 data
    """
    # Extract area from dictionary providing north, west, south and east
    area = [area[s] for s in ["north", "west", "south", "east"]]

    if variables is None:
        variables = [
            "100m_u_component_of_wind",
            "100m_v_component_of_wind",
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_temperature",
            "boundary_layer_height",
            "geopotential",
            "mean_sea_level_pressure",
            "surface_pressure",
            "total_cloud_cover",
        ]

    era5_filename = _generate_era5_filename(
        data_path=data_path,
        prefix=prefix,
        timesteps=timesteps,
        time=time,
        filename_type="sl",
    )
    time_list = _generate_time_list(timesteps=timesteps, time=time)

    if os.path.exists(era5_filename) and not overwrite:
        return era5_filename

    cds = cdsapi.Client()

    query = {
        "product_type": "reanalysis",
        "date": time.strftime("%Y-%m-%d"),
        "time": time_list,
        "format": "netcdf",
        "variable": variables,
        "grid": [0.25, 0.25],
        "area": area,
    }

    cds.retrieve("reanalysis-era5-single-levels", query, era5_filename)

    return era5_filename

