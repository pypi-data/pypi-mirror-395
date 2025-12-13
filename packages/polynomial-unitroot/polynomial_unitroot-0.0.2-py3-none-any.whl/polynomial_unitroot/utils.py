"""
Utility Functions for Polynomial Unit Root Testing.

This module provides helper functions for:
- Generating simulated data for Monte Carlo studies
- Size and power analysis
- Empirical rejection probability computation

Based on:
- Wagner, M. (2012). The Phillips unit root tests for polynomials of integrated processes.
  Economics Letters, 114, 299-303.
- Stypka, O., & Wagner, M. (2019). The Phillips unit root tests for polynomials of 
  integrated processes revisited. Economics Letters, 176, 109-113.

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
GitHub: https://github.com/merwanroudane/polyunitroottest
"""

import numpy as np
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass


def generate_random_walk(T: int, sigma: float = 1.0, 
                         y0: float = 0.0, 
                         seed: Optional[int] = None) -> np.ndarray:
    """
    Generate a random walk process.
    
    y_t = y_{t-1} + u_t, where u_t ~ N(0, σ²)
    
    Parameters
    ----------
    T : int
        Sample size
    sigma : float
        Standard deviation of innovations
    y0 : float
        Initial value
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Random walk process of length T
    """
    if seed is not None:
        np.random.seed(seed)
    
    innovations = sigma * np.random.randn(T)
    innovations[0] = y0
    return np.cumsum(innovations)


def generate_ar1_random_walk(T: int, gamma: float = 0.0, 
                              sigma: float = 1.0,
                              y0: float = 0.0,
                              seed: Optional[int] = None) -> np.ndarray:
    """
    Generate random walk with AR(1) innovations.
    
    y_t = y_{t-1} + u_t
    u_t = γ u_{t-1} + ε_t, where ε_t ~ N(0, σ²)
    
    This matches the simulation DGP from Wagner (2012) Eq. (5)-(6).
    
    Parameters
    ----------
    T : int
        Sample size
    gamma : float
        AR(1) coefficient for innovations (0 ≤ γ < 1)
    sigma : float
        Standard deviation of ε_t
    y0 : float
        Initial value
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Random walk with AR(1) errors
    """
    if seed is not None:
        np.random.seed(seed)
    
    if not (0 <= gamma < 1):
        raise ValueError(f"gamma must satisfy 0 ≤ γ < 1. Got γ={gamma}")
    
    # Generate innovations
    eps = sigma * np.random.randn(T)
    u = np.zeros(T)
    u[0] = eps[0]
    
    for t in range(1, T):
        u[t] = gamma * u[t-1] + eps[t]
    
    # Cumulate to get random walk
    y = np.zeros(T)
    y[0] = y0
    for t in range(1, T):
        y[t] = y[t-1] + u[t]
    
    return y


def generate_near_integrated(T: int, c: float = 0.0,
                              sigma: float = 1.0,
                              y0: float = 0.0,
                              seed: Optional[int] = None) -> np.ndarray:
    """
    Generate near-integrated process for local power analysis.
    
    y_t = (1 - c/T) y_{t-1} + ε_t
    
    This matches the local asymptotic power simulation from 
    Stypka & Wagner (2019) Eq. (18).
    
    Parameters
    ----------
    T : int
        Sample size
    c : float
        Local-to-unity parameter (c=0 gives unit root, c>0 is stationary)
    sigma : float
        Standard deviation of innovations
    y0 : float
        Initial value
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Near-integrated process
    """
    if seed is not None:
        np.random.seed(seed)
    
    rho = 1 - c / T
    eps = sigma * np.random.randn(T)
    
    y = np.zeros(T)
    y[0] = y0
    
    for t in range(1, T):
        y[t] = rho * y[t-1] + eps[t]
    
    return y


def generate_stationary_ar1(T: int, rho: float = 0.9,
                            sigma: float = 1.0,
                            seed: Optional[int] = None) -> np.ndarray:
    """
    Generate stationary AR(1) process.
    
    y_t = ρ y_{t-1} + ε_t
    
    Parameters
    ----------
    T : int
        Sample size
    rho : float
        AR(1) coefficient (-1 < ρ < 1)
    sigma : float
        Innovation standard deviation
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Stationary AR(1) process
    """
    if seed is not None:
        np.random.seed(seed)
    
    if not (-1 < rho < 1):
        raise ValueError(f"For stationarity, -1 < ρ < 1. Got ρ={rho}")
    
    eps = sigma * np.random.randn(T)
    
    y = np.zeros(T)
    y[0] = eps[0] * np.sqrt(1 / (1 - rho**2))
    
    for t in range(1, T):
        y[t] = rho * y[t-1] + eps[t]
    
    return y


@dataclass
class MonteCarloResult:
    """Container for Monte Carlo simulation results."""
    rejection_rate: float
    sample_size: int
    n_replications: int
    polynomial_degree: int
    statistic_type: str
    significance_level: float
    dgp_description: str
    mean_statistic: float
    std_statistic: float
    
    def __repr__(self):
        return (f"MonteCarloResult(rejection_rate={self.rejection_rate:.4f}, "
                f"T={self.sample_size}, k={self.polynomial_degree}, "
                f"stat={self.statistic_type})")


def monte_carlo_size(T: int, k: int, 
                      statistic: str = 'Z_rho',
                      gamma: float = 0.0,
                      n_replications: int = 1000,
                      significance: float = 0.05,
                      kernel: str = 'bartlett',
                      seed: Optional[int] = None) -> MonteCarloResult:
    """
    Monte Carlo simulation for empirical size.
    
    Replicates the simulation design from Wagner (2012) Table 2.
    
    Parameters
    ----------
    T : int
        Sample size
    k : int
        Polynomial degree
    statistic : str
        Test statistic to use
    gamma : float
        AR(1) coefficient for innovations
    n_replications : int
        Number of Monte Carlo replications
    significance : float
        Significance level
    kernel : str
        Kernel for HAC estimation
    seed : int, optional
        Random seed
    
    Returns
    -------
    MonteCarloResult
        Simulation results including rejection rate
    """
    from .tests import phillips_polynomial_test
    
    if seed is not None:
        np.random.seed(seed)
    
    rejections = 0
    statistics = []
    
    for i in range(n_replications):
        y = generate_ar1_random_walk(T, gamma=gamma)
        
        try:
            result = phillips_polynomial_test(y, k=k, statistic=statistic,
                                              kernel=kernel)
            statistics.append(result.statistic)
            
            if statistic.lower() in ['z_rho_dstar', 'z_t_dstar']:
                cv = result.critical_values.get(1 - significance, np.inf)
                if result.statistic > cv:
                    rejections += 1
            else:
                cv = result.critical_values.get(significance, -np.inf)
                if result.statistic < cv:
                    rejections += 1
        except Exception:
            continue
    
    n_valid = len(statistics)
    rejection_rate = rejections / n_valid if n_valid > 0 else np.nan
    
    dgp_desc = f"Random walk with AR(1) errors (γ={gamma})"
    
    return MonteCarloResult(
        rejection_rate=rejection_rate,
        sample_size=T,
        n_replications=n_valid,
        polynomial_degree=k,
        statistic_type=statistic,
        significance_level=significance,
        dgp_description=dgp_desc,
        mean_statistic=np.mean(statistics) if statistics else np.nan,
        std_statistic=np.std(statistics) if statistics else np.nan
    )


def monte_carlo_power(T: int, k: int, c: float,
                       statistic: str = 'Z_rho',
                       n_replications: int = 1000,
                       significance: float = 0.05,
                       kernel: str = 'bartlett',
                       seed: Optional[int] = None) -> MonteCarloResult:
    """
    Monte Carlo simulation for empirical local asymptotic power.
    
    Replicates the power analysis from Stypka & Wagner (2019) Figure 2.
    """
    from .tests import phillips_polynomial_test
    
    if seed is not None:
        np.random.seed(seed)
    
    rejections = 0
    statistics = []
    
    for i in range(n_replications):
        y = generate_near_integrated(T, c=c)
        
        try:
            result = phillips_polynomial_test(y, k=k, statistic=statistic,
                                              kernel=kernel)
            statistics.append(result.statistic)
            
            if statistic.lower() in ['z_rho_dstar', 'z_t_dstar']:
                cv = result.critical_values.get(1 - significance, np.inf)
                if result.statistic > cv:
                    rejections += 1
            else:
                cv = result.critical_values.get(significance, -np.inf)
                if result.statistic < cv:
                    rejections += 1
        except Exception:
            continue
    
    n_valid = len(statistics)
    rejection_rate = rejections / n_valid if n_valid > 0 else np.nan
    
    return MonteCarloResult(
        rejection_rate=rejection_rate,
        sample_size=T,
        n_replications=n_valid,
        polynomial_degree=k,
        statistic_type=statistic,
        significance_level=significance,
        dgp_description=f"Near-integrated with c={c}",
        mean_statistic=np.mean(statistics) if statistics else np.nan,
        std_statistic=np.std(statistics) if statistics else np.nan
    )