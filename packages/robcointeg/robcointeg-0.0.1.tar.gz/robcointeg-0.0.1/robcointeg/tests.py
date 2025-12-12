"""
Cointegration tests: Pseudolikelihood Ratio (PLR) and Johansen tests.

This module implements the outlier-robust cointegration test from 
Franses & Lucas (1998) based on the Student-t pseudolikelihood ratio,
as well as the standard Johansen (1991) Gaussian-based test for comparison.

The key equation implemented is Equation (3):
    PLR = 2 ln(L(θ̂)/L(θ̃))

where θ̂ and θ̃ are the parameter estimates under the alternative and 
null hypotheses, respectively.

References:
    Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis",
    Journal of Business & Economic Statistics, 16:4, 459-468.
    
    Johansen, S. (1991). "Estimation and Hypothesis Testing of Cointegration 
    Vectors in Gaussian Vector Autoregressive Models", Econometrica, 59, 1551-1580.
    
    Lucas, A. (1997). "Cointegration Testing Using Pseudo Likelihood Ratio Tests",
    Econometric Theory, 13, 149-169.
"""

import numpy as np
from numpy.linalg import inv, slogdet, eig
from typing import Tuple, Optional, Dict, List, Union
from dataclasses import dataclass
import warnings

from .core import robust_var_estimate, student_t_pseudolikelihood, gaussian_likelihood
from .critical_values import get_critical_value, CriticalValueTable
from .weights import compute_weights, detect_outliers, weight_threshold


@dataclass
class CointegrationTestResult:
    """
    Container for cointegration test results.
    
    Attributes
    ----------
    test_statistic : float
        The test statistic value.
    critical_values : Dict[float, float]
        Dictionary mapping significance levels to critical values.
    null_hypothesis : str
        Description of the null hypothesis.
    alternative_hypothesis : str
        Description of the alternative hypothesis.
    rank_tested : int
        The cointegrating rank being tested.
    p_value : Optional[float]
        Approximate p-value (if available).
    reject : Dict[float, bool]
        Dictionary indicating rejection at each significance level.
    eigenvalues : np.ndarray
        Eigenvalues from the test.
    method : str
        Test method used.
    nu : Optional[float]
        Degrees of freedom (for Student-t based test).
    """
    test_statistic: float
    critical_values: Dict[float, float]
    null_hypothesis: str
    alternative_hypothesis: str
    rank_tested: int
    p_value: Optional[float]
    reject: Dict[float, bool]
    eigenvalues: np.ndarray
    method: str
    nu: Optional[float]


@dataclass  
class RobustCointegrationTest:
    """
    Results from a complete robust cointegration analysis.
    
    Attributes
    ----------
    test_results : List[CointegrationTestResult]
        Test results for each rank hypothesis.
    selected_rank : int
        Selected cointegrating rank based on sequential testing.
    eigenvalues : np.ndarray
        All eigenvalues from the analysis.
    weights : np.ndarray
        Observation weights.
    outlier_indices : np.ndarray
        Detected outlier indices.
    log_likelihood_unrestricted : float
        Log pseudolikelihood under the unrestricted model.
    k : int
        Number of variables.
    p : int
        VAR lag order.
    T : int
        Effective sample size.
    nu : float
        Degrees of freedom parameter.
    with_drift : bool
        Whether drift was included.
    summary : str
        Textual summary of results.
    """
    test_results: List[CointegrationTestResult]
    selected_rank: int
    eigenvalues: np.ndarray
    weights: np.ndarray
    outlier_indices: np.ndarray
    log_likelihood_unrestricted: float
    k: int
    p: int
    T: int
    nu: float
    with_drift: bool
    summary: str


def plr_test(y: np.ndarray, p: int, nu: float = 5,
             r: int = 0, with_drift: bool = True,
             significance_level: float = 0.05) -> CointegrationTestResult:
    """
    Perform the Pseudolikelihood Ratio (PLR) test for cointegration.
    
    Implements Equation (3) from Franses & Lucas (1998):
    
        PLR = 2 ln(L(θ̂)/L(θ̃))
    
    where L is the Student-t pseudolikelihood from Equation (2).
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    p : int
        VAR lag order.
    nu : float, optional
        Degrees of freedom parameter. Default is 5.
    r : int, optional
        Cointegrating rank under the null hypothesis. Default is 0.
    with_drift : bool, optional
        Whether to use critical values for DGP with drift. Default is True.
    significance_level : float, optional
        Significance level for the test. Default is 0.05.
        
    Returns
    -------
    CointegrationTestResult
        Test result object.
        
    Notes
    -----
    The test compares:
        H_r: rank(Π) ≤ r (null)
        H_k: rank(Π) = k (alternative)
    
    From the paper (p. 461):
    "Because (3) is based on a ratio of two pseudolikelihoods, we call it 
    a pseudolikelihood ratio (PLR) test. Note that the test of Johansen 
    becomes a special case when ν → ∞."
    
    Examples
    --------
    >>> import numpy as np
    >>> from robcointeg import plr_test
    >>> 
    >>> # Generate cointegrated data
    >>> np.random.seed(42)
    >>> T = 100
    >>> e = np.random.randn(T, 2)
    >>> y = np.cumsum(e, axis=0)
    >>> 
    >>> # Test H0: r = 0 vs H1: r > 0
    >>> result = plr_test(y, p=1, nu=5, r=0)
    >>> print(f"Test statistic: {result.test_statistic:.2f}")
    >>> print(f"Reject at 5%: {result.reject[0.05]}")
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T_total, k = y.shape
    T = T_total - p
    
    # Estimate under alternative (unrestricted)
    result_alt = robust_var_estimate(y, p, nu, r=None)
    log_lik_alt = result_alt.log_likelihood
    eigenvalues = result_alt.eigenvalues
    
    # Estimate under null (restricted to rank r)
    if r == 0:
        # Under H0: r = 0, Π = 0
        # Estimate VAR in differences
        result_null = robust_var_estimate(np.diff(y, axis=0), p - 1 if p > 1 else 1, nu, r=None)
        log_lik_null = result_null.log_likelihood
    else:
        result_null = robust_var_estimate(y, p, nu, r=r)
        log_lik_null = result_null.log_likelihood
    
    # PLR test statistic (Equation 3)
    # Using trace test form: -T Σ_{i=r+1}^k ln(1 - λ_i)
    plr_stat = 0.0
    for i in range(r, k):
        if i < len(eigenvalues) and eigenvalues[i] > 0 and eigenvalues[i] < 1:
            plr_stat -= T * np.log(1 - eigenvalues[i])
    
    # Alternative: use likelihood ratio directly
    # plr_stat = 2 * (log_lik_alt - log_lik_null)
    
    # Get critical values
    k_minus_r = k - r
    cv_table = CriticalValueTable(with_drift=with_drift)
    
    critical_values = {
        0.10: cv_table.get_critical_value(k_minus_r, nu, 0.10),
        0.05: cv_table.get_critical_value(k_minus_r, nu, 0.05),
        0.01: cv_table.get_critical_value(k_minus_r, nu, 0.01),
    }
    
    # Rejection decisions
    reject = {level: plr_stat > cv for level, cv in critical_values.items()}
    
    return CointegrationTestResult(
        test_statistic=plr_stat,
        critical_values=critical_values,
        null_hypothesis=f"rank(Π) ≤ {r}",
        alternative_hypothesis=f"rank(Π) = {k}",
        rank_tested=r,
        p_value=None,  # P-value requires simulation
        reject=reject,
        eigenvalues=eigenvalues,
        method=f"Student-t PLR (ν={nu})",
        nu=nu
    )


def johansen_trace_test(y: np.ndarray, p: int, r: int = 0,
                        with_drift: bool = True,
                        significance_level: float = 0.05) -> CointegrationTestResult:
    """
    Perform the standard Johansen trace test for cointegration.
    
    This is the Gaussian-based test from Johansen (1988, 1991), which is
    a special case of the PLR test when ν → ∞.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    p : int
        VAR lag order.
    r : int, optional
        Cointegrating rank under the null hypothesis. Default is 0.
    with_drift : bool, optional
        Whether to use critical values for DGP with drift. Default is True.
    significance_level : float, optional
        Significance level. Default is 0.05.
        
    Returns
    -------
    CointegrationTestResult
        Test result object.
        
    Notes
    -----
    The trace statistic is:
        λ_trace = -T Σ_{i=r+1}^k ln(1 - λ̂_i)
    
    where λ̂_i are the eigenvalues from the reduced rank regression.
    
    From the paper: "For ν → ∞, the distribution collapses to the one 
    derived by Johansen (1988, 1991)."
    """
    return plr_test(y, p, nu=np.inf, r=r, with_drift=with_drift,
                    significance_level=significance_level)


def sequential_plr_test(y: np.ndarray, p: int, nu: float = 5,
                        with_drift: bool = True,
                        significance_level: float = 0.05,
                        detect_outliers_flag: bool = True,
                        alpha_outlier: float = 0.005) -> RobustCointegrationTest:
    """
    Perform sequential PLR testing for cointegrating rank determination.
    
    Tests H_0: r = 0, H_1: r = 1, ..., H_{k-1}: r = k-1 sequentially
    until the first non-rejection.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    p : int
        VAR lag order.
    nu : float, optional
        Degrees of freedom parameter. Default is 5.
    with_drift : bool, optional
        Whether to use critical values with drift. Default is True.
    significance_level : float, optional
        Significance level. Default is 0.05.
    detect_outliers_flag : bool, optional
        Whether to perform outlier detection. Default is True.
    alpha_outlier : float, optional
        Significance level for outlier detection. Default is 0.005.
        
    Returns
    -------
    RobustCointegrationTest
        Complete test results including selected rank and outlier detection.
        
    Notes
    -----
    This implements the sequential testing procedure described in the paper.
    The cointegrating rank is determined by testing H_r: rank ≤ r vs 
    H_k: rank = k for r = 0, 1, ..., k-1.
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T_total, k = y.shape
    T = T_total - p
    
    # Estimate unrestricted model to get eigenvalues and weights
    result_full = robust_var_estimate(y, p, nu, r=None)
    eigenvalues = result_full.eigenvalues
    weights = result_full.weights
    log_lik_unrestricted = result_full.log_likelihood
    
    # Sequential testing
    test_results = []
    selected_rank = k  # Default to full rank
    
    for r in range(k):
        # Test H_r: rank ≤ r
        test_result = plr_test(y, p, nu, r=r, with_drift=with_drift,
                               significance_level=significance_level)
        test_results.append(test_result)
        
        # Check for non-rejection
        if not test_result.reject[significance_level]:
            selected_rank = r
            break
    
    # Outlier detection
    if detect_outliers_flag:
        outlier_result = detect_outliers(weights, nu, k, alpha=alpha_outlier, p=p)
        outlier_indices = outlier_result.outlier_indices
    else:
        outlier_indices = np.array([])
    
    # Generate summary
    summary = _generate_test_summary(
        test_results, selected_rank, eigenvalues, weights,
        outlier_indices, k, p, T, nu, with_drift, significance_level
    )
    
    return RobustCointegrationTest(
        test_results=test_results,
        selected_rank=selected_rank,
        eigenvalues=eigenvalues,
        weights=weights,
        outlier_indices=outlier_indices,
        log_likelihood_unrestricted=log_lik_unrestricted,
        k=k,
        p=p,
        T=T,
        nu=nu,
        with_drift=with_drift,
        summary=summary
    )


def compare_tests(y: np.ndarray, p: int, nu: float = 5,
                  with_drift: bool = True,
                  significance_level: float = 0.05) -> Dict:
    """
    Compare robust (Student-t) and non-robust (Gaussian) cointegration tests.
    
    This is the key diagnostic comparison recommended in the paper.
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    p : int
        VAR lag order.
    nu : float, optional
        Degrees of freedom for robust test. Default is 5.
    with_drift : bool, optional
        Whether DGP includes drift. Default is True.
    significance_level : float, optional
        Significance level. Default is 0.05.
        
    Returns
    -------
    dict
        Dictionary with comparison results including:
        - robust_test: RobustCointegrationTest results
        - gaussian_test: Johansen test results
        - rank_difference: Difference in selected ranks
        - conflict: Whether the tests give different conclusions
        - recommendation: Interpretation guidance
        
    Notes
    -----
    From the paper (p. 460):
    
    "Our outlier-robust cointegration test provides a new diagnostic tool 
    for signaling when standard cointegration results might be driven by 
    a few aberrant observations."
    
    "First, our outlier-robust test can be compared with the nonrobust test 
    to check whether the standard cointegration results are driven by a few 
    atypical events."
    
    Examples
    --------
    >>> from robcointeg import compare_tests
    >>> import numpy as np
    >>> 
    >>> # Generate data with an outlier
    >>> np.random.seed(42)
    >>> y = np.cumsum(np.random.randn(100, 2), axis=0)
    >>> y[50, 0] += 10  # Add outlier
    >>> 
    >>> # Compare tests
    >>> comparison = compare_tests(y, p=2, nu=5)
    >>> print(f"Robust rank: {comparison['robust_rank']}")
    >>> print(f"Gaussian rank: {comparison['gaussian_rank']}")
    >>> print(f"Conflict: {comparison['conflict']}")
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    k = y.shape[1]
    
    # Robust test (Student-t)
    robust_results = sequential_plr_test(y, p, nu=nu, with_drift=with_drift,
                                          significance_level=significance_level)
    robust_rank = robust_results.selected_rank
    
    # Non-robust test (Gaussian/Johansen)
    gaussian_results = sequential_plr_test(y, p, nu=np.inf, with_drift=with_drift,
                                            significance_level=significance_level,
                                            detect_outliers_flag=False)
    gaussian_rank = gaussian_results.selected_rank
    
    # Compare
    rank_difference = gaussian_rank - robust_rank
    conflict = rank_difference != 0
    
    # Generate recommendation
    if conflict:
        if gaussian_rank > robust_rank:
            recommendation = (
                "The Gaussian test indicates more cointegrating relations than the "
                "robust test. This suggests the Gaussian results may be biased toward "
                "stationarity by outliers (e.g., additive outliers). Examine the "
                "observation weights to identify influential observations."
            )
        else:
            recommendation = (
                "The robust test indicates more cointegrating relations than the "
                "Gaussian test. This is less common but may occur in specific "
                "outlier configurations. Careful examination of the data is recommended."
            )
    else:
        recommendation = (
            "The robust and Gaussian tests agree on the cointegrating rank. "
            "This suggests the results are not unduly influenced by outliers."
        )
    
    # Create comparison summary table
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("Comparison of Robust and Non-Robust Cointegration Tests")
    lines.append("=" * 70)
    lines.append(f"\nModel: VAR({p}) with {k} variables")
    lines.append(f"Sample size: {robust_results.T} (effective)")
    lines.append(f"Significance level: {significance_level:.0%}")
    
    lines.append("\n" + "-" * 70)
    lines.append("Test Statistics (Trace Test)")
    lines.append("-" * 70)
    lines.append(f"{'H0: r ≤':>10} {'Gaussian':>15} {'Student-t(ν='+str(nu)+')':>20}")
    lines.append("-" * 70)
    
    for i in range(min(len(robust_results.test_results), len(gaussian_results.test_results))):
        r = robust_results.test_results[i].rank_tested
        gauss_stat = gaussian_results.test_results[i].test_statistic
        robust_stat = robust_results.test_results[i].test_statistic
        gauss_cv = gaussian_results.test_results[i].critical_values[significance_level]
        robust_cv = robust_results.test_results[i].critical_values[significance_level]
        
        gauss_sig = "*" if gauss_stat > gauss_cv else ""
        robust_sig = "*" if robust_stat > robust_cv else ""
        
        lines.append(f"{r:>10} {gauss_stat:>14.2f}{gauss_sig:<1} {robust_stat:>19.2f}{robust_sig:<1}")
    
    lines.append("-" * 70)
    lines.append(f"{'Selected rank:':>10} {gaussian_rank:>15} {robust_rank:>20}")
    lines.append("\n* indicates rejection at the specified significance level")
    
    lines.append("\n" + "-" * 70)
    lines.append("Diagnosis")
    lines.append("-" * 70)
    lines.append(f"Conflict: {'Yes' if conflict else 'No'}")
    lines.append(f"Rank difference (Gaussian - Robust): {rank_difference}")
    lines.append(f"\n{recommendation}")
    
    if len(robust_results.outlier_indices) > 0:
        lines.append(f"\nOutliers detected: {len(robust_results.outlier_indices)}")
        lines.append(f"Outlier indices: {robust_results.outlier_indices[:10]}")
        if len(robust_results.outlier_indices) > 10:
            lines.append(f"... and {len(robust_results.outlier_indices) - 10} more")
    
    lines.append("\n" + "=" * 70)
    comparison_summary = "\n".join(lines)
    
    return {
        "robust_test": robust_results,
        "gaussian_test": gaussian_results,
        "robust_rank": robust_rank,
        "gaussian_rank": gaussian_rank,
        "rank_difference": rank_difference,
        "conflict": conflict,
        "recommendation": recommendation,
        "summary": comparison_summary,
        "eigenvalues_robust": robust_results.eigenvalues,
        "eigenvalues_gaussian": gaussian_results.eigenvalues,
        "weights": robust_results.weights,
        "outlier_indices": robust_results.outlier_indices,
    }


def _generate_test_summary(test_results: List[CointegrationTestResult],
                           selected_rank: int, eigenvalues: np.ndarray,
                           weights: np.ndarray, outlier_indices: np.ndarray,
                           k: int, p: int, T: int, nu: float,
                           with_drift: bool, significance_level: float) -> str:
    """Generate a formatted summary of test results."""
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("Robust Cointegration Analysis Results")
    lines.append("Franses & Lucas (1998) PLR Test")
    lines.append("=" * 70)
    
    lines.append(f"\nModel Specification:")
    lines.append(f"  VAR order (p): {p}")
    lines.append(f"  Number of variables (k): {k}")
    lines.append(f"  Effective sample size (T): {T}")
    lines.append(f"  Degrees of freedom (ν): {nu if nu < np.inf else '∞ (Gaussian)'}")
    lines.append(f"  Drift included: {'Yes' if with_drift else 'No'}")
    
    lines.append(f"\n" + "-" * 70)
    lines.append(f"Eigenvalues:")
    for i, ev in enumerate(eigenvalues):
        lines.append(f"  λ_{i+1} = {ev:.6f}")
    
    lines.append(f"\n" + "-" * 70)
    lines.append(f"Sequential Trace Tests (significance level: {significance_level:.0%})")
    lines.append("-" * 70)
    lines.append(f"{'H0':>10} {'Statistic':>12} {'CV ('+str(int(100-100*significance_level))+'%)':>12} {'Decision':>12}")
    lines.append("-" * 70)
    
    for result in test_results:
        stat = result.test_statistic
        cv = result.critical_values[significance_level]
        decision = "Reject" if result.reject[significance_level] else "Accept"
        lines.append(f"{'r ≤ ' + str(result.rank_tested):>10} {stat:>12.2f} {cv:>12.2f} {decision:>12}")
    
    lines.append("-" * 70)
    lines.append(f"Selected cointegrating rank: r = {selected_rank}")
    
    lines.append(f"\n" + "-" * 70)
    lines.append("Outlier Analysis:")
    lines.append("-" * 70)
    threshold = weight_threshold(nu, k, 0.005)
    lines.append(f"  Weight threshold (α=0.005): {threshold:.4f}")
    lines.append(f"  Min weight: {weights.min():.4f}")
    lines.append(f"  Max weight: {weights.max():.4f}")
    lines.append(f"  Mean weight: {weights.mean():.4f}")
    lines.append(f"  Outliers detected: {len(outlier_indices)}")
    
    if len(outlier_indices) > 0:
        lines.append(f"  Outlier time indices: {outlier_indices[:10].tolist()}")
        if len(outlier_indices) > 10:
            lines.append(f"  ... and {len(outlier_indices) - 10} more")
    
    lines.append("\n" + "=" * 70)
    
    return "\n".join(lines)


def monte_carlo_critical_values(k_minus_r: int, nu: float, n_sim: int = 10000,
                                 T: int = 100, with_drift: bool = True,
                                 seed: Optional[int] = None) -> Dict[float, float]:
    """
    Simulate critical values for the PLR test.
    
    Parameters
    ----------
    k_minus_r : int
        Number of common stochastic trends.
    nu : float
        Degrees of freedom parameter.
    n_sim : int, optional
        Number of Monte Carlo simulations. Default is 10000.
    T : int, optional
        Sample size. Default is 100.
    with_drift : bool, optional
        Whether to include drift. Default is True.
    seed : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    dict
        Dictionary with quantiles (0.80, 0.90, 0.95, 0.99) as keys.
        
    Notes
    -----
    This replicates the simulation procedure described in the note to Table 1:
    
    "The entries are based on 10,000 Monte Carlo simulations. In each simulation 
    a k-r-dimensional Gaussian random walk is generated, possibly with nonzero 
    drift. Next, the PLR test of the hypothesis of 0 versus k-r cointegrating 
    relations was computed."
    """
    if seed is not None:
        np.random.seed(seed)
    
    k = k_minus_r
    test_stats = []
    
    for _ in range(n_sim):
        # Generate k-dimensional random walk
        if with_drift:
            drift = np.ones(k)  # "drift term equal to the standard deviation"
        else:
            drift = np.zeros(k)
        
        innovations = np.random.randn(T, k)
        y = np.cumsum(innovations + drift, axis=0)
        
        try:
            # Compute PLR test statistic
            result = plr_test(y, p=1, nu=nu, r=0, with_drift=with_drift)
            test_stats.append(result.test_statistic)
        except:
            continue
    
    test_stats = np.array(test_stats)
    
    return {
        0.80: float(np.percentile(test_stats, 80)),
        0.90: float(np.percentile(test_stats, 90)),
        0.95: float(np.percentile(test_stats, 95)),
        0.99: float(np.percentile(test_stats, 99)),
    }
