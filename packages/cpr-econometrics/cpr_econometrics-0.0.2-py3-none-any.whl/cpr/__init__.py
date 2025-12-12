"""
CPR: Cointegrating Polynomial Regressions
==========================================

A Python library for residual-based cointegration and non-cointegration tests
for cointegrating polynomial regressions (CPRs).

This package provides:
- FM-OLS estimation for cointegrating polynomial regressions
- CT test: KPSS-Shin type test with H0: cointegration
- PU test: Phillips-Ouliaris type test with H0: no cointegration
- Long-run variance estimation with various kernels and bandwidths
- Critical values for all test specifications

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
GitHub: https://github.com/merwanroudane/cpr

References
----------
Wagner, M. (2023). Residual-based cointegration and non-cointegration tests
    for cointegrating polynomial regressions. Empirical Economics, 65, 1-31.

Wagner, M., & Hong, S. H. (2016). Cointegrating polynomial regressions: 
    Fully modified OLS estimation and inference. Econometric Theory, 32(6), 1289-1315.

Shin, Y. (1994). A residual-based test for the null of cointegration against
    the alternative of no cointegration. Econometric Theory, 10(1), 91-115.
    
Phillips, P. C. B., & Ouliaris, S. (1990). Asymptotic properties of residual
    based tests for cointegration. Econometrica, 58(1), 165-193.

Example
-------
>>> import numpy as np
>>> from cpr import fm_cpr, ct_test, pu_test
>>>
>>> # Generate sample data
>>> np.random.seed(42)
>>> T = 200
>>> x = np.cumsum(np.random.randn(T))  # I(1) regressor
>>> y = 1.0 + 0.5 * x + 0.2 * x**2 + np.random.randn(T) * 0.5  # Quadratic CPR
>>>
>>> # Create deterministic components (intercept and trend)
>>> deter = np.column_stack([np.ones(T), np.arange(1, T + 1)])
>>>
>>> # FM-OLS estimation
>>> result = fm_cpr(y, x.reshape(-1, 1), orders=2, deter=deter)
>>> print(f"FM-OLS coefficients: {result.beta_fm}")
>>>
>>> # CT test (H0: cointegration)
>>> ct_result = ct_test(result.u_plus, result.Omega_udotv, d=1, m=1, p=2)
>>> print(ct_result)
>>>
>>> # PU test (H0: no cointegration)
>>> pu_result = pu_test(y, x.reshape(-1, 1), d=1, m=1, orders=2)
>>> print(pu_result)
"""

__version__ = "0.0.2"
__author__ = "Dr Merwan Roudane"
__email__ = "merwanroudane920@gmail.com"

# Main estimation function
from .fmols import fm_cpr, FMOLSResult

# Test functions
from .tests import (
    ct_test, 
    pu_test, 
    phillips_ouliaris,
    CTTestResult, 
    PUTestResult,
    CPRTestSummary
)

# Critical values
from .critical_values import (
    get_ct_critical_value,
    get_pu_critical_value,
    get_all_critical_values,
    get_p_value,
    CT_CRITICAL_VALUES,
    PU_CRITICAL_VALUES,
    PERCENTILES
)

# Long-run variance estimation
from .lr_variance import (
    lr_var,
    lr_weights,
    bandwidth_nw,
    bandwidth_andrews,
    andmon_hac92,
    andmon_stab,
    compute_lr_variance
)

# Polynomial terms generation
from .poly_terms import (
    gen_var_poly_terms,
    gen_power_reg,
    gen_cpr_corr_vec,
    PolyTermsResult
)

# Utility functions
from .utils import (
    trimr,
    lag,
    cumsum,
    diff,
    ensure_2d,
    ensure_1d,
    generate_deterministics,
    ols,
    var_estimate
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    
    # Main estimation
    "fm_cpr",
    "FMOLSResult",
    
    # Tests
    "ct_test",
    "pu_test",
    "phillips_ouliaris",
    "CTTestResult",
    "PUTestResult",
    "CPRTestSummary",
    
    # Critical values
    "get_ct_critical_value",
    "get_pu_critical_value",
    "get_all_critical_values",
    "get_p_value",
    "CT_CRITICAL_VALUES",
    "PU_CRITICAL_VALUES",
    "PERCENTILES",
    
    # Long-run variance
    "lr_var",
    "lr_weights",
    "bandwidth_nw",
    "bandwidth_andrews",
    "andmon_hac92",
    "andmon_stab",
    "compute_lr_variance",
    
    # Polynomial terms
    "gen_var_poly_terms",
    "gen_power_reg",
    "gen_cpr_corr_vec",
    "PolyTermsResult",
    
    # Utilities
    "trimr",
    "lag",
    "cumsum",
    "diff",
    "ensure_2d",
    "ensure_1d",
    "generate_deterministics",
    "ols",
    "var_estimate",
]
