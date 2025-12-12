import collections
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
import ucat
import xarray as xr

import ddeq

from typing import Union, Tuple


def get_location(sources: xr.Dataset, name: str = None) -> Tuple[float, float, float]:
    """
    Get longitude, latitude and diameter of source or sources.
    """
    if name is not None:
        sources = sources.sel(source=name)
    return sources["lon"], sources["lat"], sources["diameter"]


def get_true_emissions(sources, name, gases):
    true_emissions = []
    for gas in gases:
        varname = f"true_{'NOx' if gas == 'NO2' else gas}_emissions"
        if varname in sources:
            true_emissions.append(sources[varname].sel(source=name))
        else:
            true_emissions.append(np.nan)

    if np.all(np.isnan(true_emissions)):
        return None
    return true_emissions


def buffer_point(point, distance):
    """
    Make buffer around point (lon-lat coords) with distance (in meters).
    """
    distance = float(distance)

    lat_distance_deg = distance / 111320.0
    lon_distance_deg = distance / (111320.0 * np.cos(np.deg2rad(point.y)))

    # create a circular buffer in degrees (assuming the distance is the same in both directions)
    buffer = point.buffer(lat_distance_deg)

    # scale the buffer to account for the different distances per degree in longitude and latitude
    buffer = shapely.affinity.scale(
        buffer, xfact=lon_distance_deg / lat_distance_deg, yfact=1
    )

    return buffer


def merge_all(sources, source_name):
    """\
    Merge all given sources under new name.
    """
    merged = xr.Dataset()
    merged["source"] = xr.DataArray([source_name], dims="source")
    merged["label"] = xr.DataArray([source_name], dims="source")

    merged["org_source"] = xr.DataArray(
        [", ".join(str(v) for v in sources.source.values)],
        dims="source"
    )

    for name in ["lon", "lat"]:
        merged[name] = xr.DataArray([sources[name].mean()], dims="source")
        merged[name].attrs.update(sources[name].attrs)

    for name in ["diameter"] + [key for key in sources.keys() if key.endswith("_emissions")]:
        merged[name] = xr.DataArray([sources[name].sum()], dims="source")
        merged[name].attrs.update(sources[name].attrs)

    return merged


def merge_sources(ps, distance=10e3):
    """
    Merge sources within distance.
    """

    # Create buffer around each source
    buffers = [buffer_point(point, 0.5 * distance) for point in ps.geometry]
    ps_buffer = ps.set_geometry(buffers)

    # Create new DataFrame combining intersecting buffers
    merged = gpd.GeoDataFrame(geometry=list(ps_buffer.unary_union.geoms))

    # Check overlapping sources for each merged polygon and get IDs
    overlaps = []

    for poly in merged.geometry:
        indices = ps[ps.geometry.intersects(poly)].index.tolist()
        overlaps.append(indices)

    merged["original_indices"] = overlaps

    # concat attrs for merged indices
    columns = collections.defaultdict(list)
    centroids = []

    for i, row in merged.iterrows():
        org = ps.loc[row["original_indices"]]

        centroids.append(org["geometry"].unary_union.centroid)

        for name in ["ISO3", "plant_name", "sector"]:
            columns[name].append(", ".join(sorted(set(org[name]))))

        for name in ["co2_kty", "ch4_kty", "nox_kty", "sox_kty", "co_kty"]:
            columns[name].append(sum(org[name]))

    # add merged attrs
    for name in columns:
        merged[name] = columns[name]

    merged = merged.set_geometry(centroids)

    return merged


def read_smartcarb(filename=None, time=None):
    """\
    Read list of cities and power plants inside the SMARTCARB model domain.
    The emissions provided with the dataset are annual mean emissions used
    in the COSMO simulations to generate the synthetic CO2M observations.
    Note that emissions in the simulations vary temporally. The time-varying
    emissions can be read using `ddeq.smartcarb.read_true_emissions`.

    Parameters
    ----------
    filename : str, default: None
        Name of CSV file with point source information
        (see "sources-smartcarb.csv" in `ddeq.DATA_PATH`).

    time : pd.Timestamp, default: None
        If provided, true CO2 and NOx emissions in the dataset are added
        at given time.

    Returns
    -------
    xr.Dataset
        xarray dataset containing point source locations
    """
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), "data", "sources-smartcarb.csv"
        )

    sources = pd.read_csv(filename, index_col=0, skiprows=1).to_xarray()

    sources = sources.rename_vars(
        longitude="lon",
        latitude="lat",
        annual_co2_emissions_in_MtCO2="CO2_emissions",
        annual_nox_emissions_in_ktNO2="NOx_emissions",
        annual_co2_emissions_in_MtCO2_std="CO2_emissions_precision",
        annual_nox_emissions_in_ktNO2_std="NOx_emissions_precision",
    )

    # Emissions to kg/s
    sources["CO2_emissions"] = ucat.convert_mass_per_time_unit(
        sources["CO2_emissions"], "Mt/a", "kg/s"
    )
    sources["CO2_emissions"].attrs.update(
        {"long_name": "annual CO2 emissions", "units": "kg/s"}
    )
    sources["NOx_emissions"] = ucat.convert_mass_per_time_unit(
        sources["NOx_emissions"], "kt/a", "kg/s"
    )
    sources["NOx_emissions"].attrs.update(
        {"long_name": "annual NOx emissions", "units": "kg/s"}
    )
    sources["CO2_emissions_precision"] = ucat.convert_mass_per_time_unit(
        sources["CO2_emissions_precision"], "Mt/a", "kg/s"
    )
    sources["CO2_emissions_precision"].attrs.update(
        {"long_name": "temporal variability of CO2 emissions", "units": "kg/s"}
    )
    sources["NOx_emissions_precision"] = ucat.convert_mass_per_time_unit(
        sources["NOx_emissions_precision"], "kt/a", "kg/s"
    )
    sources["NOx_emissions_precision"].attrs.update(
        {"long_name": "temporal variability of NOx emissions", "units": "kg/s"}
    )
    sources.attrs["description"] = (
        "Cities and power plants inside the SMARTCARB model domain."
    )

    # Add true emissions at given time.
    if time is not None:
        time = pd.Timestamp(time.values)
        for gas in ["CO2", "NOx"]:
            true_emissions = [
                ddeq.smartcarb.read_true_emissions(gas, name, time=time)
                for name, source in sources.groupby("source", squeeze=False)
            ]
            attrs = {
                "long_name": f"true {gas} emissions",
                "units": "kg/s",
                "time": str(time),
            }
            sources[f"true_{gas}_emissions"] = xr.DataArray(
                true_emissions, attrs=attrs, dims="source"
            )

    return sources


def read_corso_ps_database(filename=None, merge=False, distance=10e3):
    if filename is None:
        filename = "/output/CORSO/CORSO_PS_Catalogue/Corso_emis_allv0.4.csv"

    sources = pd.read_csv(
        filename,
        index_col=0,
        usecols=np.arange(12),
        sep=";",
        keep_default_na=False
    )

    sources = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(sources.longitude, sources.latitude, crs="EPSG:4326"),
        data=sources
    )

    if merge:
        sources = merge_sources(sources, distance=distance)

        # FIXME: this should not be necessary
        sources.index.name = "ID"
        sources["longitude"] = sources.geometry.x
        sources["latitude"] = sources.geometry.y

    sources = sources.to_xarray()
    sources = sources.rename_dims(ID="source").rename_vars(
        ID="source",
        ISO3="country_code",
        plant_name="label",
        longitude="lon",
        latitude="lat",
        co2_kty="CO2_emissions",
        ch4_kty="CH4_emissions",
        nox_kty="NOx_emissions",
        sox_kty="SOx_emissions",
        co_kty="CO_emissions",
    )


    sources["diameter"] = xr.DataArray(np.full(sources.source.shape, 1000.0),
                                       dims="source")
    sources["diameter"].attrs["long_name"] = "diameter of source"
    sources["diameter"].attrs["units"] ="m"

    for gas in ["CO2", "CH4", "NOx", "SOx", "CO"]:
        sources[f"{gas}_emissions"] = ucat.convert_mass_per_time_unit(sources[f"{gas}_emissions"], "kt/a", "kg/s")
        sources[f"{gas}_emissions"].attrs["long_name"] = f"Annual {gas} emissions"
        sources[f"{gas}_emissions"].attrs["units"] = "kg/s"

    return sources
