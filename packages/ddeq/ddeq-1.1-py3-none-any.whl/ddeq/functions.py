from scipy.special import erf
import scipy.integrate

import numpy as np


class PointPlumeModel:
    def __init__(self, x0=None):
        self.x0 = x0

    def __call__(self, x, Q, x0=None):
        if x0 is None:
            x0 = self.x0

        if x0 is None:
            return np.full(x.shape, Q)
        else:
            return Q * decay_function(x, 0.0, x0)


def city_plume_model(x, Q, sigma, x0=None, x_source=0.0, B=0.0, dx=1e3):
    """
    Function describes how flux changes when passing over an area source
    (e.g., city).

    x : along-plume distance (in meters)
    sigma: width of gaussian
    x_source : plume source
    x0: decay distance

    B: background
    """
    # high-resolution x-distance
    xhigh = np.arange(x[0] - 50e3, x[-1] + 200e3, dx)

    # decay function
    e = decay_function(xhigh, x_source, x0)

    # gaussian
    xgauss = np.arange(-50e3, +50e3 + dx / 2, dx)
    g = gauss(xgauss, 1.0, sigma, 0.0)

    # convolution
    f = scipy.ndimage.convolve(e, g, mode="nearest")

    # scaling with source strength assumed
    M = Q * f / f.max() + B

    # interpolate
    M = np.interp(x, xhigh, M)

    return M


class FixedGaussCurve:
    def __init__(self, sigma, shift):
        """\
        A Gauss curve with fixed standard width (sigma) and center position
        (shift).
        """
        self.sigma = sigma
        self.shift = shift

    def __call__(self, x, E0, slope=0.0, offset=0.0):
        return gauss(x, E0, self.sigma, self.shift, slope, offset)


def gauss(x, E0, sigma, shift, slope=0.0, offset=0.0):
    """ """
    if np.isnan(slope):
        slope = 0.0
    if np.isnan(offset):
        offset = 0.0

    e = E0 / (sigma * np.sqrt(2.0 * np.pi)) * np.exp(-0.5 * ((x - shift) / sigma) ** 2)
    e += slope * x + offset

    return e


def decay_function(x, x_source, x0=None):
    """
    Exp. decay in x direction downstream of x_source with decay distance x0.
    """
    e = np.zeros_like(x)
    downstream = x >= x_source

    if x0 is None:
        e[downstream] = 1.0
    else:
        e[downstream] = np.exp(-(x[downstream] - x_source) / x0)

    return e


def error_function(x, E0, sigma, box_width=20e3, shift=0.0, slope=0.0, offset=0.0):
    """\
    An error function plus a linear function.

    The error function is the convolution of Gaussian and box function. The
    integral of the error function is E0.

    sigma - standard deivation of the Gaussian
    box_width - widht of the box function
    slope - slope of the linear function
    offset - offset of the linear function
    """
    delta = 0.5 * box_width
    a = sigma * np.sqrt(2.0)

    x1 = (x - shift + delta) / a
    x2 = (x - shift - delta) / a

    g = E0 * (erf(x1) - erf(x2)) / (4.0 * delta)
    g += x * slope + offset

    return g


class NO2toNOxConversion:

    # Meier et al. 2024
    _PARAMS = {
        "Belchatow": [3.8, 546.0, 1.66],
        "Janschwalde": [1.6, 1638.0, 1.31],
        "Lipetsk": [4.2, 486.0, 1.36],
        "Matimba": [6.1, 744.0, 1.90],
    }
    _PARAMS_STD = {
        "Belchatow": [0.7, 48.0, 0.01],
        "Janschwalde": [0.1, 162.0, 0.01],
        "Lipetsk": [0.3, 24.0, 0.02],
        "Matimba": [1.3, 84.0, 0.02],
    }

    def __init__(self, params=None, params_std=None, name=None):
        """
        Model to convert NO2 to NOx line densities using a negative exponential
        function.

        f(t) = m * np.exp(- t / r [s]) + f

        Parameters
        ----------
        params : np.ndarray
            model parameters (m, tau and f)

        params_std : np.ndarray
            1-sigma uncertainty of model parameters

        name : str
            Name for parameters from Meier et al. 2024
        """
        if name is None:
            self.params = params
            self.params_std = params_std
        else:
            self.params = NO2toNOxConversion._PARAMS[name]
            self.params_std = NO2toNOxConversion._PARAMS_STD[name]

    def neg_exp(self, t, m, r, f0):
        return m * np.exp(-t / r) + f0

    def get_sigma(self, t, popt, pcov):
        m, r, f0 = popt
        m_std, r_std, f0_std = pcov
        return np.sqrt(
            np.exp(-t / r) ** 2 * m_std**2
            + (m / r**2 * np.exp(-t / r)) ** 2 * r_std**2
            + f0_std**2  # df/df0 = 1
        )

    def __call__(self, time):
        """\
        Compute scaling factors and their precision to convert NO2 to NOx line
        densities as a function of time since emissions.
        """
        f = self.neg_exp(time, *self.params)
        f_std = self.get_sigma(time, self.params, self.params_std)

        # set upstream values to background f0
        f[time < 0] = self.params[2]
        f_std[time < 0] = self.params_std[2]

        return f, f_std


def NO2_line_density_along_plume(x, b):
    """
    Compute NO2 line density in along-plume direction accounting for NO2
    decay with decay time (tau) and NO2-to-NOx conversion (m, r and f0).

    q(t) = 1 / u * Q * exp(-t/tau) / (m * exp(-t/r) + f0)

    """
    Q, tau, m, r, f0 = x
    u = b['u']
    t = b['t']

    q = 1.0 / u * Q * np.exp(-t / tau)
    q /= m * np.exp(-t / r) + f0

    q[t < 0] = 0.0

    return q


def peak_model(Q, sigma_x, sigma_y, x0, y0, corr, B, grids):
    """
    Model that describes a peak in divergence map, which we want to fit at
    each source

    Q = peak integral corresponding emission in kg/s
    sigma_x, sigma_y = deviations x and y directions in km
    x0, y0 = center of the peak
    corr = correlation between x and y dimensions
    theta = parameters that to be optimized
    B = Background in kg/m²/s
    grid = cropped grid around the source
    """
    # Kilometer grids
    X, Y = grids[0], grids[1]

    # Normalization
    N = Q / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - corr**2))
    G = (
        N
        * np.exp(
            -((X - x0) ** 2) / (2 * sigma_x**2 * (1 - corr**2))
            - (Y - y0) ** 2 / (2 * sigma_y**2 * (1 - corr**2))
            + corr * (X - x0) * (Y - y0) / (sigma_x * sigma_y * (1 - corr**2))
        )
        + B
    )

    return G
