import os

import cartopy.crs as ccrs
import geopandas as gpd
import numpy as np
import skimage
import ucat
import pandas as pd
import xarray as xr

CASES = [
    ["DWD", "Belchatow"],
    ["DWD", "Jaenschwalde"],
    ["Empa", "Belchatow"],
    ["Empa", "Berlin"],
    ["Empa", "Jaenschwalde"],
    ["Empa", "Lipetsk"],
    ["Empa", "Matimba"],
    ["Empa", "Paris"],
    ["LSCE", "Paris"],
    ["TNO", "Belchatow"],
    ["TNO", "Belchatow", "wNO"],
    ["TNO", "Berlin"],
    ["TNO", "Jaenschwalde"],
    ["TNO", "Jaenschwalde", "wNO"],
    ["TNO", "Randstad_S"],
    ["TNO", "Randstad_W"],
    ["WUR", "Belchatow"],
    ["WUR", "Belchatow", "wNO"],
    ["WUR", "Jaenschwalde"],
    ["WUR", "Jaenschwalde", "wNO"],
    ["WUR", "Lipetsk"],
    ["WUR", "Lipetsk", "wNO"],
    ["WUR", "Matimba"],
    ["WUR", "Matimba", "wNO"],
]


def get_filename(team, region, suffix="", data_path="."):
    """
    Return filename to CoCO2 library of plume file.

    Parameters
    ----------
    team : str
        "DWD", "Empa", "LSCE", "TNO" or "WUR"

    region : str
        e.g., "Belchatow", "Janschwalde", "Lipetsk", "Matimba"

    suffix : str, optional
        Set to "wNO" to include files with NO fields (only MicroHH output).

    Returns
    -------
    str
    """
    if suffix:
        filename = f"{team}_{region}_{suffix}.nc"
    else:
        filename = f"{team}_{region}.nc"

    return os.path.join(data_path, filename)


def read_level2(
    filename,
    data_path=".",
    co2_noise=0.7,
    no2_noise=33e-6,
    mask_out_of_domain=False,
    drop_duplicates=True,
):
    """\
    Read CO2M-like Level-2 from CoCO2 library of plumes [Koene2022]_.

    Parameters
    ----------
    filename : str
        {team}_{region}_{suffix}.nc

    data_path : str, optional
        Data path to `filename`.

    co2_noise : float, optional
        Random noise added to CO2 fields (default: 0.7 ppm)

    no2_noise : float, optional
        Random noise added to NO2 fields (default: 33 µmol m-2 = 2e15 cm-2)

    mask_out_of_domain : boolean, optional
        For MicroHH simulations, remove CO2/NO2 values from CAMS outside MicroHH
        model domain.

    drop_duplicates : boolean, optional
        If True, drop duplicated times.

    Returns
    -------
    xr.Dataset

    Notes
    -----
    .. [Koene2022] Erik Koene, & Dominik Brunner. (2022). CoCO2 WP4.1 Library of
       Plumes (1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.7448144

    """
    # read data
    d = xr.open_dataset(filename)
    d = d.rename_vars(
        {"lon_bnds": "lonc", "lat_bnds": "latc", "surface_pressure": "psurf"}
    )
    d = d.rename_dims({"x": "nobs", "y": "nrows"})

    if region in ["Berlin", "Paris"]:
        name = "CITY"
    elif region in ["Randstad_S", "Randstad_W"]:
        name = "RS"
    else:
        name = "PP_M"

    shape = d[f"XCO2_{name}"].shape
    d["CO2"] = (
        d[f"XCO2_{name}"]
        + d.get("XCO2_ANTH", 0.0)
        + d.get("XCO2_BIO", 0.0)
        + d.get("XCO2_BG", 0.0)
        + co2_noise * np.random.randn(*shape)
    )

    d["CO2_signal"] = d[f"XCO2_{name}"].copy()
    d["CO2_std"] = xr.full_like(d["CO2"], co2_noise)
    d["CO2"].attrs["units"] = "ppm"
    d["CO2"].attrs["noise_level"] = co2_noise

    if f"NO2_{name}" in d and f"NO_{name}" in d:
        d["NOx"] = (
            d[f"NO_{name}"]
            + d[f"NO2_{name}"]
            + d["NO_BG"]
            + d["NO2_BG"]
            + d.get("NO_ANTH", 0.0)
            + d.get("NO2_ANTH", 0.0)
            + d.get("NO_BIO", 0.0)
            + d.get("NO2_BIO", 0.0)
            + no2_noise * np.random.randn(*shape)
        )
        d["NOx_signal"] = d[f"NO_{name}"] + d[f"NO2_{name}"]
        d["NOx_std"] = xr.full_like(d["NOx"], no2_noise)

        d["NOx"].attrs["units"] = "mol m-2"
        d["NOx"].attrs["noise_level"] = no2_noise

    if f"NO2_{name}" in d:
        d["NO2"] = (
            d[f"NO2_{name}"]
            + d["NO2_BG"]
            + d.get("NO2_ANTH", 0.0)
            + d.get("NO2_BIO", 0.0)
            + no2_noise * np.random.randn(*shape)
        )
        d["NO2_signal"] = d[f"NO2_{name}"].copy()
        d["NO2_std"] = xr.full_like(d["NO2"], no2_noise)

        d["NO2"].attrs["units"] = "mol m-2"
        d["NO2"].attrs["noise_level"] = no2_noise

    d["clouds"] = xr.zeros_like(d["CO2"])

    # remove non-continous fields on boundary (only WUR MicroHH)
    if mask_out_of_domain:
        mask = np.any(np.isnan(d["CO2"].values), axis=0)
        mask = skimage.morphology.dilation(mask, skimage.morphology.square(10))

        for name in ["CO2", "NOx", "NO2"]:
            if name in d:
                d[name].values[:, mask] = np.nan
                d[name + "_signal"].values[:, mask] = np.nan
                d[name + "_std"].values[:, mask] = np.nan

    if drop_duplicates:
        d = d.drop_duplicates("time")

    return d


def read_ps_catalogue(filename=None):
    """\
    Read CoCO2 point source catalogue [Guevara2023]_ in the format supported by
    ddeq.

    Parameters
    ----------
    filename : str, default: None
        Name of CSV file with point source information from CoCO2 database
        (see "coco2_ps_catalogue_v1.1.csv" in ddeq.DATA_PATH for an example).

    Returns
    -------
    xr.Dataset
        xarray dataset containing point source locations

    Notes
    -----
    .. [Guevara2023] Guevara, M., Enciso, S., Tena, C., Jorba, O., Dellaert, S.,
           Denier van der Gon, H., and Pérez García-Pando, C.: A global
           catalogue of CO2 emissions and co-emitted species from power plants
           at a very high spatial and temporal resolution, Earth Syst. Sci. Data
           Discuss. [preprint], https://doi.org/10.5194/essd-2023-95, in review,
           2023.
    """
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__),
            "data",
            "coco2_ps_database",
            "coco2_ps_catalogue_v1.1.csv",
        )

    sources = pd.read_csv(filename, index_col=0)
    sources = xr.Dataset(sources)
    sources = sources.rename_dims({"ID": "source"})
    sources = sources.rename_vars(
        {"ID": "source", "longitude": "lon", "latitude": "lat"}
    )
    sources["label"] = xr.DataArray(sources["source"], dims="source")
    sources["diameter"] = xr.DataArray(np.full(sources.source.shape, 1000.0),
                                       attrs={"units": "m"},
                                       dims="source")

    sources.attrs["ORIGIN"] = "CoCO2 Point Source Database (Guevara et al. 2023)"
    sources.attrs["DOI"] = "https://doi.org/10.24380/mxjo-nram"

    return sources


def read_ps_catalogue_v2():
    s = gpd.read_file("/output/CORSO/coco2_ps_catalogue_v2.0_merged.gpkg")

    sources = xr.Dataset(coords={"source": xr.DataArray(s["source"], dims=("source"))})

    for col in s.columns:
        if col not in sources:
            sources[col] = xr.DataArray(s[col].values, dims="source")

    sources = sources.rename_vars({"longitude": "lon", "latitude": "lat"})
    sources["diameter"] = xr.DataArray(np.full(sources.source.shape, 1000.0),
                                       attrs={"units": "m"},
                                       dims="source")

    del sources["geometry"]

    return sources


def merge_sources(sources, names, new_name=None):
    """
    Merge to (neighboring) sources in CoCO2 point source database.

    Example
    =======
    >>> sources = ddeq.coco2.read_ps_catalogue_v2()
    >>> sources = merge_sources(sources, ['Matimba', 'Medupi'])
    """
    try:
        merged = sources.sel(source=names[0]).copy()
    except KeyError:
        print(names, 'not in sources.')
        return sources

    if new_name is None:
        merged['source'] = ' & '.join(names)
        merged['label'] = ' & '.join(names)
    else:
        merged['source'] = new_name
        merged['label'] = new_name

    # Average loation
    for var_name in ['lon', 'lat']:
        merged[var_name] = np.mean([sources.sel(source=name)[var_name]
                                    for name in names])

    # Sum emissions and diameter
    # TODO: diameter should be the distance between sources
    for var_name in ['co2_emis_ty', 'nox_emis_ty', 'sox_emis_ty', 'co_emis_ty', 'ch4_emis_ty', 'diameter']:
        merged[var_name] = np.sum([sources.sel(source=name)[var_name]
                                   for name in names])

    # Concatenate strings
    for var_name in ['ID', 'ISO3', 'fuel', 'ID_MonthFact', 'ID_WeekFact', 'ID_HourFact', 'ID_VertProf']:
        merged[var_name] = ', '.join(sorted(set(str(sources.sel(source=name)[var_name].values)
                                                for name in names)))

    # Add merged sources and remove orginally sources.
    return xr.concat(
        [sources.sel(source=[name for name in sources.source.values
                             if name not in names]), merged],
        dim='source'
    )

