"""
Estimate time profiles of emissions using satellite observations.


annual time profile
- low-order polynomial
- periodic boundary conditions
- a priori state vector and covariance matrix
- ...

weekly cycle:
- weekday and weekend value
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.interpolate
import scipy.optimize
import xarray as xr

import ddeq


def hermite_spline(x, p, t, last_years_value=None):
    """
    Hermite spline with periodic boundary conditions.
    """
    delta = np.diff(p)
    m = np.zeros_like(p)

    m[0] = 0.5 * (p[0] - p[-2])
    m[-1] = m[0]

    for k in range(1, m.size - 1):
        m[k] = 0.5 * (p[(k + 1) % p.size] - p[(k - 1) % p.size])

    # compute spline
    y = np.zeros(x.shape, dtype="f8")
    k = 0
    for i in range(x.size):
        if x[i] > t[k + 1] and k < t.size - 2:
            k += 1

        s = (x[i] - t[k]) / (t[k + 1] - t[k])

        y[i] += p[k] * (1 + 2 * s) * (1 - s) ** 2
        y[i] += m[k] * s * (1 - s) ** 2
        y[i] += p[k + 1] * s**2 * (3 - 2 * s)
        y[i] += m[k + 1] * s**2 * (s - 1)

    return y


class SeasonalCycle:
    def __init__(self, x, y, knots, ystd=1.0, gamma=None, last_years_value=None):
        self.x = x
        self.y = y
        self.gamma = gamma
        self.last_years_value = last_years_value

        if np.all(ystd == 0.0):
            print("All ystd are 0.0: Set weights to 1.0!")
            self.ystd = np.ones_like(ystd)
        else:
            self.ystd = ystd

        self.knots = knots
        self.w0 = np.full(knots.size - 1, y.mean())

    def __call__(self, w, x=None, last_years_value=None):
        w = np.append(w, w[0])
        s = hermite_spline(
            self.x if x is None else x,
            w,
            self.knots,
            last_years_value=self.last_years_value,
        )

        return s

    def integrate(self, w, w_std=None):
        """
        Integrate seasonal cycle to obtain annual emissions.

        w:      emissions at knots
        w_std:  uncertainty at knots
        """
        total = 0.0
        unc = 0.0

        for k in range(w.size - 1):

            if w_std is not None:
                unc += w_std[(k - 1) % w.size] ** 2 * (1 / 24) ** 2
                unc += w_std[k] ** 2 * (13 / 24) ** 2
                unc += w_std[(k + 1) % w.size] ** 2 * (13 / 24) ** 2
                unc += w_std[(k + 2) % w.size] ** 2 * (1 / 24) ** 2

            p0 = w[k]
            p1 = w[(k + 1) % w.size]
            m0 = 0.5 * (w[(k + 1) % w.size] - w[(k - 1) % w.size])
            m1 = 0.5 * (w[(k + 2) % w.size] - w[k])

            total += 1 / 2 * p0 + 1 / 12 * m0 + 1 / 2 * p1 - 1 / 12 * m1

        if w_std is not None:
            unc = np.sqrt(unc) / (w.size - 1)

            return total / (w.size - 1), unc

        return total / (w.size - 1)

    def residual(self, w):

        res = (self(w) - self.y) / self.ystd

        if self.gamma is not None:
            d = self.gamma * np.append(np.diff(w), w[-1] - w[0])
            res = np.concatenate([res, d])

        return res


def fit(
    times, ts, ts_std, n_knots=None, gamma=None, use_std=True, last_years_value=None
):
    """
    Fit periodic C-spline to indvidual emission estimates, which can be used to
    estimate the seasonal cycle of the emissions and for computing the annual
    total and its uncertainty. The function does not account for temporal
    sampling biases.

    Parameters
    ----------
    times : pd.datetime
        The times of the individual emission estimates.

    ts: np.array
        Individual emission estimates at the given times.

    ts_std: np.array
        Uncertainty of individual emission estimates (one standard deviation) at
        given times.

    n_knots : integer, optional
        Number of knots used in the C-spline. By default uses `n_years*3 + 1`.

    gamma : float, optional
        If given, the fit will additional constraint by minimzing the difference
        between the sum of absolute differences between the control points
        scaled by `gamma`.

    Returns
    -------
    OptimizeResult
        Results from the least square fit.

    SeasonalCycle
        Data class with the individual estimates and their uncertainties.

    np.array
        Array with seconds since starting time every hour.

    np.array
        Seasonal cycle at seconds since starting time.

    float
        chi2 value of the fit.
    """

    if isinstance(times, np.ndarray):
        times = pd.to_datetime(times)

    n_years = len(times.year.unique())

    if n_knots is None:
        n_knots = n_years * 3 + 1

    # seconds per year
    knots = np.linspace(0, n_years * 31536000, n_knots + 1)

    start = pd.to_datetime(f"{times.min().year}-01-01")

    # Calculate xdata by subtracting the start date and converting to seconds
    xdata = (times - start).total_seconds()
    ydata = ts
    ystd = ts_std

    # remove invalid data
    valids = np.isfinite(ydata) & np.isfinite(ystd)

    xdata = xdata[valids]
    ydata = ydata[valids]
    ystd = ystd[valids]

    # model
    if use_std:
        cycle = SeasonalCycle(
            xdata,
            ydata,
            knots,
            ystd=ystd,
            gamma=gamma,
            last_years_value=last_years_value,
        )
    else:
        cycle = SeasonalCycle(
            xdata,
            ydata,
            knots,
            ystd=0.0,
            gamma=gamma,
            last_years_value=last_years_value,
        )

    # fit
    if ydata.size < n_knots:
        res = None
        x = np.full(n_knots, np.nan)
        x_std = np.full(n_knots, np.nan)
        chi2 = np.nan
    else:
        res = scipy.optimize.least_squares(cycle.residual, cycle.w0, method="lm")
        x = res.x
        K = res.jac

        chi2 = np.sum(cycle.residual(x) ** 2) / (ydata.size - x.size)

        # compute uncertainty assuming moderate quality of fit
        # Sx = chi2 * np.linalg.inv(K.T @ K)

        # compute uncertainty
        if use_std:
            Sx = np.linalg.inv(K.T @ K)
        else:
            inv_Se = np.diag(1.0 / ystd**2)
            Sx = np.linalg.inv(K.T @ inv_Se @ K)

        res.x_std = np.sqrt(Sx.diagonal())

    # hourly values
    seconds = np.arange(0, n_years * 31536000, 60 * 60)
    times = start + pd.to_timedelta(seconds, unit="s")

    return res, cycle, times, cycle(x, seconds), chi2


def fit_years(times, ts, ts_std, n_knots=4, gamma=None, use_std=True):

    df = pd.DataFrame({"time": pd.to_datetime(times), "ts": ts, "ts_std": ts_std})
    df = df.set_index("time")
    df = df.dropna()

    all_times = []
    all_cycle = []

    for i, year in enumerate(df.index.year.unique()):

        df_year = df[df.index.year == year]

        fit_result, func, times, cycle, chi2 = fit(
            df_year.index.values,
            df_year["ts"].values,
            ts_std=df_year["ts_std"].values,
            n_knots=n_knots,
            gamma=gamma,
            use_std=use_std,
            last_years_value=cycle[-1] if i > 0 else None,
        )

        all_times.extend(times)
        all_cycle.extend(cycle)

    return all_times, all_cycle


def add_cycle(
    dataset,
    n_knots=4,
    nsat=None,
    gamma=None,
    varname="est_emissions",
    cyclename="fitted_cycle",
    use_error=True,
):

    if nsat is not None:
        lon_eqs_in_constellation = ddeq.smartcarb.lon_eq_by_nsat(nsat)
        valids = np.isin(dataset.lon_eq, lon_eqs_in_constellation)
        valids &= np.isfinite(dataset[varname])
        valids &= np.isfinite(dataset[varname + "_std"])
    else:
        valids = np.isfinite(dataset[varname])
        valids &= np.isfinite(dataset[varname + "_std"])

    if use_error:
        ystd = dataset[varname + "_std"][valids]
    else:
        ystd = xr.zeros_like(dataset[varname])[valids]

    fit_result, func, times, cycle, chi2 = fit(
        dataset["overpass"][valids],
        dataset[varname][valids],
        ystd,
        n_knots=n_knots,
        gamma=gamma,
    )

    dataset[cyclename] = xr.DataArray(cycle, dims="time")

    if fit_result is None:
        dataset[cyclename].attrs["annual_mean"] = np.nan
        dataset[cyclename].attrs["annual_mean_std"] = np.nan
    else:
        em, em_std = func.integrate(fit_result.x, fit_result.x_std)
        dataset[cyclename].attrs["annual_mean"] = em
        dataset[cyclename].attrs["annual_mean_std"] = em_std

    dataset[cyclename].attrs["units"] = ""  # TODO
    dataset[cyclename].attrs["chi2"] = chi2

    dataset[cyclename].attrs["number of overpasses"] = int(valids.sum())

    return dataset
