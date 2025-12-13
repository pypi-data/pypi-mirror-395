# polynomial_unitroot

[![PyPI version](https://badge.fury.io/py/polynomial-unitroot.svg)](https://badge.fury.io/py/polynomial-unitroot)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Phillips Unit Root Tests for Polynomials of Integrated Processes

A comprehensive Python library implementing the Phillips unit root tests for polynomials of integrated processes, based on the seminal papers:

- **Wagner, M. (2012).** "The Phillips unit root tests for polynomials of integrated processes." *Economics Letters*, 114, 299-303.
  
- **Stypka, O., & Wagner, M. (2019).** "The Phillips unit root tests for polynomials of integrated processes revisited." *Economics Letters*, 176, 109-113.

## Motivation

In empirical economics, it is common to analyze relationships involving powers or polynomials of integrated processes. A key example is the **Environmental Kuznets Curve (EKC)** hypothesis, which postulates an inverse U-shaped relationship between pollution and per capita GDP. Testing this hypothesis requires regressing emissions on GDP and its square.

However, **if GDP is an I(1) process, its square is NOT an I(1) process**. Standard unit root tests (ADF, PP, etc.) applied to y² when y ~ I(1) will produce misleading results due to inappropriate critical values.

This package provides the correct test statistics and critical values for unit root testing on polynomials of integrated processes.

## Installation

```bash
pip install polynomial_unitroot
```

Or install from source:

```bash
git clone https://github.com/merwanroudane/polyunitroottest.git
cd polyunitroottest
pip install -e .
```

## Quick Start

```python
import numpy as np
from polynomial_unitroot import (
    phillips_polynomial_test,
    all_phillips_tests,
    print_all_tests_summary
)

# Generate a random walk (I(1) process)
np.random.seed(42)
y = np.cumsum(np.random.randn(200))

# Test unit root on y² (k=2)
result = phillips_polynomial_test(y, k=2, statistic='Z_rho')
print(result)

# Run all six test statistics
results = all_phillips_tests(y, k=2)
print_all_tests_summary(results)
```

## Test Statistics

The package implements **six test statistics** from Stypka & Wagner (2019):

| Statistic | Description | Limiting Distribution |
|-----------|-------------|----------------------|
| Z_ρ | Phillips coefficient statistic | Eq. (8) in Stypka & Wagner (2019) |
| Z_t | Phillips t-statistic | Eq. (9) in Stypka & Wagner (2019) |
| Z*_ρ | Bias-corrected coefficient | Eq. (14) - removes additive bias term |
| Z*_t | Bias-corrected t-statistic | Eq. (15) - removes additive bias term |
| Z**_ρ | Itô-based coefficient | Eq. (16) - uses W(1)^{2k} numerator |
| Z**_t | Itô-based t-statistic | Eq. (17) - uses W(1)^{2k} numerator |

### Test Regression

All tests are based on the regression:

$$x_t = \rho x_{t-1} + v_t$$

where $x_t = y_t^k$ and $y_t$ is the original I(1) process.

### Critical Values

Critical values are provided for **k = 1, 2, 3** at significance levels 1%, 2.5%, 5%, 50%, 95%, 97.5%, and 99%.

For **k = 1**, the tests reduce to the standard Phillips (1987) unit root tests.

## Detailed Usage

### Single Test

```python
from polynomial_unitroot import phillips_polynomial_test

# Z_rho test for k=2 (squared process)
result = phillips_polynomial_test(y, k=2, statistic='Z_rho')

print(f"Test statistic: {result.statistic:.4f}")
print(f"Critical value (5%): {result.critical_values[0.05]:.4f}")
print(f"p-value: {result.p_value:.4f}")
print(f"Reject H0 at 5%: {result.reject_null['5%']}")
```

### All Six Tests

```python
from polynomial_unitroot import all_phillips_tests, print_all_tests_summary

# Run all six test statistics
results = all_phillips_tests(y, k=2)

# Print formatted summary
print_all_tests_summary(results)
```

### Convenience Functions

```python
from polynomial_unitroot import (
    Z_rho_test, Z_t_test,
    Z_rho_star_test, Z_t_star_test,
    Z_rho_dstar_test, Z_t_dstar_test
)

# Each function returns a PolynomialUnitRootResult
result = Z_t_test(y, k=2)
```

### Custom Kernel and Bandwidth

```python
result = phillips_polynomial_test(
    y, k=2, 
    statistic='Z_rho',
    kernel='parzen',           # 'bartlett', 'parzen', 'qs', 'tukey_hanning'
    bandwidth=10,              # Fixed bandwidth
    # Or automatic bandwidth:
    # bandwidth_method='andrews'  # or 'newey_west'
)
```

### Simulating Critical Values

```python
from polynomial_unitroot import (
    generate_critical_value_table,
    print_critical_value_table
)

# Replicate Table 1 from Stypka & Wagner (2019)
cv_table = generate_critical_value_table(
    k_values=[1, 2, 3],
    n_simulations=50000,
    T=1000,
    seed=42
)

print_critical_value_table(cv_table, 'Z_rho')
```

### Monte Carlo Size Analysis

```python
from polynomial_unitroot import monte_carlo_size

# Replicate Table 2 from Wagner (2012)
result = monte_carlo_size(
    T=200, 
    k=2, 
    statistic='Z_t',
    gamma=0.6,           # AR(1) coefficient for innovations
    n_replications=10000,
    significance=0.05
)

print(f"Empirical rejection rate: {result.rejection_rate:.4f}")
```

### Data Generation for Simulations

```python
from polynomial_unitroot import (
    generate_random_walk,
    generate_ar1_random_walk,
    generate_near_integrated
)

# Simple random walk
y = generate_random_walk(T=200, sigma=1.0, seed=42)

# Random walk with AR(1) errors (Wagner 2012 DGP)
y = generate_ar1_random_walk(T=200, gamma=0.5, seed=42)

# Near-integrated process (for power analysis)
y = generate_near_integrated(T=1000, c=10, seed=42)
```

## Critical Value Tables

### From Wagner (2012) - Table 1

Limiting distributions for serially uncorrelated innovations:

**Coefficient Statistic T(ρ̂ - 1):**

| k | 1% | 5% | 50% | Mean | Std |
|---|------|------|------|-------|------|
| 1 | -13.58 | -7.95 | -0.85 | -1.77 | 9.93 |
| 2 | -21.49 | -13.22 | -2.21 | -3.29 | 27.43 |
| 3 | -35.01 | -22.01 | -4.49 | -6.14 | 73.06 |

**t-Statistic:**

| k | 1% | 5% | 50% | Mean | Std |
|---|------|------|------|------|------|
| 1 | -2.56 | -1.94 | -0.50 | -0.42 | 0.96 |
| 2 | -3.26 | -2.53 | -0.94 | -0.73 | 1.76 |
| 3 | -4.18 | -3.30 | -1.41 | -1.17 | 2.65 |

### From Stypka & Wagner (2019) - Table 1

Updated critical values based on 50,000 replications (see paper for all six statistics).

## Theoretical Background

### The Problem

When $y_t \sim I(1)$ (e.g., a random walk), standard unit root tests assume:
- The process being tested is itself I(1)
- Critical values from the Dickey-Fuller distribution

However, $y_t^k$ for $k > 1$ is **not** an I(1) process. The limiting distributions differ substantially:

For **k=1** (standard case):
$$T(\hat{\rho} - 1) \Rightarrow \frac{\int_0^1 W(r)dW(r)}{\int_0^1 W(r)^2 dr}$$

For **k > 1**:
$$T(\hat{\rho} - 1) \Rightarrow \frac{k\int_0^1 W(r)^{2k-1}dW(r) + \binom{k}{2}\int_0^1 W(r)^{2(k-1)}dr}{\int_0^1 W(r)^{2k}dr}$$

### Implications

Using standard DF critical values for $y^2$ or $y^3$ leads to:
- **Conservative tests** (under-rejection of true null)
- Increasing conservativeness with higher k

## Applications

This methodology is relevant for:

1. **Environmental Kuznets Curve (EKC)** analysis
2. **Intensity of use** studies (GDP vs. energy/metals usage)
3. **Exchange rate target zone** models
4. Any regression involving powers of integrated regressors

## Citation

If you use this package in your research, please cite:

```bibtex
@article{wagner2012phillips,
  title={The {Phillips} unit root tests for polynomials of integrated processes},
  author={Wagner, Martin},
  journal={Economics Letters},
  volume={114},
  number={3},
  pages={299--303},
  year={2012},
  publisher={Elsevier}
}

@article{stypka2019phillips,
  title={The {Phillips} unit root tests for polynomials of integrated processes revisited},
  author={Stypka, Oliver and Wagner, Martin},
  journal={Economics Letters},
  volume={176},
  pages={109--113},
  year={2019},
  publisher={Elsevier}
}
```

## Author

**Dr Merwan Roudane**
- Email: merwanroudane920@gmail.com
- GitHub: [https://github.com/merwanroudane/polyunitroottest](https://github.com/merwanroudane/polyunitroottest)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This implementation is based on the theoretical work of Martin Wagner and Oliver Stypka. The critical values and test statistics are reproduced exactly as specified in their papers.
