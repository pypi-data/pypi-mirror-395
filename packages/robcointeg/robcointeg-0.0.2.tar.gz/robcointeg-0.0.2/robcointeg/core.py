"""
Core estimation routines for outlier-robust cointegration analysis.

This module implements the robust VAR estimation using Student-t 
pseudolikelihood as described in Franses & Lucas (1998).

The key equations implemented are:
- Equation (1): VAR/VECM model specification
- Equation (2): Student-t pseudolikelihood
- Equation (5): First-order condition for MPL estimator
- Equation (8): Observation weights
- Equation (9): Weighted first-order condition

References:
    Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis",
    Journal of Business & Economic Statistics, 16:4, 459-468.
    
    Lucas, A. (1997). "Cointegration Testing Using Pseudo Likelihood Ratio Tests",
    Econometric Theory, 13, 149-169.
"""

import numpy as np
from numpy.linalg import inv, det, slogdet, eig, cholesky
from scipy.special import gammaln
from scipy.optimize import minimize
from typing import Tuple, Optional, Dict, List, Union
import warnings
from dataclasses import dataclass, field

from .utils import (
    difference_matrix, 
    lag_matrix, 
    vec_ar_to_vecm,
    compute_residuals_vecm,
    compute_covariance_matrix,
    reduced_rank_regression,
    akaike_criterion,
    schwarz_criterion,
)


@dataclass
class VAREstimationResult:
    """
    Container for VAR estimation results.
    
    Attributes
    ----------
    Pi : np.ndarray
        Long-run impact matrix (αβ').
    alpha : np.ndarray
        Loading matrix.
    beta : np.ndarray
        Cointegrating vectors.
    Gamma : List[np.ndarray]
        Short-run coefficient matrices.
    mu : np.ndarray
        Intercept vector.
    Sigma : np.ndarray
        Residual covariance matrix.
    residuals : np.ndarray
        Model residuals.
    weights : np.ndarray
        Observation weights from Student-t estimation.
    nu : float
        Degrees of freedom parameter.
    log_likelihood : float
        Log pseudolikelihood value.
    eigenvalues : np.ndarray
        Eigenvalues from reduced rank regression.
    T : int
        Effective sample size.
    k : int
        Number of variables.
    p : int
        VAR lag order.
    method : str
        Estimation method used.
    converged : bool
        Whether the optimization converged.
    n_iterations : int
        Number of iterations.
    """
    Pi: np.ndarray
    alpha: np.ndarray
    beta: np.ndarray
    Gamma: List[np.ndarray]
    mu: np.ndarray
    Sigma: np.ndarray
    residuals: np.ndarray
    weights: np.ndarray
    nu: float
    log_likelihood: float
    eigenvalues: np.ndarray
    T: int
    k: int
    p: int
    method: str
    converged: bool
    n_iterations: int


def student_t_pseudolikelihood(residuals: np.ndarray, V: np.ndarray, 
                                nu: float) -> float:
    """
    Compute the Student-t pseudolikelihood.
    
    Implements Equation (2) from Franses & Lucas (1998):
    
        L(θ) = ∏_{t=1}^T [Γ((ν+k)/2) / (Γ(ν/2)|πνV|^{1/2})] 
               × (1 + ε_t'V^{-1}ε_t/ν)^{-(ν+k)/2}
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual matrix of shape (T, k).
    V : np.ndarray
        Scale matrix (covariance matrix) of shape (k, k).
    nu : float
        Degrees of freedom parameter.
        
    Returns
    -------
    float
        Log pseudolikelihood value.
        
    Notes
    -----
    We use the log-likelihood for numerical stability:
    
        log L(θ) = T × [log Γ((ν+k)/2) - log Γ(ν/2) - (k/2)log(πν) - (1/2)log|V|]
                   - ((ν+k)/2) × Σ_{t=1}^T log(1 + ε_t'V^{-1}ε_t/ν)
                   
    For the Gaussian case (ν → ∞), use gaussian_likelihood instead.
    """
    T, k = residuals.shape
    
    # For Gaussian case, use Gaussian likelihood
    if nu == np.inf or nu > 1e10:
        return gaussian_likelihood(residuals, V)
    
    # Ensure V is positive definite
    try:
        V_inv = inv(V)
        sign, logdet_V = slogdet(V)
        if sign <= 0:
            return -np.inf
    except np.linalg.LinAlgError:
        return -np.inf
    
    # Constant term
    const = (gammaln((nu + k) / 2) - gammaln(nu / 2) 
             - (k / 2) * np.log(np.pi * nu) 
             - 0.5 * logdet_V)
    
    # Sum over observations
    log_lik = T * const
    
    for t in range(T):
        eps_t = residuals[t, :]
        quad_form = eps_t @ V_inv @ eps_t
        if quad_form < 0:
            quad_form = 0
        log_lik -= ((nu + k) / 2) * np.log(1 + quad_form / nu)
    
    return log_lik


def gaussian_likelihood(residuals: np.ndarray, V: np.ndarray) -> float:
    """
    Compute the Gaussian likelihood (limiting case when ν → ∞).
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual matrix of shape (T, k).
    V : np.ndarray
        Covariance matrix of shape (k, k).
        
    Returns
    -------
    float
        Log-likelihood value.
    """
    T, k = residuals.shape
    
    try:
        V_inv = inv(V)
        sign, logdet_V = slogdet(V)
        if sign <= 0:
            return -np.inf
    except np.linalg.LinAlgError:
        return -np.inf
    
    const = -0.5 * (k * np.log(2 * np.pi) + logdet_V)
    
    log_lik = T * const
    for t in range(T):
        eps_t = residuals[t, :]
        log_lik -= 0.5 * eps_t @ V_inv @ eps_t
    
    return log_lik


def compute_weights_internal(residuals: np.ndarray, V: np.ndarray, 
                              nu: float) -> np.ndarray:
    """
    Compute observation weights from Student-t estimation.
    
    Implements Equation (8) from Franses & Lucas (1998):
    
        w_t = (ν / (ν + ε_t'V^{-1}ε_t))^{1/2}
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual matrix of shape (T, k).
    V : np.ndarray
        Scale matrix of shape (k, k).
    nu : float
        Degrees of freedom parameter.
        
    Returns
    -------
    np.ndarray
        Weight vector of shape (T,).
        
    Notes
    -----
    From the paper: "One can interpret w_t as the weight for the observation 
    at time t. A low value of w_t indicates that the observation does not 
    correspond to the general pattern of the model."
    
    Note that w_t is not bounded from above by 1 but by (ν+1)/ν.
    
    For the Gaussian case (ν → ∞), all weights equal 1.
    """
    T = residuals.shape[0]
    
    # For Gaussian case (nu=inf), all weights are 1
    if nu == np.inf or nu > 1e10:
        return np.ones(T)
    
    try:
        V_inv = inv(V)
    except np.linalg.LinAlgError:
        return np.ones(T)
    
    weights = np.zeros(T)
    
    for t in range(T):
        eps_t = residuals[t, :]
        quad_form = eps_t @ V_inv @ eps_t
        # Ensure numerical stability
        if quad_form < 0:
            quad_form = 0
        weights[t] = np.sqrt(nu / (nu + quad_form))
    
    return weights


def iterative_reweighted_estimation(y: np.ndarray, p: int, nu: float = 5,
                                     max_iter: int = 100, tol: float = 1e-6,
                                     r: Optional[int] = None) -> VAREstimationResult:
    """
    Iteratively reweighted least squares for Student-t pseudolikelihood.
    
    This implements the MPL estimation by solving the first-order conditions
    in Equation (9) iteratively.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    p : int
        VAR lag order.
    nu : float, optional
        Degrees of freedom parameter. Default is 5.
    max_iter : int, optional
        Maximum number of iterations. Default is 100.
    tol : float, optional
        Convergence tolerance. Default is 1e-6.
    r : int, optional
        Cointegrating rank. If None, estimates unrestricted model.
        
    Returns
    -------
    VAREstimationResult
        Estimation results.
        
    Notes
    -----
    The algorithm iteratively computes weights based on Equation (8) and
    re-estimates the model using weighted least squares, which corresponds
    to solving the first-order condition in Equation (9):
    
        Σ_{t=1}^T [(ν + k)ε_t(θ)' / (ν + ε_t(θ)'V^{-1}ε_t(θ))] × ∂ε_t(θ)/∂θ' = 0
        
        = Σ_{t=1}^T w_t² ε_t(θ)' × ∂ε_t(θ)/∂θ'
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T_total, k = y.shape
    T = T_total - p  # Effective sample size
    
    # Construct data matrices for VECM
    Dy = difference_matrix(y)
    
    # Z0: Δy_t (dependent variable)
    Z0 = Dy[p - 1:, :]
    
    # Z1: y_{t-1} (levels for cointegration)
    Z1 = y[p - 1:T_total - 1, :]
    
    # Z2: Δy_{t-1}, ..., Δy_{t-p+1}, constant
    Z2_list = []
    for j in range(1, p):
        Z2_list.append(Dy[p - 1 - j:T_total - 1 - j, :])
    Z2_list.append(np.ones((T, 1)))  # Constant
    Z2 = np.hstack(Z2_list) if Z2_list else np.ones((T, 1))
    
    # Initialize with OLS
    X = np.hstack([Z1, Z2])
    beta_ols = np.linalg.lstsq(X, Z0, rcond=None)[0]
    residuals = Z0 - X @ beta_ols
    Sigma = compute_covariance_matrix(residuals, adjust_df=False)
    
    # Initialize weights to 1
    weights = np.ones(T)
    prev_log_lik = -np.inf
    converged = False
    n_iter = 0
    
    for iteration in range(max_iter):
        n_iter = iteration + 1
        
        # Weighted estimation
        sqrt_weights = np.sqrt(weights)
        W = np.diag(sqrt_weights)
        
        Z0_w = W @ Z0
        Z1_w = W @ Z1
        Z2_w = W @ Z2
        
        # Concentrate out Z2 effects
        if Z2.shape[1] > 0:
            # M = I - Z2(Z2'Z2)^{-1}Z2'
            try:
                Z2Z2_inv = inv(Z2_w.T @ Z2_w + 1e-10 * np.eye(Z2_w.shape[1]))
                M = np.eye(T) - Z2_w @ Z2Z2_inv @ Z2_w.T
            except np.linalg.LinAlgError:
                M = np.eye(T)
            
            R0 = M @ Z0_w
            R1 = M @ Z1_w
        else:
            R0 = Z0_w - Z0_w.mean(axis=0)
            R1 = Z1_w - Z1_w.mean(axis=0)
        
        # Reduced rank regression for Pi = αβ'
        alpha, beta, eigenvalues, eigenvectors = reduced_rank_regression(R0, R1, r=r)
        
        # Compute Pi
        if r is not None and r > 0:
            Pi = alpha @ beta.T
        else:
            Pi = alpha @ eigenvectors.T if eigenvectors is not None else np.zeros((k, k))
        
        # Estimate Gamma and mu
        X_full = np.hstack([Z1, Z2])
        
        # Compute fitted values from Pi term
        Pi_fitted = Z1 @ Pi.T
        
        # Residuals for Gamma estimation
        Z0_adj = Z0 - Pi_fitted
        
        # Weighted estimation of Gamma and mu
        if Z2.shape[1] > 0:
            try:
                gamma_mu = np.linalg.lstsq(W @ Z2, W @ Z0_adj, rcond=None)[0]
            except np.linalg.LinAlgError:
                gamma_mu = np.zeros((Z2.shape[1], k))
            
            # Extract Gamma matrices
            Gamma = []
            col_idx = 0
            for j in range(1, p):
                Gamma_j = gamma_mu[col_idx:col_idx + k, :].T
                Gamma.append(Gamma_j)
                col_idx += k
            
            # Extract mu
            mu = gamma_mu[-1, :] if Z2.shape[1] > 0 else np.zeros(k)
        else:
            Gamma = []
            mu = np.zeros(k)
        
        # Compute residuals
        fitted = Pi_fitted + Z2 @ gamma_mu if Z2.shape[1] > 0 else Pi_fitted
        residuals = Z0 - fitted
        
        # Update covariance matrix (scale matrix V)
        Sigma = compute_covariance_matrix(residuals, adjust_df=False)
        
        # Add regularization for stability
        Sigma = Sigma + 1e-10 * np.eye(k)
        
        # Update weights using Equation (8)
        weights = compute_weights_internal(residuals, Sigma, nu)
        
        # Compute log pseudolikelihood
        log_lik = student_t_pseudolikelihood(residuals, Sigma, nu)
        
        # Check convergence
        if abs(log_lik - prev_log_lik) < tol:
            converged = True
            break
        
        prev_log_lik = log_lik
    
    # Final alpha and beta decomposition if r is specified
    if r is not None and r > 0:
        # Normalize beta (first r×r block is identity)
        try:
            beta_normalized = beta @ inv(beta[:r, :].T @ beta[:r, :]) @ beta[:r, :].T
            alpha_normalized = (R0.T @ R1 @ beta) / T
        except np.linalg.LinAlgError:
            beta_normalized = beta
            alpha_normalized = alpha
    else:
        beta_normalized = eigenvectors if eigenvectors is not None else np.eye(k)
        alpha_normalized = alpha
    
    return VAREstimationResult(
        Pi=Pi,
        alpha=alpha_normalized,
        beta=beta_normalized,
        Gamma=Gamma,
        mu=mu,
        Sigma=Sigma,
        residuals=residuals,
        weights=weights,
        nu=nu,
        log_likelihood=log_lik,
        eigenvalues=eigenvalues,
        T=T,
        k=k,
        p=p,
        method="student-t" if nu < np.inf else "gaussian",
        converged=converged,
        n_iterations=n_iter
    )


def robust_var_estimate(y: np.ndarray, p: int, nu: float = 5,
                        r: Optional[int] = None,
                        max_iter: int = 100, tol: float = 1e-6) -> VAREstimationResult:
    """
    Estimate a VAR model using Student-t pseudolikelihood (robust estimation).
    
    This is the main estimation function implementing the methodology of
    Franses & Lucas (1998) for outlier-robust VAR/VECM estimation.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k) where T is the number of observations
        and k is the number of variables.
    p : int
        VAR lag order.
    nu : float, optional
        Degrees of freedom parameter for Student-t pseudolikelihood.
        Default is 5, as recommended in the paper.
        Use np.inf for Gaussian estimation (Johansen method).
    r : int, optional
        Cointegrating rank. If None, estimates unrestricted model.
    max_iter : int, optional
        Maximum number of iterations. Default is 100.
    tol : float, optional
        Convergence tolerance. Default is 1e-6.
        
    Returns
    -------
    VAREstimationResult
        Object containing all estimation results.
        
    Examples
    --------
    >>> import numpy as np
    >>> from robcointeg import robust_var_estimate
    >>> 
    >>> # Generate sample data
    >>> np.random.seed(42)
    >>> T = 100
    >>> y = np.cumsum(np.random.randn(T, 2), axis=0)
    >>> 
    >>> # Robust estimation with nu=5
    >>> result = robust_var_estimate(y, p=2, nu=5)
    >>> print(f"Log-likelihood: {result.log_likelihood:.2f}")
    >>> print(f"Converged: {result.converged}")
    
    Notes
    -----
    The choice of ν = 5 is based on extensive Monte Carlo simulations
    as described in Franses & Lucas (1998). This value represents a
    reasonable compromise between reducing sensitivity to outliers
    and maintaining good power when outliers are absent.
    """
    return iterative_reweighted_estimation(y, p, nu, max_iter, tol, r)


class RobustVAR:
    """
    Robust VAR/VECM model with Student-t pseudolikelihood estimation.
    
    This class provides an object-oriented interface for robust VAR estimation
    and cointegration testing following Franses & Lucas (1998).
    
    Parameters
    ----------
    p : int
        VAR lag order.
    nu : float, optional
        Degrees of freedom parameter. Default is 5.
    with_constant : bool, optional
        Include constant term. Default is True.
        
    Attributes
    ----------
    is_fitted : bool
        Whether the model has been estimated.
    result : VAREstimationResult
        Estimation results (available after fitting).
        
    Examples
    --------
    >>> from robcointeg import RobustVAR
    >>> import numpy as np
    >>> 
    >>> # Generate data
    >>> np.random.seed(42)
    >>> y = np.cumsum(np.random.randn(100, 2), axis=0)
    >>> 
    >>> # Fit model
    >>> model = RobustVAR(p=2, nu=5)
    >>> model.fit(y)
    >>> 
    >>> # Access results
    >>> print(model.weights)
    >>> print(model.log_likelihood)
    """
    
    def __init__(self, p: int, nu: float = 5, with_constant: bool = True):
        """
        Initialize the RobustVAR model.
        
        Parameters
        ----------
        p : int
            VAR lag order.
        nu : float, optional
            Degrees of freedom parameter. Default is 5.
        with_constant : bool, optional
            Include constant term. Default is True.
        """
        self.p = p
        self.nu = nu
        self.with_constant = with_constant
        self.is_fitted = False
        self.result = None
        self._y = None
    
    def fit(self, y: np.ndarray, r: Optional[int] = None,
            max_iter: int = 100, tol: float = 1e-6) -> 'RobustVAR':
        """
        Fit the model to data.
        
        Parameters
        ----------
        y : np.ndarray
            Data array of shape (T, k).
        r : int, optional
            Cointegrating rank.
        max_iter : int, optional
            Maximum iterations. Default is 100.
        tol : float, optional
            Convergence tolerance. Default is 1e-6.
            
        Returns
        -------
        self
            Fitted model instance.
        """
        self._y = np.asarray(y)
        if self._y.ndim == 1:
            self._y = self._y.reshape(-1, 1)
        
        self.result = robust_var_estimate(
            self._y, self.p, self.nu, r, max_iter, tol
        )
        self.is_fitted = True
        
        return self
    
    @property
    def weights(self) -> np.ndarray:
        """Get observation weights."""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        return self.result.weights
    
    @property
    def residuals(self) -> np.ndarray:
        """Get model residuals."""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        return self.result.residuals
    
    @property
    def log_likelihood(self) -> float:
        """Get log pseudolikelihood."""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        return self.result.log_likelihood
    
    @property
    def Pi(self) -> np.ndarray:
        """Get long-run impact matrix."""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        return self.result.Pi
    
    @property
    def alpha(self) -> np.ndarray:
        """Get loading matrix."""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        return self.result.alpha
    
    @property
    def beta(self) -> np.ndarray:
        """Get cointegrating vectors."""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        return self.result.beta
    
    @property
    def eigenvalues(self) -> np.ndarray:
        """Get eigenvalues from reduced rank regression."""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        return self.result.eigenvalues
    
    def predict(self, steps: int = 1) -> np.ndarray:
        """
        Generate forecasts.
        
        Parameters
        ----------
        steps : int, optional
            Number of steps ahead to forecast. Default is 1.
            
        Returns
        -------
        np.ndarray
            Forecasts of shape (steps, k).
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Get last observations
        y_last = self._y[-self.p:, :]
        
        forecasts = []
        for h in range(steps):
            # Compute Δy_t forecast
            # Use the VECM representation
            Pi = self.result.Pi
            Gamma = self.result.Gamma
            mu = self.result.mu
            
            # Latest level
            y_t_minus_1 = y_last[-1, :] if h == 0 else y_last[-1, :] + sum(forecasts)
            
            # Compute Δy forecast
            dy_forecast = Pi @ y_t_minus_1 + mu
            
            # Add short-run dynamics (simplified)
            for j, G in enumerate(Gamma):
                if h - j - 1 >= 0 and h - j - 1 < len(forecasts):
                    dy_forecast += G @ forecasts[h - j - 1]
            
            forecasts.append(dy_forecast)
        
        return np.array(forecasts)
    
    def summary(self) -> str:
        """
        Generate a summary of the estimation results.
        
        Returns
        -------
        str
            Formatted summary string.
        """
        if not self.is_fitted:
            return "Model not fitted."
        
        r = self.result
        lines = []
        lines.append("\n" + "=" * 70)
        lines.append("Robust VAR Estimation Results (Student-t Pseudolikelihood)")
        lines.append("=" * 70)
        lines.append(f"\nMethod: {r.method}")
        lines.append(f"Degrees of Freedom (ν): {r.nu}")
        lines.append(f"VAR Order (p): {r.p}")
        lines.append(f"Number of Variables (k): {r.k}")
        lines.append(f"Effective Sample Size (T): {r.T}")
        lines.append(f"\nLog Pseudolikelihood: {r.log_likelihood:.4f}")
        lines.append(f"Converged: {r.converged}")
        lines.append(f"Iterations: {r.n_iterations}")
        
        lines.append("\n" + "-" * 70)
        lines.append("Eigenvalues (sorted):")
        for i, ev in enumerate(r.eigenvalues):
            lines.append(f"  λ_{i+1} = {ev:.6f}")
        
        lines.append("\n" + "-" * 70)
        lines.append("Long-run Impact Matrix (Π = αβ'):")
        lines.append(np.array2string(r.Pi, precision=4))
        
        lines.append("\n" + "-" * 70)
        lines.append("Weight Statistics:")
        lines.append(f"  Min weight: {r.weights.min():.4f}")
        lines.append(f"  Max weight: {r.weights.max():.4f}")
        lines.append(f"  Mean weight: {r.weights.mean():.4f}")
        n_low = np.sum(r.weights < 0.67)
        lines.append(f"  Observations with w_t < 0.67: {n_low}")
        
        lines.append("\n" + "=" * 70)
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        status = "fitted" if self.is_fitted else "not fitted"
        return f"RobustVAR(p={self.p}, nu={self.nu}, {status})"
