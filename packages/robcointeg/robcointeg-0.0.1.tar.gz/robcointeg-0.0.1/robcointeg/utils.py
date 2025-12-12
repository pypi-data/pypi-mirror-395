"""
Utility functions for robust cointegration analysis.

This module provides helper functions for VAR/VECM modeling, lag selection,
and matrix operations needed for the robust cointegration methodology.

References:
    Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis",
    Journal of Business & Economic Statistics, 16:4, 459-468.
"""

import numpy as np
from numpy.linalg import inv, det, eig, slogdet
from scipy import stats
from typing import Tuple, Optional, Union, List
import warnings


def difference_matrix(y: np.ndarray) -> np.ndarray:
    """
    Compute the first differences of a multivariate time series.
    
    Parameters
    ----------
    y : np.ndarray
        Input data array of shape (T, k) where T is the number of observations
        and k is the number of variables.
        
    Returns
    -------
    np.ndarray
        First differences of shape (T-1, k).
        
    Notes
    -----
    Implements Δy_t = y_t - y_{t-1} as defined in Franses & Lucas (1998), Eq. (1).
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    return np.diff(y, axis=0)


def lag_matrix(y: np.ndarray, p: int, include_contemporaneous: bool = False) -> np.ndarray:
    """
    Create a matrix of lagged values for VAR estimation.
    
    Parameters
    ----------
    y : np.ndarray
        Input data array of shape (T, k).
    p : int
        Number of lags.
    include_contemporaneous : bool, optional
        If True, include the contemporaneous value. Default is False.
        
    Returns
    -------
    np.ndarray
        Matrix of lagged values.
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T, k = y.shape
    
    if include_contemporaneous:
        n_cols = k * (p + 1)
        start_idx = 0
    else:
        n_cols = k * p
        start_idx = 1
    
    n_rows = T - p
    Z = np.zeros((n_rows, n_cols))
    
    for i in range(p + 1 if include_contemporaneous else p):
        lag = i if include_contemporaneous else i + 1
        col_start = i * k
        col_end = (i + 1) * k
        Z[:, col_start:col_end] = y[p - lag:T - lag, :]
    
    return Z


def vec_ar_to_vecm(Phi: List[np.ndarray], mu: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray], np.ndarray]:
    """
    Convert VAR representation to VECM representation.
    
    Transforms VAR(p) model:
        y_t = Φ_1 y_{t-1} + ... + Φ_p y_{t-p} + μ + ε_t
    
    to VECM representation (Eq. 1 in Franses & Lucas 1998):
        Δy_t = αβ'y_{t-1} + Γ_1 Δy_{t-1} + ... + Γ_{p-1} Δy_{t-p+1} + μ + ε_t
    
    Parameters
    ----------
    Phi : List[np.ndarray]
        List of VAR coefficient matrices [Φ_1, ..., Φ_p].
    mu : np.ndarray
        Intercept vector.
        
    Returns
    -------
    Pi : np.ndarray
        Long-run impact matrix Π = αβ' = Σ Φ_i - I.
    Gamma : List[np.ndarray]
        Short-run coefficient matrices [Γ_1, ..., Γ_{p-1}].
    mu : np.ndarray
        Intercept vector (unchanged).
        
    Notes
    -----
    The transformation follows Johansen (1991):
        Π = Σ_{i=1}^p Φ_i - I_k
        Γ_j = -Σ_{i=j+1}^p Φ_i  for j = 1, ..., p-1
    """
    p = len(Phi)
    k = Phi[0].shape[0]
    
    # Long-run impact matrix: Π = Σ Φ_i - I
    Pi = sum(Phi) - np.eye(k)
    
    # Short-run dynamics: Γ_j = -Σ_{i=j+1}^p Φ_i
    Gamma = []
    for j in range(p - 1):
        Gamma_j = -sum(Phi[j + 1:])
        Gamma.append(Gamma_j)
    
    return Pi, Gamma, mu


def vecm_to_vec_ar(Pi: np.ndarray, Gamma: List[np.ndarray], mu: np.ndarray) -> Tuple[List[np.ndarray], np.ndarray]:
    """
    Convert VECM representation back to VAR representation.
    
    Parameters
    ----------
    Pi : np.ndarray
        Long-run impact matrix.
    Gamma : List[np.ndarray]
        Short-run coefficient matrices.
    mu : np.ndarray
        Intercept vector.
        
    Returns
    -------
    Phi : List[np.ndarray]
        VAR coefficient matrices.
    mu : np.ndarray
        Intercept vector.
    """
    k = Pi.shape[0]
    p = len(Gamma) + 1
    
    Phi = []
    
    if p == 1:
        Phi_1 = Pi + np.eye(k)
        Phi.append(Phi_1)
    else:
        # Φ_1 = Π + I + Γ_1
        Phi_1 = Pi + np.eye(k) + Gamma[0]
        Phi.append(Phi_1)
        
        # Φ_j = Γ_j - Γ_{j-1} for j = 2, ..., p-1
        for j in range(1, p - 1):
            Phi_j = Gamma[j] - Gamma[j - 1]
            Phi.append(Phi_j)
        
        # Φ_p = -Γ_{p-1}
        Phi_p = -Gamma[-1]
        Phi.append(Phi_p)
    
    return Phi, mu


def compute_residuals_vecm(y: np.ndarray, Pi: np.ndarray, Gamma: List[np.ndarray], 
                            mu: np.ndarray) -> np.ndarray:
    """
    Compute residuals from VECM model.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    Pi : np.ndarray
        Long-run impact matrix.
    Gamma : List[np.ndarray]
        Short-run coefficient matrices.
    mu : np.ndarray
        Intercept vector.
        
    Returns
    -------
    np.ndarray
        Residuals from the VECM model.
    """
    T, k = y.shape
    p = len(Gamma) + 1
    
    Dy = difference_matrix(y)
    effective_T = T - p
    
    residuals = np.zeros((effective_T, k))
    
    for t in range(effective_T):
        t_orig = t + p
        
        # Δy_t
        dy_t = Dy[t_orig - 1, :]
        
        # αβ'y_{t-1}
        pi_term = Pi @ y[t_orig - 1, :]
        
        # Short-run dynamics
        gamma_term = np.zeros(k)
        for j, Gamma_j in enumerate(Gamma):
            gamma_term += Gamma_j @ Dy[t_orig - 2 - j, :]
        
        residuals[t, :] = dy_t - pi_term - gamma_term - mu
    
    return residuals


def compute_covariance_matrix(residuals: np.ndarray, adjust_df: bool = True,
                               n_params: int = 0) -> np.ndarray:
    """
    Compute the covariance matrix of residuals.
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual matrix of shape (T, k).
    adjust_df : bool, optional
        If True, use degrees of freedom adjustment. Default is True.
    n_params : int, optional
        Number of estimated parameters for degrees of freedom adjustment.
        
    Returns
    -------
    np.ndarray
        Covariance matrix of shape (k, k).
    """
    T, k = residuals.shape
    
    if adjust_df:
        denominator = T - n_params if n_params > 0 else T - k
    else:
        denominator = T
    
    return (residuals.T @ residuals) / denominator


def akaike_criterion(log_likelihood: float, n_params: int, T: int) -> float:
    """
    Compute the Akaike Information Criterion (AIC).
    
    Parameters
    ----------
    log_likelihood : float
        Log-likelihood value.
    n_params : int
        Number of estimated parameters.
    T : int
        Number of observations.
        
    Returns
    -------
    float
        AIC value (lower is better).
    """
    return -2 * log_likelihood / T + 2 * n_params / T


def schwarz_criterion(log_likelihood: float, n_params: int, T: int) -> float:
    """
    Compute the Schwarz/Bayesian Information Criterion (BIC/SIC).
    
    Parameters
    ----------
    log_likelihood : float
        Log-likelihood value.
    n_params : int
        Number of estimated parameters.
    T : int
        Number of observations.
        
    Returns
    -------
    float
        BIC/SIC value (lower is better).
    """
    return -2 * log_likelihood / T + n_params * np.log(T) / T


def select_lag_order(y: np.ndarray, max_lags: int = 8, criterion: str = "aic",
                     method: str = "gaussian") -> Tuple[int, dict]:
    """
    Select optimal lag order for VAR model using information criteria.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    max_lags : int, optional
        Maximum number of lags to consider. Default is 8.
    criterion : str, optional
        Information criterion to use: "aic" or "bic". Default is "aic".
    method : str, optional
        Estimation method: "gaussian" or "student-t". Default is "gaussian".
        
    Returns
    -------
    optimal_lag : int
        Optimal lag order.
    results : dict
        Dictionary containing information criteria for all lag orders.
        
    Notes
    -----
    As mentioned in Franses & Lucas (1998), both AIC and Schwarz criteria
    can be used for model selection. The paper notes that it is "yet unknown
    how model selection is affected by outliers and by the use of robust
    estimation techniques."
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T, k = y.shape
    
    results = {
        "lag": [],
        "aic": [],
        "bic": [],
        "log_likelihood": []
    }
    
    for p in range(1, max_lags + 1):
        try:
            # Simple OLS estimation for lag selection
            Dy = difference_matrix(y)
            effective_T = T - p
            
            # Construct regressors
            Y = Dy[p - 1:, :]  # Dependent variable
            
            # Lagged levels and differences
            X_list = [y[p - 1:T - 1, :]]  # y_{t-1}
            for j in range(1, p):
                X_list.append(Dy[p - 1 - j:T - 1 - j, :])  # Δy_{t-j}
            X_list.append(np.ones((effective_T, 1)))  # Constant
            
            X = np.hstack(X_list)
            
            # OLS estimation
            beta = np.linalg.lstsq(X, Y, rcond=None)[0]
            residuals = Y - X @ beta
            
            # Covariance matrix
            Sigma = (residuals.T @ residuals) / effective_T
            
            # Log-likelihood (Gaussian)
            sign, logdet = slogdet(Sigma)
            if sign <= 0:
                continue
            
            log_lik = -0.5 * effective_T * (k * np.log(2 * np.pi) + logdet + k)
            
            # Number of parameters
            n_params = k * (k * p + 1)  # VAR coefficients + constant
            
            # Information criteria
            aic = akaike_criterion(log_lik, n_params, effective_T)
            bic = schwarz_criterion(log_lik, n_params, effective_T)
            
            results["lag"].append(p)
            results["aic"].append(aic)
            results["bic"].append(bic)
            results["log_likelihood"].append(log_lik)
            
        except (np.linalg.LinAlgError, ValueError):
            continue
    
    if len(results["lag"]) == 0:
        warnings.warn("Could not estimate any VAR model. Returning lag=1.")
        return 1, results
    
    # Select optimal lag
    if criterion.lower() == "aic":
        optimal_idx = np.argmin(results["aic"])
    else:
        optimal_idx = np.argmin(results["bic"])
    
    optimal_lag = results["lag"][optimal_idx]
    
    return optimal_lag, results


def reduced_rank_regression(Z0: np.ndarray, Z1: np.ndarray, Z2: Optional[np.ndarray] = None,
                            r: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Perform reduced rank regression for cointegration analysis.
    
    This implements the Johansen (1988, 1991) procedure for estimating
    cointegrating vectors via reduced rank regression.
    
    Parameters
    ----------
    Z0 : np.ndarray
        Dependent variable (Δy_t concentrated out).
    Z1 : np.ndarray
        y_{t-1} (concentrated out).
    Z2 : np.ndarray, optional
        Additional regressors (Δy_{t-1}, ..., Δy_{t-p+1}, constant).
    r : int, optional
        Cointegrating rank. If None, returns full eigendecomposition.
        
    Returns
    -------
    alpha : np.ndarray
        Loading matrix (k × r).
    beta : np.ndarray
        Cointegrating vectors (k × r).
    eigenvalues : np.ndarray
        Eigenvalues from the canonical correlation analysis.
    eigenvectors : np.ndarray
        Eigenvectors corresponding to the eigenvalues.
        
    Notes
    -----
    Implements the maximum likelihood estimation procedure from
    Johansen (1991) as referenced in Franses & Lucas (1998).
    """
    T = Z0.shape[0]
    k = Z0.shape[1] if Z0.ndim > 1 else 1
    
    if Z0.ndim == 1:
        Z0 = Z0.reshape(-1, 1)
    if Z1.ndim == 1:
        Z1 = Z1.reshape(-1, 1)
    
    # Concentrate out Z2 if provided
    if Z2 is not None and Z2.shape[1] > 0:
        # Residuals from regressing Z0 and Z1 on Z2
        M = np.eye(T) - Z2 @ np.linalg.lstsq(Z2, np.eye(T), rcond=None)[0]
        R0 = M @ Z0
        R1 = M @ Z1
    else:
        R0 = Z0 - Z0.mean(axis=0)
        R1 = Z1 - Z1.mean(axis=0)
    
    # Moment matrices
    S00 = (R0.T @ R0) / T
    S11 = (R1.T @ R1) / T
    S01 = (R0.T @ R1) / T
    S10 = S01.T
    
    # Add small regularization for numerical stability
    eps = 1e-10
    S00 = S00 + eps * np.eye(S00.shape[0])
    S11 = S11 + eps * np.eye(S11.shape[0])
    
    # Solve generalized eigenvalue problem
    try:
        S00_inv = inv(S00)
        S11_inv = inv(S11)
        
        # Form the matrix for eigendecomposition
        M = S11_inv @ S10 @ S00_inv @ S01
        
        eigenvalues, eigenvectors = eig(M)
        
        # Sort eigenvalues in descending order
        idx = np.argsort(eigenvalues.real)[::-1]
        eigenvalues = eigenvalues.real[idx]
        eigenvectors = eigenvectors.real[:, idx]
        
        # Ensure eigenvalues are in [0, 1]
        eigenvalues = np.clip(eigenvalues, 0, 1)
        
        # Normalize eigenvectors
        for i in range(eigenvectors.shape[1]):
            norm = eigenvectors[:, i].T @ S11 @ eigenvectors[:, i]
            if norm > 0:
                eigenvectors[:, i] /= np.sqrt(norm)
        
        # Extract alpha and beta if r is specified
        if r is not None and r > 0:
            beta = eigenvectors[:, :r]
            alpha = S01 @ beta
        else:
            beta = eigenvectors
            alpha = S01 @ eigenvectors
        
    except np.linalg.LinAlgError:
        warnings.warn("Singular matrix in reduced rank regression. Using regularization.")
        eigenvalues = np.zeros(k)
        eigenvectors = np.eye(k)
        alpha = np.zeros((k, r if r else k))
        beta = np.eye(k)[:, :r] if r else np.eye(k)
    
    return alpha, beta, eigenvalues, eigenvectors


def check_stationarity(y: np.ndarray, method: str = "adf") -> dict:
    """
    Perform unit root tests on each variable.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    method : str, optional
        Test method: "adf" for Augmented Dickey-Fuller. Default is "adf".
        
    Returns
    -------
    dict
        Dictionary containing test statistics and p-values for each variable.
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T, k = y.shape
    results = {
        "variable": [],
        "statistic": [],
        "pvalue": [],
        "conclusion": []
    }
    
    for i in range(k):
        # Simple ADF test implementation
        series = y[:, i]
        Dy = np.diff(series)
        y_lag = series[:-1]
        
        # Regression: Δy_t = α + ρ*y_{t-1} + ε_t
        X = np.column_stack([np.ones(len(y_lag)), y_lag])
        beta = np.linalg.lstsq(X, Dy, rcond=None)[0]
        
        residuals = Dy - X @ beta
        sigma = np.std(residuals)
        
        # Standard error of ρ
        XtX_inv = inv(X.T @ X)
        se_rho = sigma * np.sqrt(XtX_inv[1, 1])
        
        # t-statistic
        t_stat = beta[1] / se_rho
        
        # Approximate p-value (using normal approximation, 
        # proper ADF critical values should be used in practice)
        # For unit root, critical values are non-standard
        # Using approximate critical values: -2.86 (5%), -3.43 (1%)
        if t_stat < -3.43:
            conclusion = "Stationary (1%)"
            pvalue = 0.01
        elif t_stat < -2.86:
            conclusion = "Stationary (5%)"
            pvalue = 0.05
        else:
            conclusion = "Non-stationary"
            pvalue = 0.10
        
        results["variable"].append(f"Variable {i+1}")
        results["statistic"].append(t_stat)
        results["pvalue"].append(pvalue)
        results["conclusion"].append(conclusion)
    
    return results
