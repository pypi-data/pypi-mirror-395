"""
Data utilities for robcointeg package.

This module provides functions for loading example datasets and
generating simulated data for testing and demonstration purposes.
"""

import numpy as np
from typing import Tuple, Optional


def generate_cointegrated_data(T: int = 100, k: int = 2, r: int = 1,
                                seed: Optional[int] = None) -> Tuple[np.ndarray, dict]:
    """
    Generate cointegrated time series data.
    
    Parameters
    ----------
    T : int, optional
        Sample size. Default is 100.
    k : int, optional
        Number of variables. Default is 2.
    r : int, optional
        Cointegrating rank. Default is 1.
    seed : int, optional
        Random seed.
        
    Returns
    -------
    y : np.ndarray
        Generated data of shape (T, k).
    params : dict
        Dictionary containing true parameter values.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate cointegrating vectors (k x r)
    beta = np.eye(k, r)
    beta[r:, :] = np.random.randn(k - r, r)
    
    # Generate loading matrix (k x r)
    alpha = np.zeros((k, r))
    alpha[:r, :] = -0.3 * np.eye(r)
    
    # Generate innovations
    Sigma = np.eye(k) * 0.5 + 0.5 * np.ones((k, k)) * 0.1
    eps = np.random.multivariate_normal(np.zeros(k), Sigma, T)
    
    # Generate data from VECM
    y = np.zeros((T, k))
    y[0, :] = eps[0, :]
    
    for t in range(1, T):
        # Error correction term
        ec = alpha @ beta.T @ y[t-1, :]
        y[t, :] = y[t-1, :] + ec + eps[t, :]
    
    params = {
        'alpha': alpha,
        'beta': beta,
        'Sigma': Sigma,
        'r': r,
    }
    
    return y, params


def generate_data_with_outliers(T: int = 100, k: int = 2, 
                                 outlier_type: str = "additive",
                                 outlier_size: float = 5.0,
                                 outlier_fraction: float = 0.05,
                                 seed: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Generate data with outliers for testing robust methods.
    
    Parameters
    ----------
    T : int, optional
        Sample size. Default is 100.
    k : int, optional
        Number of variables. Default is 2.
    outlier_type : str, optional
        Type of outlier: "additive", "innovative", "level_shift", "variance".
        Default is "additive".
    outlier_size : float, optional
        Size of outliers in standard deviations. Default is 5.0.
    outlier_fraction : float, optional
        Fraction of observations to contaminate. Default is 0.05.
    seed : int, optional
        Random seed.
        
    Returns
    -------
    y_contaminated : np.ndarray
        Contaminated data.
    outlier_indices : np.ndarray
        Indices of outlying observations.
    info : dict
        Information about the generated data.
        
    Notes
    -----
    This function replicates the simulation setup from Section 2.1 of
    Franses & Lucas (1998), which examines different types of outliers:
    
    - Additive Outliers (AO): Isolated measurement errors
    - Innovative Outliers: Large shocks that propagate through the system
    - Level Shifts: Permanent changes in the level
    - Variance Shifts: Changes in the variance of innovations
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate base random walk
    eps = np.random.randn(T, k)
    y_clean = np.cumsum(eps, axis=0)
    
    y_contaminated = y_clean.copy()
    n_outliers = max(1, int(T * outlier_fraction))
    
    if outlier_type == "additive":
        # Additive outliers (AO) - isolated measurement errors
        outlier_indices = np.random.choice(T, n_outliers, replace=False)
        for idx in outlier_indices:
            # Random direction
            direction = np.random.randn(k)
            direction /= np.linalg.norm(direction)
            y_contaminated[idx, :] += outlier_size * direction
            
    elif outlier_type == "innovative":
        # Innovative outliers - large innovations
        outlier_indices = np.random.choice(T - 1, n_outliers, replace=False) + 1
        for idx in outlier_indices:
            direction = np.random.randn(k)
            direction /= np.linalg.norm(direction)
            shock = outlier_size * direction
            # Shock propagates
            y_contaminated[idx:, :] += shock
            
    elif outlier_type == "level_shift":
        # Level shift - permanent change at a random point
        shift_point = np.random.randint(T // 4, 3 * T // 4)
        outlier_indices = np.array([shift_point])
        shift = outlier_size * np.ones(k)
        y_contaminated[shift_point:, :] += shift
        
    elif outlier_type == "variance":
        # Variance shift - increased variance from a point onward
        shift_point = np.random.randint(T // 2, 3 * T // 4)
        outlier_indices = np.arange(shift_point, T)
        # Regenerate with larger variance
        new_eps = np.random.randn(T - shift_point, k) * outlier_size
        y_contaminated[shift_point:, :] = y_contaminated[shift_point - 1, :] + np.cumsum(new_eps, axis=0)
        
    else:
        raise ValueError(f"Unknown outlier type: {outlier_type}")
    
    info = {
        'T': T,
        'k': k,
        'outlier_type': outlier_type,
        'outlier_size': outlier_size,
        'outlier_fraction': outlier_fraction,
        'n_outliers': len(outlier_indices),
        'y_clean': y_clean,
    }
    
    return y_contaminated, outlier_indices, info


def generate_franses_lucas_dgp(T: int = 100, seed: Optional[int] = None) -> Tuple[np.ndarray, dict]:
    """
    Generate data from the DGP used in Franses & Lucas (1998).
    
    This replicates the bivariate model from Equation (10) of the paper,
    which was derived from estimated parameters for long-run and short-run
    interest rates.
    
    Parameters
    ----------
    T : int, optional
        Sample size. Default is 100.
    seed : int, optional
        Random seed.
        
    Returns
    -------
    y : np.ndarray
        Generated data of shape (T, 2).
    params : dict
        True parameter values from the paper.
        
    Notes
    -----
    From the paper (Equation 10):
    
        (Δy_{1t})   (3.7)              (y_{1,t-1})
        (       ) = (   ) × (-0.060, 0.075, 0.018) × (y_{2,t-1}) + ε_t
        (Δy_{2t})   (-0.3)             (   1     )
    
    where ε_t ~ N(0, Σ) with Σ = [[1.00, 0.28], [0.28, 0.20]]
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Parameters from the paper (p. 462)
    alpha = np.array([[3.7], [-0.3]])  # 2x1 loading
    beta = np.array([[-0.060], [0.075], [0.018]])  # Cointegrating vector with constant
    
    # Covariance matrix
    Sigma = np.array([[1.00, 0.28], 
                      [0.28, 0.20]])
    
    # Generate innovations
    eps = np.random.multivariate_normal(np.zeros(2), Sigma, T)
    
    # Generate data
    y = np.zeros((T, 2))
    y[0, :] = eps[0, :]
    
    for t in range(1, T):
        # Equilibrium error: β'(y_{t-1}, 1) = -0.060*y1 + 0.075*y2 + 0.018
        eq_error = beta[0, 0] * y[t-1, 0] + beta[1, 0] * y[t-1, 1] + beta[2, 0]
        
        # Error correction
        dy = alpha[:, 0] * eq_error + eps[t, :]
        
        y[t, :] = y[t-1, :] + dy
    
    params = {
        'alpha': alpha,
        'beta': beta,
        'Sigma': Sigma,
        'source': 'Franses & Lucas (1998), Equation 10',
    }
    
    return y, params
