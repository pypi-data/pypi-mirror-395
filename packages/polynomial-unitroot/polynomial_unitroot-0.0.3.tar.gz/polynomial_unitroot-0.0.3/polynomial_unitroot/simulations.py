"""
Simulation of Limiting Distributions for Unit Root Tests on Polynomials of I(1) Processes.

Based on:
- Wagner, M. (2012). The Phillips unit root tests for polynomials of integrated processes.
  Economics Letters, 114, 299-303.
- Stypka, O., & Wagner, M. (2019). The Phillips unit root tests for polynomials of 
  integrated processes revisited. Economics Letters, 176, 109-113.

This module simulates the limiting distributions given in:
- Wagner (2012) Corollary 1 (serially uncorrelated case)
- Stypka & Wagner (2019) Proposition 1 and Corollary 1

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
GitHub: https://github.com/merwanroudane/polyunitroottest
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
from scipy import stats


def simulate_brownian_motion(T: int = 1000, n_paths: int = 1, 
                             seed: Optional[int] = None) -> np.ndarray:
    """
    Simulate standard Brownian motion paths.
    
    W(r) for r ∈ [0, 1] is approximated using partial sums of i.i.d. N(0,1) variables.
    
    Parameters
    ----------
    T : int
        Number of time points (discretization fineness)
    n_paths : int
        Number of paths to simulate
    seed : int, optional
        Random seed for reproducibility
    
    Returns
    -------
    np.ndarray
        Array of shape (n_paths, T) containing Brownian motion paths
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate standard normal increments
    dW = np.random.standard_normal((n_paths, T)) / np.sqrt(T)
    
    # Cumulative sum to get Brownian motion
    W = np.cumsum(dW, axis=1)
    
    return W


def simulate_stochastic_integral(W: np.ndarray, power: int) -> np.ndarray:
    """
    Simulate ∫₀¹ W(r)^p dW(r) using Riemann-Stieltjes approximation.
    
    Uses the Itô integral approximation:
    ∫₀¹ W(r)^p dW(r) ≈ Σ_{i=0}^{T-1} W(i/T)^p * (W((i+1)/T) - W(i/T))
    
    Parameters
    ----------
    W : np.ndarray
        Brownian motion paths of shape (n_paths, T)
    power : int
        Power p for W(r)^p
    
    Returns
    -------
    np.ndarray
        Array of shape (n_paths,) containing the simulated integrals
    """
    # Increments: dW = W(t+1) - W(t)
    dW = np.diff(W, axis=1)
    
    # W^p at each time point (excluding last)
    W_power = W[:, :-1] ** power
    
    # Riemann-Stieltjes sum
    integral = np.sum(W_power * dW, axis=1)
    
    return integral


def simulate_time_integral(W: np.ndarray, power: int) -> np.ndarray:
    """
    Simulate ∫₀¹ W(r)^p dr using trapezoidal rule.
    
    Parameters
    ----------
    W : np.ndarray
        Brownian motion paths of shape (n_paths, T)
    power : int
        Power p for W(r)^p
    
    Returns
    -------
    np.ndarray
        Array of shape (n_paths,) containing the simulated integrals
    """
    T = W.shape[1]
    dt = 1.0 / T
    
    # W^p at each time point
    W_power = W ** power
    
    # Trapezoidal integration
    integral = dt * (0.5 * W_power[:, 0] + np.sum(W_power[:, 1:-1], axis=1) + 
                     0.5 * W_power[:, -1])
    
    return integral


def simulate_Z_rho_distribution(k: int, n_simulations: int = 50000,
                                T: int = 1000, seed: Optional[int] = None) -> np.ndarray:
    """
    Simulate the limiting distribution of Z_ρ statistic.
    
    From Stypka & Wagner (2019) Proposition 1:
    Z_ρ ⇒ [k∫₀¹W(r)^{2k-1}dW(r) + (k choose 2)∫₀¹W(r)^{2(k-1)}dr] / ∫₀¹W(r)^{2k}dr
    
    Parameters
    ----------
    k : int
        Polynomial degree (≥ 1)
    n_simulations : int
        Number of Monte Carlo simulations
    T : int
        Discretization fineness
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Simulated distribution values
    """
    if seed is not None:
        np.random.seed(seed)
    
    results = np.zeros(n_simulations)
    batch_size = min(1000, n_simulations)
    
    for i in range(0, n_simulations, batch_size):
        current_batch = min(batch_size, n_simulations - i)
        
        # Simulate Brownian motions
        W = simulate_brownian_motion(T, current_batch)
        
        # Compute integrals
        # ∫ W^{2k-1} dW
        int_stoch = simulate_stochastic_integral(W, 2*k - 1)
        
        # ∫ W^{2(k-1)} dr
        int_bias = simulate_time_integral(W, 2*(k - 1))
        
        # ∫ W^{2k} dr
        int_denom = simulate_time_integral(W, 2*k)
        
        # Binomial coefficient (k choose 2) = k(k-1)/2
        binom_k2 = k * (k - 1) / 2
        
        # Z_ρ = [k * int_stoch + binom_k2 * int_bias] / int_denom
        numerator = k * int_stoch + binom_k2 * int_bias
        results[i:i+current_batch] = numerator / int_denom
    
    return results


def simulate_Z_t_distribution(k: int, n_simulations: int = 50000,
                               T: int = 1000, seed: Optional[int] = None) -> np.ndarray:
    """
    Simulate the limiting distribution of Z_t statistic.
    
    From Stypka & Wagner (2019) Proposition 1:
    Z_t ⇒ [∫₀¹W(r)^{2k-1}dW(r) + (k-1)/2 * ∫₀¹W(r)^{2(k-1)}dr] / 
          √[∫₀¹W(r)^{2(k-1)}dr * ∫₀¹W(r)^{2k}dr]
    
    Parameters
    ----------
    k : int
        Polynomial degree
    n_simulations : int
        Number of simulations
    T : int
        Discretization fineness
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Simulated distribution values
    """
    if seed is not None:
        np.random.seed(seed)
    
    results = np.zeros(n_simulations)
    batch_size = min(1000, n_simulations)
    
    for i in range(0, n_simulations, batch_size):
        current_batch = min(batch_size, n_simulations - i)
        
        W = simulate_brownian_motion(T, current_batch)
        
        int_stoch = simulate_stochastic_integral(W, 2*k - 1)
        int_bias = simulate_time_integral(W, 2*(k - 1))
        int_denom = simulate_time_integral(W, 2*k)
        
        # Z_t numerator: ∫W^{2k-1}dW + (k-1)/2 * ∫W^{2(k-1)}dr
        numerator = int_stoch + (k - 1) / 2 * int_bias
        
        # Z_t denominator: √(∫W^{2(k-1)}dr * ∫W^{2k}dr)
        denominator = np.sqrt(int_bias * int_denom)
        
        results[i:i+current_batch] = numerator / denominator
    
    return results


def simulate_Z_rho_star_distribution(k: int, n_simulations: int = 50000,
                                      T: int = 1000, seed: Optional[int] = None) -> np.ndarray:
    """
    Simulate the limiting distribution of Z*_ρ statistic (bias-corrected).
    
    From Stypka & Wagner (2019) Corollary 1:
    Z*_ρ ⇒ k∫₀¹W(r)^{2k-1}dW(r) / ∫₀¹W(r)^{2k}dr
    
    Parameters
    ----------
    k : int
        Polynomial degree
    n_simulations : int
        Number of simulations
    T : int
        Discretization fineness
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Simulated distribution values
    """
    if seed is not None:
        np.random.seed(seed)
    
    results = np.zeros(n_simulations)
    batch_size = min(1000, n_simulations)
    
    for i in range(0, n_simulations, batch_size):
        current_batch = min(batch_size, n_simulations - i)
        
        W = simulate_brownian_motion(T, current_batch)
        
        int_stoch = simulate_stochastic_integral(W, 2*k - 1)
        int_denom = simulate_time_integral(W, 2*k)
        
        # Z*_ρ = k * ∫W^{2k-1}dW / ∫W^{2k}dr
        results[i:i+current_batch] = k * int_stoch / int_denom
    
    return results


def simulate_Z_t_star_distribution(k: int, n_simulations: int = 50000,
                                    T: int = 1000, seed: Optional[int] = None) -> np.ndarray:
    """
    Simulate the limiting distribution of Z*_t statistic (bias-corrected).
    
    From Stypka & Wagner (2019) Corollary 1:
    Z*_t ⇒ ∫₀¹W(r)^{2k-1}dW(r) / √[∫₀¹W(r)^{2(k-1)}dr * ∫₀¹W(r)^{2k}dr]
    
    Parameters
    ----------
    k : int
        Polynomial degree
    n_simulations : int
        Number of simulations
    T : int
        Discretization fineness
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Simulated distribution values
    """
    if seed is not None:
        np.random.seed(seed)
    
    results = np.zeros(n_simulations)
    batch_size = min(1000, n_simulations)
    
    for i in range(0, n_simulations, batch_size):
        current_batch = min(batch_size, n_simulations - i)
        
        W = simulate_brownian_motion(T, current_batch)
        
        int_stoch = simulate_stochastic_integral(W, 2*k - 1)
        int_bias = simulate_time_integral(W, 2*(k - 1))
        int_denom = simulate_time_integral(W, 2*k)
        
        # Z*_t = ∫W^{2k-1}dW / √(∫W^{2(k-1)}dr * ∫W^{2k}dr)
        denominator = np.sqrt(int_bias * int_denom)
        results[i:i+current_batch] = int_stoch / denominator
    
    return results


def simulate_Z_rho_dstar_distribution(k: int, n_simulations: int = 50000,
                                       T: int = 1000, seed: Optional[int] = None) -> np.ndarray:
    """
    Simulate the limiting distribution of Z**_ρ statistic (Itô-based).
    
    From Stypka & Wagner (2019) Corollary 1:
    Z**_ρ ⇒ W(1)^{2k} / (2∫₀¹W(r)^{2k}dr)
    
    Parameters
    ----------
    k : int
        Polynomial degree
    n_simulations : int
        Number of simulations
    T : int
        Discretization fineness
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Simulated distribution values
    """
    if seed is not None:
        np.random.seed(seed)
    
    results = np.zeros(n_simulations)
    batch_size = min(1000, n_simulations)
    
    for i in range(0, n_simulations, batch_size):
        current_batch = min(batch_size, n_simulations - i)
        
        W = simulate_brownian_motion(T, current_batch)
        
        # W(1) is the final value
        W1 = W[:, -1]
        
        # ∫W^{2k}dr
        int_denom = simulate_time_integral(W, 2*k)
        
        # Z**_ρ = W(1)^{2k} / (2 * ∫W^{2k}dr)
        results[i:i+current_batch] = (W1 ** (2*k)) / (2 * int_denom)
    
    return results


def simulate_Z_t_dstar_distribution(k: int, n_simulations: int = 50000,
                                     T: int = 1000, seed: Optional[int] = None) -> np.ndarray:
    """
    Simulate the limiting distribution of Z**_t statistic (Itô-based).
    
    From Stypka & Wagner (2019) Corollary 1:
    Z**_t ⇒ W(1)^{2k} / (2k√[∫₀¹W(r)^{2(k-1)}dr * ∫₀¹W(r)^{2k}dr])
    
    Parameters
    ----------
    k : int
        Polynomial degree
    n_simulations : int
        Number of simulations
    T : int
        Discretization fineness
    seed : int, optional
        Random seed
    
    Returns
    -------
    np.ndarray
        Simulated distribution values
    """
    if seed is not None:
        np.random.seed(seed)
    
    results = np.zeros(n_simulations)
    batch_size = min(1000, n_simulations)
    
    for i in range(0, n_simulations, batch_size):
        current_batch = min(batch_size, n_simulations - i)
        
        W = simulate_brownian_motion(T, current_batch)
        
        W1 = W[:, -1]
        int_bias = simulate_time_integral(W, 2*(k - 1))
        int_denom = simulate_time_integral(W, 2*k)
        
        # Z**_t = W(1)^{2k} / (2k * √(∫W^{2(k-1)}dr * ∫W^{2k}dr))
        denominator = 2 * k * np.sqrt(int_bias * int_denom)
        results[i:i+current_batch] = (W1 ** (2*k)) / denominator
    
    return results


def simulate_all_distributions(k: int, n_simulations: int = 50000,
                               T: int = 1000, seed: Optional[int] = None) -> Dict[str, np.ndarray]:
    """
    Simulate all six test statistic distributions for a given k.
    
    Parameters
    ----------
    k : int
        Polynomial degree
    n_simulations : int
        Number of simulations
    T : int
        Discretization fineness
    seed : int, optional
        Random seed
    
    Returns
    -------
    dict
        Dictionary with keys: 'Z_rho', 'Z_t', 'Z_rho_star', 'Z_t_star', 
                              'Z_rho_dstar', 'Z_t_dstar'
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate Brownian motions once
    W = simulate_brownian_motion(T, n_simulations)
    
    # Compute all required integrals
    int_stoch = simulate_stochastic_integral(W, 2*k - 1)  # ∫W^{2k-1}dW
    int_bias = simulate_time_integral(W, 2*(k - 1))        # ∫W^{2(k-1)}dr
    int_denom = simulate_time_integral(W, 2*k)             # ∫W^{2k}dr
    W1 = W[:, -1]                                           # W(1)
    
    binom_k2 = k * (k - 1) / 2
    
    # Z_ρ
    Z_rho = (k * int_stoch + binom_k2 * int_bias) / int_denom
    
    # Z_t
    Z_t = (int_stoch + (k - 1) / 2 * int_bias) / np.sqrt(int_bias * int_denom)
    
    # Z*_ρ
    Z_rho_star = k * int_stoch / int_denom
    
    # Z*_t
    Z_t_star = int_stoch / np.sqrt(int_bias * int_denom)
    
    # Z**_ρ
    Z_rho_dstar = (W1 ** (2*k)) / (2 * int_denom)
    
    # Z**_t
    Z_t_dstar = (W1 ** (2*k)) / (2 * k * np.sqrt(int_bias * int_denom))
    
    return {
        'Z_rho': Z_rho,
        'Z_t': Z_t,
        'Z_rho_star': Z_rho_star,
        'Z_t_star': Z_t_star,
        'Z_rho_dstar': Z_rho_dstar,
        'Z_t_dstar': Z_t_dstar
    }


def compute_critical_values(distribution: np.ndarray,
                            percentiles: List[float] = None) -> Dict:
    """
    Compute critical values from simulated distribution.
    
    Parameters
    ----------
    distribution : np.ndarray
        Simulated distribution values
    percentiles : list of float, optional
        Percentiles to compute. Default: [0.01, 0.025, 0.05, 0.5, 0.95, 0.975, 0.99]
    
    Returns
    -------
    dict
        Dictionary with percentiles and summary statistics
    """
    if percentiles is None:
        percentiles = [0.01, 0.025, 0.05, 0.5, 0.95, 0.975, 0.99]
    
    result = {}
    for p in percentiles:
        result[p] = np.percentile(distribution, p * 100)
    
    result['mean'] = np.mean(distribution)
    result['std'] = np.std(distribution)
    result['median'] = np.median(distribution)
    
    return result


def generate_critical_value_table(k_values: List[int] = [1, 2, 3],
                                   n_simulations: int = 50000,
                                   T: int = 1000,
                                   seed: Optional[int] = None) -> Dict:
    """
    Generate complete critical value tables for all statistics.
    
    This replicates the simulation procedure from Wagner (2012) and 
    Stypka & Wagner (2019) to generate Table 1.
    
    Parameters
    ----------
    k_values : list of int
        Polynomial degrees to simulate
    n_simulations : int
        Number of Monte Carlo replications
    T : int
        Sample size for approximating Brownian motion functionals
    seed : int, optional
        Random seed for reproducibility
    
    Returns
    -------
    dict
        Nested dictionary: {statistic: {k: {percentile: value}}}
    """
    results = {
        'Z_rho': {}, 'Z_t': {},
        'Z_rho_star': {}, 'Z_t_star': {},
        'Z_rho_dstar': {}, 'Z_t_dstar': {}
    }
    
    for k in k_values:
        print(f"Simulating distributions for k={k}...")
        
        # Use different seed for each k to ensure independence
        k_seed = seed + k if seed is not None else None
        distributions = simulate_all_distributions(k, n_simulations, T, k_seed)
        
        for stat_name, dist in distributions.items():
            results[stat_name][k] = compute_critical_values(dist)
    
    return results


def print_critical_value_table(cv_table: Dict, statistic: str = 'Z_rho'):
    """
    Print critical value table in publication format.
    
    Parameters
    ----------
    cv_table : dict
        Output from generate_critical_value_table()
    statistic : str
        Which statistic to print
    """
    print(f"\nCritical Values for {statistic}")
    print("=" * 80)
    
    percentiles = [0.01, 0.025, 0.05, 0.5, 0.95, 0.975, 0.99]
    
    # Header
    header = "k".ljust(4)
    for p in percentiles:
        header += f"{p:.3f}".rjust(10)
    header += "Mean".rjust(10) + "Std".rjust(10)
    print(header)
    print("-" * 80)
    
    # Values for each k
    for k in sorted(cv_table[statistic].keys()):
        row = str(k).ljust(4)
        cv = cv_table[statistic][k]
        for p in percentiles:
            row += f"{cv[p]:.3f}".rjust(10)
        row += f"{cv['mean']:.3f}".rjust(10) + f"{cv['std']:.3f}".rjust(10)
        print(row)


def verify_against_published_values(generated: Dict, k: int = 2,
                                     tolerance: float = 0.5) -> bool:
    """
    Verify generated critical values against published values.
    
    Parameters
    ----------
    generated : dict
        Generated critical values
    k : int
        Polynomial degree to check
    tolerance : float
        Acceptable deviation from published values
    
    Returns
    -------
    bool
        True if values match within tolerance
    """
    # Published values from Stypka & Wagner (2019), Table 1
    published = {
        'Z_rho': {
            2: {0.05: -13.574, 0.5: -2.236, 'mean': -3.369}
        },
        'Z_t': {
            2: {0.05: -2.590, 0.5: -0.946, 'mean': -0.736}
        }
    }
    
    all_match = True
    for stat in ['Z_rho', 'Z_t']:
        for p, pub_val in published[stat][k].items():
            gen_val = generated[stat][k][p]
            if abs(gen_val - pub_val) > tolerance:
                print(f"Mismatch for {stat}, k={k}, p={p}: "
                      f"generated={gen_val:.3f}, published={pub_val:.3f}")
                all_match = False
    
    return all_match
