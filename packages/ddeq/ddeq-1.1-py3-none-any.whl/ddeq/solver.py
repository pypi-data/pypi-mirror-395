#! /usr/bin/env python
# coding: utf-8

import numpy as np

from scipy.linalg import LinAlgError


def compute_forward_difference(j, x, f0, vecfunc, b, EPS):
    temp = x[j]

    h = EPS * abs(temp)
    if h == 0.0:
        h = EPS

    # Trick to reduce finite precision error (Press et al.).
    x[j] = temp + h
    h = x[j] - temp

    f = vecfunc(x, b)
    x[j] = temp

    # Forward difference formula.
    return (f - f0) / h



def forward_jacobian(x, vecfunc, b):
    """\
    Computes forward-difference approximation to Jacobian. On input,
    x[1..n] is the point at which the Jacobian is to be evaluated,
    fvec[1..n] is the vector of function values at the point, and
    vecfunc(n,x,f) is a user-supplied routine that returns the vector
    of functions at x. On output, df[1..n][1..n] is the Jacobian array.
    """
    EPS = 1.0e-4 # approximated square root of the machine precision.

    if b is None:
        b = {}

    f0 = vecfunc(x, b)
    df = np.zeros((f0.size, x.size))

    for j in range(x.size):
        xc = x.copy()
        df[:,j] = compute_forward_difference(j, xc, f0, vecfunc, b, EPS)

    return df


def compute_forward_difference_to_b(key, x, f0, vecfunc, b, EPS):
    temp = b[key]

    h = EPS * abs(temp)
    if h == 0.0:
        h = EPS

    # Trick to reduce finite precision error (Press et al.).
    b[key] = temp + h
    h = b[key] - temp

    f = vecfunc(x, b)
    b[key] = temp

    # Forward difference formula.
    return (f - f0) / h


def forward_jacobian_to_b(x, vecfunc, b, keys):
    """
    Compute sensitivity of forward model (vecfunc) to parameter vector b.
    """
    EPS = 1.0e-4 # approximated square root of the machine precision.

    f0 = vecfunc(x, b)
    df = np.zeros((f0.size, len(keys) ))

    for j,key in enumerate(keys):
        df[:,j] = compute_forward_difference_to_b(key, x, f0, vecfunc, b, EPS)

    return df




def gain_matrix(K, S_eps, S_a=None):
    """\
    Calculate gain matrix.
    """
    # m measurements, n state vector elements
    m,n = K.shape

    if np.size(S_eps) == m: # vector
        K = np.asarray(K)
        S_eps = np.asarray(S_eps)

        w = 1.0 / S_eps
        W = w[:,np.newaxis] * K

        #       inv(K.T @ W + inv(S_a)) @ W
        if S_a is None:
            G = np.dot(np.inv(np.dot(K.T, W)), W.T)
        else:
            S_a = np.asarray(S_a)
            G = np.dot(np.inv(np.dot(K.T, W) + np.inv(S_a)), W.T)

    else:
        S_eps_I = S_eps.I
        G = (K.T * S_eps_I * K + S_a.I).I * K.T * S_eps_I

    return G


def linear_least_square(x0,y,f, b):
    """\
    Linear least square.
    """
    K = forward_jacobian(x0, f, b)
    return np.dot(np.dot(np.inv(np.dot(K.T, K)), K.T), y)



def calculate_chi2(x, y, f, Se, Sa, xa, b=None):
    try:
        Se = inv(Se)
        Sa = inv(Sa)
    except ValueError:
        return np.nan

    r = y - f(x,b)
    ra = x - xa

    return np.dot(r, np.dot(Se, r)) + np.dot(ra, np.dot(Sa, ra))




def gauss_newton(x0, y, f,  Se=np.nan, Sa=np.nan, xa=np.nan, fprime=None,
                 b=None, Kb_keys=None, max_iters=100, no_error=None):
    """\
    Find optimal state vector x using Gauss-Newton method.
    """
    # make sure everyting is double precision float
    x0 = np.array(x0, dtype='f8')
    y = np.array(y, dtype='f8')

    if no_error is None:
        no_error = np.any(np.isnan(Se))

    no_prior = np.any(np.isnan(xa)) or np.any(np.isnan(Sa))

    if fprime is None:
        fprime = forward_jacobian

    if no_error:
        Se = np.nan
        Se_inv = 1.0
    else:
        if np.ndim(Se) == 1:
            Se_inv = 1.0 / Se
        elif np.ndim(Se) == 0:
            Se_inv = 1.0 / np.full(np.shape(y), Se)
        else:
            Se_inv = inv(Se)


    if no_prior:
        Sa_inv = 0.0
    else:
        Sa_inv = np.linalg.inv(Sa)

    xi = x0.copy()

    for i in range(max_iters):

        Fi = f(xi, b)

        if np.any(np.isnan(Fi)):
            return np.full(x0.shape, np.nan), {
                'n_iter':  i+1,
                'S':       np.nan,
                'K':       np.nan,
                'Kb':      np.nan,
                'success': False,
                'msg':    'forward model returns nan'
            }

        K = fprime(xi, f, b)

        if np.any(np.isnan(K)):
            return xi, {
                'n_iter': i+1,
                'S':      np.nan,
                'K':      K,
                'success': False,
                'msg':    'nans in jacobian'
            }

        if np.ndim(Se) == 1:
            # K.T @ inv(Se) @ K + inv(Sa)
            S = np.dot(K.T, np.dot(np.diag(Se_inv), K)) + Sa_inv
            a = np.dot(K.T, Se_inv * (y - Fi))
        else:
            S = np.dot(K.T, np.dot(Se_inv, K)) + Sa_inv
            a = np.dot(K.T, np.dot(Se_inv, (y - Fi)))

        if no_prior:
            a2 = 0.0
        else:
            a2 = np.dot(Sa_inv, xi - xa)


        if np.isnan(S).sum() > 0:
            return np.full(x0.shape, np.nan), {
                'n_iter': i+1,
                'S':      np.nan,
                'K':      K,
                'success': False,
                'msg':    'nans in matrix S'
            }
        try:
            S_inv = np.linalg.inv(S)
        except LinAlgError:
            print('LinAlgError on inv(S)')
            return np.full(x0.shape, np.nan), {
                'n_iter': i+1,
                'S':      np.nan,
                'K':      K,
                'success': False,
                'msg':    'LinAlgError'
            }
        x = xi + np.dot(S_inv, a - a2) # TODO: SVD option

        if no_error:
            if np.dot(x - xi, x - xi) < x.size * 1e-8: # TODO: allow setting thresholds
                break
        else:
            if np.dot(x - xi, np.dot(S, x - xi)) < x.size:
                break

        xi = x.copy()

    else:
        return x, {
            'n_iter': i+1,
            'S':      np.nan,
            'K':      K,
            'success': False,
            'msg':    'reach maximum number of iterations'
        }


    # calculate error from chi2 = n
    if no_error:
        F = f(x, b)
        Se = np.sum((F - y)**2) / F.size
        S = np.dot(K.T, K) / Se

    if Kb_keys is not None:
        Kb = forward_jacobian_to_b(x, f, b, Kb_keys)
    else:
        Kb = np.nan

    return x, {
        'n_iter': i+1,
        'S':      np.linalg.inv(S),
        'K':      K,
        'Kb':     Kb,
        'success': True,
        'msg':    'everything seems to have worked fine'
    }




if __name__ == '__main__':
    pass
