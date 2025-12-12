"""
Cointegration and Non-cointegration Tests for CPRs.

This module implements residual-based tests for cointegrating polynomial 
regressions (CPRs):
- CT test: KPSS-Shin type test with H0: cointegration
- PU test: Phillips-Ouliaris type test with H0: no cointegration

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com

References
----------
Wagner, M. (2023). Residual-based cointegration and non-cointegration tests
    for cointegrating polynomial regressions. Empirical Economics, 65, 1-31.
    
Shin, Y. (1994). A residual-based test for the null of cointegration against
    the alternative of no cointegration. Econometric Theory, 10(1), 91-115.
    
Phillips, P. C. B., & Ouliaris, S. (1990). Asymptotic properties of residual
    based tests for cointegration. Econometrica, 58(1), 165-193.
"""

import numpy as np
from typing import Optional, Union, List, Tuple
from dataclasses import dataclass
from .critical_values import (
    get_ct_critical_value, get_pu_critical_value, 
    get_all_critical_values, get_p_value
)
from .poly_terms import gen_var_poly_terms
from .lr_variance import (
    lr_var, bandwidth_andrews, bandwidth_nw, andmon_hac92
)
from .utils import ensure_2d, lag, trimr, generate_deterministics


@dataclass
class CTTestResult:
    """
    Results container for CT (cointegration) test.
    
    Attributes
    ----------
    statistic : float
        CT test statistic
    critical_values : dict
        Critical values at standard significance levels
    p_value : float
        Approximate p-value (interpolated)
    reject : dict
        Rejection decisions at standard significance levels
    d : int
        Deterministic specification used
    m : int
        Number of integrated regressors
    p : int
        Highest power of the regressor entering with powers
    null_hypothesis : str
        Description of the null hypothesis
    """
    statistic: float
    critical_values: dict
    p_value: float
    reject: dict
    d: int
    m: int
    p: int
    null_hypothesis: str = "Cointegration (stationary residuals)"
    
    def __repr__(self) -> str:
        return self._format_output()
    
    def _format_output(self) -> str:
        """Format output for publication-quality display."""
        lines = [
            "",
            "=" * 70,
            "CT Test for Cointegration (KPSS-Shin type)",
            "=" * 70,
            f"H0: {self.null_hypothesis}",
            f"Deterministics: {self._det_description()}",
            f"Integrated regressors (m): {self.m}",
            f"Highest power (p): {self.p}",
            "-" * 70,
            f"Test Statistic: {self.statistic:.6f}",
            f"Approximate p-value: {self.p_value:.4f}",
            "-" * 70,
            "Critical Values and Decisions:",
        ]
        
        for alpha in [0.01, 0.025, 0.05, 0.1]:
            cv = self.critical_values.get(alpha, np.nan)
            rej = self.reject.get(alpha, False)
            decision = "Reject H0" if rej else "Fail to reject H0"
            lines.append(f"  {int(alpha*100):3d}%: CV = {cv:.4f}, {decision}")
        
        lines.append("=" * 70)
        lines.append("Note: Reject H0 if statistic > critical value (upper tail test)")
        lines.append("")
        
        return "\n".join(lines)
    
    def _det_description(self) -> str:
        if self.d == -1:
            return "None"
        elif self.d == 0:
            return "Intercept only"
        elif self.d == 1:
            return "Intercept and linear trend"
        return f"Unknown (d={self.d})"


@dataclass
class PUTestResult:
    """
    Results container for PU (non-cointegration) test.
    
    Attributes
    ----------
    statistic : float
        PU test statistic
    critical_values : dict
        Critical values at standard significance levels
    p_value : float
        Approximate p-value (interpolated)
    reject : dict
        Rejection decisions at standard significance levels
    d : int
        Deterministic specification used
    m : int
        Number of integrated regressors
    p : int
        Highest power of the regressor entering with powers
    null_hypothesis : str
        Description of the null hypothesis
    """
    statistic: float
    critical_values: dict
    p_value: float
    reject: dict
    d: int
    m: int
    p: int
    null_hypothesis: str = "No cointegration (spurious regression)"
    
    def __repr__(self) -> str:
        return self._format_output()
    
    def _format_output(self) -> str:
        """Format output for publication-quality display."""
        lines = [
            "",
            "=" * 70,
            "PU Test for Non-Cointegration (Phillips-Ouliaris type)",
            "=" * 70,
            f"H0: {self.null_hypothesis}",
            f"Deterministics: {self._det_description()}",
            f"Integrated regressors (m): {self.m}",
            f"Highest power (p): {self.p}",
            "-" * 70,
            f"Test Statistic: {self.statistic:.6f}",
            f"Approximate p-value: {self.p_value:.4f}",
            "-" * 70,
            "Critical Values and Decisions:",
        ]
        
        for alpha in [0.01, 0.025, 0.05, 0.1]:
            cv = self.critical_values.get(alpha, np.nan)
            rej = self.reject.get(alpha, False)
            decision = "Reject H0" if rej else "Fail to reject H0"
            lines.append(f"  {int(alpha*100):3d}%: CV = {cv:.4f}, {decision}")
        
        lines.append("=" * 70)
        lines.append("Note: Reject H0 if statistic > critical value (upper tail test)")
        lines.append("")
        
        return "\n".join(lines)
    
    def _det_description(self) -> str:
        if self.d == -1:
            return "None"
        elif self.d == 0:
            return "Intercept only"
        elif self.d == 1:
            return "Intercept and linear trend"
        return f"Unknown (d={self.d})"


def ct_test(u_plus: np.ndarray, 
            omega: float, 
            d: int, 
            m: int, 
            p: int,
            alpha_vec: Optional[List[float]] = None) -> CTTestResult:
    """
    CT Test: KPSS-Shin type test for cointegration in CPRs.
    
    Tests the null hypothesis of cointegration against the alternative
    of no cointegration.
    
    Parameters
    ----------
    u_plus : np.ndarray
        FM-OLS residuals, shape (T-1,) or (T-1, 1)
    omega : float
        Estimated long-run variance omega_{u.v}
    d : int
        Deterministic specification:
        -1: no deterministics
         0: intercept only
         1: intercept and linear trend
    m : int
        Number of integrated regressors (1-4)
    p : int
        Highest power of the regressor entering with powers (1-4)
    alpha_vec : list of float, optional
        Significance levels for test decisions.
        Default is [0.01, 0.025, 0.05, 0.1]
    
    Returns
    -------
    CTTestResult
        Dataclass with test statistic, critical values, p-value, and decisions
    
    Notes
    -----
    The test statistic is computed as:
        CT = (1/(T*omega)) * sum_{t=1}^T (partial_sum_t)^2
    
    where partial_sum_t = (1/sqrt(T)) * sum_{j=1}^t u_plus_j
    
    Reject H0 (cointegration) if CT > critical value.
    
    Examples
    --------
    >>> from cpr import fm_cpr, ct_test
    >>> # After FM-OLS estimation
    >>> result = fm_cpr(y, x, orders=2, deter=deter)
    >>> ct_result = ct_test(result.u_plus, result.Omega_udotv, d=1, m=1, p=2)
    >>> print(ct_result)
    """
    if alpha_vec is None:
        alpha_vec = [0.01, 0.025, 0.05, 0.1]
    
    u_plus = np.asarray(u_plus).flatten()
    T = len(u_plus)
    
    # Compute test statistic
    partsum = (1 / np.sqrt(T)) * np.cumsum(u_plus)
    CT_stat = (1 / (T * omega)) * np.sum(partsum**2)
    
    # Get critical values and make decisions
    critical_values = {}
    reject = {}
    
    for alpha in alpha_vec:
        try:
            cv = get_ct_critical_value(d, m, p, alpha)
            critical_values[alpha] = cv
            reject[alpha] = CT_stat > cv
        except ValueError:
            critical_values[alpha] = np.nan
            reject[alpha] = None
    
    # Compute approximate p-value
    try:
        p_value = get_p_value('CT', d, m, p, CT_stat)
    except ValueError:
        p_value = np.nan
    
    return CTTestResult(
        statistic=CT_stat,
        critical_values=critical_values,
        p_value=p_value,
        reject=reject,
        d=d,
        m=m,
        p=p
    )


def pu_test(y: np.ndarray,
            x: np.ndarray,
            d: int,
            m: int,
            orders: Union[int, List[np.ndarray]],
            kern: str = 'ba',
            band: Union[str, float] = 'NW',
            deme: int = 0,
            alpha_vec: Optional[List[float]] = None) -> PUTestResult:
    """
    PU Test: Phillips-Ouliaris type test for non-cointegration in CPRs.
    
    Tests the null hypothesis of no cointegration (spurious regression)
    against the alternative of cointegration.
    
    Parameters
    ----------
    y : np.ndarray
        Dependent variable, shape (T,) or (T, 1)
    x : np.ndarray
        Integrated regressors, shape (T, m)
    d : int
        Deterministic specification:
        -1: no deterministics
         0: intercept only
         1: intercept and linear trend
    m : int
        Number of integrated regressors
    orders : int or list of arrays
        If scalar: highest power of the m-th regressor (powers 1,...,orders included)
        If list of arrays: specific powers for each regressor
    kern : str, optional
        Kernel function ('tr', 'ba', 'pa', 'bo', 'da', 'qs'), default is 'ba'
    band : str or float, optional
        Bandwidth: 'And91', 'NW', 'AM92', or numeric value. Default is 'NW'
    deme : int, optional
        Demeaning of residuals (0: no, 1: yes), default is 0
    alpha_vec : list of float, optional
        Significance levels. Default is [0.01, 0.025, 0.05, 0.1]
    
    Returns
    -------
    PUTestResult
        Dataclass with test statistic, critical values, p-value, and decisions
    
    Notes
    -----
    The test statistic is:
        PU = omega_{w.v} / (T^{-2} * sum(u_hat^2))
    
    where omega_{w.v} is the conditional long-run variance from VAR(1) residuals.
    
    Reject H0 (no cointegration) if PU > critical value.
    
    Examples
    --------
    >>> from cpr import pu_test
    >>> result = pu_test(y, x, d=1, m=1, orders=2)
    >>> print(result)
    """
    if alpha_vec is None:
        alpha_vec = [0.01, 0.025, 0.05, 0.1]
    
    y = ensure_2d(y).flatten()
    x = ensure_2d(x)
    T = len(y)
    
    # Generate deterministic components
    deter = generate_deterministics(T, d)
    
    # Stack y and x for VAR estimation
    z = np.column_stack([y, x])
    
    # Generate powers of the m-th regressor
    xpower = x[:, m - 1:m]  # Last column of x
    
    if isinstance(orders, (int, np.integer)) and orders == 1:
        powerreg = None
    else:
        reg = gen_var_poly_terms(xpower, orders, stochastic=True)
        powerreg = reg.X
    
    # Build regressor matrix for OLS residuals
    if isinstance(orders, (int, np.integer)) and orders == 1:
        if deter is not None:
            regmat4uhat = np.hstack([deter, x])
        else:
            regmat4uhat = x
    else:
        x_ = x[:, :m - 1] if m > 1 else np.zeros((T, 0))
        parts = []
        if deter is not None:
            parts.append(deter)
        if x_.shape[1] > 0:
            parts.append(x_)
        parts.append(powerreg)
        regmat4uhat = np.hstack(parts)
    
    # OLS residuals
    coeff4uhat = np.linalg.lstsq(regmat4uhat, y, rcond=None)[0]
    uhat = y - regmat4uhat @ coeff4uhat
    
    # VAR(1) for stacked series z = [y, x]
    depvar = z[1:, :]
    lagvar = lag(z, 1)
    
    if deter is not None:
        indepvar = np.hstack([deter[1:, :], lagvar[1:, :]])
    else:
        indepvar = lagvar[1:, :]
    
    # VAR(1) estimation
    varcoeff = np.linalg.lstsq(indepvar, depvar, rcond=None)[0]
    varresid = depvar - indepvar @ varcoeff
    
    # Long-run variance estimation
    if band == 'And91':
        bandw = bandwidth_andrews(varresid, kern)
        Lr, Dr, Sr = lr_var(varresid, kern, bandw, deme)
    elif band == 'NW':
        bandw = bandwidth_nw(varresid, kern, 0, None)
        Lr, Dr, Sr = lr_var(varresid, kern, bandw, deme)
    elif band == 'AM92':
        Lr, Dr, Sr = andmon_hac92(varresid, kern, 1, 1, deme)
    else:
        bandw = float(band)
        Lr, Dr, Sr = lr_var(varresid, kern, bandw, deme)
    
    # Conditional long-run variance
    omega_wdotv = Lr[0, 0] - Lr[0, 1:] @ np.linalg.inv(Lr[1:, 1:]) @ Lr[1:, 0]
    
    # Compute test statistic
    PU_stat = omega_wdotv / (T**(-2) * np.sum(uhat**2))
    
    # Get highest power for critical value lookup
    if isinstance(orders, (int, np.integer)):
        p = orders
    else:
        p = int(np.max(orders))
    
    # Get critical values and make decisions
    critical_values = {}
    reject = {}
    
    for alpha in alpha_vec:
        try:
            cv = get_pu_critical_value(d, m, p, alpha)
            critical_values[alpha] = cv
            reject[alpha] = PU_stat > cv
        except ValueError:
            critical_values[alpha] = np.nan
            reject[alpha] = None
    
    # Compute approximate p-value
    try:
        p_value = get_p_value('PU', d, m, p, PU_stat)
    except ValueError:
        p_value = np.nan
    
    return PUTestResult(
        statistic=PU_stat,
        critical_values=critical_values,
        p_value=p_value,
        reject=reject,
        d=d,
        m=m,
        p=p
    )


def phillips_ouliaris(uhat: np.ndarray,
                      d: int,
                      n: int,
                      kern: str = 'ba',
                      band: Union[str, float] = 'NW',
                      deme: int = 0,
                      alpha: float = 0.05) -> Tuple[float, float, np.ndarray, np.ndarray, int, int]:
    """
    Phillips-Ouliaris / Phillips-Perron type tests for cointegration.
    
    Computes both the Z_alpha (coefficient) and Z_t (t-statistic) versions.
    
    Parameters
    ----------
    uhat : np.ndarray
        Residuals from cointegrating OLS regression, shape (T,)
    d : int
        Deterministic specification (-1, 0, or 1)
    n : int
        Number of integrated regressors (1-5)
    kern : str, optional
        Kernel function, default is 'ba'
    band : str or float, optional
        Bandwidth specification, default is 'NW'
    deme : int, optional
        Demeaning (0 or 1), default is 0
    alpha : float, optional
        Significance level, default is 0.05
    
    Returns
    -------
    Tuple containing:
        - PO_c: Z_alpha (coefficient) test statistic
        - PO_t: Z_t (t-statistic) test statistic
        - C_val_all: Critical values for coefficient test
        - t_val_all: Critical values for t-test
        - coeff_dec: Test decision for coefficient test (1=reject, 0=no reject)
        - t_dec: Test decision for t-test (1=reject, 0=no reject)
    
    Notes
    -----
    This function implements the standard Phillips-Ouliaris tests for
    linear cointegrating relationships (not specifically for CPRs).
    Critical values are from Phillips and Ouliaris (1990), Tables IIa-IIc.
    """
    uhat = np.asarray(uhat).flatten()
    T = len(uhat)
    
    # AR(1) regression on residuals
    Yvec = uhat[1:]
    Xvec = uhat[:-1]
    ahat = np.sum(Xvec * Yvec) / np.sum(Xvec**2)
    Uvec = Yvec - Xvec * ahat
    
    # Variance and long-run variances
    if band == 'And91':
        bandw = bandwidth_andrews(Uvec.reshape(-1, 1), kern)
    elif band == 'NW':
        bandw = bandwidth_nw(Uvec.reshape(-1, 1), kern, 0, None)
    else:
        bandw = float(band) if not isinstance(band, str) else 10
    
    if band == 'AM92':
        Omega, Delta, Sigma = andmon_hac92(Uvec.reshape(-1, 1), kern, 1, 1, deme)
    else:
        Omega, Delta, Sigma = lr_var(Uvec.reshape(-1, 1), kern, bandw, deme)
    
    Omega = Omega[0, 0]
    Sigma = Sigma[0, 0]
    
    # t-value
    t_ahat = (ahat - 1) / np.sqrt(Sigma / np.sum(Xvec**2))
    
    # Phillips-Ouliaris Z_alpha and Z_t tests
    PO_c = T * (ahat - 1) - 0.5 * (Omega - Sigma) / (T**(-2) * np.sum(Xvec**2))
    PO_t = np.sqrt(Sigma) / np.sqrt(Omega) * t_ahat - 0.5 * (Omega - Sigma) / (np.sqrt(Omega) * np.sqrt(T**(-2) * np.sum(Xvec**2)))
    
    # Critical values tables from Phillips and Ouliaris (1990)
    # Format: rows = n (1-5), columns = [0.01, 0.025, 0.05, 0.075, 0.10]
    if d == -1:  # No deterministics
        tab_coeff = np.array([
            [-22.8291, -18.8833, -15.6377, -13.8123, -12.5438],
            [-29.2688, -25.2101, -21.4833, -19.6142, -18.1785],
            [-36.1619, -31.5432, -27.8526, -25.5236, -23.9225],
            [-42.8724, -37.4769, -33.4784, -30.9288, -27.3952],
            [-48.5240, -42.5473, -38.0934, -35.5142, -32.2654]
        ])
        tab_t = np.array([
            [-3.3865, -3.0547, -2.7619, -2.5822, -2.4505],
            [-3.8395, -3.5484, -3.2667, -3.1105, -2.9873],
            [-4.3038, -3.9895, -3.7371, -3.5716, -3.4446],
            [-4.6720, -4.3798, -4.1261, -3.9482, -3.8068],
            [-4.9897, -4.6676, -4.3999, -4.2521, -4.1416]
        ])
    elif d == 0:  # Intercept
        tab_coeff = np.array([
            [-28.3218, -23.8084, -20.4935, -18.4836, -17.0390],
            [-34.1686, -29.7354, -26.0943, -23.8739, -22.1948],
            [-41.1348, -35.7116, -32.0615, -29.5083, -27.5846],
            [-47.5118, -41.6431, -37.1508, -34.7110, -32.7382],
            [-52.1723, -46.5344, -41.9388, -39.1100, -37.0074]
        ])
        tab_t = np.array([
            [-3.9618, -3.6420, -3.3654, -3.1982, -3.0657],
            [-4.3078, -4.0217, -3.7675, -3.5846, -3.4494],
            [-4.7325, -4.3747, -4.1121, -3.9560, -3.8329],
            [-5.0728, -4.7075, -4.4542, -4.2883, -4.1565],
            [-5.2812, -4.9809, -4.7101, -4.5553, -4.4309]
        ])
    elif d == 1:  # Intercept and trend
        tab_coeff = np.array([
            [-35.4185, -30.8451, -27.0866, -24.7530, -23.1915],
            [-40.3427, -36.1121, -32.2231, -29.7331, -27.7803],
            [-47.3590, -42.5998, -37.7304, -34.9951, -33.1637],
            [-53.6142, -47.1068, -42.4593, -39.7286, -37.7368],
            [-58.1615, -52.4874, -47.3830, -44.5074, -42.3231]
        ])
        tab_t = np.array([
            [-4.3628, -4.0722, -3.8000, -3.6467, -3.5184],
            [-4.6451, -4.3854, -4.1567, -3.9754, -3.8429],
            [-5.0433, -4.7699, -4.4895, -4.3198, -4.1950],
            [-5.3576, -5.0180, -4.7423, -4.5837, -4.4625],
            [-5.5849, -5.3056, -5.0282, -4.8695, -4.7311]
        ])
    else:
        raise ValueError(f"d must be -1, 0, or 1, got {d}")
    
    # Get critical values for this n
    if n < 1 or n > 5:
        raise ValueError(f"n must be between 1 and 5, got {n}")
    
    C_val_all = tab_coeff[n - 1, :]
    t_val_all = tab_t[n - 1, :]
    
    # Map alpha to index
    alpha_mapping = {0.01: 0, 0.025: 1, 0.05: 2, 0.075: 3, 0.1: 4}
    if alpha not in alpha_mapping:
        raise ValueError(f"alpha must be one of {list(alpha_mapping.keys())}")
    a_ind = alpha_mapping[alpha]
    
    C_val_alpha = C_val_all[a_ind]
    t_val_alpha = t_val_all[a_ind]
    
    coeff_dec = 1 if PO_c <= C_val_alpha else 0
    t_dec = 1 if PO_t <= t_val_alpha else 0
    
    return PO_c, PO_t, C_val_all, t_val_all, coeff_dec, t_dec


@dataclass
class CPRTestSummary:
    """
    Combined summary of CT and PU test results.
    
    Provides a unified view of both cointegration and non-cointegration
    test results for easy interpretation.
    """
    ct_result: CTTestResult
    pu_result: PUTestResult
    
    def __repr__(self) -> str:
        return self._format_output()
    
    def _format_output(self) -> str:
        lines = [
            "",
            "=" * 70,
            "CPR Cointegration/Non-Cointegration Test Summary",
            "=" * 70,
            "",
            f"CT Test (H0: Cointegration)",
            f"  Statistic: {self.ct_result.statistic:.6f}",
            f"  5% CV: {self.ct_result.critical_values.get(0.05, np.nan):.4f}",
            f"  Decision: {'Reject' if self.ct_result.reject.get(0.05) else 'Fail to reject'} at 5%",
            "",
            f"PU Test (H0: No Cointegration)",
            f"  Statistic: {self.pu_result.statistic:.6f}",
            f"  5% CV: {self.pu_result.critical_values.get(0.05, np.nan):.4f}",
            f"  Decision: {'Reject' if self.pu_result.reject.get(0.05) else 'Fail to reject'} at 5%",
            "",
            "-" * 70,
            "Interpretation:",
        ]
        
        ct_reject = self.ct_result.reject.get(0.05, False)
        pu_reject = self.pu_result.reject.get(0.05, False)
        
        if not ct_reject and pu_reject:
            lines.append("  Evidence FOR cointegration")
            lines.append("  (CT: fail to reject cointegration, PU: reject no cointegration)")
        elif ct_reject and not pu_reject:
            lines.append("  Evidence AGAINST cointegration")
            lines.append("  (CT: reject cointegration, PU: fail to reject no cointegration)")
        elif ct_reject and pu_reject:
            lines.append("  CONFLICTING evidence")
            lines.append("  (Both tests reject their null hypotheses)")
        else:
            lines.append("  CONFLICTING evidence")
            lines.append("  (Neither test rejects its null hypothesis)")
        
        lines.append("=" * 70)
        lines.append("")
        
        return "\n".join(lines)
    
    def evidence_for_cointegration(self, alpha: float = 0.05) -> Optional[bool]:
        """
        Determine if there is evidence for cointegration.
        
        Parameters
        ----------
        alpha : float
            Significance level
        
        Returns
        -------
        bool or None
            True: evidence for cointegration
            False: evidence against cointegration
            None: conflicting evidence
        """
        ct_reject = self.ct_result.reject.get(alpha, None)
        pu_reject = self.pu_result.reject.get(alpha, None)
        
        if ct_reject is None or pu_reject is None:
            return None
        
        if not ct_reject and pu_reject:
            return True
        elif ct_reject and not pu_reject:
            return False
        else:
            return None
