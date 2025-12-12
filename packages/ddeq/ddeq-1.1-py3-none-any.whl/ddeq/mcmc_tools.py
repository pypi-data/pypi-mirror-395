#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 15:09:13 2023

@author: nurmelaj
"""
import time
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import chi2, gamma
from scipy.optimize import least_squares, newton


def AM_MC(
    residual,
    x0,
    samples,
    warmup,
    C0=None,
    std=None,
    prior=None,
    bounds=None,
    names=None,
    init_fit=True,
    progress=True,
):
    """
    Adaptive Metropolis Monte-Carlo sampling algorithm.

    Parameters
    ----------
    residual : callable
        Returns a residual vector correponding the given state.
    x0 : 1d-array
        Initial value for the chain.
    samples : int
        Number of samples to draw from the posterior.
    warmup : int
        Warmup of the chain, samples drawn before the chain has converged to the true posterior.
    C0 : optinal, 2d-array
        Initial covariance for jumping distribution. If None, the initial covariance is a diagonal
        matrix with squared 10 % std for each value in x0.
    std : float or 1d-array, optional
        Standard deviation of the residual vector. If float is provided, the residual std will be sampled from
        inverse gamma conjugate prior. If 1d-array is provided, the residual std is assumed to be twice the
        std of the data vector, accounting the modeling error. If None, will be estimated first.
    prior : callable, optional
        Prior distribution.
    bounds : sequence of tuples
        Min and max values for each parameter.
    init_fit : bool, optional
        If True, optimizes x0 and computes covariance using least-square optimization.
    progress : bool, optional
        Prints percentual progress if True.

    Returns
    -------
    chain : 2d-array
        First dimension defines length of the chain and second dimension number of variables.
    Ct : 2d-numpy array
        Covariance matrix for variables in Markov chain.
    mean : 1d-numpy array
        Mean approximation of the variables of interest.
    """

    zero_indices = np.where(x0 == 0)[0]
    if len(zero_indices) > 0:
        raise ValueError(
            f"Initial value exactly zero at indices {zero_indices} is not allowed when scales is None"
        )
    if init_fit:
        scales = 10 ** np.floor(np.log10(np.abs(x0)))
        result = least_squares(residual, x0, method="lm", x_scale=scales)
        x0 = result.x
        if C0 is None:
            J = result.jac
            H = J.T @ J
            C0 = np.linalg.inv(H)
    elif C0 is None:
        C0 = np.diag(np.square(0.1 * np.abs(x0)))
    if bounds is not None:
        bounds = np.array(bounds)
        if np.any(x0 < bounds[:, 0]) or np.any(x0 > bounds[:, 1]):
            raise ValueError(f"Initial value {x0} outside bounds")
    xdim = len(x0)
    # Scaling factor for the covariance update
    sd = 2.4**2 / xdim
    if prior is None:
        prior = lambda *args: 1
    res_init = residual(x0)
    ydim = len(res_init)
    # Whether or not to sample the variance from inverse gamma prior
    sample_var = std is None or isinstance(std, float)
    # Variance of the residual vector
    if std is None:
        std = np.sqrt(np.sum(np.square(res_init)) / ydim)
    if not (isinstance(std, float) or isinstance(std, np.ndarray)):
        raise ValueError(
            f"Invalid input {std} for observation std, must be either 1d-array or float"
        )
    var = std**2
    # Weighted square sum of the residual vector
    wss = np.sum(np.square(res_init) / var)
    # Unscaled negative log posterior (corresponds loss function assuming multivariate Gaussian likelihood)
    if isinstance(var, np.ndarray):
        loss = 0.5 * wss + 0.5 * np.sum(np.log(2 * np.pi * var)) - np.log(prior(x0))
    else:
        loss = 0.5 * wss + 0.5 * ydim * np.log(2 * np.pi * var) - np.log(prior(x0))
    # Initialize chains
    chain = np.full((samples + warmup, xdim), np.nan)
    loss_chain = np.full(samples + warmup, np.nan)
    chain[0, :] = x0
    # MAximum Posteior estimate
    MAP = x0
    loss_chain[0] = loss
    # Estimate prior parameters for observation variance sampling
    var_mean, var_std = var, 0.5 * var
    # (Inverse) gamma priors
    shape, scale = (var_mean / var_std) ** 2, var_std**2 / var_mean
    # Initial covariance matrix
    Ct = C0
    # Percentual progress and number of values accepted
    percents, accepted = 0, 0
    start_time = time.process_time()
    for t in range(1, samples + warmup):
        if progress and t / (samples + warmup - 1) * 100 >= percents:
            print(f"{percents}%")
            percents += 10
        # Proposed sample
        proposed = np.random.multivariate_normal(chain[t - 1, :], Ct)
        if np.any(proposed < bounds[:, 0]) or np.any(proposed > bounds[:, 1]):
            log_acceptance_ratio = -np.inf
        else:
            wss_proposed = np.sum(np.square(residual(proposed)) / var)
            if isinstance(var, np.ndarray):
                proposed_loss = (
                    0.5 * wss_proposed
                    + 0.5 * np.sum(np.log(2 * np.pi * var))
                    - np.log(prior(proposed))
                )
            else:
                proposed_loss = (
                    0.5 * wss_proposed
                    + 0.5 * ydim * np.log(2 * np.pi * var)
                    - np.log(prior(proposed))
                )
            log_acceptance_ratio = -proposed_loss + loss

        # Accept or reject
        if np.log(np.random.uniform(0, 1)) <= log_acceptance_ratio:
            chain[t, :] = proposed
            if t >= warmup:
                accepted += 1
            loss = proposed_loss
            # Update MAP value if loss is smaller (minimum of the loss function is the maximum of posterior)
            MAP = proposed if loss < proposed_loss else MAP
            wss = wss_proposed
            # Update variance using (inverse) gamma distribution
            if sample_var:
                var = 1 / np.random.gamma(
                    shape + 0.5 * ydim, 1 / (1 / scale + 0.5 * wss * var)
                )
        else:
            chain[t, :] = chain[t - 1, :]
            loss_chain[t] = loss

        # Adaptation starts after the warmup period
        if t == warmup - 1:
            accepted = 0
            Ct = sd * np.cov(chain[:warmup, :], rowvar=False)
            mean = chain[:warmup, :].mean(axis=0).reshape((xdim, 1))
        if t >= warmup:
            # Value in chain as column vector
            vec = chain[t, :].reshape((xdim, 1))
            # Recursive update for mean
            next_mean = 1 / (t + 1) * (t * mean + vec)
            # Recursive update for the covariance matrix
            Ct = (t - 1) / t * Ct + sd / t * (
                t * mean @ mean.T - (t + 1) * next_mean @ next_mean.T + vec @ vec.T
            )
            # Update mean
            mean = next_mean
    # Value of the loss function at the MAP value
    ss = np.sum(np.square(residual(MAP)))
    # Mean and std assuming that the variance follows the inverse gamma distribution
    var = (1 / scale + 0.5 * ss) / (shape + 0.5 * ydim - 1)
    var_std = (1 / scale + 0.5 * ss) / (
        (shape + 0.5 * ydim - 1) * np.sqrt(shape + 0.5 * ydim - 2)
    )
    # Empirical posterior covariance
    cov = np.cov(chain[warmup:, :], rowvar=False)
    end_time = time.process_time()
    if progress:
        print(
            f"AM performance:\nPosterior samples = {samples}\ntime: {end_time-start_time} s\nacceptance ratio = {100*accepted/samples:.2f} %"
        )
    # Write results to xarray object
    if names is None:
        names = [f"x{i}" for i in range(1, xdim + 1)]
    ds = xr.Dataset(
        {
            "chain": xr.DataArray(
                chain,
                dims=["index", "params"],
                coords=dict(index=range(samples + warmup), params=names),
            ),
            "loss": xr.DataArray(
                loss_chain, dims=["index"], coords=dict(index=range(samples + warmup))
            ),
            "MAP": xr.DataArray(MAP, dims=["params"], coords=dict(params=names)),
            "cov": xr.DataArray(
                cov, dims=["params", "params"], coords=dict(params=names)
            ),
        }
    )
    ds["warmup"] = warmup
    ds["samples"] = samples
    ds["var"] = var
    ds["var_std"] = var_std
    return ds


def plot_MC_pairs(sampling, labels=None):
    """
    Plots samples after the warmup for each variable (columns) in the Markov chain

    Parameters
    ----------
    chain : 2d-array
        Markov chain, rows tell iterations and columns tell dimensions.
    warmup : int
        Length of the warmup period used in the chain.
    labels : list of str, optional
        Labels for each variable. Default is None in which case generic x_i labels are used.

    Returns
    -------
    tuple of fig obj
        Plots of random walk chains and pair-wise covariances.
    """

    plt.figure("random_walks")
    plt.title("Random walk for each variable")
    chain = sampling["chain"]
    length, dim = chain.shape
    mean = sampling["mu"]
    cov = sampling["cov"]
    warmup = sampling["warmup"]
    samples = sampling["samples"]
    r = np.sqrt(chi2.ppf(0.95, 1))
    for d in range(dim):
        # plt.subplot(dim,dim,d*(dim+1)+1)
        plt.subplot(dim, 1, d + 1)
        plt.plot(range(samples), chain[warmup:, d], ".", markersize=2)
        if labels is None:
            plt.ylabel(f"$x_{{{d+1}}}$")
        else:
            plt.ylabel(labels[d])
        if d != dim - 1:
            plt.xticks(ticks=[], labels=[])
        std = np.sqrt(cov[d, d])
        mu = mean[d]
        plt.axhline(y=mu - r * std, linestyle="--", color="black")
        plt.axhline(y=mu + r * std, linestyle="--", color="black")
    plt.xlabel("Posterior samples")
    plt.show()

    if "var_chain" in sampling.keys():
        """
        plt.figure('variance_distribution')
        plt.title('Observation and model variance distribution')
        var_mean, var_std = sampling['var'], sampling['var_std']
        alpha, beta = var_mean**2 / var_std**2, var_mean / var_std**2
        #mean, var = gamma.stats(alpha, moments='mv')
        xmin, xmax = var_mean-4*var_std, var_mean+4*var_std
        var_arr = np.linspace(xmin,xmax,100)
        plt.plot(var_arr, gamma.pdf(var_arr, alpha, scale = 1/beta), label='gamma')
        plt.axvline(x=var_mean,color='red',linestyle='-',label=r'$\\mu$')
        # Compute 95% confidence interval
        lower = newton(lambda x: abs(gamma.cdf(x, alpha, scale=1/beta)-0.025), var_mean)
        upper = newton(lambda x: abs(gamma.cdf(x, alpha, scale=1/beta)-0.975), var_mean)
        plt.axvline(x=lower,color='red',linestyle='--')
        plt.axvline(x=upper,color='red',linestyle='--')
        plt.xlim(var_arr[0],var_arr[-1])
        plt.legend()
        plt.show()
        """
        plt.figure("residual_variance")
        plt.title("Random walk for residual variance")
        var_chain = sampling["var_chain"]
        plt.plot(range(samples), var_chain[warmup:], "r.", markersize=2)
        var_mean, var_std = sampling["var"], sampling["var_std"]
        alpha, beta = var_mean**2 / var_std**2, var_mean / var_std**2
        # Compute 95% confidence interval
        lower = newton(
            lambda x: abs(gamma.cdf(x, alpha, scale=1 / beta) - 0.025), var_mean
        )
        upper = newton(
            lambda x: abs(gamma.cdf(x, alpha, scale=1 / beta) - 0.975), var_mean
        )
        plt.axhline(y=lower, linestyle="--", color="black")
        plt.axhline(y=upper, linestyle="--", color="black")
        # plt.axhline(y=var_mean,linestyle='-',color='black')
        plt.xlabel("Posteior samples")
        plt.show()

    plt.figure("pair_wise_covariances")
    plt.title("Pair-wise covariances")
    r = np.sqrt(chi2.ppf(0.95, 2))
    for row in range(1, dim):
        for col in range(row):
            # plt.subplot(dim,dim,row*dim+col+1)
            plt.subplot(dim - 1, dim - 1, (row - 1) * (dim - 1) + col + 1)
            # plt.title(f'Variables $x_{{{row+1}}}$ and $x_{{{col+1}}}$')
            plt.plot(chain[warmup:, col], chain[warmup:, row], ".", markersize=2)
            if col == 0:
                if labels is None:
                    plt.ylabel(f"$x_{{{row+1}}}$")
                else:
                    plt.ylabel(labels[row])
            else:
                plt.yticks(ticks=[], labels=[])
            if row == dim - 1:
                if labels is None:
                    plt.xlabel(f"$x_{{{col+1}}}$")
                else:
                    plt.xlabel(labels[col])
            else:
                plt.xticks(ticks=[], labels=[])
            pairwise_cov = np.array(
                [[cov[row, row], cov[row, col]], [cov[col, row], cov[col, col]]]
            )
            L = np.linalg.cholesky(pairwise_cov)
            mu = np.array([mean[col], mean[row]]).reshape((2, 1))
            ellipse = lambda theta: mu + r * L @ np.vstack(
                (np.cos(theta), np.sin(theta))
            )
            thetas = np.linspace(0, 2 * np.pi, 361)
            points = ellipse(thetas)
            plt.plot(points[0, :], points[1, :], "k--")
    plt.show()
