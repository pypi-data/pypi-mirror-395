from datetime import timedelta
import glob
import os

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import pandas
import ucat
import xarray as xr

import ddeq

# SMARTCARB model domain
DOMAIN = ddeq.misc.Domain.from_nml(
    os.path.join(os.path.dirname(ddeq.__file__), "data", "INPUT_ORG")
)

ATTRIBUTES = dict(
    DESCRIPTION="Synthetic XCO2 and NO2 satellite image with auxiliary data"
    " for estimating CO2/NOx emissions of cities and point"
    " sources",
    DATAORIGIN="SMARTCARB study",
    DOI="10.5281/zenodo.4048227",
    CREATOR="Gerrit Kuhlmann et al.",
    EMAIL="gerrit.kuhlmann@empa.ch",
    AFFILIATION="Empa Duebendorf, Switzerland",
)


class Level2Dataset:
    def __init__(
        self,
        data_path,
        constellation="ace",
        co2_noise_scenario="medium",
        co2_cloud_threshold=0.01,
        co2_scaling=1.0,
        no2_noise_scenario="high",
        no2_cloud_threshold=0.30,
        no2_scaling=1.0,
        co_noise_scenario=None,
        co_cloud_threshold=0.05,
        co_scaling=1.0,
        make_no2_error_cloud_dependent=True,
    ):
        """\
        A container class to provide access to SMARTCARB Level-2 data for given
        constellation and uncertainty scenario.

        Parameters
        ----------
        data_path : str
            Path tof SMARTCARB Level-2 files

        constellation : str, optional
            Code used for CO2M constellation.

        co2_noise_scenario : str, optional
            Noise scenario used to add random uncertainty to the CO2 observations
            for vegetation albedo and solar zenith angle of 50° (VEG50 scenario):
            "low" -> 0.5 ppm, "medium" -> 0.7 ppm and "high" -> 1.0 ppm.

        co2_cloud_threshold : float, optional
            Cloud fraction used for masking bad pixels with 1% default cloud
            fraction.

        co2_cloud_threshold : float, optional
            Cloud fraction used for masking bad pixels with 1% default cloud
            fraction.

        co2_scaling : float, optional
            Scaling applied to model tracer with anthropogenic CO2 emissions

        no2_noise_scenario : str, optional
            Noise scenario used to add random uncertainty to the NO2 observations:
            "low" -> 1e15 molecules cm-2 or 15% (whichever is larger) and
            "high" -> 2e15 molecules cm-2 or 20% (whichever is larger)

        no2_cloud_threshold : float, optional
            Cloud fraction used for masking bad pixels with 30% default cloud
            fraction.

        no2_scaling : float, optional
            Scaling applied to model tracer with anthropogenic NO2 emissions.

        co_noise_scenario : str, optional
            Noise scenario used to add random uncertainty to the CO observations:
            "low" -> 4e17 molecules cm-2 or 10% (whichever is larger) and
            "high" -> 4e17 molecules cm-2 or 20% (whichever is larger)

        co_cloud_threshold : float, optional
            Cloud fraction used for masking bad pixels with 5% default cloud
            fraction.

        co_scaling : float, optional
            Scaling applied to model tracer with anthropogenic CO emissions

        make_no2_error_cloud_dependent : boolean, optional
            If True, NO2 uncertainty depends on cloud fraction.

        """
        self.data_path = data_path
        self.constellation = constellation

        self.co2_noise_scenario = co2_noise_scenario
        self.co2_cloud_threshold = co2_cloud_threshold
        self.co2_scaling = co2_scaling

        self.no2_noise_scenario = no2_noise_scenario
        self.no2_cloud_threshold = no2_cloud_threshold
        self.no2_scaling = no2_scaling
        self.make_no2_error_cloud_dependent = make_no2_error_cloud_dependent

        self.co_noise_scenario = co_noise_scenario
        self.co_cloud_threshold = co_cloud_threshold
        self.co_scaling = co_scaling

    def get_filenames(self, date, tmin=10, tmax=11):
        lon_eqs = lon_eq_by_nsat(self.constellation)

        filenames = glob.glob(
            os.path.join(self.data_path, date.strftime("*%Y%m%d*.nc"))
        )
        filenames = [fn for fn in filenames if process_filename(fn)[-1] in lon_eqs]

        return sorted(filenames)

    def read_date(self, date):
        """\
        Returns a list of SMARTCARB Level-2 data for given date using
        constellation and uncertainty scenario of instance.
        """
        return [
            read_level2(
                filename,
                co2_noise_scenario=self.co2_noise_scenario,
                co2_cloud_threshold=self.co2_cloud_threshold,
                co2_scaling=self.co2_scaling,
                no2_noise_scenario=self.no2_noise_scenario,
                no2_cloud_threshold=self.no2_cloud_threshold,
                no2_scaling=self.no2_scaling,
                co_noise_scenario=self.co_noise_scenario,
                co_cloud_threshold=self.co_cloud_threshold,
                co_scaling=self.co_scaling,
                make_no2_error_cloud_dependent=self.make_no2_error_cloud_dependent,
                use_constant=False,
                seed="orbit",
                only_observations=True,
                add_background=True,
            )
            for filename in self.get_filenames(date)
        ]


def lon_eq_by_nsat(nsat):
    """
    Get equator starting longitudes (x100) as array of integers. If nsat is a
    string, a constellation of six satellites is assumed (see code below).
    """
    if isinstance(nsat, str):

        if nsat[0].isdigit():
            lon_eqs = np.array(
                {
                    "1a": [0],
                    "1b": [401],
                    "1c": [805],
                    "1d": [1207],
                    "1e": [1610],
                    "1f": [2012],
                    "2a": [0, 1207],
                    "2b": [401, 1610],
                    "2c": [805, 2012],
                    "3a": [0, 805, 1610],
                    "3b": [401, 1207, 2012],
                    "6": [0, 401, 805, 1207, 1610, 2012],
                }[nsat]
            )
        else:
            mapping = {"a": 0, "b": 401, "c": 805, "d": 1207, "e": 1610, "f": 2012}
            lon_eqs = [mapping[l] for l in nsat]

    else:
        DLON_ORBIT = 24.146341463414636
        lon_eqs = np.linspace(0, DLON_ORBIT, nsat + 1)[:-1]
        lon_eqs = np.array([int(100 * round(v, 2)) for v in lon_eqs])
    return lon_eqs


def process_filename(filename):
    """
    Extract satellite name, orbit number, timestamp and equator starting
    longitude from filename. Sentinel-7 is changed to CO2M.
    """
    filename = os.path.basename(filename)
    filename = os.path.splitext(filename)[0]

    if filename.startswith("cosmo_2d"):
        sat = None
        orbit = None
        date = pandas.to_datetime(filename, format="cosmo_2d_%Y%m%d%H")
        lon = None
    else:
        filename = filename.split("_")

        if filename[1] == "5":
            sat, n, date, orbit, lon = filename[:5]
            sat = "_".join([sat, n])
        elif filename[0] == "CO2M":
            sat, date, orbit, lon = filename
        else:
            sat, n, t, date, orbit, lon = filename[:6]
            sat = "_".join([sat, n, t])

        orbit = int(orbit[1:])
        date = pandas.to_datetime(date, format="%Y%m%d%H")
        lon = int(lon[1:])

    return sat, orbit, date, lon


def read_fields(
    filename, tracers, time=None, correct_berlin=True, slice_=Ellipsis, use_xarray=False
):
    """\
    Read fields from netCDF file.
    
    If `correct_berlin` is True, correct '*_BV' tracers for January and
    July by scaling '*_B0' with 0.55 which corrects the too high emissions
    in January and July in the SMARTCARB simulations. This is done to fix a
    bug in the first month of simulations where large point sources were
    added twice to the emission field.
    """
    with netCDF4.Dataset(filename) as nc:
        fields = []

        for tracer in tracers:
            if correct_berlin and tracer.endswith("_BV"):

                field = nc.variables[tracer]
                attrs = dict((k, field.getncattr(k)) for k in field.ncattrs())

                label = tracer.split("_")[0]

                berlin_tracers = ["%s_B%d" % (label, i) for i in range(3)]
                b0, b1, b2 = read_fields(
                    filename,
                    berlin_tracers,
                    time,
                    correct_berlin,
                    slice_,
                    use_xarray=use_xarray,
                )

                if time.month in [1, 7]:
                    field = 0.55 * b0 + b1 + b2
                else:
                    field = b0 + b1 + b2

                if use_xarray:
                    field.attrs.update(attrs)

            else:
                field = nc.variables[tracer]

                if use_xarray:
                    attrs = dict((k, field.getncattr(k)) for k in field.ncattrs())
                    field = xr.DataArray(field[:], dims=field.dimensions, attrs=attrs)

                if slice_ is Ellipsis or isinstance(slice_, slice):
                    field = field[slice_]
                else:
                    # use slice starting at last dimension (instead of first)
                    ndim = np.ndim(field)

                    if len(slice_) == ndim:
                        field = field[slice_]
                    else:
                        s = [Ellipsis] * (ndim - len(slice_)) + list(slice_)
                        field = field[s]

            # correct _BC fields
            if correct_berlin and tracer.endswith("_BC") and time.month in [1, 7]:
                if tracer.startswith("NO2"):
                    field *= 0.8038946
                elif tracer.startswith("XCO2") or tracer.startswith("YCO2"):
                    field *= 0.7078081
                else:
                    raise ValueError

            field = np.squeeze(field)
            fields.append(field)

    return fields


def read_trace_gas_field(
    filename,
    trace_gas,
    time=None,
    correct_berlin=True,
    clip_data=True,
    slice_=Ellipsis,
    use_constant_emissions=False,
    use_xarray=False,
    scaling=None,
):
    """\
    Read total field of trace gases (CO2, NO2 or CO).
    """
    if scaling is None:
        scaling = 1.0

    suffix = "_BC" if use_constant_emissions else "_BV"

    if trace_gas in ["CO2", "XCO2"]:
        fields = [
            "XCO2%s" % suffix,
            "XCO2_A",
            "XCO2_JV",
            "XCO2_RA",
            "XCO2_GPP",
            "XCO2_BG",
        ]
        bv, a, jv, ra, gpp, bg = read_fields(
            filename, fields, time, correct_berlin, slice_, use_xarray=use_xarray
        )

        field = scaling * (bv + a + jv) + ra - gpp + bg

        if use_xarray:
            attrs = {
                "standard name": "CO2_column-averaged_dry-air_mole_fraction",
                "long name": "CO2_column-averaged_dry-air_mole_fraction",
                "units": "ppmv",
            }
            field.attrs.update(attrs)

        if clip_data:
            field[:] = np.where((field < 0) | (field > 1000), np.nan, field)

    else:
        if trace_gas == "NO2":
            fields = ["NO2%s" % suffix, "NO2_A", "NO2_JV", "NO2_BG"]
            bv, a, jv, bg = read_fields(
                filename, fields, time, correct_berlin, slice_, use_xarray=use_xarray
            )
            field = scaling * (bv + a + jv) + bg

        if trace_gas == "CO":
            fields = ["CO%s" % suffix, "CO_A", "CO_JV", "CO_BG"]
            bv, a, jv, bg = read_fields(
                filename, fields, time, correct_berlin, slice_, use_xarray=use_xarray
            )
            field = scaling * (bv + a + jv) + bg

        if use_xarray:
            attrs = {
                "standard name": "%s_vertical_column_density" % trace_gas,
                "long name": "%s_vertical_column_density" % trace_gas,
                "units": "cm-2",
            }
            field.attrs.update(attrs)

    return field


def read_trace_gas_noise(
    filename,
    tracer,
    use_epf=True,
    level=0.7,
    slice_=Ellipsis,
    make_no2_error_cloud_dependent=True,
    seed="orbit",
    use_xarray=False,
):
    """
    tracer in {'CO2', 'NO2', 'CO', 'uXCO2', 'uNO2_low', 'uNO2_high',
               'uCO_low', 'uCO_high'}
    level in {0.5, 0.7, 1.0, 'low', 'high'}
    """
    sat, orbit, _, lon_eq = process_filename(filename)

    if sat == "Sentinel_5":
        utracer = "uNO2"
    else:
        if tracer == "CO2":
            utracer = "uXCO2"
        elif tracer == "NO2":
            utracer = "uNO2_%s" % level
        else:
            utracer = "uCO_%s" % level

    # read uncertainty (TODO/FIXME: correct uNO2 for Jan/Jul)
    u = read_fields(filename, [utracer], slice_=slice_, use_xarray=use_xarray)[0]

    if not use_xarray:
        u[u.mask] = np.nan
        u = u.data

    # seed based on orbit and lon_eq for same noise patterns with each species
    if seed == "orbit":
        offset = {"CO2": 0, "NO2": 300000000, "CO": 600000000}[tracer]
        np.random.seed(10000 * lon_eq + orbit + offset)
    else:
        np.random.seed(seed)

    noise = np.random.randn(*u.shape).astype(u.dtype)

    if tracer == "CO2":

        level = {"low": 0.5, "medium": 0.7, "high": 1.0}[level]

        if use_epf:
            noise = level * noise * u / 1.50
        else:
            noise = level * noise

    elif tracer == "NO2" and use_epf:
        cc = read_fields(filename, ["CLCT"], slice_=slice_)[0]

        # use Wenig et al. (2008) with `uNO2` instead of 1.5e15
        if make_no2_error_cloud_dependent:
            noise = xr.DataArray((1.0 + 3.0 * cc) * u * noise, dims=u.dims)
        else:
            noise = xr.DataArray(u * noise, dims=u.dims)

    else:
        noise = u * noise

    if use_xarray:
        if tracer == "CO2":
            name = "%s random noise (using %s and %.1f ppm)" % (tracer, utracer, level)
        else:
            name = "%s random noise (using %s)" % (tracer, utracer)

        noise.attrs["standard name"] = name
        noise.attrs["long name"] = name
        noise.attrs["units"] = "ppm" if tracer == "CO2" else "molecules cm-2"

    return noise


def read_cosmo(filename, trace_gas):

    time = process_filename(filename)[2]

    data = {}

    for name in ["rlon", "rlat", "lon", "lat", "CLCT", "PS"]:
        data[name] = read_fields(filename, [name], use_xarray=True)[0]

    data[trace_gas] = read_trace_gas_field(
        filename, trace_gas, time=time, use_xarray=True
    )

    return xr.Dataset(data)


def read_level2(
    filename,
    co2_noise_scenario="medium",
    co2_cloud_threshold=0.01,
    co2_scaling=1.0,
    no2_noise_scenario="high",
    no2_cloud_threshold=0.30,
    no2_scaling=1.0,
    co_noise_scenario=None,
    co_cloud_threshold=0.05,
    co_scaling=1.0,
    make_no2_error_cloud_dependent=True,
    use_constant=False,
    seed="orbit",
    only_observations=True,
    add_background=False,
):
    """
    Read synthetic XCO2, NO2 and CO observations from SMARTCARB project
    [Kuhlmann2020]_ .

    Parameters
    ----------
    filename : str
        Name of SMARTCARB Level-2 file

    co2_noise_scenario : str, optional
        Noise scenario used to add random uncertainty to the CO2 observations
        for vegetation albedo and solar zenith angle of 50° (VEG50 scenario):
        "low" -> 0.5 ppm, "medium" -> 0.7 ppm and "high" -> 1.0 ppm.

    co2_cloud_threshold : float, optional
        Cloud fraction used for masking bad pixels with 1% default cloud
        fraction.

    co2_cloud_threshold : float, optional
        Cloud fraction used for masking bad pixels with 1% default cloud
        fraction.

    co2_scaling : float, optional
        Scaling applied to model tracer with anthropogenic CO2 emissions

    no2_noise_scenario : str, optional
        Noise scenario used to add random uncertainty to the NO2 observations:
        "low" -> 1e15 molecules cm-2 or 15% (whichever is larger) and
        "high" -> 2e15 molecules cm-2 or 20% (whichever is larger)

    no2_cloud_threshold : float, optional
        Cloud fraction used for masking bad pixels with 30% default cloud
        fraction.

    no2_scaling : float, optional
        Scaling applied to model tracer with anthropogenic NO2 emissions.

    co_noise_scenario : str, optional
        Noise scenario used to add random uncertainty to the CO observations:
        "low" -> 4e17 molecules cm-2 or 10% (whichever is larger) and
        "high" -> 4e17 molecules cm-2 or 20% (whichever is larger)

    co_cloud_threshold : float, optional
        Cloud fraction used for masking bad pixels with 5% default cloud
        fraction.

    co_scaling : float, optional
        Scaling applied to model tracer with anthropogenic CO emissions

    make_no2_error_cloud_dependent : boolean, optional
        If True, NO2 uncertainty depends on cloud fraction.

    use_constant : boolean, optional
        Use constant emissions if True and time-varying emissions
        otherwise.

    seed : string, optional
        "seed" used before generating the random noise for the Level-2 images.
        If seed=='orbit', the seed is calculated based on the trace gas,
        satellite and orbit number, resulting in the same image every time data
        is read, which is useful for benchmarking studies.

    only_observations : boolean, optional
        If False, noise-free trace gas array without cloud filtering will be
        added to the dataset.

    add_background : boolean, optional
        If True, add array containing the background tracers, i.e. from
        anthropogenic emissions outside the model domain and, for CO2, biospheric
        fluxes.

    Returns
    -------
    xr.Dataset
        CO2M Level-2 orbit from SMARTCARB dataset.

    Notes
    -----
    .. [Kuhlmann2020] Kuhlmann, G., Clément, V., Marshall, J., Fuhrer, O.,
        Broquet, G., Schnadt-Poberaj, C., Löscher, A., Meijer, Y., & Brunner, D.
        (2020). Synthetic XCO2, CO and NO2 observations for the CO2M and
        Sentinel-5 satellites [Data set]. Zenodo.
        https://doi.org/10.5281/zenodo.4048228
    """
    data = {}
    dims = ("along", "across")
    dims2 = ("along", "across", "corners")

    satellite, orbit, time, lon_eq = process_filename(filename)

    if satellite == "Sentinel_7_CO2":
        satellite = "CO2M"

    data["time"] = pandas.Timestamp(time)

    for name1, name2 in [
        ("lon", "longitude"),
        ("lat", "latitude"),
        ("lonc", "longitude_corners"),
        ("latc", "latitude_corners"),
        ("clouds", "CLCT"),
        ("psurf", "PS"),
    ]:
        data[name1] = read_fields(filename, [name2], use_xarray=True)[0]

    if add_background:
        bg, resp, gpp = read_fields(
            filename, ["XCO2_BG", "XCO2_RA", "XCO2_GPP"], use_xarray=True
        )
        data["CO2_BG"] = bg + resp - gpp
        data["NO2_BG"] = read_fields(filename, ["NO2_BG"], use_xarray=True)[0]
        data["CO_BG"] = read_fields(filename, ["CO_BG"], use_xarray=True)[0]

    # CO2 and NO2
    for trace_gas, noise, thr, scaling in [
        ("CO2", co2_noise_scenario, co2_cloud_threshold, co2_scaling),
        ("NO2", no2_noise_scenario, no2_cloud_threshold, no2_scaling),
        ("CO", co_noise_scenario, co_cloud_threshold, co_scaling),
    ]:
        if noise is None or thr is None:
            continue

        val = read_trace_gas_field(
            filename,
            trace_gas,
            time=time,
            use_constant_emissions=use_constant,
            use_xarray=True,
            scaling=scaling,
        )

        err = read_trace_gas_noise(
            filename,
            trace_gas,
            level=noise,
            use_epf=True,
            seed=seed,
            use_xarray=True,
            make_no2_error_cloud_dependent=make_no2_error_cloud_dependent,
        )

        is_cloudy = data["clouds"] > thr

        # store noisefree/gapfree data
        if not only_observations:
            data[f"{trace_gas}_noisefree"] = val.copy()

        val[:] = np.where(is_cloudy, np.nan, val)
        err[:] = np.where(is_cloudy, np.nan, err)

        data[trace_gas] = err + val

        data[f"{trace_gas}_std"] = xr.zeros_like(val)

        if trace_gas == "NO2":
            noise_level = {"low": 1e15, "medium": 1.5e15, "high": 2e15}[noise]
        elif trace_gas == "CO":
            noise_level = {"low": 4e17, "high": 4e17}[noise]
        else:
            noise_level = {"low": 0.5, "medium": 0.7, "high": 1.0}[noise]

        data[f"{trace_gas}_std"][:] = noise_level

        if not only_observations:
            data[f"{trace_gas}_noise"] = err

        attrs = {"noise_level": noise_level, "cloud_threshold": thr}
        data[trace_gas].attrs.update(attrs)
        data[trace_gas].attrs.update(val.attrs)
        data[trace_gas].attrs["standard name"] += " with random noise"
        data[trace_gas].attrs["long name"] += " with random noise"

        if scaling is None:
            data[trace_gas].attrs["scaling"] = 1.0
        else:
            data[trace_gas].attrs["scaling"] = scaling

    data = xr.Dataset(
        data, attrs={"satellite": satellite, "orbit": orbit, "lon_eq": lon_eq}
    )
    data.attrs["time"] = pandas.Timestamp(time)
    data.attrs.update(ATTRIBUTES)

    return data


def read_true_emissions(
    gas,
    source,
    time=None,
    units='kg/s'
):
    """\
    Read true emissions for `gas` at `source` used in SMARTCARB simulations.
    If time is given, emissions are interpolated.
    """
    data_path = os.path.join(os.path.dirname(ddeq.__file__), "data")
    em = pandas.read_csv(
        os.path.join(
            data_path,
            f"SMARTCARB-{'NO2' if gas == 'NOx' else gas}-emissions.csv"),
        sep="\t",
        index_col=0,
        parse_dates=True,
    )

    em = em[f"{source} (Mt/yr)"]
    em = ucat.convert_mass_per_time_unit(em, 'Mt/a', units)
    em.index.name = 'time'
    em.name = f'true_{gas}_emissions'

    em = em.to_xarray()
    em.attrs['units'] = units

    if time is not None:
        em = em.interp(time=time)

    return em


def plot_diurnal_cycle(origin, norm=False, ax=None, add_legend=True, only_co2=False):
    """
    Plot diurnal cycle of CO2 and NO2 emissions as well as CO2:NOX emission
    ratios.
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    co2 = read_true_emissions(None, "CO2", origin)
    no2 = read_true_emissions(None, "NO2", origin)

    hod = np.arange(0, 24)
    co2 = np.array([np.mean(co2[co2.index.hour == h]) for h in hod])
    no2 = np.array([np.mean(no2[no2.index.hour == h]) for h in hod])

    if norm:
        co2 /= co2.mean()
        no2 /= no2.mean()
        factor = 1.0
    else:
        factor = 1e3

    lines = []
    lines += ax.plot(hod, co2, "o-", label="CO$_2$ emissions (Mt CO$_2$ yr$^{-1}$)")

    if not only_co2:
        lines += ax.plot(
            hod, no2, "s-", label="NO$_\\mathrm{x}$ emissions (kt NO$_2$ yr$^{-1}$)"
        )

    ax.grid(True)
    ax.set_xlabel("Hour of day (UTC)")
    ax.set_ylabel("Emissions")

    ax.set_xticks(np.arange(0, 25, 3))

    if norm:
        ax.set_ylim(0.5, 1.5)
    else:
        ax.set_ylim(0, 40)

    if not norm:
        ax2 = ax.twinx()
        lines += ax2.plot(
            hod,
            factor * co2 / no2,
            "rv-",
            label="CO$_2$:NO$_\\mathrm{x}$ emission ratios",
        )
        ax2.set_ylabel("CO$_2$:NO$_\\mathrm{x}$ emission ratios", color="red")

        ax2.set_ylim(600, 1400)
        ax2.set_yticks(np.arange(600, 1401, 100))
        ax2.set_yticklabels(np.arange(600, 1401, 100), color="red")

    if add_legend:
        plt.tight_layout()
        plt.legend(lines, [l.get_label() for l in lines])

    return hod, co2, no2


def plot_seasonal_cycle(
    origin, norm=False, ax=None, add_legend=True, only_co2=False, short_month=False
):

    if ax is None:
        fig, ax = plt.subplots(1, 1)

    co2 = read_true_emissions(None, "CO2", origin)
    no2 = read_true_emissions(None, "NO2", origin)

    moy = np.arange(1, 13)
    co2 = np.array([np.mean(co2[co2.index.month == m]) for m in moy])
    no2 = np.array([np.mean(no2[no2.index.month == m]) for m in moy])

    if norm:
        co2 /= co2.mean()
        no2 /= no2.mean()
        factor = 1.0
    else:
        factor = 1e3

    lines = []
    lines += ax.plot(moy, co2, "o-", label="CO$_2$ emissions (Mt CO$_2$ yr$^{-1}$)")

    if not only_co2:
        lines += ax.plot(
            moy, no2, "s-", label="NO$_\\mathrm{x}$ emissions (kt NO$_2$ yr$^{-1}$)"
        )

    ax.grid(True)
    ax.set_xlabel("Month of year")
    ax.set_ylabel("Emissions")

    ax.set_xticks(np.arange(1, 13))
    if short_month:
        ax.set_xticklabels(["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    else:
        ax.set_xticklabels(
            [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
        )
    ax.set_xlim(0.5, 12.5)

    if norm:
        ax.set_ylim(0.5, 1.5)
    else:
        ax.set_ylim(0, 40)

    if not norm:
        ax2 = ax.twinx()
        lines += ax2.plot(
            moy,
            factor * co2 / no2,
            "rv-",
            label="CO$_2$:NO$_\\mathrm{x}$ emission ratios",
        )
        ax2.set_ylabel("CO$_2$:NO$_\\mathrm{x}$ emission ratios", color="red")

        ax2.set_ylim(600, 1400)
        ax2.set_yticks(np.arange(600, 1401, 100), color="red")

    if add_legend:
        plt.tight_layout()
        plt.legend(lines, [l.get_label() for l in lines])


def plot_weekly_cycle(origin, norm=False, ax=None, add_legend=True, only_co2=False):

    if ax is None:
        fig, ax = plt.subplots(1, 1)

    co2 = read_true_emissions(None, "CO2", origin)
    no2 = read_true_emissions(None, "NO2", origin)

    dow = np.arange(0, 7)
    co2 = np.array([np.mean(co2[co2.index.weekday == d]) for d in dow])
    no2 = np.array([np.mean(no2[no2.index.weekday == d]) for d in dow])

    if norm:
        co2 /= co2.mean()
        no2 /= no2.mean()

    lines = []
    lines += ax.plot(dow, co2, "o-", label="CO$_2$ emissions (Mt CO$_2$ yr$^{-1}$)")

    if not only_co2:
        lines += ax.plot(
            dow, no2, "s-", label="NO$_\\mathrm{x}$ emissions (kt NO$_2$ yr$^{-1}$)"
        )

    ax.grid(True)
    ax.set_xlabel("Day of week")
    ax.set_ylabel("Emissions")

    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    ax.set_xlim(-0.5, 6.5)

    if norm:
        ax.set_ylim(0.5, 1.5)
    else:
        ax.set_ylim(0, 40)

    if not norm:
        ax2 = ax.twinx()
        lines += ax2.plot(
            dow, 1e3 * co2 / no2, "rv-", label="CO$_2$:NO$_\\mathrm{x}$ emission ratios"
        )
        ax2.set_ylabel("CO$_2$:NO$_\\mathrm{x}$ emission ratios", color="red")

        ax2.set_ylim(600, 1400)
        ax2.set_yticks(np.arange(600, 1401, 100), color="red")

    if add_legend:
        plt.tight_layout()
        plt.legend(lines, [l.get_label() for l in lines])
