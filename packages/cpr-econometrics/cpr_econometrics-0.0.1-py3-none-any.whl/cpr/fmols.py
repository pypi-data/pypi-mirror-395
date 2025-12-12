"""
Fully Modified OLS (FM-OLS) Estimator for Cointegrating Polynomial Regressions.

This module implements the FM-OLS estimator developed by Wagner and Hong (2016)
for cointegrating polynomial regressions (CPRs).

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com

References
----------
Wagner, M., & Hong, S. H. (2016). Cointegrating polynomial regressions: 
    Fully modified OLS estimation and inference. Econometric Theory, 32(6), 1289-1315.

Phillips, P. C. B., & Hansen, B. E. (1990). Statistical inference in 
    instrumental variables regression with I(1) processes. 
    Review of Economic Studies, 57(1), 99-125.
"""

import numpy as np
from typing import Union, Optional, Dict, Any, List
from dataclasses import dataclass, field
from .poly_terms import gen_var_poly_terms, PolyTermsResult
from .lr_variance import (
    lr_var, bandwidth_andrews, bandwidth_nw, andmon_hac92, compute_lr_variance
)
from .utils import ensure_2d, diff, generate_deterministics


@dataclass
class FMOLSResult:
    """
    Results container for FM-OLS estimation.
    
    Attributes
    ----------
    beta_fm : np.ndarray
        FM-OLS coefficients for polynomial terms
    delta_fm : np.ndarray
        FM-OLS coefficients for deterministic terms
    gamma_fm : np.ndarray
        FM-OLS coefficients for stationary regressors
    t_beta : np.ndarray
        t-statistics for beta coefficients
    t_delta : np.ndarray
        t-statistics for delta coefficients
    t_gamma : np.ndarray
        t-statistics for gamma coefficients
    std_beta : np.ndarray
        Standard errors for beta coefficients
    std_delta : np.ndarray
        Standard errors for delta coefficients
    std_gamma : np.ndarray
        Standard errors for gamma coefficients
    u_plus : np.ndarray
        FM-OLS residuals
    Omega_udotv : float
        Conditional long-run variance estimate
    varmat : np.ndarray
        FM-OLS variance-covariance matrix
    varmat0 : np.ndarray
        HAC-type VCV matrix for stationary regressors
    beta_ols : np.ndarray
        OLS coefficients for polynomial terms
    delta_ols : np.ndarray
        OLS coefficients for deterministic terms
    gamma_ols : np.ndarray
        OLS coefficients for stationary regressors
    u_ols : np.ndarray
        OLS residuals
    fitted : np.ndarray
        Fitted values
    y_plus : np.ndarray
        Modified dependent variable
    """
    beta_fm: np.ndarray
    delta_fm: np.ndarray
    gamma_fm: np.ndarray
    t_beta: np.ndarray
    t_delta: np.ndarray
    t_gamma: np.ndarray
    std_beta: np.ndarray
    std_delta: np.ndarray
    std_gamma: np.ndarray
    u_plus: np.ndarray
    Omega_udotv: float
    Omega_udotv1: float
    varmat: np.ndarray
    varmat1: np.ndarray
    varmat0: Optional[np.ndarray]
    beta_ols: np.ndarray
    delta_ols: np.ndarray
    gamma_ols: np.ndarray
    u_ols: np.ndarray
    fitted: np.ndarray
    y_plus: np.ndarray
    FInv: np.ndarray
    Astar: np.ndarray
    Lambda0: np.ndarray
    varmatOLS: np.ndarray
    T: int
    m: int
    kw: int
    kd: int


def fm_cpr(y: np.ndarray, 
           x: np.ndarray, 
           orders: Union[int, List[int], List[np.ndarray]],
           w: Optional[np.ndarray] = None,
           deter: Optional[np.ndarray] = None,
           kern: str = 'ba',
           band: Union[str, float] = 'NW',
           deme: int = 0) -> FMOLSResult:
    """
    Fully Modified OLS estimator for Cointegrating Polynomial Regressions.
    
    Estimates the model:
        y = gamma*w + delta*deter + beta*X + u
    
    where X contains powers of the integrated regressors x.
    
    Parameters
    ----------
    y : np.ndarray
        Dependent variable, shape (T,) or (T, 1)
    x : np.ndarray
        Integrated regressors, shape (T, m)
    orders : int, list of int, or list of arrays
        Polynomial order specification:
        - int: maximum power for all regressors
        - list of int: maximum power for each regressor
        - list of arrays: specific powers for each regressor
    w : np.ndarray, optional
        Stationary regressors, shape (T, s), default is None
    deter : np.ndarray or int, optional
        Deterministic variables:
        - np.ndarray: Pre-built deterministic matrix, shape (T, q+1)
        - int: Specification code (-1: none, 0: intercept, 1: intercept + trend)
        - None: No deterministic components
    kern : str, optional
        Kernel function for long-run variance estimation:
        'tr' (truncated), 'ba' (Bartlett), 'pa' (Parzen),
        'bo' (Bohman), 'da' (Daniell), 'qs' (Quadratic Spectral).
        Default is 'ba'.
    band : str or float, optional
        Bandwidth: 'And91' (Andrews), 'NW' (Newey-West), 'AM92' (Andrews-Monahan),
        or a numeric value. Default is 'NW'.
    deme : int, optional
        Demeaning of residuals in LR-variance computation (1: yes, 0: no).
        Default is 0.
    
    Returns
    -------
    FMOLSResult
        Dataclass containing all estimation results.
    
    Notes
    -----
    The FM-OLS estimator corrects for second-order bias in OLS estimation
    of cointegrating regressions, providing asymptotically valid inference.
    
    t-statistics for stationary regressors are based on HAC covariance estimation.
    
    Examples
    --------
    >>> import numpy as np
    >>> from cpr import fm_cpr
    >>> # Generate data
    >>> T = 200
    >>> x = np.cumsum(np.random.randn(T))  # I(1) regressor
    >>> y = 1 + 0.5*x + 0.2*x**2 + np.random.randn(T)  # Quadratic CPR
    >>> # Estimate
    >>> deter = np.column_stack([np.ones(T), np.arange(1, T+1)])
    >>> result = fm_cpr(y, x.reshape(-1, 1), orders=2, deter=deter)
    >>> print(result.beta_fm)
    """
    # Ensure proper dimensions
    y = ensure_2d(y).flatten()
    x = ensure_2d(x)
    T, m = x.shape
    
    # Generate polynomial terms and correction factors
    poly_result = gen_var_poly_terms(x, orders, stochastic=True)
    X = poly_result.X
    P = poly_result.P
    Mstar = poly_result.Mstar.copy()
    
    # First differences of x
    v = diff(x, n=1, axis=0)
    
    # Handle stationary regressors
    if w is not None:
        w = ensure_2d(w)
        kw = w.shape[1]
    else:
        w = np.zeros((T, 0))
        kw = 0
    
    # Handle deterministic components
    if deter is not None:
        if isinstance(deter, (int, np.integer)):
            # Integer specification: -1=none, 0=intercept, 1=intercept+trend
            deter = generate_deterministics(T, int(deter))
        
        if deter is not None:
            deter = ensure_2d(deter)
            kd = deter.shape[1]
        else:
            deter = np.zeros((T, 0))
            kd = 0
    else:
        deter = np.zeros((T, 0))
        kd = 0
    
    # Build regressor matrices
    J = np.hstack([deter, X]) if kd > 0 else X
    Z = np.hstack([w, J]) if kw > 0 else J
    
    # Full (Z'Z)^-1 matrix
    FInv = np.linalg.inv(Z.T @ Z)
    
    # Trimmed versions (from observation 2 onwards)
    Z_ = Z[1:, :]
    w_ = w[1:, :] if kw > 0 else w
    
    # OLS Regression
    iZZ = np.linalg.inv(Z_.T @ Z_)
    b_ols = np.linalg.lstsq(Z, y, rcond=None)[0]
    u_ols = y - Z @ b_ols
    
    # For stationary regressors
    iww = np.linalg.inv(w_.T @ w_) if kw > 0 else None
    
    # FM Estimation (Wagner & Hong 2016)
    # (1) Constructing LR variance estimators
    eta = np.column_stack([u_ols[1:], v])
    
    if band == 'And91':
        bandw = bandwidth_andrews(eta, kern)
        Lr, Dr, Sr = lr_var(eta, kern, bandw, deme)
    elif band == 'NW':
        bandw = bandwidth_nw(eta, kern, 0, None)
        Lr, Dr, Sr = lr_var(eta, kern, bandw, deme)
    elif band == 'AM92':
        Lr, Dr, Sr = andmon_hac92(eta, kern, 1, 1, deme)
    else:
        bandw = float(band)
        Lr, Dr, Sr = lr_var(eta, kern, bandw, deme)
    
    # Conditional long-run variance
    Omega_udotv = Lr[0, 0] - Lr[0, 1:] @ np.linalg.inv(Lr[1:, 1:]) @ Lr[1:, 0]
    Lr_vvvu = np.linalg.inv(Lr[1:, 1:]) @ Lr[1:, 0]
    
    # Lambda0 computation
    Lambda0 = Dr[1:, 0] - Dr[1:, 1:] @ Lr_vvvu
    
    # (2) Constructing correction terms
    for i in range(m):
        ind_start = int(P[i])
        ind_end = int(P[i + 1])
        Mstar[ind_start:ind_end] = Lambda0[i] * Mstar[ind_start:ind_end]
    
    Astar = np.zeros(Z_.shape[1])
    if kw > 0:
        Astar[:kw] = (1/T) * w_[:-1, :].T @ u_ols[1:-1] - (1/T) * w_[:-1, :].T @ v[:-1, :] @ Lr_vvvu
    Astar[-(len(Mstar)):] = Mstar
    
    # (3) FM Estimator
    yplus = y[1:] - v @ Lr_vvvu
    bplus = iZZ @ (Z_.T @ yplus - Astar)
    
    # Extract coefficients
    beta_fm = bplus[kw + kd:]
    delta_fm = bplus[kw:kw + kd] if kd > 0 else np.array([])
    gamma_fm = bplus[:kw] if kw > 0 else np.array([])
    
    beta_ols = b_ols[kw + kd:]
    delta_ols = b_ols[kw:kw + kd] if kd > 0 else np.array([])
    gamma_ols = b_ols[:kw] if kw > 0 else np.array([])
    
    # FM-OLS residuals
    u_plus = yplus - Z_ @ bplus
    
    # Fitted values
    fitted = Z @ bplus
    
    # Inference for stationary regressors (HAC)
    if kw > 0:
        S = w_ * u_plus.reshape(-1, 1)
        if band == 'AM92':
            SLr, _, _ = andmon_hac92(S, kern, 1, 1, deme)
        elif band == 'And91':
            bandw_s = bandwidth_andrews(S, kern)
            SLr, _, _ = lr_var(S, kern, bandw_s, deme)
        elif band == 'NW':
            bandw_s = bandwidth_nw(S, kern, 0, None)
            SLr, _, _ = lr_var(S, kern, bandw_s, deme)
        else:
            SLr, _, _ = lr_var(S, kern, float(band), deme)
        
        varmat0 = T * iww @ SLr @ iww
        tvm = np.sqrt(np.diag(varmat0))
        std_gamma = tvm[:kw]
        t_gamma = gamma_fm / std_gamma
    else:
        varmat0 = None
        std_gamma = np.array([])
        t_gamma = np.array([])
    
    # Recompute bandwidth for FM residuals
    if band == 'And91':
        bandb = bandwidth_andrews(u_plus.reshape(-1, 1), kern)
        Omega_udotv1, _, _ = lr_var(u_plus.reshape(-1, 1), kern, bandb, deme)
    elif band == 'NW':
        bandb = bandwidth_nw(u_plus.reshape(-1, 1), kern, 0, None)
        Omega_udotv1, _, _ = lr_var(u_plus.reshape(-1, 1), kern, bandb, deme)
    elif band == 'AM92':
        Omega_udotv1, _, _ = andmon_hac92(u_plus.reshape(-1, 1), kern, 1, 1, deme)
    else:
        Omega_udotv1, _, _ = lr_var(u_plus.reshape(-1, 1), kern, float(band), deme)
    
    Omega_udotv1 = Omega_udotv1[0, 0]
    
    # Variance-covariance matrix for beta and delta
    J_ = J[1:, :]
    varmat = Omega_udotv * np.linalg.inv(J_.T @ J_)
    varmat1 = Omega_udotv1 * np.linalg.inv(J_.T @ J_)
    
    tvm1 = np.sqrt(np.diag(varmat))
    std_delta = tvm1[:kd] if kd > 0 else np.array([])
    std_beta = tvm1[kd:]
    t_delta = delta_fm / std_delta if kd > 0 else np.array([])
    t_beta = beta_fm / std_beta
    
    # OLS inference (incorrect for cointegration but included for comparison)
    S_ols = Z * u_ols.reshape(-1, 1)
    if band == 'AM92':
        SLr_ols, _, _ = andmon_hac92(S_ols, kern, 1, 1, deme)
    elif band == 'And91':
        bandw_ols = bandwidth_andrews(S_ols, kern)
        SLr_ols, _, _ = lr_var(S_ols, kern, bandw_ols, deme)
    elif band == 'NW':
        bandw_ols = bandwidth_nw(S_ols, kern, 0, None)
        SLr_ols, _, _ = lr_var(S_ols, kern, bandw_ols, deme)
    else:
        SLr_ols, _, _ = lr_var(S_ols, kern, float(band), deme)
    
    varmatOLS = T * FInv @ SLr_ols @ FInv
    
    return FMOLSResult(
        beta_fm=beta_fm,
        delta_fm=delta_fm,
        gamma_fm=gamma_fm,
        t_beta=t_beta,
        t_delta=t_delta,
        t_gamma=t_gamma,
        std_beta=std_beta,
        std_delta=std_delta,
        std_gamma=std_gamma,
        u_plus=u_plus,
        Omega_udotv=Omega_udotv,
        Omega_udotv1=Omega_udotv1,
        varmat=varmat,
        varmat1=varmat1,
        varmat0=varmat0,
        beta_ols=beta_ols,
        delta_ols=delta_ols,
        gamma_ols=gamma_ols,
        u_ols=u_ols,
        fitted=fitted,
        y_plus=yplus,
        FInv=FInv,
        Astar=Astar,
        Lambda0=Lambda0,
        varmatOLS=varmatOLS,
        T=T,
        m=m,
        kw=kw,
        kd=kd
    )
