# CPR: Cointegrating Polynomial Regressions

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/cpr-econometrics.svg)](https://badge.fury.io/py/cpr-econometrics)

A Python library for **residual-based cointegration and non-cointegration tests for cointegrating polynomial regressions (CPRs)**.

This package implements the econometric methods developed in:

> Wagner, M. (2023). Residual-based cointegration and non-cointegration tests for cointegrating polynomial regressions. *Empirical Economics*, 65, 1-31. https://doi.org/10.1007/s00181-022-02332-3

## Features

- **FM-OLS Estimation**: Fully Modified OLS estimator for cointegrating polynomial regressions following Wagner & Hong (2016)
- **CT Test**: KPSS-Shin type test with null hypothesis of cointegration
- **PU Test**: Phillips-Ouliaris type test with null hypothesis of no cointegration
- **Long-run Variance Estimation**: Multiple kernel functions (Bartlett, Parzen, Quadratic Spectral, etc.) with automatic bandwidth selection (Andrews 1991, Newey-West 1994, Andrews-Monahan 1992)
- **Critical Values**: Pre-computed critical values for up to 4 integrated regressors and power 4
- **Publication-Ready Output**: Formatted output suitable for academic publications

## Installation

```bash
pip install cpr-econometrics
```

Or install from source:

```bash
git clone https://github.com/merwanroudane/cpr-econometrics.git
cd cpr
pip install -e .
```

## Quick Start

### Basic Example: Environmental Kuznets Curve

```python
import numpy as np
from cpr import fm_cpr, ct_test, pu_test, CPRTestSummary

# Generate sample data (simulating EKC relationship)
np.random.seed(42)
T = 150  # Typical sample size for annual macro data

# GDP per capita (I(1) process)
gdp = np.cumsum(np.random.randn(T) * 0.1) + 10

# Generate AR(1) errors (serially correlated as in real economic data)
errors = np.zeros(T)
for t in range(1, T):
    errors[t] = 0.5 * errors[t-1] + np.random.randn() * 0.3

# Emissions with quadratic relationship (inverted U-shape EKC)
emissions = 2.0 + 0.5 * gdp - 0.02 * gdp**2 + errors

# Create deterministic components (intercept and trend)
deter = np.column_stack([np.ones(T), np.arange(1, T + 1)])

# FM-OLS estimation
result = fm_cpr(
    y=emissions, 
    x=gdp.reshape(-1, 1), 
    orders=2,  # Quadratic specification
    deter=deter,
    kern='ba',  # Bartlett kernel
    band='NW'   # Newey-West bandwidth
)

print("FM-OLS Coefficients for polynomial terms:", result.beta_fm)
print("t-statistics:", result.t_beta)

# CT Test (H0: Cointegration)
ct_result = ct_test(
    u_plus=result.u_plus, 
    omega=result.Omega_udotv, 
    d=1,  # intercept and trend
    m=1,  # 1 integrated regressor
    p=2   # quadratic specification
)
print(ct_result)

# PU Test (H0: No Cointegration)
pu_result = pu_test(
    y=emissions, 
    x=gdp.reshape(-1, 1), 
    d=1, 
    m=1, 
    orders=2
)
print(pu_result)

# Combined Summary
summary = CPRTestSummary(ct_result, pu_result)
print(summary)
```

**Expected Results:**
- CT statistic: ~0.03-0.10 (should be < 0.106 for cointegration at 5%)
- PU statistic: ~50-150 (should be > 52.95 for cointegration at 5%)

## API Reference

### FM-OLS Estimation

```python
from cpr import fm_cpr

result = fm_cpr(
    y,                    # Dependent variable (T,)
    x,                    # Integrated regressors (T, m)
    orders,               # Polynomial orders (int or list)
    w=None,               # Stationary regressors (optional)
    deter=None,           # Deterministic terms (optional)
    kern='ba',            # Kernel: 'tr', 'ba', 'pa', 'bo', 'da', 'qs'
    band='NW',            # Bandwidth: 'And91', 'NW', 'AM92', or numeric
    deme=0                # Demeaning: 0 or 1
)

# Results include:
# - result.beta_fm: FM-OLS coefficients for polynomial terms
# - result.t_beta: t-statistics
# - result.u_plus: FM-OLS residuals
# - result.Omega_udotv: Conditional long-run variance
```

### CT Test (Cointegration Test)

```python
from cpr import ct_test

ct_result = ct_test(
    u_plus,               # FM-OLS residuals
    omega,                # Long-run variance estimate
    d,                    # Deterministics: -1, 0, or 1
    m,                    # Number of integrated regressors (1-4)
    p                     # Highest power (1-4)
)

# Interpretation:
# - Reject H0 (cointegration) if statistic > critical value
# - Low statistic → evidence FOR cointegration
```

### PU Test (Non-Cointegration Test)

```python
from cpr import pu_test

pu_result = pu_test(
    y,                    # Dependent variable
    x,                    # Integrated regressors
    d,                    # Deterministics: -1, 0, or 1
    m,                    # Number of integrated regressors
    orders,               # Polynomial orders
    kern='ba',            # Kernel function
    band='NW'             # Bandwidth
)

# Interpretation:
# - Reject H0 (no cointegration) if statistic > critical value
# - High statistic → evidence FOR cointegration
```

## Deterministic Specifications

| `d` | Description | Model |
|-----|-------------|-------|
| -1 | No deterministics | `y = β₁x + β₂x² + ... + u` |
| 0 | Intercept only | `y = c + β₁x + β₂x² + ... + u` |
| 1 | Intercept and trend | `y = c + δt + β₁x + β₂x² + ... + u` |

## Kernel Functions

| Code | Kernel | Use Case |
|------|--------|----------|
| `'tr'` | Truncated | Not recommended |
| `'ba'` | Bartlett | Standard choice (default) |
| `'pa'` | Parzen | Alternative to Bartlett |
| `'bo'` | Bohman | Smooth kernel |
| `'da'` | Daniell | Spectral analysis |
| `'qs'` | Quadratic Spectral | Optimal for some purposes |

## Bandwidth Selection

| Code | Method | Reference |
|------|--------|-----------|
| `'NW'` | Newey-West (1994) | Default, data-driven |
| `'And91'` | Andrews (1991) | AR(1)-based |
| `'AM92'` | Andrews-Monahan (1992) | VAR prewhitening |
| Numeric | Fixed bandwidth | User-specified |

## Decision Rule for EKC Analysis

Following Wagner (2023):

| CT Test | PU Test | Interpretation |
|---------|---------|----------------|
| Fail to reject | Reject | **Evidence FOR cointegration** |
| Reject | Fail to reject | **Evidence AGAINST cointegration** |
| Reject | Reject | Conflicting evidence |
| Fail to reject | Fail to reject | Conflicting evidence |

## Critical Values

Critical values are embedded in the package for:
- `m = 1, 2, 3, 4` integrated regressors
- `p = 1, 2, 3, 4` polynomial powers
- `d = -1, 0, 1` deterministic specifications
- Significance levels: 1%, 2.5%, 5%, 10%

```python
from cpr import get_ct_critical_value, get_pu_critical_value

# Get specific critical value
cv_ct = get_ct_critical_value(d=1, m=1, p=2, alpha=0.05)
cv_pu = get_pu_critical_value(d=1, m=1, p=2, alpha=0.05)
```

## Applications

This package is suitable for:

- **Environmental Kuznets Curve (EKC)** analysis
- **Material Kuznets Curve (MKC)** studies
- **Intensity-of-use** analysis
- **Exchange rate target-zone** models
- Any nonlinear cointegrating relationship involving powers of I(1) variables

## Requirements

- Python ≥ 3.8
- NumPy ≥ 1.20.0
- SciPy ≥ 1.7.0
- pandas ≥ 1.3.0
- statsmodels ≥ 0.13.0

## Citation

If you use this package in your research, please cite:

```bibtex
@article{wagner2023residual,
  title={Residual-based cointegration and non-cointegration tests for cointegrating polynomial regressions},
  author={Wagner, Martin},
  journal={Empirical Economics},
  volume={65},
  pages={1--31},
  year={2023},
  publisher={Springer},
  doi={10.1007/s00181-022-02332-3}
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**Dr Merwan Roudane**  
Email: merwanroudane920@gmail.com  
GitHub: [https://github.com/merwanroudane/cpr](https://github.com/merwanroudane/cpr)

## Acknowledgments

This implementation is based on the MATLAB code accompanying Wagner (2023) and follows the econometric methodology developed in Wagner & Hong (2016).
