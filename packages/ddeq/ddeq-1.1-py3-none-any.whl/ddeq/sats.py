import glob
import os
import warnings

import numpy as np
import pandas as pd
import xarray as xr
import scipy

import ddeq
import ucat

_PSD_GROUP = "PRODUCT/SUPPORT_DATA/DETAILED_RESULTS"
_PSG_GROUP = "PRODUCT/SUPPORT_DATA/GEOLOCATIONS"
_PSI_GROUP = "PRODUCT/SUPPORT_DATA/INPUT_DATA"


class Level2TropomiDataset:
    def __init__(self, pattern, root="", qa_value=0.75):
        """
        Level-2 class for TROPOMI NO2 product.

        Parameters
        ----------
        pattern : str
            A filename pattern used to match the TROPOMI files based on given
            date. Date formatting is used to find the correct file using, for
            example, "S5P_NO2_%Y%m%d.nc".

        root : str
            Data path to TROPOMI files.
        qa_value : float
            Sets the minimum quality assurance (qa) value. Recommended by the 
            TROPOMI team is to accept values above 0.75 
        """
        self.pattern = os.path.join(root, pattern)
        self.qa_value = qa_value

    def get_filenames(self, date):
        """
        foo
        """
        return sorted(glob.glob(date.strftime(self.pattern)))

    def read_date(self, date):
        """
        Returns a list of TROPOMI NO2 Level-2 data.

        Parameters
        ----------
        date : datetime.datetime

        Returns
        -------
        list of xr.Dataset
            List of TROPOMI datasets for given date.
        """
        R = []
        for filename in self.get_filenames(date):
            F = xr.open_dataset(filename)
            F = F.where(F.qa_value > self.qa_value)
            R.append(F)
        return R


def read_S5P(filename, gas='NO2', qa_value=0.75):
    """
    Read S5P/TROPOMI Level-2 file and prepare for emission quantification.
    """
    data = ddeq.download_S5P.open_netCDF(filename, path=None)
    data = ddeq.download_S5P.reduce_dims_and_vars(data)

    # Set time array and (mean) time attribute
    del data["time"]
    data = data.rename_vars(delta_time="time")
    data["time"].attrs["long_name"] = "Time of observation"
    data.attrs["time"] = str(np.mean(data["time"]).values)
    data["time_utc"] = data["time_utc"].astype('str')

    # Rename vars
    if gas == 'NO2':
        data = data.rename_vars({
            'nitrogendioxide_tropospheric_column': 'NO2',
            'nitrogendioxide_tropospheric_column_precision': 'NO2_std',
        })
    elif gas == 'SO2':
        data = data.rename_vars({
            'sulfurdioxide_total_vertical_column': 'SO2',
            'sulfurdioxide_total_vertical_column_precision': 'SO2_std',
        })

    # Mask low quality data
    data[gas] = data[gas].where(data.qa_value > qa_value, np.nan)

    # Add `noise_level` attribute
    data[gas].attrs['noise_level'] = float(data[f'{gas}_std'].mean())

    return data


def iter_S5P_swath(filename, gas='NO2', step=200, latitude_clip=[-60, +80],
                   preprocessed=False):
    """
    Iterate over Level-2 swath in small chunks of scanlines. The chunk size
    is the 2x `step` and includes an additional border of `step` scanlines
    at the bottom and top. While the inner chunk will be used for plume
    detection, the border gives space for plumes and can help to identify
    plumes of neighboring sources.

    The iterator will also clip latitude and remove scanlines of the
    descending part of the orbit.
    """
    if preprocessed:
        data = xr.open_dataset(filename)
    else:
        data = read_S5P(filename, gas=gas)

    # clip data and keep only ascending orbit
    clat = data.lat.isel(ground_pixel=data.ground_pixel.size//2).values
    gradient = np.append(np.diff(clat), clat[-1]-clat[-2])
    mask = (clat > latitude_clip[0]) & (clat < latitude_clip[1]) & (gradient > 0)
    data = data.isel(scanline=mask)

    for i in np.arange(step, data.scanline.size, step):

        # Select chunk
        chunk = data.isel(scanline=slice(i-step, i+step))

        # Add mask for center of chunk
        center = np.zeros(chunk.scanline.size, dtype="bool")
        center[step-step//2:step+step//2] = True
        chunk["chunk_center"] = xr.DataArray(
            center,
            dims="scanline",
            coords={"scanline": chunk.scanline}
        )

        yield chunk


def read_level2(
    filename, product="nitrogendioxide_tropospheric_column", qa_threshold=0.75
):
    """
    Read Tropomi NO2 fields. Works with version from NASA data portal.
    """
    warnings.warn(
        '`ddeq.sats.read_level2` is deprecated and will be removed in future versions.',
        DeprecationWarning
    )

    data = xr.Dataset()

    with xr.open_dataset(filename) as nc_file:
        data.attrs.update(nc_file.attrs)

    with xr.open_dataset(filename, group="PRODUCT") as nc_file:
        data["time_utc"] = nc_file["time_utc"].copy()
        data["time_utc"] = data["time_utc"].astype("datetime64[ns]")

        data["lon"] = nc_file["longitude"].copy()
        data["lat"] = nc_file["latitude"].copy()

        # TODO: use independent estimate of standard deviation
        data["NO2"] = nc_file[product].copy()
        data["NO2_std"] = nc_file[f"{product}_precision"].copy()
        data["NO2_std"][:] = 14e-6

        data["qa_value"] = nc_file["qa_value"].copy()
        data["NO2"] = data["NO2"].where(data["qa_value"] > qa_threshold)

    with xr.open_dataset(filename, group=_PSG_GROUP) as nc_file:
        data["lonc"] = nc_file["longitude_bounds"].copy()
        data["latc"] = nc_file["latitude_bounds"].copy()

    with xr.open_dataset(filename, group=_PSD_GROUP) as nc_file:
        data["clouds"] = nc_file[
            "cloud_radiance_fraction_nitrogendioxide_window"
        ].copy()

    # surface pressure in product from NASA portal is already in Pa
    # in contrast to user guide which claims hPa
    with xr.open_dataset(filename, group=_PSI_GROUP) as nc_file:
        data["psurf"] = nc_file["surface_pressure"].copy()

    return data


def read_S5P_NO2_matlab_file(filename):
    """
    Reads TROPOMI NO2 data from matlab files created in CoCO2 project.
    """
    warnings.warn(
        '`ddeq.sats.read_S5P_NO2_matlab_file` is deprecated and will be removed in future versions.',
        DeprecationWarning
    )

    F = scipy.io.loadmat(filename)

    time = np.asarray([pd.to_datetime(time) for time in F["time_utc"][:, 0]])[
        :, 0
    ].astype("datetime64[ns]")

    shape = F["nitrogendioxide_tropospheric_column"].T.shape

    data = xr.Dataset(
        data_vars=dict(
            NO2=(["nobs", "nrows"], F["nitrogendioxide_tropospheric_column"].T),
            NO2_std=(
                ["nobs", "nrows"],
                F["nitrogendioxide_tropospheric_column_precision"].T,
            ),
            latc=(["nobs", "nrows", "corner"], F["latitude_bounds"].T),
            lonc=(["nobs", "nrows", "corner"], F["longitude_bounds"].T),
            time_utc=(["nobs"], time),
            psurf=(["nobs", "nrows"], F["surface_pressure"].T),
            clouds=(["nobs", "nrows"], np.full(shape, 0.0)),
        ),
        coords=dict(
            lat=(["nobs", "nrows"], F["latitude"].T),
            lon=(["nobs", "nrows"], F["longitude"].T),
            time=(time[0]),
        ),
        attrs=dict(description="TROPOMI"),
    )
    data["NO2"].attrs.update(
        {
            "cloud_threshold": 0.30,
            "units": "mol m-2",
            "noise_level": 15e-6,
        }
    )
    data["NO2_std"][:] = 15e-6
    data["NO2_std"].attrs.update({"cloud_threshold": 0.30, "units": "mol m-2"})

    data["NO2"].values[F["qa_value"].T < 0.75] = np.nan
    data["NO2_std"].values[F["qa_value"].T < 0.75] = np.nan

    return data


def read_gems(filename):
    """
    Read GEMS NO2 data of IUP Bremen product.
    """
    data = xr.Dataset()
    with xr.open_dataset(filename, group="PRODUCT", mode="r") as sat:
        data["lat"] = sat["latitude"].isel(time=0)
        data["lon"] = sat["longitude"].isel(time=0)

        # mask bad values
        no2 = sat["nitrogendioxide_tropospheric_vertical_column_density"].isel(time=0)
        no2 = no2.where(sat["qa_value"].isel(time=0) > 0.75)
        no2 = ucat.convert_columns(no2, "cm-2", "mol m-2")
        data["NO2"] = no2

        # TODO: Air mass factor correction (assumming delta profile?)

    with xr.open_dataset(filename, group="PRODUCT/SUPPORT_DATA/GEOLOCATIONS") as sat:
        data["latc"] = sat["latitude_bounds"].isel(time=0)
        data["lonc"] = sat["longitude_bounds"].isel(time=0)

    with xr.open_dataset(filename, group="PRODUCT/SUPPORT_DATA/INPUT_DATA") as input:
        data["surface_height"] = 1e3 * input["surface_height"].isel(time=0)
        data["surface_height"].attrs["units"] = "m"

    return data
