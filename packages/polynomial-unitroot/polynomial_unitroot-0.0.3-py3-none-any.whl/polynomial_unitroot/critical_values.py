"""
Critical Values for Phillips Unit Root Tests for Polynomials of Integrated Processes.

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
from typing import Dict, Optional, Tuple

# =============================================================================
# Critical Values from Wagner (2012), Table 1
# Simulated percentiles for serially uncorrelated innovations case (Corollary 1)
# Based on 10,000 replications with T=1000
# =============================================================================

# Coefficient statistic T(ρ̂ - 1) - Wagner (2012) / Stypka & Wagner (2019) Z_ρ
WAGNER2012_COEF_CRITICAL_VALUES = {
    # k: {percentile: value}
    1: {
        0.010: -13.581, 0.025: -10.355, 0.050: -7.947, 0.500: -0.851,
        0.950: 1.276, 0.975: 1.600, 0.990: 2.009,
        'mean': -1.768, 'median': -0.851, 'std': 9.927
    },
    2: {
        0.010: -21.491, 0.025: -16.672, 0.050: -13.216, 0.500: -2.208,
        0.950: 2.853, 0.975: 4.215, 0.990: 6.358,
        'mean': -3.291, 'median': -2.208, 'std': 27.431
    },
    3: {
        0.010: -35.012, 0.025: -27.515, 0.050: -22.005, 0.500: -4.489,
        0.950: 4.112, 0.975: 6.925, 0.990: 11.391,
        'mean': -6.135, 'median': -4.489, 'std': 73.057
    }
}

# t-statistic t_ρ - Wagner (2012) / Stypka & Wagner (2019) Z_t
WAGNER2012_TSTAT_CRITICAL_VALUES = {
    1: {
        0.010: -2.562, 0.025: -2.224, 0.050: -1.936, 0.500: -0.498,
        0.950: 1.270, 0.975: 1.610, 0.990: 2.015,
        'mean': -0.423, 'median': -0.498, 'std': 0.955
    },
    2: {
        0.010: -3.260, 0.025: -2.860, 0.050: -2.534, 0.500: -0.941,
        0.950: 1.770, 0.975: 2.486, 0.990: 3.396,
        'mean': -0.729, 'median': -0.941, 'std': 1.760
    },
    3: {
        0.010: -4.181, 0.025: -3.698, 0.050: -3.298, 0.500: -1.412,
        0.950: 1.845, 0.975: 2.912, 0.990: 4.334,
        'mean': -1.174, 'median': -1.412, 'std': 2.645
    }
}

# =============================================================================
# Critical Values from Stypka & Wagner (2019), Table 1
# Based on 50,000 replications with T=1000
# =============================================================================

# Panel A: Coefficient statistic Z_ρ
STYPKA2019_Z_RHO_CRITICAL_VALUES = {
    1: {
        0.010: -13.698, 0.025: -10.623, 0.050: -8.239, 0.500: -0.885,
        0.950: 1.282, 0.975: 1.613, 0.990: 2.023,
        'mean': -1.816, 'std': 3.204
    },
    2: {
        0.010: -21.977, 0.025: -17.163, 0.050: -13.574, 0.500: -2.236,
        0.950: 2.870, 0.975: 4.233, 0.990: 6.413,
        'mean': -3.369, 'std': 5.351
    },
    3: {
        0.010: -36.523, 0.025: -28.565, 0.050: -22.674, 0.500: -4.509,
        0.950: 4.174, 0.975: 6.935, 0.990: 11.603,
        'mean': -6.245, 'std': 8.800
    }
}

# Panel B: t-statistic Z_t
STYPKA2019_Z_T_CRITICAL_VALUES = {
    1: {
        0.010: -2.588, 0.025: -2.262, 0.050: -1.965, 0.500: -0.513,
        0.950: 1.285, 0.975: 1.635, 0.990: 2.064,
        'mean': -0.430, 'std': 0.988
    },
    2: {
        0.010: -3.350, 0.025: -2.931, 0.050: -2.590, 0.500: -0.946,
        0.950: 1.781, 0.975: 2.522, 0.990: 3.434,
        'mean': -0.736, 'std': 1.343
    },
    3: {
        0.010: -4.445, 0.025: -3.890, 0.050: -3.405, 0.500: -1.396,
        0.950: 1.857, 0.975: 2.951, 0.990: 4.416,
        'mean': -1.176, 'std': 1.657
    }
}

# Panel C: Coefficient statistic Z*_ρ (bias-corrected)
STYPKA2019_Z_RHO_STAR_CRITICAL_VALUES = {
    1: {
        0.010: -13.698, 0.025: -10.623, 0.050: -8.239, 0.500: -0.885,
        0.950: 1.282, 0.975: 1.613, 0.990: 2.023,
        'mean': -1.816, 'std': 3.204
    },
    2: {
        0.010: -33.215, 0.025: -26.192, 0.050: -20.696, 0.500: -3.788,
        0.950: 2.038, 0.975: 3.221, 0.990: 5.089,
        'mean': -5.815, 'std': 7.559
    },
    3: {
        0.010: -60.688, 0.025: -47.690, 0.050: -38.109, 0.500: -8.249,
        0.950: 2.213, 0.975: 4.638, 0.990: 8.609,
        'mean': -11.805, 'std': 13.476
    }
}

# Panel D: t-statistic Z*_t (bias-corrected)
STYPKA2019_Z_T_STAR_CRITICAL_VALUES = {
    1: {
        0.010: -2.588, 0.025: -2.262, 0.050: -1.965, 0.500: -0.513,
        0.950: 1.285, 0.975: 1.635, 0.990: 2.064,
        'mean': -0.430, 'std': 0.988
    },
    2: {
        0.010: -4.998, 0.025: -4.389, 0.050: -3.900, 0.500: -1.551,
        0.950: 1.359, 0.975: 2.121, 0.990: 3.036,
        'mean': -1.445, 'std': 1.598
    },
    3: {
        0.010: -7.193, 0.025: -6.335, 0.050: -5.635, 0.500: -2.494,
        0.950: 1.120, 0.975: 2.194, 0.990: 3.629,
        'mean': -2.422, 'std': 2.068
    }
}

# Panel E: Coefficient statistic Z**_ρ (Itô-based)
STYPKA2019_Z_RHO_DSTAR_CRITICAL_VALUES = {
    1: {
        0.010: 0.001, 0.025: 0.003, 0.050: 0.013, 0.500: 0.779,
        0.950: 2.786, 0.975: 3.420, 0.990: 4.235,
        'mean': 0.996, 'std': 0.937
    },
    2: {
        0.010: 0.000, 0.025: 0.000, 0.050: 0.000, 0.500: 0.657,
        0.950: 5.691, 0.975: 7.655, 0.990: 10.533,
        'mean': 1.487, 'std': 2.220
    },
    3: {
        0.010: 0.000, 0.025: 0.000, 0.050: 0.000, 0.500: 0.450,
        0.950: 8.791, 0.975: 12.478, 0.990: 18.077,
        'mean': 1.971, 'std': 3.790
    }
}

# Panel F: t-statistic Z**_t (Itô-based)
STYPKA2019_Z_T_DSTAR_CRITICAL_VALUES = {
    1: {
        0.010: 0.000, 0.025: 0.001, 0.050: 0.005, 0.500: 0.445,
        0.950: 1.824, 0.975: 2.133, 0.990: 2.511,
        'mean': 0.620, 'std': 0.604
    },
    2: {
        0.010: 0.000, 0.025: 0.000, 0.050: 0.000, 0.500: 0.267,
        0.950: 2.674, 0.975: 3.373, 0.990: 4.301,
        'mean': 0.674, 'std': 0.959
    },
    3: {
        0.010: 0.000, 0.025: 0.000, 0.050: 0.000, 0.500: 0.136,
        0.950: 3.104, 0.975: 4.161, 0.990: 5.533,
        'mean': 0.671, 'std': 1.192
    }
}


def get_critical_value(statistic: str, k: int, significance: float = 0.05,
                       source: str = 'stypka2019') -> float:
    """
    Get critical value for a given test statistic.
    
    Parameters
    ----------
    statistic : str
        One of: 'Z_rho', 'Z_t', 'Z_rho_star', 'Z_t_star', 'Z_rho_dstar', 'Z_t_dstar',
                'coef' (alias for Z_rho), 't' (alias for Z_t)
    k : int
        Polynomial degree (1, 2, or 3)
    significance : float
        Significance level (0.01, 0.025, 0.05, etc.)
    source : str
        'wagner2012' or 'stypka2019' (default)
    
    Returns
    -------
    float
        Critical value at the specified significance level
    
    Notes
    -----
    - For k=1, Z_rho = Z*_rho and Z_t = Z*_t by construction (Stypka & Wagner, 2019)
    - Critical values are for left-tail tests (unit root null hypothesis)
    """
    if k not in [1, 2, 3]:
        raise ValueError(f"k must be 1, 2, or 3. Got {k}")
    
    # Map aliases
    stat_map = {
        'coef': 'Z_rho',
        't': 'Z_t',
        'coefficient': 'Z_rho',
        'tstat': 'Z_t',
    }
    statistic = stat_map.get(statistic.lower(), statistic)
    
    # Select critical value dictionary
    if source.lower() == 'wagner2012':
        if statistic in ['Z_rho', 'z_rho']:
            cv_dict = WAGNER2012_COEF_CRITICAL_VALUES
        elif statistic in ['Z_t', 'z_t']:
            cv_dict = WAGNER2012_TSTAT_CRITICAL_VALUES
        else:
            raise ValueError(f"Wagner (2012) only provides 'Z_rho' and 'Z_t'. Got {statistic}")
    else:  # stypka2019
        cv_map = {
            'Z_rho': STYPKA2019_Z_RHO_CRITICAL_VALUES,
            'z_rho': STYPKA2019_Z_RHO_CRITICAL_VALUES,
            'Z_t': STYPKA2019_Z_T_CRITICAL_VALUES,
            'z_t': STYPKA2019_Z_T_CRITICAL_VALUES,
            'Z_rho_star': STYPKA2019_Z_RHO_STAR_CRITICAL_VALUES,
            'z_rho_star': STYPKA2019_Z_RHO_STAR_CRITICAL_VALUES,
            'Z_t_star': STYPKA2019_Z_T_STAR_CRITICAL_VALUES,
            'z_t_star': STYPKA2019_Z_T_STAR_CRITICAL_VALUES,
            'Z_rho_dstar': STYPKA2019_Z_RHO_DSTAR_CRITICAL_VALUES,
            'z_rho_dstar': STYPKA2019_Z_RHO_DSTAR_CRITICAL_VALUES,
            'Z_t_dstar': STYPKA2019_Z_T_DSTAR_CRITICAL_VALUES,
            'z_t_dstar': STYPKA2019_Z_T_DSTAR_CRITICAL_VALUES,
        }
        if statistic not in cv_map:
            raise ValueError(f"Unknown statistic: {statistic}")
        cv_dict = cv_map[statistic]
    
    if significance not in cv_dict[k]:
        available = [p for p in cv_dict[k].keys() if isinstance(p, float)]
        raise ValueError(f"Significance {significance} not available. Choose from {available}")
    
    return cv_dict[k][significance]


def get_all_critical_values(statistic: str, k: int, source: str = 'stypka2019') -> Dict:
    """
    Get all critical values for a given test statistic and polynomial degree.
    
    Parameters
    ----------
    statistic : str
        Test statistic name
    k : int
        Polynomial degree
    source : str
        'wagner2012' or 'stypka2019'
    
    Returns
    -------
    dict
        Dictionary containing all percentiles and summary statistics
    """
    if k not in [1, 2, 3]:
        raise ValueError(f"k must be 1, 2, or 3. Got {k}")
    
    stat_map = {
        'coef': 'Z_rho', 't': 'Z_t', 'coefficient': 'Z_rho', 'tstat': 'Z_t',
    }
    statistic = stat_map.get(statistic.lower(), statistic)
    
    if source.lower() == 'wagner2012':
        if statistic in ['Z_rho', 'z_rho']:
            return WAGNER2012_COEF_CRITICAL_VALUES[k].copy()
        elif statistic in ['Z_t', 'z_t']:
            return WAGNER2012_TSTAT_CRITICAL_VALUES[k].copy()
        else:
            raise ValueError(f"Wagner (2012) only provides 'Z_rho' and 'Z_t'")
    else:
        cv_map = {
            'Z_rho': STYPKA2019_Z_RHO_CRITICAL_VALUES,
            'z_rho': STYPKA2019_Z_RHO_CRITICAL_VALUES,
            'Z_t': STYPKA2019_Z_T_CRITICAL_VALUES,
            'z_t': STYPKA2019_Z_T_CRITICAL_VALUES,
            'Z_rho_star': STYPKA2019_Z_RHO_STAR_CRITICAL_VALUES,
            'z_rho_star': STYPKA2019_Z_RHO_STAR_CRITICAL_VALUES,
            'Z_t_star': STYPKA2019_Z_T_STAR_CRITICAL_VALUES,
            'z_t_star': STYPKA2019_Z_T_STAR_CRITICAL_VALUES,
            'Z_rho_dstar': STYPKA2019_Z_RHO_DSTAR_CRITICAL_VALUES,
            'z_rho_dstar': STYPKA2019_Z_RHO_DSTAR_CRITICAL_VALUES,
            'Z_t_dstar': STYPKA2019_Z_T_DSTAR_CRITICAL_VALUES,
            'z_t_dstar': STYPKA2019_Z_T_DSTAR_CRITICAL_VALUES,
        }
        if statistic not in cv_map:
            raise ValueError(f"Unknown statistic: {statistic}")
        return cv_map[statistic][k].copy()


def interpolate_critical_value(statistic: str, k: int, significance: float,
                                source: str = 'stypka2019') -> float:
    """
    Interpolate critical value for arbitrary significance levels.
    
    Uses linear interpolation between available percentiles.
    
    Parameters
    ----------
    statistic : str
        Test statistic name
    k : int
        Polynomial degree
    significance : float
        Any significance level between 0.01 and 0.99
    source : str
        Source of critical values
    
    Returns
    -------
    float
        Interpolated critical value
    """
    cv = get_all_critical_values(statistic, k, source)
    percentiles = sorted([p for p in cv.keys() if isinstance(p, float)])
    values = [cv[p] for p in percentiles]
    
    return np.interp(significance, percentiles, values)


def p_value(test_stat: float, statistic: str, k: int, 
            source: str = 'stypka2019') -> float:
    """
    Calculate approximate p-value for a test statistic.
    
    Uses linear interpolation between tabulated percentiles.
    
    Parameters
    ----------
    test_stat : float
        Computed test statistic value
    statistic : str
        Type of test statistic
    k : int
        Polynomial degree
    source : str
        Source of critical values
    
    Returns
    -------
    float
        Approximate p-value (one-sided)
        - Left-tail for Z_rho, Z_t, Z_rho_star, Z_t_star
        - Right-tail for Z_rho_dstar, Z_t_dstar
    """
    # Normalize statistic name
    stat_lower = statistic.lower().replace('*', '_star').replace('**', '_dstar')
    
    cv = get_all_critical_values(statistic, k, source)
    percentiles = sorted([p for p in cv.keys() if isinstance(p, float)])
    values = [cv[p] for p in percentiles]
    
    # Interpolate to find the percentile (CDF value)
    if test_stat <= values[0]:
        cdf = percentiles[0]
    elif test_stat >= values[-1]:
        cdf = percentiles[-1]
    else:
        cdf = np.interp(test_stat, values, percentiles)
    
    # For Z**_ρ and Z**_t, rejection is right-tail, so p-value = 1 - CDF
    if statistic.lower() in ['z_rho_dstar', 'z_t_dstar']:
        return 1.0 - cdf
    else:
        # For other statistics, rejection is left-tail, so p-value = CDF
        return cdf
