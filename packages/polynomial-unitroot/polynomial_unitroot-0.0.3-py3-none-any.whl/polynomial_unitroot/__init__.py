"""
Polynomial Unit Root Tests - Python Implementation

A comprehensive Python library implementing the Phillips unit root tests 
for polynomials of integrated processes based on:

- Wagner, M. (2012). The Phillips unit root tests for polynomials of 
  integrated processes. Economics Letters, 114, 299-303.
  
- Stypka, O., & Wagner, M. (2019). The Phillips unit root tests for 
  polynomials of integrated processes revisited. 
  Economics Letters, 176, 109-113.

This package provides:
- Six test statistics: Z_rho, Z_t, Z*_rho, Z*_t, Z**_rho, Z**_t
- Critical values from published tables
- Monte Carlo simulation tools for critical value generation
- HAC variance estimation with multiple kernel options
- Data generation utilities for Monte Carlo studies

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
GitHub: https://github.com/merwanroudane/polyunitroottest

License: MIT
"""

__version__ = "0.0.3"
__author__ = "Dr Merwan Roudane"
__email__ = "merwanroudane920@gmail.com"

# Main test functions
from .tests import (
    phillips_polynomial_test,
    all_phillips_tests,
    print_all_tests_summary,
    PolynomialUnitRootResult,
    # Convenience functions
    Z_rho_test,
    Z_t_test,
    Z_rho_star_test,
    Z_t_star_test,
    Z_rho_dstar_test,
    Z_t_dstar_test,
)

# Critical values
from .critical_values import (
    get_critical_value,
    get_all_critical_values,
    p_value,
    interpolate_critical_value,
    # Published critical value tables
    WAGNER2012_COEF_CRITICAL_VALUES,
    WAGNER2012_TSTAT_CRITICAL_VALUES,
    STYPKA2019_Z_RHO_CRITICAL_VALUES,
    STYPKA2019_Z_T_CRITICAL_VALUES,
    STYPKA2019_Z_RHO_STAR_CRITICAL_VALUES,
    STYPKA2019_Z_T_STAR_CRITICAL_VALUES,
    STYPKA2019_Z_RHO_DSTAR_CRITICAL_VALUES,
    STYPKA2019_Z_T_DSTAR_CRITICAL_VALUES,
)

# Kernel and HAC estimation
from .kernels import (
    bartlett_kernel,
    parzen_kernel,
    quadratic_spectral_kernel,
    tukey_hanning_kernel,
    get_kernel,
    estimate_long_run_variance,
    estimate_half_long_run_variance,
    estimate_variances,
    andrews_bandwidth,
    newey_west_bandwidth,
    compute_bandwidth,
)

# Simulation tools
from .simulations import (
    simulate_brownian_motion,
    simulate_stochastic_integral,
    simulate_time_integral,
    simulate_Z_rho_distribution,
    simulate_Z_t_distribution,
    simulate_Z_rho_star_distribution,
    simulate_Z_t_star_distribution,
    simulate_Z_rho_dstar_distribution,
    simulate_Z_t_dstar_distribution,
    simulate_all_distributions,
    compute_critical_values,
    generate_critical_value_table,
    print_critical_value_table,
)

# Utility functions
from .utils import (
    generate_random_walk,
    generate_ar1_random_walk,
    generate_near_integrated,
    generate_stationary_ar1,
    monte_carlo_size,
    monte_carlo_power,
    MonteCarloResult,
)

__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    
    # Main test functions
    'phillips_polynomial_test',
    'all_phillips_tests',
    'print_all_tests_summary',
    'PolynomialUnitRootResult',
    'Z_rho_test',
    'Z_t_test',
    'Z_rho_star_test',
    'Z_t_star_test',
    'Z_rho_dstar_test',
    'Z_t_dstar_test',
    
    # Critical values
    'get_critical_value',
    'get_all_critical_values',
    'p_value',
    'interpolate_critical_value',
    'WAGNER2012_COEF_CRITICAL_VALUES',
    'WAGNER2012_TSTAT_CRITICAL_VALUES',
    'STYPKA2019_Z_RHO_CRITICAL_VALUES',
    'STYPKA2019_Z_T_CRITICAL_VALUES',
    'STYPKA2019_Z_RHO_STAR_CRITICAL_VALUES',
    'STYPKA2019_Z_T_STAR_CRITICAL_VALUES',
    'STYPKA2019_Z_RHO_DSTAR_CRITICAL_VALUES',
    'STYPKA2019_Z_T_DSTAR_CRITICAL_VALUES',
    
    # Kernels
    'bartlett_kernel',
    'parzen_kernel',
    'quadratic_spectral_kernel',
    'tukey_hanning_kernel',
    'get_kernel',
    'estimate_long_run_variance',
    'estimate_half_long_run_variance',
    'estimate_variances',
    'andrews_bandwidth',
    'newey_west_bandwidth',
    'compute_bandwidth',
    
    # Simulation
    'simulate_brownian_motion',
    'simulate_stochastic_integral',
    'simulate_time_integral',
    'simulate_Z_rho_distribution',
    'simulate_Z_t_distribution',
    'simulate_Z_rho_star_distribution',
    'simulate_Z_t_star_distribution',
    'simulate_Z_rho_dstar_distribution',
    'simulate_Z_t_dstar_distribution',
    'simulate_all_distributions',
    'compute_critical_values',
    'generate_critical_value_table',
    'print_critical_value_table',
    
    # Utilities
    'generate_random_walk',
    'generate_ar1_random_walk',
    'generate_near_integrated',
    'generate_stationary_ar1',
    'monte_carlo_size',
    'monte_carlo_power',
    'MonteCarloResult',
]
