"""
Utility functions for the CPR package.

This module provides helper functions for data manipulation and basic
operations required by the cointegrating polynomial regression routines.

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
"""

import numpy as np
from typing import Optional, Union


def trimr(x: np.ndarray, n1: int, n2: int) -> np.ndarray:
    """
    Return a matrix (or vector) x stripped of the specified rows.
    
    Modeled after the GAUSS trimr function.
    
    Parameters
    ----------
    x : np.ndarray
        Input matrix or vector of shape (n, k)
    n1 : int
        Number of first rows to strip
    n2 : int
        Number of last rows to strip
    
    Returns
    -------
    np.ndarray
        Trimmed array x[n1:n-n2, :]
    
    Raises
    ------
    ValueError
        If attempting to trim more rows than available
    
    Examples
    --------
    >>> x = np.array([[1], [2], [3], [4], [5]])
    >>> trimr(x, 1, 1)
    array([[2],
           [3],
           [4]])
    """
    x = np.atleast_2d(x)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    
    n = x.shape[0]
    if (n1 + n2) >= n:
        raise ValueError("Attempting to trim too much in trimr")
    
    h1 = n1
    h2 = n - n2
    return x[h1:h2, :]


def lag(x: np.ndarray, n: int = 1, v: float = 0.0) -> np.ndarray:
    """
    Create a matrix or vector of lagged values.
    
    Parameters
    ----------
    x : np.ndarray
        Input matrix or vector of shape (nobs, k)
    n : int, optional
        Order of lag, default is 1
    v : float, optional
        Initial value to fill, default is 0
    
    Returns
    -------
    np.ndarray
        Matrix (or vector) of lags with shape (nobs, k)
    
    Notes
    -----
    If n <= 0, an empty array is returned.
    
    Examples
    --------
    >>> x = np.array([[1], [2], [3], [4], [5]])
    >>> lag(x, 1)
    array([[0],
           [1],
           [2],
           [3],
           [4]])
    """
    x = np.atleast_2d(x)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    
    if n < 1:
        return np.array([]).reshape(0, x.shape[1])
    
    nobs, k = x.shape
    zt = np.ones((n, k)) * v
    z = np.vstack([zt, trimr(x, 0, n)])
    
    return z


def cumsum(x: np.ndarray, axis: int = 0) -> np.ndarray:
    """
    Cumulative sum along specified axis.
    
    Parameters
    ----------
    x : np.ndarray
        Input array
    axis : int, optional
        Axis along which to compute cumulative sum, default is 0
    
    Returns
    -------
    np.ndarray
        Cumulative sum array
    """
    return np.cumsum(x, axis=axis)


def diff(x: np.ndarray, n: int = 1, axis: int = 0) -> np.ndarray:
    """
    Calculate the n-th discrete difference along the given axis.
    
    Parameters
    ----------
    x : np.ndarray
        Input array
    n : int, optional
        The number of times values are differenced, default is 1
    axis : int, optional
        The axis along which the difference is taken, default is 0
    
    Returns
    -------
    np.ndarray
        The n-th differences
    """
    return np.diff(x, n=n, axis=axis)


def ensure_2d(x: np.ndarray) -> np.ndarray:
    """
    Ensure array is 2-dimensional.
    
    Parameters
    ----------
    x : np.ndarray
        Input array
    
    Returns
    -------
    np.ndarray
        2D array (column vector if 1D input)
    """
    x = np.asarray(x)
    if x.ndim == 1:
        return x.reshape(-1, 1)
    return x


def ensure_1d(x: np.ndarray) -> np.ndarray:
    """
    Ensure array is 1-dimensional.
    
    Parameters
    ----------
    x : np.ndarray
        Input array
    
    Returns
    -------
    np.ndarray
        1D array (flattened if 2D with single column)
    """
    x = np.asarray(x)
    if x.ndim == 2 and x.shape[1] == 1:
        return x.flatten()
    elif x.ndim == 1:
        return x
    else:
        raise ValueError(f"Cannot convert array of shape {x.shape} to 1D")


def generate_deterministics(T: int, d: int) -> Optional[np.ndarray]:
    """
    Generate deterministic components.
    
    Parameters
    ----------
    T : int
        Sample size
    d : int
        Specification:
        -1: no deterministics (returns None)
         0: intercept only
         1: intercept and linear trend
    
    Returns
    -------
    np.ndarray or None
        Deterministic components matrix of shape (T, q+1) or None
    """
    if d == -1:
        return None
    elif d == 0:
        return np.ones((T, 1))
    elif d == 1:
        const = np.ones((T, 1))
        trend = np.arange(1, T + 1).reshape(-1, 1)
        return np.hstack([const, trend])
    else:
        raise ValueError(f"d must be -1, 0, or 1, got {d}")


def ols(y: np.ndarray, X: np.ndarray) -> tuple:
    """
    Ordinary Least Squares estimation.
    
    Parameters
    ----------
    y : np.ndarray
        Dependent variable (T x 1)
    X : np.ndarray
        Regressors (T x k)
    
    Returns
    -------
    tuple
        (coefficients, residuals, fitted_values)
    """
    y = ensure_2d(y)
    X = ensure_2d(X)
    
    # Solve using least squares
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ beta
    residuals = y - fitted
    
    return beta.flatten(), residuals.flatten(), fitted.flatten()


def var_estimate(y: np.ndarray, p: int) -> tuple:
    """
    Estimate VAR(p) model using OLS.
    
    Parameters
    ----------
    y : np.ndarray
        Observations (T x s)
    p : int
        Order of the VAR
    
    Returns
    -------
    tuple
        (coefficients, residuals, aic, bic)
        - coefficients: (s x s*p) matrix [a_1, ..., a_p]
        - residuals: (T-p x s) matrix
        - aic: Akaike Information Criterion
        - bic: Bayesian Information Criterion
    
    Notes
    -----
    No deterministic variables are included in this version.
    The model is: y_t = a_1*y_{t-1} + ... + a_p*y_{t-p} + e_t
    """
    y = ensure_2d(y)
    T, s = y.shape
    
    # Generate lagged regressor matrix
    regs = np.zeros((T, s * p))
    for i in range(1, p + 1):
        regs[:, (i - 1) * s:i * s] = lag(y, i)
    
    # Cut lost observations
    y_eff = trimr(y, p, 0)
    r_eff = trimr(regs, p, 0)
    
    # Regression
    coeffs = np.linalg.solve(r_eff.T @ r_eff, r_eff.T @ y_eff)
    resids = y_eff - r_eff @ coeffs
    
    # Information criteria
    T_eff = T - p
    VCV = resids.T @ resids
    rVCV = VCV / (T_eff - p * s)
    
    # AIC
    aic = np.log(np.linalg.det(rVCV)) + (2 * p * s * s) / T_eff
    # BIC
    bic = np.log(np.linalg.det(rVCV)) + (p * s * s * np.log(T_eff)) / T_eff
    
    # Transpose coefficients to match MATLAB output format
    coeffs = coeffs.T
    
    return coeffs, resids, aic, bic
