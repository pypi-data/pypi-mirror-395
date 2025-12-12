"""
Weight computation and outlier detection for robust cointegration analysis.

This module implements the observation weighting scheme from Franses & Lucas (1998)
and provides tools for identifying outlying observations.

The key equations implemented are:
- Equation (6): Weight formula w_t²
- Equation (8): Square root weight formula w_t
- Decision rule based on χ² distribution

References:
    Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis",
    Journal of Business & Economic Statistics, 16:4, 459-468.
"""

import numpy as np
from numpy.linalg import inv
from scipy.stats import chi2
from typing import Tuple, List, Optional, Dict, Union
from dataclasses import dataclass
import warnings


@dataclass
class OutlierDetectionResult:
    """
    Container for outlier detection results.
    
    Attributes
    ----------
    weights : np.ndarray
        Observation weights w_t.
    outlier_indices : np.ndarray
        Indices of observations identified as outliers.
    outlier_dates : List
        Time indices or dates of outliers (if provided).
    threshold : float
        Weight threshold used for classification.
    n_outliers : int
        Number of detected outliers.
    outlier_fraction : float
        Fraction of observations classified as outliers.
    critical_value : float
        Chi-square critical value used.
    summary : str
        Textual summary of results.
    """
    weights: np.ndarray
    outlier_indices: np.ndarray
    outlier_dates: List
    threshold: float
    n_outliers: int
    outlier_fraction: float
    critical_value: float
    summary: str


def compute_weights(residuals: np.ndarray, V: np.ndarray, 
                    nu: float = 5) -> np.ndarray:
    """
    Compute observation weights from robust estimation.
    
    Implements Equation (8) from Franses & Lucas (1998):
    
        w_t = (ν / (ν + ε_t'V^{-1}ε_t))^{1/2}
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual matrix of shape (T, k).
    V : np.ndarray
        Covariance/scale matrix of shape (k, k).
    nu : float, optional
        Degrees of freedom parameter. Default is 5.
        
    Returns
    -------
    np.ndarray
        Weight vector of shape (T,).
        
    Notes
    -----
    From the paper (p. 461):
    
    "One can interpret w_t as the weight for the observation at time t. 
    A low value of w_t indicates that the observation does not correspond 
    to the general pattern of the model."
    
    "Note that w_t is not bounded from above by 1 but by (ν+1)/ν."
    
    The squared weight formula (Equation 6) is:
    
        w_t² = (1 + (y_t - μ̂)²/ν)^{-1} × (T^{-1} Σ(1 + (y_t - μ̂)²/ν)^{-1})^{-1}
    
    for the simple location model. In the multivariate case (Equation 8):
    
        w_t = (ν / (ν + ε_t'V^{-1}ε_t))^{1/2}
        
    Examples
    --------
    >>> import numpy as np
    >>> from robcointeg import compute_weights
    >>> 
    >>> # Simulate residuals
    >>> np.random.seed(42)
    >>> residuals = np.random.randn(100, 2)
    >>> V = np.cov(residuals.T)
    >>> 
    >>> # Compute weights
    >>> weights = compute_weights(residuals, V, nu=5)
    >>> print(f"Mean weight: {weights.mean():.3f}")
    >>> print(f"Min weight: {weights.min():.3f}")
    """
    if residuals.ndim == 1:
        residuals = residuals.reshape(-1, 1)
    
    T, k = residuals.shape
    
    # Ensure V is valid
    try:
        V_inv = inv(V)
    except np.linalg.LinAlgError:
        warnings.warn("Singular covariance matrix. Adding regularization.")
        V_inv = inv(V + 1e-10 * np.eye(k))
    
    weights = np.zeros(T)
    
    for t in range(T):
        eps_t = residuals[t, :]
        # Quadratic form: ε_t'V^{-1}ε_t
        quad_form = eps_t @ V_inv @ eps_t
        # Weight from Equation (8)
        weights[t] = np.sqrt(nu / (nu + quad_form))
    
    return weights


def compute_squared_weights(residuals: np.ndarray, V: np.ndarray,
                             nu: float = 5) -> np.ndarray:
    """
    Compute squared observation weights.
    
    This is the w_t² from Equation (6) which appears in the first-order
    condition (Equation 9).
    
    Parameters
    ----------
    residuals : np.ndarray
        Residual matrix of shape (T, k).
    V : np.ndarray
        Covariance matrix of shape (k, k).
    nu : float, optional
        Degrees of freedom parameter. Default is 5.
        
    Returns
    -------
    np.ndarray
        Squared weight vector of shape (T,).
        
    Notes
    -----
    From the paper, w_t² appears in the weighted estimation equation (9):
    
        Σ w_t² ε_t(θ)' ∂ε_t(θ)/∂θ' = 0
    """
    weights = compute_weights(residuals, V, nu)
    return weights ** 2


def weight_threshold(nu: float, k: int, alpha: float = 0.005) -> float:
    """
    Compute the threshold for identifying outlying observations.
    
    From the paper (p. 462):
    
    "Under the assumption that the ε_t are standard normally distributed, 
    ε_t'V^{-1}ε_t has a χ² distribution with k df. [...] Weights are then 
    found to be extraordinarily small if w_t² < (ν + k)/(ν + c_k(0.005))."
    
    Parameters
    ----------
    nu : float
        Degrees of freedom parameter.
    k : int
        Number of variables.
    alpha : float, optional
        Significance level. Default is 0.005 (0.5%) as in the paper.
        
    Returns
    -------
    float
        Threshold for w_t below which observations are considered outliers.
        
    Examples
    --------
    >>> from robcointeg import weight_threshold
    >>> # For nu=5, k=2 (bivariate case)
    >>> threshold = weight_threshold(5, 2, 0.005)
    >>> print(f"Threshold: {threshold:.3f}")
    Threshold: 0.669
    
    Notes
    -----
    The paper notes: "For example, for ν = 5 and k = 2, this means that 
    observations with weights smaller than approximately .67 deserve a 
    closer inspection."
    """
    # Critical value of χ² distribution
    c_k = chi2.ppf(1 - alpha, df=k)
    
    # Threshold for w_t²
    w_sq_threshold = (nu + k) / (nu + c_k)
    
    # Return threshold for w_t (not squared)
    return np.sqrt(w_sq_threshold)


def detect_outliers(weights: np.ndarray, nu: float, k: int,
                    alpha: float = 0.005,
                    dates: Optional[np.ndarray] = None,
                    p: int = 1) -> OutlierDetectionResult:
    """
    Detect outlying observations based on observation weights.
    
    Parameters
    ----------
    weights : np.ndarray
        Observation weights from robust estimation.
    nu : float
        Degrees of freedom parameter used in estimation.
    k : int
        Number of variables.
    alpha : float, optional
        Significance level for the χ² test. Default is 0.005.
    dates : np.ndarray, optional
        Time indices or dates corresponding to observations.
    p : int, optional
        VAR lag order (for interpreting consecutive outliers). Default is 1.
        
    Returns
    -------
    OutlierDetectionResult
        Object containing outlier detection results.
        
    Notes
    -----
    From Franses & Lucas (1998, p. 462-463):
    
    "Note that the AO can in this case be viewed as a large, negative 
    innovative outlier in period 49, followed by a large, positive 
    innovative outlier in period 50 because we consider a VAR(1) model. 
    This generalizes to VAR models of order p, in which case a patch of 
    p + 1 low weights can be expected in case of an AO."
    
    Examples
    --------
    >>> import numpy as np
    >>> from robcointeg import RobustVAR, detect_outliers
    >>> 
    >>> # Fit model and get weights
    >>> model = RobustVAR(p=2, nu=5)
    >>> model.fit(data)
    >>> 
    >>> # Detect outliers
    >>> result = detect_outliers(model.weights, nu=5, k=2)
    >>> print(f"Number of outliers: {result.n_outliers}")
    >>> print(f"Outlier indices: {result.outlier_indices}")
    """
    T = len(weights)
    
    # Compute threshold
    threshold = weight_threshold(nu, k, alpha)
    
    # Critical value
    c_k = chi2.ppf(1 - alpha, df=k)
    
    # Identify outliers
    outlier_mask = weights < threshold
    outlier_indices = np.where(outlier_mask)[0]
    n_outliers = len(outlier_indices)
    outlier_fraction = n_outliers / T
    
    # Get dates if provided
    if dates is not None:
        # Adjust for lag offset
        if len(dates) == T + p:
            adjusted_dates = dates[p:]
        else:
            adjusted_dates = dates
        outlier_dates = [adjusted_dates[i] for i in outlier_indices]
    else:
        outlier_dates = outlier_indices.tolist()
    
    # Generate summary
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("Outlier Detection Results")
    lines.append("=" * 60)
    lines.append(f"\nParameters:")
    lines.append(f"  Degrees of freedom (ν): {nu}")
    lines.append(f"  Number of variables (k): {k}")
    lines.append(f"  Significance level (α): {alpha}")
    lines.append(f"  Chi-square critical value: {c_k:.4f}")
    lines.append(f"  Weight threshold: {threshold:.4f}")
    lines.append(f"\nResults:")
    lines.append(f"  Total observations: {T}")
    lines.append(f"  Outliers detected: {n_outliers}")
    lines.append(f"  Outlier fraction: {outlier_fraction:.2%}")
    
    if n_outliers > 0:
        lines.append(f"\n  Outlying observations:")
        for i, idx in enumerate(outlier_indices[:20]):  # Show max 20
            date_str = str(outlier_dates[i]) if dates is not None else str(idx)
            lines.append(f"    t = {date_str}: w_t = {weights[idx]:.4f}")
        if n_outliers > 20:
            lines.append(f"    ... and {n_outliers - 20} more")
    
    # Check for consecutive outliers (potential AO pattern)
    if n_outliers >= 2:
        consecutive_pairs = []
        for i in range(len(outlier_indices) - 1):
            if outlier_indices[i + 1] - outlier_indices[i] == 1:
                consecutive_pairs.append((outlier_indices[i], outlier_indices[i + 1]))
        
        if consecutive_pairs:
            lines.append(f"\n  Note: {len(consecutive_pairs)} consecutive outlier pairs detected.")
            lines.append(f"  This pattern may indicate additive outliers (AO).")
            lines.append(f"  For VAR({p}), expect {p+1} consecutive low weights per AO.")
    
    lines.append("\n" + "=" * 60)
    summary = "\n".join(lines)
    
    return OutlierDetectionResult(
        weights=weights,
        outlier_indices=outlier_indices,
        outlier_dates=outlier_dates,
        threshold=threshold,
        n_outliers=n_outliers,
        outlier_fraction=outlier_fraction,
        critical_value=c_k,
        summary=summary
    )


def classify_outlier_type(weights: np.ndarray, outlier_indices: np.ndarray,
                          p: int = 1) -> Dict[str, List[int]]:
    """
    Attempt to classify outliers by type based on weight patterns.
    
    Based on the discussion in Section 2.1 of Franses & Lucas (1998):
    - Additive Outliers (AO): p+1 consecutive low weights
    - Level shifts: Low weights at start and end of shift period
    - Variance shifts: Many low weights in a contiguous region
    - Innovative outliers: Single low weight
    
    Parameters
    ----------
    weights : np.ndarray
        Observation weights.
    outlier_indices : np.ndarray
        Indices of detected outliers.
    p : int, optional
        VAR lag order. Default is 1.
        
    Returns
    -------
    dict
        Dictionary with outlier type classifications.
        
    Notes
    -----
    This is a heuristic classification. From the paper (p. 465):
    
    "In some circumstances, the weights can even be used to identify the 
    type of model failure, as in the relatively simple case of an AO. In 
    other cases, it is much more difficult, as can be seen from the graphs 
    for variance shifts and patches of innovative outliers."
    """
    if len(outlier_indices) == 0:
        return {
            "additive": [],
            "level_shift": [],
            "variance_shift": [],
            "innovative": [],
            "unclassified": []
        }
    
    T = len(weights)
    classified = set()
    results = {
        "additive": [],
        "level_shift": [],
        "variance_shift": [],
        "innovative": [],
        "unclassified": []
    }
    
    # Sort outlier indices
    sorted_indices = np.sort(outlier_indices)
    
    # Find runs of consecutive outliers
    runs = []
    current_run = [sorted_indices[0]]
    
    for i in range(1, len(sorted_indices)):
        if sorted_indices[i] - sorted_indices[i-1] == 1:
            current_run.append(sorted_indices[i])
        else:
            runs.append(current_run)
            current_run = [sorted_indices[i]]
    runs.append(current_run)
    
    for run in runs:
        run_length = len(run)
        
        if run_length == p + 1:
            # Likely additive outlier
            results["additive"].extend(run)
            classified.update(run)
        elif run_length == 2 and p == 1:
            # Could be temporary level shift or AO
            # Check if there's a matching pair later
            start_idx = run[0]
            # Look for isolated pair (level shift pattern)
            gap_found = False
            for other_run in runs:
                if other_run[0] > run[-1] + 2:
                    if len(other_run) == 1:
                        gap_found = True
                        break
            if gap_found:
                results["level_shift"].extend(run)
            else:
                results["additive"].extend(run)
            classified.update(run)
        elif run_length >= 5:
            # Long run suggests variance shift or patch of innovative outliers
            results["variance_shift"].extend(run)
            classified.update(run)
        elif run_length == 1:
            # Single outlier - innovative outlier
            results["innovative"].extend(run)
            classified.update(run)
        else:
            # Unclassified
            results["unclassified"].extend(run)
            classified.update(run)
    
    return results


def outlier_adjusted_data(y: np.ndarray, outlier_indices: np.ndarray,
                          method: str = "interpolate") -> np.ndarray:
    """
    Create outlier-adjusted data by treating detected outliers.
    
    Parameters
    ----------
    y : np.ndarray
        Original data array of shape (T, k).
    outlier_indices : np.ndarray
        Indices of observations to treat.
    method : str, optional
        Treatment method: "interpolate", "winsorize", or "remove".
        Default is "interpolate".
        
    Returns
    -------
    np.ndarray
        Adjusted data array.
        
    Notes
    -----
    From the paper (p. 460):
    
    "If the robust and nonrobust cointegration results are in conflict 
    and outliers have been identified, the practitioner has to decide 
    on how to proceed. Basically, there are two possibilities: Discard 
    the aberrant observations and retain the model, or retain all 
    observations and respecify the model."
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    y_adj = y.copy()
    T, k = y.shape
    
    if method == "interpolate":
        for idx in outlier_indices:
            if idx == 0:
                y_adj[idx, :] = y[1, :]
            elif idx == T - 1:
                y_adj[idx, :] = y[-2, :]
            else:
                y_adj[idx, :] = 0.5 * (y[idx - 1, :] + y[idx + 1, :])
    
    elif method == "winsorize":
        for j in range(k):
            q1, q99 = np.percentile(y[:, j], [1, 99])
            for idx in outlier_indices:
                if y[idx, j] < q1:
                    y_adj[idx, j] = q1
                elif y[idx, j] > q99:
                    y_adj[idx, j] = q99
    
    elif method == "remove":
        mask = np.ones(T, dtype=bool)
        mask[outlier_indices] = False
        y_adj = y[mask, :]
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return y_adj


def weight_based_diagnostics(weights: np.ndarray, nu: float, k: int) -> Dict:
    """
    Compute diagnostic statistics based on observation weights.
    
    Parameters
    ----------
    weights : np.ndarray
        Observation weights.
    nu : float
        Degrees of freedom parameter.
    k : int
        Number of variables.
        
    Returns
    -------
    dict
        Dictionary containing diagnostic statistics.
    """
    T = len(weights)
    threshold = weight_threshold(nu, k, 0.005)
    
    # Basic statistics
    stats = {
        "n_obs": T,
        "mean_weight": float(np.mean(weights)),
        "std_weight": float(np.std(weights)),
        "min_weight": float(np.min(weights)),
        "max_weight": float(np.max(weights)),
        "median_weight": float(np.median(weights)),
        "threshold_005": float(threshold),
        "n_below_threshold": int(np.sum(weights < threshold)),
        "fraction_below_threshold": float(np.mean(weights < threshold)),
    }
    
    # Quantiles
    quantiles = [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    for q in quantiles:
        stats[f"quantile_{int(q*100):02d}"] = float(np.percentile(weights, q * 100))
    
    # Upper bound check (should be ≤ sqrt((nu+1)/nu))
    upper_bound = np.sqrt((nu + 1) / nu)
    stats["upper_bound"] = float(upper_bound)
    stats["max_exceeds_bound"] = bool(np.max(weights) > upper_bound + 1e-10)
    
    return stats
