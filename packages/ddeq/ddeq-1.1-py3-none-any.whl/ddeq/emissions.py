import numpy as np
import pandas as pd
import xarray as xr
import ucat
import ddeq
from typing import Union, Tuple, List
from pathlib import Path


def compute_plume_signal(data, trace_gas):
    """
    Compute plume signal for trace gas
    """
    name = f"{trace_gas}_minus_estimated_background"
    signal = data[trace_gas] - data[f"{trace_gas}_estimated_background"]

    data[name] = xr.DataArray(
        signal, dims=data[trace_gas].dims, attrs=data[trace_gas].attrs
    )
    return data


def convert_units(data, gas, variable):

    values = data[variable]
    attrs = values.attrs

    name = f"{variable}_mass"

    if data[gas].attrs["units"] == "molecules cm-2":
        input_unit = "cm-2"
    elif data[gas].attrs["units"] == "ppm":
        input_unit = "ppmv"
    else:
        input_unit = str(data[gas].attrs["units"])

    if gas == "NOx":
        molar_mass = "NO2"
    else:
        molar_mass = str(gas)

    psurf = data["psurf"] if "psurf" in data else data["surface_pressure"]
    data[name] = xr.DataArray(
            ucat.convert_columns(
                values, input_unit, 'kg m-2', p_surface=psurf,
                molar_mass=molar_mass
            ),
            dims=values.dims,
            attrs=values.attrs,
    )

    if "noise_level" in attrs:
        noise_level = attrs["noise_level"]

        # noise scenarios from SMARTCARB project
        if isinstance(noise_level, str):
            if gas == "CO2":
                noise_level = {"low": 0.5, "medium": 0.7, "high": 1.0}[noise_level]

            elif gas in ["NO2", "NOx"]:
                noise_level = {"low": 1.0e15, "high": 2e15, "S5": 1.3e15}[
                    noise_level
                ]
            else:
                raise ValueError

        attrs["noise_level"] = ucat.convert_columns(
            noise_level,
            input_unit,
            "kg m-2",
            molar_mass=molar_mass,
            p_surface=np.nanmean(psurf),
        )

    data[name].attrs.update(attrs)
    data[name].attrs["units"] = "kg m-2"


def prepare_data(data, gas="CO2"):
    """
    The functions prepares `data` for emission quantification with includes
    estimating the background field, computing the local enhancement above the
    background (plume signal) and converting units to mass column densities
    (in kg m-2).

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing dataset with trace gas variable.

    gas : str, optional
        Name of trace gas in in data.

    Returns
    -------
    xr.Dataset
        The dataset `data` with added background fields and variables with gas
        fields in mass column densities denoted with the "_mass" suffix.
    """
    raise NotImplementedError

    data[f"{gas}_isfinite"] = np.isfinite(data[gas])

    # estimate background
    data = ddeq.background.estimate(data, gas)

    # compute CO2/NO2 enhancement
    data = compute_plume_signal(data, gas)

    # convert ppm to kg/m2
    for variable in [
        gas,
        f"{gas}_estimated_background",
        f"{gas}_minus_estimated_background",
    ]:
        convert_units(data, gas, variable)

    return data


def convert_NO2_to_NOx_emissions(results, f=1.32):
    """
    Convert NO2 fluxes/emissions (i.e. units: "kg s-1") to NOx fluxes/emissions
    using the NO2 to NOx conversion factor assuming that a fraction of NOx is in
    is nitrogen monoxide.

    Parameters
    ----------
    results : xr.Dataset
        Results dataset with estimated emissions.

    f : float, optional
        The scaling factor using a default value of 1.32.

    Returns
    -------
    xr.Dataset
        The results dataset with added variables for NOx emissions.
    """
    for key in results:
        if key.startswith("NO2") and results[key].attrs.get("units") == "kg s-1":
            new_key = key.replace("NO2", "NOx")
            results[new_key] = f * xr.DataArray(results[key], dims=results[key].dims)
            results[new_key].attrs.update(results[key].attrs)
        if key.startswith('NO2') and results[key].attrs.get('units') == 's':
            new_key = key.replace('NO2', 'NOx')
            results = results.rename({key: new_key})
    return results


def prepare_bottom_up_emissions(
    data: xr.Dataset, gases: Union[str, list], name_pattern: str, to_unit: str = "kg/s"
) -> xr.Dataset:
    """Prepare bottom-up reported emissions to be digestible by ddeq.

    Args:
        data (xr.Dataset):
            Dataset containing the bottom-up reported emissions.
        gases (Union[str, list]):
            Name of gas(es) contained in the bottom-up reported emissions.
        name_pattern (str):
            Naming pattern of the bottom-up reported emissions.
            Should contain a placeholder 'gas', e.g '{gas}_reported_emissions'
        to_unit (str, optional):
            Unit to which the bottom-up reported emissions should be converted to.
            Defaults to "kt/a".

    Returns:
        xr.Dataset: Dataset containing the formatted bottom-up reported emissions.
    """
    if isinstance(gases, str):
        gases = [gases]

    for gas in gases:
        var_name = name_pattern.format(gas=gas)
        new_var_name = f"{gas}_bottom_up_emissions"

        # convert units
        from_unit = data[var_name].attrs.get("units", None)
        data[new_var_name] = ucat.convert_mass_per_time_unit(
            data[var_name], from_unit, to_unit
        )

    return data


def ts_csv_to_xarray(
    data: Union[str, Path, pd.DataFrame],
    date_name: str = "Date",
) -> xr.Dataset:
    if isinstance(data, (str, Path)):
        df = pd.read_csv(data, parse_dates=[date_name])
    elif isinstance(data, pd.DataFrame):
        df = data.reset_index()
    else:
        raise ValueError("Data must be a string, pathlib.Path or pd.DataFrame.")

    # Set the 'Date' column as the index
    df.set_index(date_name, inplace=True)

    # rename date_name to "time"
    df.rename_axis("time", inplace=True)

    # Convert the DataFrame to an xarray Dataset
    data = xr.Dataset.from_dataframe(df)

    return data


def bottom_up_reported_like(
    gases: Union[str, List[str]],
    emissions: Union[int, float, List[Union[int, float]]],
    unit: Union[str, List[str]],
    data: xr.Dataset,
) -> xr.Dataset:

    if "time" not in data.dims:
        raise ValueError("Input data must contain the dimension 'time'.")

    # Ensure gases, emissions, and unit are lists
    if isinstance(gases, str):
        gases = [gases]
        emissions = [emissions]
        unit = [unit]
    elif not (
        isinstance(gases, list)
        and isinstance(emissions, list)
        and isinstance(unit, list)
    ):
        raise TypeError(
            "gases, emissions, and unit must all be lists if any of them are lists."
        )
    elif not (len(gases) == len(emissions) == len(unit)):
        raise ValueError("gases, emissions, and unit lists must have the same length.")

    # Create a new xarray Dataset with the same dimensions as the input data
    bottom_up_reported = xr.Dataset(coords={"time": data["time"]})

    for gas, emission, u in zip(gases, emissions, unit):
        variable_name = f"{gas}_bottom_up_emissions"
        bottom_up_reported[variable_name] = (
            "time",
            np.repeat(emission, data.time.size),
        )
        bottom_up_reported[variable_name].attrs["units"] = u

    bottom_up_reported = prepare_bottom_up_emissions(
        bottom_up_reported, gases, name_pattern="{gas}_bottom_up_emissions"
    )

    return bottom_up_reported


def get_power_generation_data(
    client,
    power_plant_name: str,
    country_code: str,
    psr_type: str,
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    # from entsoe import EntsoePandasClient
    # client: EntsoePandasClient(api_key=api_key)
    # Get the data via API from https://transparency.entsoe.eu/generation/r2/actualGenerationPerGenerationUnit/show
    # The API documentation is available at https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html
    # For larger datasets, e.g., annual data, the retrieval migth fail some times. Splitting the required time span or re-running the code often solves the problem.
    # e.g power_plant_name = 'Jänschwalde' | 'Bełchatów'
    # e.g country_code = 'DE_50HZ' | 'PL'
    # e.g psr_type='B02' | 'B02' (is Fossil Brown coal/Lignite)

    monthly_data = []

    for year in range(start_year, end_year + 1):
        # data has to be queried monthly to prevent the api from crashing
        for month in range(1, 13):
            print(f"Querying year {year}, month {month}")

            start = pd.Timestamp(year=year, month=month, day=1, hour=0, tz="UTC")
            end = pd.Timestamp(
                year=year, month=month, day=1, hour=0, tz="UTC"
            ) + pd.DateOffset(months=1)

            data_country = client.query_generation_per_plant(
                country_code, start=start, end=end, psr_type=psr_type
            )  # B02 is Fossil Brown coal/Lignite
            data_pp = data_country.filter(like=power_plant_name)
            data_pp.columns = data_pp.columns.map(lambda x: x[0].split(",")[0].strip())
            data_pp.index = data_pp.index.tz_convert("UTC")
            data_pp.index = data_pp.index.strftime("%Y-%m-%d %H:%M:%S")

            monthly_data.append(data_pp)

    # Concatenate the monthly DataFrames into a single DataFrame
    full_data = pd.concat(monthly_data)

    # Combine data of different generators
    full_data["total_energy"] = full_data.sum(axis=1)

    return full_data


def interpolate_emission_data(
    emission_data: pd.DataFrame,
    power_generation_data: pd.DataFrame,
    gases: Union[str, list],
    name_pattern: str,
) -> pd.DataFrame:

    # Ensure gases is a list for consistent iteration
    if isinstance(gases, str):
        gases = [gases]

    # Ensure emission_data and power_generation_data have datetime indices
    emission_data.index = pd.to_datetime(emission_data.index)
    power_generation_data.index = pd.to_datetime(power_generation_data.index)

    # Resample emission data to the frequency of power generation data
    emission_data_resampled = emission_data.reindex(
        power_generation_data.index, method="ffill"
    )

    # Keep only the overlapping periods in power_generation_data
    valid_periods = emission_data_resampled.index.intersection(
        power_generation_data.index
    )
    power_generation_data = power_generation_data.loc[valid_periods]

    # Function to calculate weights by period
    def calculate_weights(data, freq):
        if freq == "Y":
            grouped = data.groupby(data.index.year)
        if freq == "M":
            grouped = data.groupby([data.index.year, data.index.month])
        if freq == "D":
            grouped = data.groupby([data.index.year, data.index.month, data.index.day])
        else:
            raise NotImplementedError

        weights = grouped.transform(lambda x: x / x.mean())
        return weights

    # Determine the frequency of the emission data
    if emission_data.index.to_series().diff().dropna().dt.days.isin([365, 366]).all():
        freq = "Y"
    elif (
        emission_data.index.to_series()
        .diff()
        .dropna()
        .dt.days.isin([28, 29, 30, 31])
        .all()
    ):
        freq = "M"
    elif (
        emission_data.index.to_series().diff().dropna().dt.total_seconds() / 3600 == 1
    ).all():
        freq = "D"
    else:
        raise ValueError

    # Calculate weights based on power generation by determined frequency
    weights = calculate_weights(power_generation_data["total_energy"], freq)

    # Apply weights and calculate interpolated emissions
    for gas in gases:
        gas_column = name_pattern.format(gas=gas)
        interpolated_emissions = emission_data_resampled[gas_column] * weights
        power_generation_data[f"{gas}_bottom_up_emissions"] = interpolated_emissions

    # Convert pd.DataFrame to xr.Dataset
    name_pattern = "{gas}_bottom_up_emissions"
    interpolated_emissions_dataset = ts_csv_to_xarray(
        data=power_generation_data, date_name="Date"
    )
    interpolated_emissions_dataset = _assign_units(
        interpolated_emissions_dataset, gases=gases, name_pattern=name_pattern
    )
    interpolated_emissions_dataset = prepare_bottom_up_emissions(
        interpolated_emissions_dataset, gases=gases, name_pattern=name_pattern
    )

    return interpolated_emissions_dataset


def _assign_units(data, gases: Union[str, list], name_pattern: str):

    if isinstance(gases, str):
        gases = [gases]

    for gas in gases:
        data[name_pattern.format(gas=gas)].attrs["units"] = "t/a"

    data["total_energy"].attrs["units"] = "MWh"
    data["time"].attrs["long_name"] = "Time UTC"

    return data
