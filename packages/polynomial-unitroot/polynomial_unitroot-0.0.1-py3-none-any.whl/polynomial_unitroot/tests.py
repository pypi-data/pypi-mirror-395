"""
Phillips Unit Root Tests for Polynomials of Integrated Processes.

This module implements the unit root tests from:
- Wagner, M. (2012). The Phillips unit root tests for polynomials of integrated processes.
  Economics Letters, 114, 299-303.
- Stypka, O., & Wagner, M. (2019). The Phillips unit root tests for polynomials of 
  integrated processes revisited. Economics Letters, 176, 109-113.

Test Statistics Implemented:
- T(ρ̂ - 1): Coefficient statistic (Wagner, 2012)
- t_ρ: t-statistic (Wagner, 2012)  
- Z_ρ: Phillips-type coefficient statistic (Stypka & Wagner, 2019)
- Z_t: Phillips-type t-statistic (Stypka & Wagner, 2019)
- Z*_ρ: Bias-corrected coefficient statistic (Stypka & Wagner, 2019)
- Z*_t: Bias-corrected t-statistic (Stypka & Wagner, 2019)
- Z**_ρ: Itô-based coefficient statistic (Stypka & Wagner, 2019)
- Z**_t: Itô-based t-statistic (Stypka & Wagner, 2019)

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
GitHub: https://github.com/merwanroudane/polyunitroottest
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Union
import warnings

from .kernels import (estimate_variances, estimate_long_run_variance,
                      estimate_half_long_run_variance, get_kernel,
                      compute_bandwidth)
from .critical_values import (get_critical_value, get_all_critical_values,
                               p_value, interpolate_critical_value)


@dataclass
class PolynomialUnitRootResult:
    """
    Result container for polynomial unit root tests.
    
    Attributes
    ----------
    statistic : float
        Test statistic value
    statistic_type : str
        Type of statistic ('Z_rho', 'Z_t', etc.)
    k : int
        Polynomial degree
    critical_values : dict
        Critical values at different significance levels
    p_value : float
        Approximate p-value
    reject_null : dict
        Whether to reject H0 at 1%, 5%, 10% levels
    rho_hat : float
        Estimated serial correlation coefficient
    t_stat : float
        t-statistic for ρ = 1
    variance_estimates : dict
        Estimated variances (σ², ω, λ)
    bandwidth : int
        Bandwidth used for HAC estimation
    sample_size : int
        Number of observations
    method : str
        Description of the test method
    """
    statistic: float
    statistic_type: str
    k: int
    critical_values: Dict
    p_value: float
    reject_null: Dict
    rho_hat: float
    t_stat: float
    variance_estimates: Dict
    bandwidth: int
    sample_size: int
    method: str
    
    def __repr__(self):
        return self._format_output()
    
    def _format_output(self) -> str:
        """Format results for publication-quality output."""
        lines = []
        lines.append("=" * 70)
        lines.append("Phillips Unit Root Test for Polynomials of Integrated Processes")
        lines.append("=" * 70)
        lines.append(f"Polynomial degree (k): {self.k}")
        lines.append(f"Sample size: {self.sample_size}")
        lines.append(f"Bandwidth: {self.bandwidth}")
        lines.append("")
        lines.append(f"Test statistic ({self.statistic_type}): {self.statistic:.4f}")
        lines.append(f"Estimated ρ: {self.rho_hat:.6f}")
        lines.append(f"t-statistic: {self.t_stat:.4f}")
        lines.append("")
        lines.append("Critical Values:")
        lines.append("-" * 40)
        for level, cv in sorted(self.critical_values.items()):
            if isinstance(level, float):
                lines.append(f"  {int(level*100):3d}%: {cv:.4f}")
        lines.append("")
        lines.append(f"Approximate p-value: {self.p_value:.4f}")
        lines.append("")
        lines.append("Null Hypothesis Rejection:")
        lines.append("-" * 40)
        for level, reject in self.reject_null.items():
            result = "Reject" if reject else "Fail to Reject"
            lines.append(f"  {level}: {result}")
        lines.append("")
        lines.append("Variance Estimates:")
        lines.append("-" * 40)
        lines.append(f"  σ²_v: {self.variance_estimates['sigma2']:.6f}")
        lines.append(f"  ω_v:  {self.variance_estimates['omega']:.6f}")
        lines.append(f"  λ_v:  {self.variance_estimates['lambda']:.6f}")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def summary(self) -> str:
        """Return a brief summary of results."""
        return (f"{self.statistic_type} = {self.statistic:.4f}, "
                f"p-value = {self.p_value:.4f}, "
                f"Reject at 5%: {self.reject_null['5%']}")


def polynomial_transform(y: np.ndarray, k: int) -> np.ndarray:
    """
    Compute the k-th power of a time series.
    
    Following Wagner (2012) and Stypka & Wagner (2019), the polynomial 
    transformation x_t = y_t^k is considered since asymptotically only 
    the highest order term matters.
    
    Parameters
    ----------
    y : np.ndarray
        Integrated process y_t
    k : int
        Polynomial degree
    
    Returns
    -------
    np.ndarray
        x_t = y_t^k
    """
    return y ** k


def estimate_regression(x: np.ndarray) -> Tuple[float, float, np.ndarray]:
    """
    Estimate the first-order autoregression x_t = ρ x_{t-1} + v_t.
    
    Following Eq. (3)-(5) in Stypka & Wagner (2019):
    - ρ̂ = Σ x_t x_{t-1} / Σ x²_{t-1}
    - t_ρ = (ρ̂ - 1) / √(σ̂²_v * (Σ x²_{t-1})^{-1})
    - σ̂²_v = (1/T) Σ v̂²_t
    
    Parameters
    ----------
    x : np.ndarray
        Polynomial transformed series x_t
    
    Returns
    -------
    rho_hat : float
        OLS estimate of ρ
    t_stat : float
        t-statistic for H₀: ρ = 1
    residuals : np.ndarray
        OLS residuals v̂_t = x_t - ρ̂ x_{t-1}
    """
    T = len(x)
    
    # x_{t-1} and x_t for t = 2, ..., T
    x_lag = x[:-1]  # x_{t-1}
    x_t = x[1:]     # x_t
    
    # OLS estimator: ρ̂ = Σ x_t x_{t-1} / Σ x²_{t-1}
    sum_xx_lag = np.sum(x_lag * x_t)
    sum_x_lag_sq = np.sum(x_lag ** 2)
    
    if sum_x_lag_sq == 0:
        raise ValueError("Sum of squared lagged values is zero. Check input data.")
    
    rho_hat = sum_xx_lag / sum_x_lag_sq
    
    # Residuals: v̂_t = x_t - ρ̂ x_{t-1}
    residuals = x_t - rho_hat * x_lag
    
    # Variance estimate: σ̂²_v = (1/T) Σ v̂²_t
    sigma2_v = np.mean(residuals ** 2)
    
    # t-statistic: t_ρ = (ρ̂ - 1) / √(σ̂²_v / Σ x²_{t-1})
    t_stat = (rho_hat - 1) / np.sqrt(sigma2_v / sum_x_lag_sq)
    
    return rho_hat, t_stat, residuals


def compute_Z_rho(rho_hat: float, T: int, sum_x_lag_sq: float,
                  lambda_v: float) -> float:
    """
    Compute Phillips-type Z_ρ statistic.
    
    From Eq. (6) in Stypka & Wagner (2019):
    Z_ρ = T(ρ̂ - 1) - λ̂_v / ((1/T²) Σ x²_{t-1})
    
    Parameters
    ----------
    rho_hat : float
        Estimated serial correlation coefficient
    T : int
        Sample size
    sum_x_lag_sq : float
        Sum of squared lagged values Σ x²_{t-1}
    lambda_v : float
        Estimated half long-run variance
    
    Returns
    -------
    float
        Z_ρ statistic
    """
    # (1/T²) Σ x²_{t-1}
    scaled_sum = sum_x_lag_sq / (T ** 2)
    
    return T * (rho_hat - 1) - lambda_v / scaled_sum


def compute_Z_t(t_stat: float, sigma2_v: float, omega_v: float,
                T: int, sum_x_lag_sq: float, lambda_v: float) -> float:
    """
    Compute Phillips-type Z_t statistic.
    
    From Eq. (7) in Stypka & Wagner (2019):
    Z_t = √(σ̂²_v/ω̂_v) * t_ρ - (λ̂_v/√ω̂_v) / ((1/T²) Σ x²_{t-1})
    
    Parameters
    ----------
    t_stat : float
        t-statistic for ρ = 1
    sigma2_v : float
        Short-run variance estimate
    omega_v : float
        Long-run variance estimate
    T : int
        Sample size
    sum_x_lag_sq : float
        Sum of squared lagged values
    lambda_v : float
        Half long-run variance estimate
    
    Returns
    -------
    float
        Z_t statistic
    """
    scaled_sum = sum_x_lag_sq / (T ** 2)
    
    return (np.sqrt(sigma2_v / omega_v) * t_stat - 
            (lambda_v / np.sqrt(omega_v)) / scaled_sum)


def compute_Z_rho_star(rho_hat: float, T: int, sum_x_lag_sq: float,
                       lambda_v: float, omega_v: float, k: int) -> float:
    """
    Compute bias-corrected Z*_ρ statistic.
    
    From Eq. (10) in Stypka & Wagner (2019):
    Z*_ρ = Z_ρ - ((k-1)ω̂_v)/(2k * (1/T²) Σ x²_{t-1})
    
    This removes the additive bias term (k choose 2)∫W^{2(k-1)}dr from 
    the limiting distribution.
    
    Parameters
    ----------
    rho_hat : float
        Estimated serial correlation coefficient
    T : int
        Sample size
    sum_x_lag_sq : float
        Sum of squared lagged values
    lambda_v : float
        Half long-run variance
    omega_v : float
        Long-run variance
    k : int
        Polynomial degree
    
    Returns
    -------
    float
        Z*_ρ statistic
    """
    scaled_sum = sum_x_lag_sq / (T ** 2)
    
    Z_rho = T * (rho_hat - 1) - lambda_v / scaled_sum
    
    # Additional correction term
    correction = ((k - 1) * omega_v) / (2 * k * scaled_sum)
    
    return Z_rho - correction


def compute_Z_t_star(t_stat: float, sigma2_v: float, omega_v: float,
                     T: int, sum_x_lag_sq: float, lambda_v: float, k: int) -> float:
    """
    Compute bias-corrected Z*_t statistic.
    
    From Eq. (11) in Stypka & Wagner (2019):
    Z*_t = Z_t - ((k-1)ω̂_v)/(2k√ω̂_v * (1/T²) Σ x²_{t-1})
    
    Parameters
    ----------
    t_stat : float
        t-statistic
    sigma2_v : float
        Short-run variance
    omega_v : float
        Long-run variance
    T : int
        Sample size
    sum_x_lag_sq : float
        Sum of squared lagged values
    lambda_v : float
        Half long-run variance
    k : int
        Polynomial degree
    
    Returns
    -------
    float
        Z*_t statistic
    """
    scaled_sum = sum_x_lag_sq / (T ** 2)
    
    Z_t = (np.sqrt(sigma2_v / omega_v) * t_stat - 
           (lambda_v / np.sqrt(omega_v)) / scaled_sum)
    
    # Additional correction term
    correction = ((k - 1) * omega_v) / (2 * k * np.sqrt(omega_v) * scaled_sum)
    
    return Z_t - correction


def compute_Z_rho_dstar(rho_hat: float, T: int, sum_x_lag_sq: float,
                        sigma2_v: float) -> float:
    """
    Compute Itô-based Z**_ρ statistic.
    
    From Eq. (12) in Stypka & Wagner (2019):
    Z**_ρ = T(ρ̂ - 1) + σ̂²_v / (2 * (1/T²) Σ x²_{t-1})
    
    The limiting distribution involves W(1)^{2k}, the k-th power of a 
    chi-squared random variable with one degree of freedom.
    
    Parameters
    ----------
    rho_hat : float
        Estimated serial correlation coefficient
    T : int
        Sample size
    sum_x_lag_sq : float
        Sum of squared lagged values
    sigma2_v : float
        Short-run variance
    
    Returns
    -------
    float
        Z**_ρ statistic
    """
    scaled_sum = sum_x_lag_sq / (T ** 2)
    
    return T * (rho_hat - 1) + sigma2_v / (2 * scaled_sum)


def compute_Z_t_dstar(t_stat: float, sigma2_v: float, omega_v: float,
                      T: int, sum_x_lag_sq: float) -> float:
    """
    Compute Itô-based Z**_t statistic.
    
    From Eq. (13) in Stypka & Wagner (2019):
    Z**_t = √(σ̂²_v/ω̂_v) * t_ρ + σ̂²_v / (2√ω̂_v * (1/T²) Σ x²_{t-1})
    
    Parameters
    ----------
    t_stat : float
        t-statistic
    sigma2_v : float
        Short-run variance
    omega_v : float
        Long-run variance
    T : int
        Sample size
    sum_x_lag_sq : float
        Sum of squared lagged values
    
    Returns
    -------
    float
        Z**_t statistic
    """
    scaled_sum = sum_x_lag_sq / (T ** 2)
    
    return (np.sqrt(sigma2_v / omega_v) * t_stat + 
            sigma2_v / (2 * np.sqrt(omega_v) * scaled_sum))


def phillips_polynomial_test(y: np.ndarray, k: int = 2,
                              statistic: str = 'Z_rho',
                              kernel: str = 'bartlett',
                              bandwidth: Optional[int] = None,
                              bandwidth_method: str = 'andrews') -> PolynomialUnitRootResult:
    """
    Perform Phillips unit root test for polynomials of integrated processes.
    
    This function tests the null hypothesis that y_t is an I(1) process
    against the alternative that it is stationary, using the polynomial
    transformation x_t = y_t^k.
    
    Parameters
    ----------
    y : np.ndarray
        Time series to test (assumed to be an I(1) process under H₀)
    k : int
        Polynomial degree (typically 1, 2, or 3)
    statistic : str
        Test statistic to compute:
        - 'Z_rho': Phillips coefficient statistic (default)
        - 'Z_t': Phillips t-statistic
        - 'Z_rho_star': Bias-corrected coefficient statistic
        - 'Z_t_star': Bias-corrected t-statistic
        - 'Z_rho_dstar': Itô-based coefficient statistic
        - 'Z_t_dstar': Itô-based t-statistic
    kernel : str
        Kernel function for HAC estimation ('bartlett', 'parzen', 'qs')
    bandwidth : int, optional
        Bandwidth for HAC estimation. If None, computed automatically
    bandwidth_method : str
        Method for automatic bandwidth selection ('andrews', 'newey_west')
    
    Returns
    -------
    PolynomialUnitRootResult
        Test results including statistic, critical values, and decision
    
    Notes
    -----
    The test is based on the regression:
        x_t = ρ x_{t-1} + v_t
    
    where x_t = y_t^k. Under the null hypothesis that y_t ~ I(1), the 
    limiting distributions are given in Stypka & Wagner (2019).
    
    For k=1, this reduces to the standard Phillips (1987) unit root test.
    For k>1, the test applies to polynomials of integrated processes.
    
    References
    ----------
    Wagner, M. (2012). The Phillips unit root tests for polynomials of 
    integrated processes. Economics Letters, 114, 299-303.
    
    Stypka, O., & Wagner, M. (2019). The Phillips unit root tests for 
    polynomials of integrated processes revisited. Economics Letters, 
    176, 109-113.
    
    Examples
    --------
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> # Generate random walk
    >>> y = np.cumsum(np.random.randn(200))
    >>> # Test on squared process (k=2)
    >>> result = phillips_polynomial_test(y, k=2, statistic='Z_rho')
    >>> print(result.summary())
    """
    y = np.asarray(y, dtype=float)
    T = len(y)
    
    if T < 20:
        raise ValueError(f"Sample size T={T} is too small. Need at least 20 observations.")
    
    if k < 1:
        raise ValueError(f"Polynomial degree k must be >= 1. Got k={k}")
    
    if k > 3:
        warnings.warn(f"Critical values for k={k} are not tabulated. "
                      "Results may be unreliable.", UserWarning)
    
    # Polynomial transformation
    x = polynomial_transform(y, k)
    
    # Estimate regression
    rho_hat, t_stat, residuals = estimate_regression(x)
    
    # Compute variance estimates using HAC
    var_est = estimate_variances(residuals, kernel=kernel, 
                                  bandwidth=bandwidth,
                                  bandwidth_method=bandwidth_method)
    
    sigma2_v = var_est['sigma2']
    omega_v = var_est['omega']
    lambda_v = var_est['lambda']
    bw = var_est['bandwidth']
    
    # Sum of squared lagged values (T-1 terms)
    x_lag = x[:-1]
    sum_x_lag_sq = np.sum(x_lag ** 2)
    
    # Compute test statistic
    stat_lower = statistic.lower()
    
    if stat_lower == 'z_rho':
        test_stat = compute_Z_rho(rho_hat, T, sum_x_lag_sq, lambda_v)
        stat_type = 'Z_rho'
    elif stat_lower == 'z_t':
        test_stat = compute_Z_t(t_stat, sigma2_v, omega_v, T, 
                                sum_x_lag_sq, lambda_v)
        stat_type = 'Z_t'
    elif stat_lower == 'z_rho_star':
        test_stat = compute_Z_rho_star(rho_hat, T, sum_x_lag_sq, 
                                        lambda_v, omega_v, k)
        stat_type = 'Z_rho_star'
    elif stat_lower == 'z_t_star':
        test_stat = compute_Z_t_star(t_stat, sigma2_v, omega_v, T,
                                      sum_x_lag_sq, lambda_v, k)
        stat_type = 'Z_t_star'
    elif stat_lower == 'z_rho_dstar':
        test_stat = compute_Z_rho_dstar(rho_hat, T, sum_x_lag_sq, sigma2_v)
        stat_type = 'Z_rho_dstar'
    elif stat_lower == 'z_t_dstar':
        test_stat = compute_Z_t_dstar(t_stat, sigma2_v, omega_v, T, sum_x_lag_sq)
        stat_type = 'Z_t_dstar'
    else:
        raise ValueError(f"Unknown statistic: {statistic}. "
                        f"Choose from: Z_rho, Z_t, Z_rho_star, Z_t_star, "
                        f"Z_rho_dstar, Z_t_dstar")
    
    # Get critical values
    k_cv = min(k, 3)  # Use k=3 critical values for k>3
    try:
        cv = get_all_critical_values(stat_type, k_cv)
        pval = p_value(test_stat, stat_type, k_cv)
    except ValueError:
        # Fall back for statistics that might not be in the tables
        cv = {0.01: np.nan, 0.05: np.nan, 0.10: np.nan}
        pval = np.nan
    
    # Determine rejection at different levels
    # Note: For Z**_ρ and Z**_t, rejection is for large positive values
    if stat_type in ['Z_rho_dstar', 'Z_t_dstar']:
        reject = {
            '1%': test_stat > cv.get(0.99, np.inf),
            '5%': test_stat > cv.get(0.95, np.inf),
            '10%': test_stat > cv.get(0.90, cv.get(0.95, np.inf))
        }
    else:
        # For other statistics, rejection is for small (negative) values
        reject = {
            '1%': test_stat < cv.get(0.01, -np.inf),
            '5%': test_stat < cv.get(0.05, -np.inf),
            '10%': test_stat < cv.get(0.10, cv.get(0.05, -np.inf))
        }
    
    # Method description
    method_desc = (f"Phillips unit root test for y^{k} using {stat_type} "
                   f"with {kernel} kernel (bandwidth={bw})")
    
    return PolynomialUnitRootResult(
        statistic=test_stat,
        statistic_type=stat_type,
        k=k,
        critical_values=cv,
        p_value=pval,
        reject_null=reject,
        rho_hat=rho_hat,
        t_stat=t_stat,
        variance_estimates=var_est,
        bandwidth=bw,
        sample_size=T,
        method=method_desc
    )


def all_phillips_tests(y: np.ndarray, k: int = 2,
                       kernel: str = 'bartlett',
                       bandwidth: Optional[int] = None,
                       bandwidth_method: str = 'andrews') -> Dict[str, PolynomialUnitRootResult]:
    """
    Compute all six Phillips test statistics for polynomials of integrated processes.
    
    Parameters
    ----------
    y : np.ndarray
        Time series to test
    k : int
        Polynomial degree
    kernel : str
        Kernel function for HAC estimation
    bandwidth : int, optional
        Bandwidth for HAC estimation
    bandwidth_method : str
        Bandwidth selection method
    
    Returns
    -------
    dict
        Dictionary with keys 'Z_rho', 'Z_t', 'Z_rho_star', 'Z_t_star',
        'Z_rho_dstar', 'Z_t_dstar' containing test results
    
    Examples
    --------
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> y = np.cumsum(np.random.randn(200))
    >>> results = all_phillips_tests(y, k=2)
    >>> for name, res in results.items():
    ...     print(f"{name}: {res.statistic:.4f}, reject at 5%: {res.reject_null['5%']}")
    """
    statistics = ['Z_rho', 'Z_t', 'Z_rho_star', 'Z_t_star', 
                  'Z_rho_dstar', 'Z_t_dstar']
    
    results = {}
    for stat in statistics:
        results[stat] = phillips_polynomial_test(
            y, k=k, statistic=stat, kernel=kernel,
            bandwidth=bandwidth, bandwidth_method=bandwidth_method
        )
    
    return results


def print_all_tests_summary(results: Dict[str, PolynomialUnitRootResult]):
    """
    Print summary table of all test statistics.
    
    Parameters
    ----------
    results : dict
        Output from all_phillips_tests()
    """
    print("=" * 75)
    print("Summary of Phillips Unit Root Tests for Polynomials of I(1) Processes")
    print("=" * 75)
    
    # Get common info from first result
    first = list(results.values())[0]
    print(f"Sample size: {first.sample_size}")
    print(f"Polynomial degree (k): {first.k}")
    print(f"Bandwidth: {first.bandwidth}")
    print("-" * 75)
    
    print(f"{'Statistic':<15} {'Value':>12} {'5% CV':>12} {'p-value':>10} {'Reject 5%':>12}")
    print("-" * 75)
    
    for name, res in results.items():
        cv_5 = res.critical_values.get(0.05, np.nan)
        reject = "Yes" if res.reject_null['5%'] else "No"
        print(f"{name:<15} {res.statistic:>12.4f} {cv_5:>12.4f} "
              f"{res.p_value:>10.4f} {reject:>12}")
    
    print("=" * 75)


# =============================================================================
# Convenience functions for specific test types
# =============================================================================

def Z_rho_test(y: np.ndarray, k: int = 2, **kwargs) -> PolynomialUnitRootResult:
    """Phillips Z_ρ test for polynomials of I(1) processes."""
    return phillips_polynomial_test(y, k=k, statistic='Z_rho', **kwargs)


def Z_t_test(y: np.ndarray, k: int = 2, **kwargs) -> PolynomialUnitRootResult:
    """Phillips Z_t test for polynomials of I(1) processes."""
    return phillips_polynomial_test(y, k=k, statistic='Z_t', **kwargs)


def Z_rho_star_test(y: np.ndarray, k: int = 2, **kwargs) -> PolynomialUnitRootResult:
    """Bias-corrected Z*_ρ test for polynomials of I(1) processes."""
    return phillips_polynomial_test(y, k=k, statistic='Z_rho_star', **kwargs)


def Z_t_star_test(y: np.ndarray, k: int = 2, **kwargs) -> PolynomialUnitRootResult:
    """Bias-corrected Z*_t test for polynomials of I(1) processes."""
    return phillips_polynomial_test(y, k=k, statistic='Z_t_star', **kwargs)


def Z_rho_dstar_test(y: np.ndarray, k: int = 2, **kwargs) -> PolynomialUnitRootResult:
    """Itô-based Z**_ρ test for polynomials of I(1) processes."""
    return phillips_polynomial_test(y, k=k, statistic='Z_rho_dstar', **kwargs)


def Z_t_dstar_test(y: np.ndarray, k: int = 2, **kwargs) -> PolynomialUnitRootResult:
    """Itô-based Z**_t test for polynomials of I(1) processes."""
    return phillips_polynomial_test(y, k=k, statistic='Z_t_dstar', **kwargs)
