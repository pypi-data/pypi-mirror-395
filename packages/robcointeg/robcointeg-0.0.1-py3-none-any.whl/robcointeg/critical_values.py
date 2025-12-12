"""
Critical values for the Student-t based Pseudolikelihood Ratio Test.

This module provides the critical values from Table 1 of Franses & Lucas (1998)
for the PLR cointegration test based on the Student-t pseudolikelihood.

References:
    Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis",
    Journal of Business & Economic Statistics, 16:4, 459-468.
    
    Table 1 on page 461.
"""

import numpy as np
from typing import Optional, Tuple, Union
import warnings


class CriticalValueTable:
    """
    Critical values for the Student-t based PLR test.
    
    The table contains quantiles of the PLR test based on the Student-t 
    pseudolikelihood. These values are from Table 1 of Franses & Lucas (1998),
    which were computed using 10,000 Monte Carlo simulations.
    
    The critical values depend on:
    - k - r: The number of common stochastic trends under the null hypothesis
    - ν (nu): The degrees of freedom parameter of the Student-t pseudolikelihood
    - drift: Whether the data generating process includes drift
    
    Parameters
    ----------
    with_drift : bool, optional
        If True, use critical values for DGP with non-zero drift.
        Default is True.
        
    Notes
    -----
    From Table 1 (Franses & Lucas 1998, p. 461):
    
    "The table contains the quantiles of the PLR test based on the Student-t 
    pseudolikelihood. ν denotes the degrees of freedom parameter of the 
    pseudolikelihood. The entries are based on 10,000 Monte Carlo simulations.
    In each simulation a k-r-dimensional Gaussian random walk is generated, 
    possibly with nonzero drift. Next, the PLR test of the hypothesis of 0 
    versus k-r cointegrating relations was computed, using Model (1). The 
    constant in (1) enters unrestrictedly in the regression model."
    
    When ν → ∞, the distribution converges to that of Johansen (1988, 1991).
    """
    
    # Critical values from Table 1: With drift (α'⊥μ ≠ 0)
    # Structure: CRITICAL_DRIFT[(k_minus_r, nu)][quantile]
    # Quantiles: 0.80, 0.90, 0.95, 0.99
    CRITICAL_DRIFT = {
        # k - r = 1
        (1, np.inf): (1.7, 2.8, 4.0, 6.7),
        (1, 10): (1.7, 2.8, 4.1, 6.7),
        (1, 7): (1.8, 2.9, 4.2, 6.8),
        (1, 5): (1.8, 3.0, 4.3, 7.0),
        (1, 3): (2.0, 3.3, 4.6, 7.6),
        # k - r = 2
        (2, np.inf): (11.4, 13.8, 15.9, 20.5),
        (2, 10): (11.6, 14.1, 16.3, 21.2),
        (2, 7): (11.8, 14.3, 16.5, 21.5),
        (2, 5): (12.1, 14.6, 16.9, 22.1),
        (2, 3): (12.6, 15.4, 17.9, 23.4),
        # k - r = 3
        (3, np.inf): (24.3, 27.5, 30.1, 35.6),
        (3, 10): (24.9, 28.3, 30.9, 36.5),
        (3, 7): (25.3, 28.7, 31.4, 37.1),
        (3, 5): (25.8, 29.2, 32.2, 38.0),
        (3, 3): (27.0, 30.6, 33.7, 40.1),
    }
    
    # Critical values from Table 1: Without drift (α'⊥μ = 0)
    CRITICAL_NO_DRIFT = {
        # k - r = 1
        (1, np.inf): (4.9, 6.6, 8.3, 12.0),
        (1, 10): (4.9, 6.7, 8.4, 12.0),
        (1, 7): (5.0, 6.8, 8.6, 12.2),
        (1, 5): (5.1, 7.0, 8.7, 12.5),
        (1, 3): (5.3, 7.2, 9.2, 13.3),
        # k - r = 2
        (2, np.inf): (13.5, 16.0, 18.3, 22.6),
        (2, 10): (13.8, 16.3, 18.7, 23.2),
        (2, 7): (14.0, 16.6, 19.1, 23.6),
        (2, 5): (14.3, 17.0, 19.5, 24.2),
        (2, 3): (14.9, 17.7, 20.4, 25.5),
        # k - r = 3
        (3, np.inf): (26.1, 29.4, 32.4, 38.4),
        (3, 10): (26.8, 30.2, 33.3, 39.9),
        (3, 7): (27.2, 30.7, 33.8, 40.4),
        (3, 5): (27.8, 31.4, 34.5, 41.1),
        (3, 3): (28.9, 32.8, 36.1, 43.1),
    }
    
    # Quantile mapping
    QUANTILE_MAP = {
        0.80: 0,
        0.90: 1,
        0.95: 2,
        0.99: 3,
    }
    
    def __init__(self, with_drift: bool = True):
        """
        Initialize the critical value table.
        
        Parameters
        ----------
        with_drift : bool, optional
            If True, use critical values for DGP with non-zero drift.
            Default is True.
        """
        self.with_drift = with_drift
        self._table = self.CRITICAL_DRIFT if with_drift else self.CRITICAL_NO_DRIFT
    
    def get_critical_value(self, k_minus_r: int, nu: float, 
                           significance_level: float = 0.05) -> float:
        """
        Get the critical value for a specific test configuration.
        
        Parameters
        ----------
        k_minus_r : int
            Number of common stochastic trends (k - r).
        nu : float
            Degrees of freedom parameter. Use np.inf for Gaussian case.
        significance_level : float, optional
            Significance level (0.01, 0.05, 0.10, 0.20). Default is 0.05.
            
        Returns
        -------
        float
            Critical value for the specified configuration.
            
        Raises
        ------
        ValueError
            If the configuration is not available in the table.
        """
        # Convert significance level to quantile
        quantile = 1 - significance_level
        
        # Find closest quantile
        if quantile >= 0.99:
            q_idx = 3
        elif quantile >= 0.95:
            q_idx = 2
        elif quantile >= 0.90:
            q_idx = 1
        else:
            q_idx = 0
        
        # Find closest nu
        available_nus = [np.inf, 10, 7, 5, 3]
        
        if nu >= 30:
            closest_nu = np.inf
        elif nu >= 8.5:
            closest_nu = 10
        elif nu >= 6:
            closest_nu = 7
        elif nu >= 4:
            closest_nu = 5
        else:
            closest_nu = 3
        
        # Check if k_minus_r is available
        if k_minus_r not in [1, 2, 3]:
            warnings.warn(f"k - r = {k_minus_r} not in table. Using interpolation.")
            # For k - r > 3, use approximate scaling based on Johansen tables
            if k_minus_r > 3:
                base_cv = self._table.get((3, closest_nu), (27.0, 30.6, 33.7, 40.1))[q_idx]
                # Approximate scaling factor
                scale = 1 + 0.1 * (k_minus_r - 3)
                return base_cv * scale
            else:
                return self._table.get((1, closest_nu), (2.0, 3.3, 4.6, 7.6))[q_idx]
        
        key = (k_minus_r, closest_nu)
        if key not in self._table:
            raise ValueError(f"Configuration not found: k-r={k_minus_r}, nu={nu}")
        
        return self._table[key][q_idx]
    
    def get_all_critical_values(self, k_minus_r: int, nu: float) -> dict:
        """
        Get all critical values for a specific k-r and nu combination.
        
        Parameters
        ----------
        k_minus_r : int
            Number of common stochastic trends.
        nu : float
            Degrees of freedom parameter.
            
        Returns
        -------
        dict
            Dictionary with significance levels as keys and critical values as values.
        """
        return {
            0.20: self.get_critical_value(k_minus_r, nu, 0.20),
            0.10: self.get_critical_value(k_minus_r, nu, 0.10),
            0.05: self.get_critical_value(k_minus_r, nu, 0.05),
            0.01: self.get_critical_value(k_minus_r, nu, 0.01),
        }
    
    def __repr__(self) -> str:
        drift_str = "with drift" if self.with_drift else "without drift"
        return f"CriticalValueTable({drift_str})"
    
    def print_table(self) -> str:
        """
        Print the complete critical value table.
        
        Returns
        -------
        str
            Formatted table string.
        """
        lines = []
        drift_str = "With drift" if self.with_drift else "Without drift"
        lines.append(f"\nCritical Values for PLR Test ({drift_str})")
        lines.append("=" * 60)
        lines.append(f"{'k-r':>6} {'ν':>8} {'80%':>8} {'90%':>8} {'95%':>8} {'99%':>8}")
        lines.append("-" * 60)
        
        for k_minus_r in [1, 2, 3]:
            for nu in [np.inf, 10, 7, 5, 3]:
                nu_str = "∞" if nu == np.inf else str(nu)
                key = (k_minus_r, nu)
                if key in self._table:
                    vals = self._table[key]
                    lines.append(f"{k_minus_r:>6} {nu_str:>8} {vals[0]:>8.1f} {vals[1]:>8.1f} {vals[2]:>8.1f} {vals[3]:>8.1f}")
            lines.append("-" * 60)
        
        lines.append("\nSource: Franses & Lucas (1998), Table 1")
        
        return "\n".join(lines)


def get_critical_value(k_minus_r: int, nu: float = 5, 
                       significance_level: float = 0.05,
                       with_drift: bool = True) -> float:
    """
    Convenience function to get a single critical value.
    
    Parameters
    ----------
    k_minus_r : int
        Number of common stochastic trends (k - r).
    nu : float, optional
        Degrees of freedom parameter. Default is 5.
    significance_level : float, optional
        Significance level. Default is 0.05.
    with_drift : bool, optional
        Whether the DGP includes drift. Default is True.
        
    Returns
    -------
    float
        Critical value.
        
    Examples
    --------
    >>> from robcointeg import get_critical_value
    >>> # 95% critical value for k-r=2 with nu=5 and drift
    >>> cv = get_critical_value(2, nu=5, significance_level=0.05)
    >>> print(f"Critical value: {cv}")
    Critical value: 16.9
    
    Notes
    -----
    Critical values from Table 1 of Franses & Lucas (1998).
    For the Gaussian case (Johansen test), use nu=np.inf.
    """
    table = CriticalValueTable(with_drift=with_drift)
    return table.get_critical_value(k_minus_r, nu, significance_level)


def interpolate_critical_value(k_minus_r: int, nu: float, 
                                significance_level: float = 0.05,
                                with_drift: bool = True) -> float:
    """
    Interpolate critical value for intermediate values of nu.
    
    This function performs linear interpolation between the tabulated
    values for more precise critical values.
    
    Parameters
    ----------
    k_minus_r : int
        Number of common stochastic trends.
    nu : float
        Degrees of freedom parameter.
    significance_level : float, optional
        Significance level. Default is 0.05.
    with_drift : bool, optional
        Whether the DGP includes drift. Default is True.
        
    Returns
    -------
    float
        Interpolated critical value.
    """
    table = CriticalValueTable(with_drift=with_drift)
    
    # Available nu values
    nus = [3, 5, 7, 10, 30]  # Using 30 as proxy for infinity
    
    if nu <= 3:
        return table.get_critical_value(k_minus_r, 3, significance_level)
    elif nu >= 30:
        return table.get_critical_value(k_minus_r, np.inf, significance_level)
    
    # Find bracketing nu values
    for i in range(len(nus) - 1):
        if nus[i] <= nu <= nus[i + 1]:
            nu_low, nu_high = nus[i], nus[i + 1]
            break
    
    # Get critical values at bracketing points
    nu_low_arg = nu_low if nu_low < 30 else np.inf
    nu_high_arg = nu_high if nu_high < 30 else np.inf
    
    cv_low = table.get_critical_value(k_minus_r, nu_low_arg, significance_level)
    cv_high = table.get_critical_value(k_minus_r, nu_high_arg, significance_level)
    
    # Linear interpolation
    weight = (nu - nu_low) / (nu_high - nu_low)
    return cv_low + weight * (cv_high - cv_low)


def get_johansen_critical_value(k_minus_r: int, significance_level: float = 0.05,
                                 with_drift: bool = True) -> float:
    """
    Get critical value for standard Johansen (Gaussian) test.
    
    This is equivalent to calling get_critical_value with nu=np.inf.
    
    Parameters
    ----------
    k_minus_r : int
        Number of common stochastic trends.
    significance_level : float, optional
        Significance level. Default is 0.05.
    with_drift : bool, optional
        Whether the DGP includes drift. Default is True.
        
    Returns
    -------
    float
        Critical value for Johansen test.
        
    Notes
    -----
    These values can be compared to tables A1 and A2 of Johansen and 
    Juselius (1990) as noted in the paper.
    """
    return get_critical_value(k_minus_r, np.inf, significance_level, with_drift)


# Export commonly used critical value tables as dictionaries for quick reference
CRITICAL_VALUES_5PCT_DRIFT = {
    1: {np.inf: 4.0, 10: 4.1, 7: 4.2, 5: 4.3, 3: 4.6},
    2: {np.inf: 15.9, 10: 16.3, 7: 16.5, 5: 16.9, 3: 17.9},
    3: {np.inf: 30.1, 10: 30.9, 7: 31.4, 5: 32.2, 3: 33.7},
}

CRITICAL_VALUES_5PCT_NO_DRIFT = {
    1: {np.inf: 8.3, 10: 8.4, 7: 8.6, 5: 8.7, 3: 9.2},
    2: {np.inf: 18.3, 10: 18.7, 7: 19.1, 5: 19.5, 3: 20.4},
    3: {np.inf: 32.4, 10: 33.3, 7: 33.8, 5: 34.5, 3: 36.1},
}
