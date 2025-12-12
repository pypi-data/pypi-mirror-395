"""
Long-run variance estimation for the CPR package.

This module provides kernel-based long-run variance estimation routines,
including automatic bandwidth selection methods following Andrews (1991)
and Newey-West (1994).

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com

References
----------
Andrews, D. W. K. (1991). Heteroskedasticity and autocorrelation consistent
    covariance matrix estimation. Econometrica, 59(3), 817-858.
    
Andrews, D. W. K., & Monahan, J. C. (1992). An improved heteroskedasticity
    and autocorrelation consistent covariance matrix estimator.
    Econometrica, 60(4), 953-966.
    
Newey, W. K., & West, K. D. (1994). Automatic lag selection in covariance
    matrix estimation. Review of Economic Studies, 61(4), 631-653.
"""

import numpy as np
from typing import Tuple, Optional, Union
from .utils import ensure_2d, var_estimate


def lr_weights(T: int, kern: str, band: float) -> Tuple[np.ndarray, int]:
    """
    Compute kernel weights for long-run variance estimation.
    
    Parameters
    ----------
    T : int
        Time series dimension of data
    kern : str
        Kernel function specification:
        - 'tr': Truncated (uniform)
        - 'ba': Bartlett (triangle)
        - 'pa': Parzen
        - 'bo': Bohman
        - 'da': Daniell (sinc)
        - 'qs': Quadratic Spectral
    band : float
        Bandwidth parameter
    
    Returns
    -------
    Tuple[np.ndarray, int]
        - w: Vector of size (T-1,) containing the weights
        - upper: Index to largest non-zero entry in w
    
    Notes
    -----
    Only weights for positive arguments are computed since kernels are symmetric.
    """
    w = np.zeros(T - 1)
    M = band
    
    if kern == 'tr':  # Truncated
        upper = min(int(M), T - 1)
        w[:upper] = 1.0
        
    elif kern == 'ba':  # Bartlett
        upper = int(np.ceil(M)) - 1
        for j in range(1, upper + 1):
            w[j - 1] = 1.0 - j / M
            
    elif kern == 'pa':  # Parzen
        half_M = int(np.floor(M / 2))
        for j in range(1, half_M + 1):
            jj = j / M
            w[j - 1] = 1.0 - 6 * jj**2 + 6 * jj**3
        for j in range(half_M + 1, int(M) + 1):
            if j <= T - 1:
                jj = j / M
                w[j - 1] = 2 * (1 - jj)**3
        upper = int(np.ceil(M)) - 1
        
    elif kern == 'bo':  # Bohman
        upper = int(np.ceil(M)) - 1
        for j in range(1, upper + 1):
            jj = j / M
            w[j - 1] = (1 - jj) * np.cos(np.pi * jj) + np.sin(np.pi * jj) / np.pi
            
    elif kern == 'da':  # Daniell
        upper = T - 1
        for j in range(1, T):
            w[j - 1] = np.sin(np.pi * j / M) / (np.pi * j / M)
            
    elif kern == 'qs':  # Quadratic Spectral
        upper = T - 1
        sc = (6 * np.pi) / 5
        for j in range(1, T):
            jj = j / M
            w[j - 1] = 25 / (12 * np.pi**2 * jj**2) * (np.sin(sc * jj) / (sc * jj) - np.cos(sc * jj))
    else:
        raise ValueError(f"Unknown kernel: {kern}. Use 'tr', 'ba', 'pa', 'bo', 'da', or 'qs'")
    
    return w, min(upper, T - 1)


def lr_var(u: np.ndarray, kern: str, band: float, deme: int = 0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute long-run variance, one-sided long-run variance, and variance.
    
    Parameters
    ----------
    u : np.ndarray
        Residual matrix of shape (T, m)
    kern : str
        Kernel function ('tr', 'ba', 'pa', 'bo', 'da', 'qs')
    band : float
        Bandwidth parameter
    deme : int, optional
        Demeaning of residuals (1: yes, 0: no), default is 0
    
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        - Omega: Long-run variance matrix (m x m)
        - Delta: One-sided long-run variance matrix (m x m)
        - Sigma: Variance matrix (m x m)
    """
    u = ensure_2d(u)
    T, m = u.shape
    
    # Demeaning residuals
    if deme == 1:
        u = u - np.mean(u, axis=0)
    
    # Get weights
    w, j_max = lr_weights(T, kern, band)
    
    # Initialize
    Omega = np.zeros((m, m))
    Delta = np.zeros((m, m))
    
    # Variance (scaling by 1/T)
    Sigma = (u.T @ u) / T
    
    # Compute autocovariances
    for j in range(1, j_max + 1):
        # Lag j autocovariance
        T1 = u[j:, :].T @ u[:T - j, :] / T
        T2 = u[:T - j, :].T @ u[j:, :] / T
        
        # Scale with weight function
        T_Omega = w[j - 1] * (T1 + T2)
        T_Delta = w[j - 1] * T2
        
        # Sum
        Omega += T_Omega
        Delta += T_Delta
    
    # Add contemporaneous variance
    Omega += Sigma
    Delta += Sigma
    
    return Omega, Delta, Sigma


def bandwidth_nw(v: np.ndarray, kern: str, inter: int = 0, 
                  weights: Optional[np.ndarray] = None) -> float:
    """
    Compute Newey-West (1994) automatic bandwidth.
    
    Parameters
    ----------
    v : np.ndarray
        Data matrix of shape (T, m)
    kern : str
        Kernel function ('ba', 'pa', 'qs')
    inter : int, optional
        Intercept indicator (0: no intercept, 1: intercept), default is 0
    weights : np.ndarray, optional
        Weight vector of shape (m,), default is ones (or [0, 1, ..., 1] with intercept)
    
    Returns
    -------
    float
        Selected bandwidth
    
    References
    ----------
    Newey, W. K., & West, K. D. (1994). Automatic lag selection in covariance
        matrix estimation. Review of Economic Studies, 61(4), 631-653.
    """
    v = ensure_2d(v)
    T, m = v.shape
    
    # Set default weights
    if weights is None:
        weights = np.ones(m)
        if inter == 1:
            weights[0] = 0
    
    # Select lag truncation parameter n
    if kern == 'ba':
        npower = 2 / 9
    elif kern == 'pa':
        npower = 4 / 25
    elif kern == 'qs':
        npower = 2 / 25
    else:
        raise ValueError(f"Kernel {kern} not supported for NW bandwidth. Use 'ba', 'pa', or 'qs'")
    
    n = int(np.floor(4 * (T / 100)**npower))
    
    # Compute weighted series
    vmatw = weights @ v.T  # Shape: (T,)
    
    # Compute sigma_j for j = 0, 1, ..., n
    sigma = np.zeros(n + 1)
    for j in range(n + 1):
        sigma[j] = np.sum(vmatw[j:T] * vmatw[:T - j]) / T
    
    # Compute s^(q) for q = 0, 1, 2
    s0 = sigma[0] + 2 * np.sum(sigma[1:])
    s1 = 2 * np.sum(np.arange(1, n + 1) * sigma[1:])
    s2 = 2 * np.sum(np.arange(1, n + 1)**2 * sigma[1:])
    
    # Compute gamma and bandwidth
    if kern == 'ba':
        q = 1
    else:
        q = 2
    Tpower = 1 / (2 * q + 1)
    
    if kern == 'ba':
        gamma = 1.1447 * ((s1 / s0)**2)**Tpower
    elif kern == 'pa':
        gamma = 2.6614 * ((s2 / s0)**2)**Tpower
    elif kern == 'qs':
        gamma = 1.3221 * ((s2 / s0)**2)**Tpower
    
    bandw = gamma * T**Tpower
    
    return bandw


def bandwidth_andrews(v: np.ndarray, kern: str) -> float:
    """
    Compute Andrews (1991) automatic bandwidth.
    
    Uses AR(1) individual version for bandwidth selection.
    
    Parameters
    ----------
    v : np.ndarray
        Data matrix of shape (T, dimv)
    kern : str
        Kernel function ('tr', 'ba', 'pa', 'th', 'qs')
    
    Returns
    -------
    float
        Selected bandwidth
    
    References
    ----------
    Andrews, D. W. K. (1991). Heteroskedasticity and autocorrelation consistent
        covariance matrix estimation. Econometrica, 59(3), 817-858.
    """
    v = ensure_2d(v)
    T, dimv = v.shape
    
    rhovec = np.zeros(dimv)
    sigma2vec = np.zeros(dimv)
    
    # Compute rho and sigma^2 for each coordinate
    for j in range(dimv):
        y = v[1:, j]
        x = v[:-1, j]
        # AR(1) coefficient
        rhovec[j] = np.sum(x * y) / np.sum(x * x) if np.sum(x * x) > 0 else 0
        # Residual variance
        resid = y - x * rhovec[j]
        sigma2vec[j] = np.sum(resid**2) / T
    
    # Compute alpha(2): Andrews (1991), eq. (6.4)
    denom = np.sum(sigma2vec**2 / (1 - rhovec)**4)
    numer2 = np.sum(4 * rhovec**2 * sigma2vec**2 / (1 - rhovec)**8)
    a2 = numer2 / denom if denom > 0 else 0
    
    # Compute alpha(1): Andrews (1991), eq. (6.4)
    numer1 = np.sum(4 * rhovec**2 * sigma2vec**2 / ((1 - rhovec)**6 * (1 + rhovec)**2))
    a1 = numer1 / denom if denom > 0 else 0
    
    # Compute bandwidth: Andrews (1991), eq. (6.2)
    if kern == 'tr':
        bandwidth = 0.6611 * (a2 * T)**(1/5)
    elif kern == 'ba':
        bandwidth = 1.1447 * (a1 * T)**(1/3)
    elif kern == 'pa':
        bandwidth = 2.6614 * (a2 * T)**(1/5)
    elif kern == 'th':  # Tukey-Hanning
        bandwidth = 1.7462 * (a2 * T)**(1/5)
    elif kern == 'qs':
        bandwidth = 1.3221 * (a2 * T)**(1/5)
    else:
        raise ValueError(f"Unknown kernel: {kern}")
    
    return bandwidth


def andmon_stab(A: np.ndarray) -> np.ndarray:
    """
    Compute eigenvalue stabilized LS estimates for A(1).
    
    Stabilizes eigenvalues to be at most 0.97 in absolute value.
    
    Parameters
    ----------
    A : np.ndarray
        Estimated AR polynomial at z=1
    
    Returns
    -------
    np.ndarray
        Modified version with eigenvalues <= 0.97 in absolute value
    
    Notes
    -----
    This follows Andrews & Monahan (1992) for AR(1) pre-whitening.
    """
    # Eigenvalue decomposition of A @ A.T
    eig_vals_left, B = np.linalg.eig(A @ A.T)
    # Eigenvalue decomposition of A.T @ A
    eig_vals_right, C = np.linalg.eig(A.T @ A)
    
    # Diagonal elements
    dD = np.diag(B.T @ A @ C)
    
    # Stabilize eigenvalues
    D = np.diag(np.where(np.abs(dD) > 0.97, 0.97 * np.sign(dD), dD))
    
    # Reconstruct
    AMstab = B @ D @ C.T
    
    return np.real(AMstab)


def andmon_hac92(u: np.ndarray, kern: str, pw_lag: int = 1, 
                  stab: int = 1, deme: int = 0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute VAR pre-whitened long-run variance estimates.
    
    Combines VAR pre-whitening with Andrews (1991) long-run variance estimation.
    
    Parameters
    ----------
    u : np.ndarray
        Residual matrix of shape (T, m)
    kern : str
        Kernel function ('tr', 'ba', 'pa', 'th', 'qs')
    pw_lag : int, optional
        Pre-whitening lag, default is 1
    stab : int, optional
        Eigenvalue stabilization (0: no, 1: yes), default is 1
    deme : int, optional
        Demeaning of residuals (0: no, 1: yes), default is 0
    
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        - Omega: Long-run variance matrix
        - Delta: One-sided long-run variance matrix
        - Sigma: Variance matrix
    
    References
    ----------
    Andrews, D. W. K., & Monahan, J. C. (1992). An improved heteroskedasticity
        and autocorrelation consistent covariance matrix estimator.
        Econometrica, 60(4), 953-966.
    """
    u = ensure_2d(u)
    T, m = u.shape
    
    # Demeaning
    if deme == 1:
        u = u - np.mean(u, axis=0)
    
    # VAR pre-whitening
    coeffs, resids, _, _ = var_estimate(u, pw_lag)
    
    # Compute coefficient polynomial evaluated at 1
    if pw_lag == 1:
        a1 = np.eye(m) - coeffs
    else:
        # For higher order VAR
        coeff_ext = np.hstack([np.eye(m), coeffs])
        mult1 = np.kron(-np.ones((pw_lag, 1)), np.eye(m))
        multmat = np.vstack([np.eye(m), mult1])
        a1 = coeff_ext @ multmat
    
    inva1 = np.linalg.inv(a1)
    
    # Eigenvalue stabilization
    if stab == 1:
        inva1 = andmon_stab(inva1)
    
    # Andrews (1991) lag length computation
    band_pw = bandwidth_andrews(resids, kern)
    
    # Variance (computed directly from original residuals)
    Sigma = (u.T @ u) / T
    
    # Long-run variance for pre-whitened residuals
    Omega_pw, Delta_pw, Sigma_pw = lr_var(resids, kern, band_pw, deme)
    
    # "Re-coloring" of long-run variance
    Omega = inva1 @ Omega_pw @ inva1.T
    
    # One-sided long-run covariance matrix
    Lambda_pw = Delta_pw - Sigma_pw
    Delta = Sigma + inva1 @ Lambda_pw @ inva1.T + inva1 @ coeffs @ Sigma
    
    return Omega, Delta, Sigma


def compute_lr_variance(u: np.ndarray, kern: str, band: Union[str, float], 
                        deme: int = 0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Unified interface for long-run variance estimation.
    
    Parameters
    ----------
    u : np.ndarray
        Residual matrix of shape (T, m)
    kern : str
        Kernel function ('tr', 'ba', 'pa', 'bo', 'da', 'qs')
    band : str or float
        Bandwidth: 'And91', 'NW', 'AM92', or numeric value
    deme : int, optional
        Demeaning (0: no, 1: yes), default is 0
    
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        - Omega: Long-run variance matrix
        - Delta: One-sided long-run variance matrix  
        - Sigma: Variance matrix
    """
    u = ensure_2d(u)
    
    if band == 'And91':
        bandw = bandwidth_andrews(u, kern)
        return lr_var(u, kern, bandw, deme)
    elif band == 'NW':
        bandw = bandwidth_nw(u, kern, 0, None)
        return lr_var(u, kern, bandw, deme)
    elif band == 'AM92':
        return andmon_hac92(u, kern, 1, 1, deme)
    else:
        bandw = float(band)
        return lr_var(u, kern, bandw, deme)
