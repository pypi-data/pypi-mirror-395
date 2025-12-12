#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:59:25 2022

@author: nurmelaj
"""

import glob
import fnmatch
import time

import numpy as np
import pandas as pd
import scipy.optimize
import xarray as xr
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

import ddeq
import ucat


def gridded_divergence(
    datasets,
    wind,
    date,
    latgrid,
    longrid,
    latgrid_km,
    longrid_km,
    wind_product="ERA5",
    varname="CO2",
    gas="CO2",
    smooth_data=True,
    remove_background=True,
):
    """
    smooth_data
    remove_background
    """
    # NOTE: species = 'NO2' actually corresponds 'NOx' divergence

    # Shape of the area
    shape = (len(latgrid_km), len(longrid_km))

    # Initiate gridded array for chosen species
    species_gridded = np.full(shape, np.nan)
    species_Fx_flux = np.full(shape, np.nan)
    species_Fy_flux = np.full(shape, np.nan)

    images = []
    species_grids = []
    div_grids = []

    for i, file in enumerate(datasets.read_date(date)):

        filename = datasets.get_filenames(date)[i]

        if "psurf" in file:
            psurf = file.psurf.data.flatten()
        else:
            psurf = file.surface_pressure.data.flatten()

        lon = file.lon.data.flatten()
        lat = file.lat.data.flatten()

        data = file[varname].data
        units = file[varname].attrs["units"]

        if smooth_data:
            kernel = np.ones((5, 5)) / 25
            data = ddeq.misc.normalized_convolution(data, kernel).flatten()
        else:
            data = data.flatten()

        inside_ind = indices_inside_grid(lon, lat, longrid, latgrid, enlarge=0.1)

        if len(inside_ind) == 0:
            continue

        psurf, lon, lat = psurf[inside_ind], lon[inside_ind], lat[inside_ind]
        data = data[inside_ind]

        # Check if the area contains any data for the chosen species
        if np.all(np.isnan(data)):
            continue

        # Append the file name/image
        images.append(filename)

        # XCO2 anomaly inside the chosen grid, excluding points with distance
        # less than 10 km to the grid center
        center_lon = longrid[(shape[0] - 1) // 2, (shape[1] - 1) // 2]
        center_lat = latgrid[(shape[0] - 1) // 2, (shape[1] - 1) // 2]

        # Distances in metres of each data pixel to the center point of the grid
        dists = np.asarray(
            ddeq.misc.EARTH.inverse(
                np.repeat([(center_lon, center_lat)], len(data), axis=0),
                np.column_stack((lon, lat)),
            )
        )[:, 0]

        # Remove CO2 background
        if remove_background:
            data = data - np.nanmedian(data[np.where(dists >= 10000)])

        # Change units from to molec/m^2
        data = ucat.convert_columns(data, units, "m-2", molar_mass=gas, p_surface=psurf)

        # Get wind data from xarray dataset
        wu = wind["U_GNFR_A"][0, :, :].data
        wv = wind["V_GNFR_A"][0, :, :].data

        if wind_product == "ERA5":
            wlon = wind["longitude"][:].data
            wlat = wind["latitude"][:].data
        elif wind_product == "SMARTCARB":
            wlon = wind["lon"][:, :].data
            wlat = wind["lat"][:, :].data

        # Interpolate wind spatially in spherical coordinates
        wu_interp = ddeq.wind.spatial_interpolation(wu, wlon, wlat, lon, lat)
        wv_interp = ddeq.wind.spatial_interpolation(wv, wlon, wlat, lon, lat)

        # Fluxes at each data coordinate
        Fx = data * wu_interp
        Fy = data * wv_interp

        # Gridding using undersampling, grid resolution should be about the same
        # or less than the data resolution, each value of the grid is an average
        # of the values inside the grid pixel
        for r in range(shape[0]):
            if r == 0:
                lat_diff_north = np.mean(latgrid[0, :] - latgrid[1, :])
                lat_diff_south = latgrid[r, 0] - latgrid[r + 1, 0]
            elif r == shape[0] - 1:
                lat_diff_north = latgrid[r - 1, 0] - latgrid[r, 0]
                lat_diff_south = np.mean(latgrid[-2, :] - latgrid[-1, :])
            else:
                lat_diff_north = latgrid[r - 1, 0] - latgrid[r, 0]
                lat_diff_south = latgrid[r, 0] - latgrid[r + 1, 0]
            ind_lat = np.where(
                (latgrid[r, 0] - lat_diff_south / 2 <= lat)
                & (lat <= latgrid[r, 0] + lat_diff_north / 2)
            )[0]

            if not ind_lat.any():
                continue

            for c in range(shape[1]):
                if c == 0:
                    lon_diff_east = longrid[r, c + 1] - longrid[r, c]
                    lon_diff_west = longrid[r, 1] - longrid[r, 0]
                elif c == shape[1] - 1:
                    lon_diff_east = longrid[r, -1] - longrid[r, -2]
                    lon_diff_west = longrid[r, c] - longrid[r, c - 1]
                else:
                    lon_diff_east = longrid[r, c + 1] - longrid[r, c]
                    lon_diff_west = longrid[r, c] - longrid[r, c - 1]

                ind_lon = np.where(
                    (longrid[r, c] - lon_diff_west / 2 <= lon[ind_lat])
                    & (lon[ind_lat] <= (longrid[r, c] + lon_diff_east / 2))
                )[0]

                if not ind_lon.any():
                    continue

                # Average data values inside each grid pixels
                if np.isnan(species_gridded[r, c]):
                    species_gridded[r, c] = np.nanmean(data[ind_lat][ind_lon])
                else:
                    species_gridded[r, c] += np.nanmean(data[ind_lat][ind_lon])

                if np.isnan(species_Fx_flux[r, c]):
                    species_Fx_flux[r, c] = np.nanmean(Fx[ind_lat][ind_lon])
                else:
                    species_Fx_flux[r, c] += np.nanmean(Fx[ind_lat][ind_lon])

                if np.isnan(species_Fy_flux[r, c]):
                    species_Fy_flux[r, c] = np.nanmean(Fy[ind_lat][ind_lon])
                else:
                    species_Fy_flux[r, c] += np.nanmean(Fy[ind_lat][ind_lon])

        species_grids.append(species_gridded)

        # Divergence map for gridded values in g/m²/s or Mg/km²/s
        # Coefficient to convert NO2 to NOx, normally above 1.0
        coef = 0.9571 if gas == "NO2" else 1.0
        div_map = (
            1e3
            * ucat.M[gas]
            / ucat.N_A
            * divergence(
                [coef * species_Fx_flux, coef * species_Fy_flux],
                [longrid_km * 1e3, latgrid_km * 1e3],
            )
        )
        # Conversion from Mg/km²/s to g/km²/s
        div_map = 1e6 * div_map
        div_grids.append(div_map)

    if len(images) != 0:
        grid_xr = xr.DataArray(
            species_grids,
            dims=["n_images", "latgrid", "longrid"],
            attrs={"long name": f"gridded {gas}", "units": "molec m-2"},
        )
        div_xr = xr.DataArray(
            div_grids,
            dims=["n_images", "latgrid", "longrid"],
            attrs={"long name": f"Divergence of {gas}", "units": "g m-2 s-1"},
        )
    else:
        grid_xr = xr.DataArray(
            np.full((0, shape[0], shape[1]), np.nan),
            dims=["n_images", "latgrid", "longrid"],
            attrs={"long name": f"gridded {gas}", "units": "molec m-2"},
        )
        div_xr = xr.DataArray(
            np.full((0, shape[0], shape[1]), np.nan),
            dims=["n_images", "latgrid", "longrid"],
            attrs={"long name": f"Divergence of {gas}", "units": "g m-2 s-1"},
        )

    # Save to xarray dataset
    data_vars = {
        f"{gas}_grid": grid_xr,
        f"{gas}_div": div_xr,
        "longrid": xr.DataArray(longrid, dims=["latgrid", "longrid"]),
        "latgrid": xr.DataArray(latgrid, dims=["latgrid", "longrid"]),
        "longrid_km": xr.DataArray(longrid_km, dims=["longrid"]),
        "latgrid_km": xr.DataArray(latgrid_km, dims=["latgrid"]),
        "images": xr.DataArray(images, dims=["n_images"]),
    }
    attrs = {"Description": f"Gridded {gas} data values and fluxes"}

    return xr.Dataset(data_vars=data_vars, attrs=attrs)


def divergence(f, sp):
    """
    Computes divergence of vector field
    f: array -> vector field components [Fx,Fy,Fz,...]
    sp: array -> spacing between points in respective directions
    [spx,spy,spz,...]
    """
    d = len(f)
    grad = [np.gradient(f[i], sp[i], axis=d - 1 - i) for i in range(d)]
    return np.ufunc.reduce(np.add, grad)


def indices_inside_grid(data_x, data_y, grid_x, grid_y, enlarge=0.0):
    if grid_x.ndim == 1 and grid_y.ndim == 1:
        indices = np.where(
            (np.min(grid_x) - enlarge <= data_x)
            & (data_x <= np.max(grid_x) + enlarge)
            & (np.min(grid_y) - enlarge <= data_y)
            & (data_y <= np.max(grid_y) + enlarge)
        )[0]
    elif grid_x.ndim == 2 and grid_y.ndim == 2:
        # Four lines limiting the grid
        top_line = (
            lambda x: (grid_y[0, -1] - grid_y[0, 0])
            / (grid_x[0, -1] - grid_x[0, 0])
            * (x - grid_x[0, 0])
            + grid_y[0, 0]
            + enlarge
        )
        bottom_line = (
            lambda x: (grid_y[-1, -1] - grid_y[-1, 0])
            / (grid_x[-1, -1] - grid_x[-1, 0])
            * (x - grid_x[-1, -1])
            + grid_y[-1, -1]
            - enlarge
        )
        left_line = (
            lambda y: (grid_x[-1, 0] - grid_x[0, 0])
            / (grid_y[-1, 0] - grid_y[0, 0])
            * (y - grid_y[0, 0])
            + grid_x[0, 0]
            - enlarge
        )
        right_line = (
            lambda y: (grid_x[-1, -1] - grid_x[0, -1])
            / (grid_y[-1, -1] - grid_y[0, -1])
            * (y - grid_y[0, -1])
            + grid_x[0, -1]
            + enlarge
        )

        indices = np.where(
            (bottom_line(data_x) <= data_y)
            & (data_y <= top_line(data_x))
            & (left_line(data_y) <= data_x)
            & (data_x <= right_line(data_y))
        )[0]
    return indices


def model_residual(theta, grids, data):
    """
    Residual function.
    """
    G = ddeq.functions.peak_model(*theta, grids)
    # Remove nan, inf and -inf values
    valids = np.isfinite(data)
    # Residual vector with length equal to the valid data values
    residual = (G[valids] - data[valids]).ravel()
    return residual


def estimate_emissions(
    datasets,
    wind_folder,
    sources,
    lon_km=50,
    lat_km=50,
    grid_reso=5,
    varnames=["CO2"],
    wind_product="ERA5",
    pattern="ERA5-gnfra-%Y%m%dt%H00.nc",
    start_date="2015-01-01",
    end_date="2015-12-24",
    hour=11,
    AM_options={"warmup": 10000, "samples": 100000},
    trace_gases=["CO2"],
    smooth_data=[True],
    remove_background=[True],
):
    """
    Estimate emissions using the divergence (DIV) method for given sources over
    the chosen time period. The method computes first the divergence map and
    second the emissions using a peak fitting model.

    Parameters
    ----------
    datasets : object
        A dataset class such as `ddeq.sats.Level2TropomiDataset` or
        `ddeq.smartcarb.Level2Dataset` with a `read_date` method that returns
        a list of remote sensing datasets for a given day.

    wind_folder : str
        The data path to the wind product.

    sources : xr.Dataset
        Source dataset for which emissions will be estimated.

    lon_km : float, optional
        The east-west extension of the grid around a source in kilometers.

    lat_km : float, optional
        The south-north extension of the grid around a source in kilometers.

    grid_reso : float, optional
        The resolution of the grid in kilometers.

    wind_product : str, optional
        Name of the wind product ("ERA5" or "SMARTCARB")

    pattern : str, optional
        File pattern with data format to match filename of wind product to date.

    start_date : str, optional
        The first date processed in string format ('%Y-%m-%d').

    end_date : str, optional
        The last date processed in string format ('%Y-%m-%d').

    hour : int, optional
        The hour of the wind product that is used instead of the exact
        measurement time of the remote sensing images.

    AM_options : dict, optional
        Options for the peak fitting algoritm (see code for details).

    trace_gases : list of str, optional
        List of trace gases for which emissions are estimated.

    smooth_data : list of boolean, optional
        List of boolean if data should be smoothed

    remove_background : list of boolean, optional
        List of boolean if background should be removed

    Returns
    -------
    xr.Dataset
        The results dataset with the estimated emissions of each sources as well
        as the divergence and flux maps for visualization.
    """
    # Process start time
    estimation_start = time.process_time()

    # Dates
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    dates = pd.date_range(start_date, end_date)

    if wind_product not in ["ERA5", "SMARTCARB"]:
        raise ValueError(f"Unknown wind product {wind_product}")

    global_attrs = {"method": "divergence method"}
    wind_method = "GNFR-A weighted vertical mean"  # winds.attrs.get("METHOD", None)

    if wind_method is not None:
        global_attrs["wind method"] = wind_method

    results_ds = ddeq.misc.init_results_dataset(
        sources, trace_gases, units="kg s-1", global_attrs=global_attrs
    )

    for source_name, source in sources.groupby("source", squeeze=False):

        # Regular km grid around the source
        center_lon, center_lat, _ = ddeq.sources.get_location(source)
        center_lon, center_lat = float(center_lon), float(center_lat)
        longrid, latgrid, longrid_km, latgrid_km = ddeq.misc.generate_grids(
            center_lon, center_lat, lon_km, lat_km, grid_reso
        )

        # Add grid to results dataset
        if "longrid" not in results_ds:
            shape = results_ds.source.shape + longrid.shape
            dims = results_ds.source.dims + ("latgrid", "longrid")

            results_ds["longrid"] = xr.DataArray(np.full(shape, np.nan), dims=dims)
            results_ds["latgrid"] = xr.DataArray(np.full(shape, np.nan), dims=dims)
            results_ds["longrid_km"] = xr.DataArray(np.full(shape, np.nan), dims=dims)
            results_ds["latgrid_km"] = xr.DataArray(np.full(shape, np.nan), dims=dims)

            for gas in trace_gases:
                results_ds[f"{gas}_grid"] = xr.DataArray(
                    np.full(shape, np.nan), dims=dims, attrs={"units": "molecules m-2"}
                )
                results_ds[f"{gas}_div"] = xr.DataArray(
                    np.full(shape, np.nan), dims=dims, attrs={"units": "g m-2 s-1"}
                )

        source_index = dict(source=source_name)
        results_ds["longrid"].loc[source_index] = longrid
        results_ds["latgrid"].loc[source_index] = latgrid
        results_ds["longrid_km"].loc[source_index] = longrid_km
        results_ds["latgrid_km"].loc[source_index] = latgrid_km

        for i, gas in enumerate(trace_gases):
            print(f"Computing divergence map for source '{source_name}'...")
            start_time = time.process_time()

            # Area limits
            latlims = np.min(latgrid), np.max(latgrid)
            lonlims = np.min(longrid), np.max(longrid)

            # Gridded divergence as xarray datasets
            div_xrs = []

            for date in dates:
                datetime = pd.Timestamp(date) + pd.Timedelta(hours=hour)
                date = date.date()
                wind = ddeq.wind.read_gnfra_wind(
                    wind_folder,
                    datetime,
                    pattern,
                    latlims=latlims,
                    lonlims=lonlims,
                    dataset=wind_product,
                )
                # Gridded divergence for each individual gridded data file
                div_gridded = gridded_divergence(
                    datasets,
                    wind,
                    date,
                    latgrid,
                    longrid,
                    latgrid_km,
                    longrid_km,
                    wind_product=wind_product,
                    gas=gas,
                    varname=varnames[i],
                    smooth_data=smooth_data[i],
                    remove_background=remove_background[i],
                )
                div_xrs.append(div_gridded)
            # Concatenate gridded divergence together
            div_xr = xr.concat(div_xrs, "n_images")

            # Average divergence maps over all timestamps
            div_xr = div_xr.mean(dim="n_images", skipna=True)

            # Add divergence map and gas enhancement
            results_ds[f"{gas}_grid"].loc[source_index] = div_xr[f"{gas}_grid"]
            results_ds[f"{gas}_div"].loc[source_index] = div_xr[f"{gas}_div"]

            end_time = time.process_time()
            print(f"...done in {end_time-start_time} seconds")

            print(f"Optimizing trace gas {gas} emissions for source '{source_name}'...")
            start_time = time.process_time()
            fitting_xr = peak_fitting(div_xr, species=gas, AM_options=AM_options)
            end_time = time.process_time()
            print(f"...done in {end_time-start_time} seconds")

            # Emission estimation and standard deviation in kg/s
            emis_est = fitting_xr["opt"].data[0] / 1000
            emis_std = np.sqrt(fitting_xr["cov"].data[0, 0]) / 1000

            # Write results to xarray dataset
            results_ds[f"{gas}_emissions"].loc[dict(source=source_name)] = emis_est
            results_ds[f"{gas}_emissions_precision"].loc[dict(source=source_name)] = (
                emis_std
            )

    estimation_end = time.process_time()
    print(f"Estimations done in {estimation_end-estimation_start} seconds")

    return results_ds


def peak_fitting(div_xr, species="CO2", pixels=4, AM_options=None):

    latgrid_km, longrid_km = div_xr["latgrid_km"].data, div_xr["longrid_km"].data

    # Create pixels x pixels sized kilometer grid around the source
    row_slice = slice(
        (len(latgrid_km) - 1) // 2 - pixels, (len(latgrid_km) + 1) // 2 + pixels, 1
    )
    col_slice = slice(
        (len(longrid_km) - 1) // 2 - pixels, (len(longrid_km) + 1) // 2 + pixels, 1
    )

    # Corresponding 2d X and Y kilometer grids around the source
    Y, X = np.meshgrid(latgrid_km[row_slice], longrid_km[col_slice], indexing="ij")

    # Intial values
    if species == "NO2":
        init = [900, 5, 6, 0.0, 0.0, 0.0, -0.5]
        bounds = np.array(
            [(0, 2000), (1, 9), (1, 9), (-10, 10), (-10, 10), (-1, 1), (-1, 1)]
        )
        scales = [1e3, 1e0, 1e0, 1e0, 1e0, 1e0, 1e-1]

    elif species == "CO2":
        init = [9e5, 7, 7, 0.0, 0.0, 0.0, -500]
        bounds = np.array(
            [(0, 2e6), (1, 9), (1, 9), (-10, 10), (-10, 10), (-1, 1), (-1000, 1000)]
        )
        scales = [1e5, 1e0, 1e0, 1e0, 1e0, 1e0, 1e2]

    else:  # TODO: have good init for other gases
        init = [900, 5, 6, 0.0, 0.0, 0.0, -0.5]
        bounds = np.array(
            [(0, 2000), (1, 9), (1, 9), (-10, 10), (-10, 10), (-1, 1), (-1, 1)]
        )
        scales = [1e3, 1e0, 1e0, 1e0, 1e0, 1e0, 1e-1]

    # Divergence near the source
    div_map = div_xr[f"{species}_div"].data[row_slice, col_slice]

    # Residual vector or component-wise difference between the model and the data
    residual = lambda params: model_residual(params, (X, Y), div_map)

    # Least square optimization using scipy with default Trust Region Reflective algorithm
    optimized = scipy.optimize.least_squares(
        residual, init, x_scale=scales, bounds=bounds.T, method="trf"
    )
    opt = optimized.x
    J = optimized.jac
    cov = np.linalg.inv(J.T @ J)

    # Optimization using adaptive metropolis algorithm if AM_options are given
    if AM_options is not None:
        warmup, samples = AM_options["warmup"], AM_options["samples"]
        sampling = ddeq.mcmc_tools.AM_MC(
            residual,
            opt,
            samples,
            warmup,
            C0=cov,
            bounds=bounds,
            init_fit=False,
            progress=False,
        )
        opt, cov = sampling["MAP"].data, sampling["cov"].data

    names = ["peak_integral", "sigma_x", "sigma_y", "x0", "y0", "corr", "background"]
    ds = xr.Dataset(
        {
            "opt": xr.DataArray(opt, dims=["params"], coords=dict(params=names)),
            "cov": xr.DataArray(
                cov, dims=["params", "params"], coords=dict(params=names)
            ),
            "bg": opt[-1],
        }
    )
    return ds


# Currently not used
def compute_divergence_map(flux_xr, species="CO2"):
    """
    Computes divergence from fluxes averaged over timestamps.

    Parameters
    ----------
    flux_xr : xarray dataset
        Precomputed species fluxes.
    species : str, optional
        Chosen species, either 'CO2' or 'NO2'. The default is 'CO2'.

    Returns
    -------
    xarray-dataset
        Computed divergence for the chosen species.
    """
    Fx = flux_xr[f"{species}_Fx"].mean(dim="n_images", skipna=True).data
    Fy = flux_xr[f"{species}_Fy"].mean(dim="n_images", skipna=True).data
    longrid_km = flux_xr["longrid_km"][dict(n_images=0)]
    latgrid_km = flux_xr["latgrid_km"][dict(n_images=0)]

    if species == "CO2":
        # Divergence of CO2 in g/m²/s or Mg/km²/s
        div = (
            44.01
            / 6.0221409e23
            * divergence([Fx, Fy], [longrid_km.data * 1e3, latgrid_km.data * 1e3])
        )

    elif species == "NO2":
        # NOx fluxes from NO2 fluxes with correction coeffcient, normally above 1.0
        coef = 0.9571
        Fx, Fy = coef * Fx, coef * Fy

        # Divergence of NO2 in g/m²/s or Mg/km²/s
        div = (
            46.0055
            / 6.0221409e23
            * divergence([Fx, Fy], [longrid_km.data * 1e3, latgrid_km.data * 1e3])
        )

        # NO2 Sinks in g/m²/s assuming 4h lifetime
        # sinks = 46.0055/6.0221409e23*0.9571*species_gridded/(4*3600)
        # sinks = sinks*1e6
        # Corresponding NO2 emissions
        # emissions = div+sinks

    # Conversion from Mg/km²/s to g/km²/s
    div = 1e6 * div

    # Return as xarray dataset
    div_xr = xr.DataArray(
        div,
        dims=["latgrid", "longrid"],
        attrs={"long name": f"Gridded {species} divergence", "units": "g m-2 s-1"},
    )

    data_vars = {
        "longitude": flux_xr["longrid"][dict(n_images=0)],
        "latitude": flux_xr["latgrid"][dict(n_images=0)],
        "longrid_km": longrid_km,
        "latgrid_km": latgrid_km,
        f"{species}_div": div_xr,
        f"{species}_grid": flux_xr[f"{species}_grid"].mean(dim="n_images", skipna=True),
    }

    attrs = {"Description": f"Gridded {species} divergence"}

    return xr.Dataset(data_vars=data_vars, attrs=attrs)
