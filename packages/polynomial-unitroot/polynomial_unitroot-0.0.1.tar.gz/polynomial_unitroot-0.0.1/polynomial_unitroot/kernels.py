"""
Kernel Functions and Bandwidth Selection for HAC Estimation.

Based on:
- Andrews, D.W.K. (1991). Heteroskedasticity and autocorrelation consistent 
  covariance matrix estimation. Econometrica, 59, 817-858.
- Stypka, O., & Wagner, M. (2019). The Phillips unit root tests for polynomials 
  of integrated processes revisited. Economics Letters, 176, 109-113.

Assumption 2 (Stypka & Wagner, 2019):
- K(0) = 1
- K(·) is continuous at zero
- K̄(0) := sup_{x≥0} |K(x)| < ∞
- ∫_0^∞ K̄(x)dx < ∞, where K̄(x) := sup_{y≥x} |K(y)|
- M_T → ∞ with M_T = O(T^b), 0 < b < 1/3

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
GitHub: https://github.com/merwanroudane/polyunitroottest
"""

import numpy as np
from typing import Callable, Optional


def bartlett_kernel(x: np.ndarray) -> np.ndarray:
    """
    Bartlett (triangular) kernel function.
    
    K(x) = (1 - |x|) * I(|x| ≤ 1)
    
    This kernel satisfies Assumption 2 of Stypka & Wagner (2019).
    
    Parameters
    ----------
    x : np.ndarray
        Input values (typically h/M where h is lag and M is bandwidth)
    
    Returns
    -------
    np.ndarray
        Kernel weights
    
    Notes
    -----
    The Bartlett kernel is used in the original Phillips (1987) paper
    and is recommended in Stypka & Wagner (2019) for unit root tests
    on polynomials of integrated processes.
    """
    x = np.asarray(x)
    return np.where(np.abs(x) <= 1, 1 - np.abs(x), 0)


def parzen_kernel(x: np.ndarray) -> np.ndarray:
    """
    Parzen kernel function.
    
    K(x) = 1 - 6x² + 6|x|³    for 0 ≤ |x| ≤ 0.5
         = 2(1 - |x|)³        for 0.5 < |x| ≤ 1
         = 0                  for |x| > 1
    
    Parameters
    ----------
    x : np.ndarray
        Input values
    
    Returns
    -------
    np.ndarray
        Kernel weights
    """
    x = np.asarray(x)
    abs_x = np.abs(x)
    result = np.zeros_like(x, dtype=float)
    
    mask1 = abs_x <= 0.5
    mask2 = (abs_x > 0.5) & (abs_x <= 1)
    
    result[mask1] = 1 - 6 * abs_x[mask1]**2 + 6 * abs_x[mask1]**3
    result[mask2] = 2 * (1 - abs_x[mask2])**3
    
    return result


def quadratic_spectral_kernel(x: np.ndarray) -> np.ndarray:
    """
    Quadratic Spectral (QS) kernel function.
    
    K(x) = (25/(12π²x²)) * (sin(6πx/5)/(6πx/5) - cos(6πx/5))
    
    For x = 0: K(0) = 1
    
    Parameters
    ----------
    x : np.ndarray
        Input values
    
    Returns
    -------
    np.ndarray
        Kernel weights
    """
    x = np.asarray(x)
    result = np.ones_like(x, dtype=float)
    
    # Handle non-zero values
    mask = x != 0
    if np.any(mask):
        z = 6 * np.pi * x[mask] / 5
        result[mask] = 25 / (12 * np.pi**2 * x[mask]**2) * (np.sin(z)/z - np.cos(z))
    
    return result


def tukey_hanning_kernel(x: np.ndarray) -> np.ndarray:
    """
    Tukey-Hanning kernel function.
    
    K(x) = (1 + cos(πx))/2    for |x| ≤ 1
         = 0                   for |x| > 1
    
    Parameters
    ----------
    x : np.ndarray
        Input values
    
    Returns
    -------
    np.ndarray
        Kernel weights
    """
    x = np.asarray(x)
    return np.where(np.abs(x) <= 1, (1 + np.cos(np.pi * x)) / 2, 0)


def truncated_kernel(x: np.ndarray) -> np.ndarray:
    """
    Truncated (uniform) kernel function.
    
    K(x) = 1    for |x| ≤ 1
         = 0    for |x| > 1
    
    Parameters
    ----------
    x : np.ndarray
        Input values
    
    Returns
    -------
    np.ndarray
        Kernel weights
    
    Warning
    -------
    This kernel may not produce positive semi-definite HAC estimators.
    """
    x = np.asarray(x)
    return np.where(np.abs(x) <= 1, 1, 0)


def get_kernel(name: str) -> Callable:
    """
    Get kernel function by name.
    
    Parameters
    ----------
    name : str
        Kernel name: 'bartlett', 'parzen', 'qs', 'quadratic_spectral',
                    'tukey_hanning', 'truncated'
    
    Returns
    -------
    Callable
        Kernel function
    """
    kernels = {
        'bartlett': bartlett_kernel,
        'triangular': bartlett_kernel,
        'parzen': parzen_kernel,
        'qs': quadratic_spectral_kernel,
        'quadratic_spectral': quadratic_spectral_kernel,
        'tukey_hanning': tukey_hanning_kernel,
        'tukey-hanning': tukey_hanning_kernel,
        'truncated': truncated_kernel,
        'uniform': truncated_kernel,
    }
    
    name_lower = name.lower()
    if name_lower not in kernels:
        raise ValueError(f"Unknown kernel: {name}. Available: {list(kernels.keys())}")
    
    return kernels[name_lower]


# =============================================================================
# Bandwidth Selection Methods
# =============================================================================

def andrews_bandwidth(residuals: np.ndarray, kernel: str = 'bartlett') -> int:
    """
    Andrews (1991) automatic bandwidth selection.
    
    This implements the data-dependent bandwidth selection rule from
    Andrews (1991), as used in Stypka & Wagner (2019).
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual series from the regression
    kernel : str
        Kernel type ('bartlett', 'parzen', 'qs')
    
    Returns
    -------
    int
        Optimal bandwidth
    
    Notes
    -----
    For the Bartlett kernel, the optimal bandwidth is:
        M_T = 1.1447 * (α(1) * T)^(1/3)
    
    where α(1) = 4ρ̂²/(1-ρ̂)⁴ and ρ̂ is the AR(1) coefficient estimate.
    
    References
    ----------
    Andrews, D.W.K. (1991). Heteroskedasticity and autocorrelation consistent
    covariance matrix estimation. Econometrica, 59, 817-858.
    """
    T = len(residuals)
    
    # Estimate AR(1) coefficient
    y = residuals[1:]
    x = residuals[:-1]
    rho_hat = np.sum(x * y) / np.sum(x**2) if np.sum(x**2) > 0 else 0
    
    # Bound rho to avoid numerical issues
    rho_hat = np.clip(rho_hat, -0.99, 0.99)
    
    # Calculate alpha(q) for different kernels
    # For AR(1): alpha(1) = 4*rho^2 / (1-rho)^4
    #            alpha(2) = 4*rho^2 / (1-rho)^4  (same for Bartlett)
    
    kernel_lower = kernel.lower()
    
    if kernel_lower in ['bartlett', 'triangular']:
        # Bartlett kernel: M = 1.1447 * (alpha(1) * T)^(1/3)
        alpha = 4 * rho_hat**2 / (1 - rho_hat)**4 if abs(rho_hat) < 1 else 0
        bandwidth = 1.1447 * (alpha * T)**(1/3)
    elif kernel_lower == 'parzen':
        # Parzen kernel: M = 2.6614 * (alpha(2) * T)^(1/5)
        alpha = 4 * rho_hat**2 / (1 - rho_hat)**4 if abs(rho_hat) < 1 else 0
        bandwidth = 2.6614 * (alpha * T)**(1/5)
    elif kernel_lower in ['qs', 'quadratic_spectral']:
        # QS kernel: M = 1.3221 * (alpha(2) * T)^(1/5)
        alpha = 4 * rho_hat**2 / (1 - rho_hat)**4 if abs(rho_hat) < 1 else 0
        bandwidth = 1.3221 * (alpha * T)**(1/5)
    else:
        # Default to Bartlett
        alpha = 4 * rho_hat**2 / (1 - rho_hat)**4 if abs(rho_hat) < 1 else 0
        bandwidth = 1.1447 * (alpha * T)**(1/3)
    
    # Round and ensure positive
    bandwidth = max(1, int(np.floor(bandwidth)))
    
    return bandwidth


def newey_west_bandwidth(T: int, rule: str = 'floor') -> int:
    """
    Newey-West bandwidth selection rule.
    
    M_T = floor(4 * (T/100)^(2/9)) for Bartlett kernel
    
    Parameters
    ----------
    T : int
        Sample size
    rule : str
        'floor' or 'ceiling' for rounding
    
    Returns
    -------
    int
        Bandwidth
    
    References
    ----------
    Newey, W.K., & West, K.D. (1994). Automatic lag selection in covariance
    matrix estimation. Review of Economic Studies, 61, 631-653.
    """
    bandwidth = 4 * (T / 100)**(2/9)
    
    if rule == 'floor':
        return max(1, int(np.floor(bandwidth)))
    else:
        return max(1, int(np.ceil(bandwidth)))


def fixed_bandwidth(T: int, b: float = 0.2) -> int:
    """
    Fixed proportion bandwidth.
    
    M_T = floor(T^b)
    
    Following Assumption 2 in Stypka & Wagner (2019), 0 < b < 1/3.
    
    Parameters
    ----------
    T : int
        Sample size
    b : float
        Exponent (must satisfy 0 < b < 1/3 for consistency)
    
    Returns
    -------
    int
        Bandwidth
    
    Raises
    ------
    ValueError
        If b is not in (0, 1/3)
    """
    if not (0 < b < 1/3):
        raise ValueError(f"Parameter b must satisfy 0 < b < 1/3. Got b={b}")
    
    return max(1, int(np.floor(T**b)))


def compute_bandwidth(residuals: np.ndarray, method: str = 'andrews',
                      kernel: str = 'bartlett', **kwargs) -> int:
    """
    Compute optimal bandwidth using specified method.
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual series
    method : str
        'andrews', 'newey_west', 'nw', 'fixed', or an integer
    kernel : str
        Kernel type for Andrews method
    **kwargs
        Additional arguments for specific methods
    
    Returns
    -------
    int
        Computed bandwidth
    """
    T = len(residuals)
    
    if method == 'andrews':
        return andrews_bandwidth(residuals, kernel=kernel)
    elif method in ['newey_west', 'nw']:
        return newey_west_bandwidth(T, **kwargs)
    elif method == 'fixed':
        b = kwargs.get('b', 0.2)
        return fixed_bandwidth(T, b=b)
    elif isinstance(method, int):
        return method
    else:
        raise ValueError(f"Unknown bandwidth method: {method}")


# =============================================================================
# HAC Variance Estimation
# =============================================================================

def estimate_long_run_variance(residuals: np.ndarray, 
                               kernel: str = 'bartlett',
                               bandwidth: Optional[int] = None,
                               bandwidth_method: str = 'andrews') -> float:
    """
    Estimate long-run variance using kernel-based HAC estimator.
    
    ω̂ = σ̂² + 2 * Σ_{h=1}^{M} K(h/M) * γ̂(h)
    
    where γ̂(h) = (1/T) * Σ_{t=h+1}^{T} v̂_t * v̂_{t-h}
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual series v̂_t
    kernel : str
        Kernel function name
    bandwidth : int, optional
        Bandwidth M. If None, computed automatically
    bandwidth_method : str
        Method for automatic bandwidth selection
    
    Returns
    -------
    float
        Estimated long-run variance ω̂
    
    Notes
    -----
    This implements Eq. (6)-(7) in Stypka & Wagner (2019):
    ω̂_v = σ̂²_v + 2 * Σ_{h=1}^{M_T} K(h/M_T) * (1/T) * Σ_{t=1}^{T-h} v̂_t * v̂_{t-j}
    """
    residuals = np.asarray(residuals)
    T = len(residuals)
    
    # Get kernel function
    K = get_kernel(kernel)
    
    # Compute bandwidth if not provided
    if bandwidth is None:
        bandwidth = compute_bandwidth(residuals, method=bandwidth_method, kernel=kernel)
    
    # Variance estimate: σ̂² = (1/T) * Σ v̂_t²
    sigma2 = np.mean(residuals**2)
    
    # Compute autocovariances with kernel weights
    lrv = sigma2
    for h in range(1, bandwidth + 1):
        weight = K(h / bandwidth)
        # γ̂(h) = (1/T) * Σ_{t=h+1}^{T} v̂_t * v̂_{t-h}
        gamma_h = np.mean(residuals[h:] * residuals[:-h])
        lrv += 2 * weight * gamma_h
    
    # Ensure non-negative
    return max(0, lrv)


def estimate_half_long_run_variance(residuals: np.ndarray,
                                     kernel: str = 'bartlett',
                                     bandwidth: Optional[int] = None,
                                     bandwidth_method: str = 'andrews') -> float:
    """
    Estimate half long-run variance.
    
    λ̂ = (1/2) * (ω̂ - σ̂²)
    
    where λ_u = Σ_{j=1}^{∞} E(u_t * u_{t-j})
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual series
    kernel : str
        Kernel function name
    bandwidth : int, optional
        Bandwidth
    bandwidth_method : str
        Bandwidth selection method
    
    Returns
    -------
    float
        Estimated half long-run variance λ̂
    """
    lrv = estimate_long_run_variance(residuals, kernel, bandwidth, bandwidth_method)
    sigma2 = np.mean(residuals**2)
    
    return 0.5 * (lrv - sigma2)


def estimate_variances(residuals: np.ndarray,
                       kernel: str = 'bartlett',
                       bandwidth: Optional[int] = None,
                       bandwidth_method: str = 'andrews') -> dict:
    """
    Estimate all variance quantities needed for Phillips tests.
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual series v̂_t
    kernel : str
        Kernel function name
    bandwidth : int, optional
        Bandwidth
    bandwidth_method : str
        Bandwidth selection method
    
    Returns
    -------
    dict
        Dictionary with keys: 'sigma2', 'omega', 'lambda', 'bandwidth'
        - sigma2: Short-run variance σ̂²_v
        - omega: Long-run variance ω̂_v  
        - lambda: Half long-run variance λ̂_v
        - bandwidth: Used bandwidth M_T
    """
    residuals = np.asarray(residuals)
    
    # Get kernel function
    K = get_kernel(kernel)
    
    # Compute bandwidth if not provided
    if bandwidth is None:
        bandwidth = compute_bandwidth(residuals, method=bandwidth_method, kernel=kernel)
    
    # Variance estimate
    sigma2 = np.mean(residuals**2)
    
    # Long-run variance
    omega = sigma2
    for h in range(1, bandwidth + 1):
        weight = K(h / bandwidth)
        gamma_h = np.mean(residuals[h:] * residuals[:-h])
        omega += 2 * weight * gamma_h
    
    omega = max(0, omega)
    
    # Half long-run variance
    lambda_v = 0.5 * (omega - sigma2)
    
    return {
        'sigma2': sigma2,
        'omega': omega,
        'lambda': lambda_v,
        'bandwidth': bandwidth
    }
