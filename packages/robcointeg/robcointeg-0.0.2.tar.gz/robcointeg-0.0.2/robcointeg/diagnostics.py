"""
Diagnostic tools and visualization for robust cointegration analysis.

This module provides functions for visualizing weights, identifying outliers,
and generating publication-quality reports.

References:
    Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis",
    Journal of Business & Economic Statistics, 16:4, 459-468.
"""

import numpy as np
from typing import Optional, Tuple, List, Dict, Union
import warnings

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    warnings.warn("matplotlib not available. Plotting functions will not work.")

from .weights import weight_threshold, detect_outliers
from .tests import compare_tests, RobustCointegrationTest


def plot_weights(weights: np.ndarray, nu: float, k: int,
                 dates: Optional[np.ndarray] = None,
                 alpha: float = 0.005,
                 figsize: Tuple[float, float] = (12, 5),
                 title: Optional[str] = None,
                 save_path: Optional[str] = None,
                 show: bool = True) -> Optional[object]:
    """
    Plot observation weights with outlier threshold.
    
    Recreates Figure 1 and Figure 2 style plots from Franses & Lucas (1998).
    
    Parameters
    ----------
    weights : np.ndarray
        Observation weights from robust estimation.
    nu : float
        Degrees of freedom parameter.
    k : int
        Number of variables.
    dates : np.ndarray, optional
        Time indices or dates for x-axis.
    alpha : float, optional
        Significance level for threshold. Default is 0.005.
    figsize : Tuple[float, float], optional
        Figure size. Default is (12, 5).
    title : str, optional
        Plot title.
    save_path : str, optional
        Path to save figure.
    show : bool, optional
        Whether to display the figure. Default is True.
        
    Returns
    -------
    fig : matplotlib.figure.Figure or None
        Figure object if matplotlib is available.
        
    Examples
    --------
    >>> from robcointeg import RobustVAR, plot_weights
    >>> 
    >>> model = RobustVAR(p=2, nu=5)
    >>> model.fit(data)
    >>> plot_weights(model.weights, nu=5, k=data.shape[1])
    """
    if not HAS_MATPLOTLIB:
        warnings.warn("matplotlib not available.")
        return None
    
    T = len(weights)
    threshold = weight_threshold(nu, k, alpha)
    
    if dates is None:
        dates = np.arange(1, T + 1)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot weights
    ax.plot(dates, weights, 'b-', linewidth=1, label='Weights $w_t$')
    
    # Plot threshold
    ax.axhline(y=threshold, color='r', linestyle='--', linewidth=1.5,
               label=f'Threshold ({alpha:.1%} level): {threshold:.3f}')
    
    # Mark outliers
    outlier_mask = weights < threshold
    if np.any(outlier_mask):
        ax.scatter(dates[outlier_mask], weights[outlier_mask],
                  color='red', s=50, zorder=5, label='Outliers')
    
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('$w_t$', fontsize=12)
    
    if title is None:
        title = f'Observation Weights (ν = {nu}, k = {k})'
    ax.set_title(title, fontsize=14)
    
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    
    # Set y-axis limits
    upper_bound = np.sqrt((nu + 1) / nu)
    ax.set_ylim([0, max(upper_bound * 1.05, weights.max() * 1.05)])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def plot_series_with_outliers(y: np.ndarray, outlier_indices: np.ndarray,
                               dates: Optional[np.ndarray] = None,
                               variable_names: Optional[List[str]] = None,
                               figsize: Tuple[float, float] = (12, 8),
                               title: Optional[str] = None,
                               save_path: Optional[str] = None,
                               show: bool = True) -> Optional[object]:
    """
    Plot time series with outlying observations marked.
    
    Recreates the left panels of Figure 1 from Franses & Lucas (1998).
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    outlier_indices : np.ndarray
        Indices of outlying observations.
    dates : np.ndarray, optional
        Time indices or dates.
    variable_names : List[str], optional
        Names for each variable.
    figsize : Tuple[float, float], optional
        Figure size.
    title : str, optional
        Plot title.
    save_path : str, optional
        Path to save figure.
    show : bool, optional
        Whether to display.
        
    Returns
    -------
    fig : matplotlib.figure.Figure or None
        Figure object if matplotlib is available.
    """
    if not HAS_MATPLOTLIB:
        warnings.warn("matplotlib not available.")
        return None
    
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T, k = y.shape
    
    if dates is None:
        dates = np.arange(1, T + 1)
    
    if variable_names is None:
        variable_names = [f'$y_{{{i+1}t}}$' for i in range(k)]
    
    fig, axes = plt.subplots(k, 1, figsize=figsize, sharex=True)
    if k == 1:
        axes = [axes]
    
    for i, ax in enumerate(axes):
        # Plot series
        ax.plot(dates, y[:, i], 'b-', linewidth=1)
        
        # Mark outliers
        if len(outlier_indices) > 0:
            # Adjust indices if necessary
            valid_indices = outlier_indices[outlier_indices < T]
            ax.scatter(dates[valid_indices], y[valid_indices, i],
                      facecolors='none', edgecolors='red', s=100,
                      linewidths=2, zorder=5, label='Outlier')
        
        ax.set_ylabel(variable_names[i], fontsize=12)
        ax.grid(True, alpha=0.3)
        
        if i == 0:
            ax.legend(loc='upper right')
    
    axes[-1].set_xlabel('Time', fontsize=12)
    
    if title is None:
        title = 'Time Series with Detected Outliers'
    fig.suptitle(title, fontsize=14, y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def plot_comparison_panel(y: np.ndarray, weights: np.ndarray,
                          outlier_indices: np.ndarray,
                          nu: float, k: int,
                          dates: Optional[np.ndarray] = None,
                          variable_names: Optional[List[str]] = None,
                          figsize: Tuple[float, float] = (14, 10),
                          title: Optional[str] = None,
                          save_path: Optional[str] = None,
                          show: bool = True) -> Optional[object]:
    """
    Create a panel plot combining series and weights (like Figure 1 in the paper).
    
    Parameters
    ----------
    y : np.ndarray
        Data array.
    weights : np.ndarray
        Observation weights.
    outlier_indices : np.ndarray
        Outlier indices.
    nu : float
        Degrees of freedom.
    k : int
        Number of variables.
    dates : np.ndarray, optional
        Time indices.
    variable_names : List[str], optional
        Variable names.
    figsize : Tuple[float, float], optional
        Figure size.
    title : str, optional
        Overall title.
    save_path : str, optional
        Save path.
    show : bool, optional
        Whether to display.
        
    Returns
    -------
    fig : matplotlib.figure.Figure or None
    """
    if not HAS_MATPLOTLIB:
        warnings.warn("matplotlib not available.")
        return None
    
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T_y, n_vars = y.shape
    T_w = len(weights)
    
    if dates is None:
        dates = np.arange(1, T_y + 1)
    
    if variable_names is None:
        variable_names = [f'$y_{{{i+1}t}}$' for i in range(n_vars)]
    
    # Create figure with GridSpec
    fig = plt.figure(figsize=figsize)
    
    # Left panel: Time series
    ax1 = fig.add_subplot(1, 2, 1)
    
    for i in range(n_vars):
        style = '-' if i == 0 else '--'
        ax1.plot(dates, y[:, i], style, linewidth=1, label=variable_names[i])
    
    # Mark outliers on first series
    if len(outlier_indices) > 0:
        # Need to offset for VAR lag
        offset = T_y - T_w
        adjusted_indices = outlier_indices + offset
        valid_mask = adjusted_indices < T_y
        valid_indices = adjusted_indices[valid_mask]
        
        ax1.scatter(dates[valid_indices], y[valid_indices, 0],
                   facecolors='none', edgecolors='red', s=100,
                   linewidths=2, zorder=5, label='Outlier')
    
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Series Values', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('Time Series', fontsize=12)
    
    # Right panel: Weights
    ax2 = fig.add_subplot(1, 2, 2)
    
    threshold = weight_threshold(nu, k, 0.005)
    dates_w = dates[-T_w:] if len(dates) > T_w else dates[:T_w]
    
    ax2.plot(dates_w, weights, 'b-', linewidth=1)
    ax2.axhline(y=threshold, color='r', linestyle='--', linewidth=1.5,
                label=f'Threshold: {threshold:.3f}')
    
    outlier_mask = weights < threshold
    if np.any(outlier_mask):
        ax2.scatter(dates_w[outlier_mask], weights[outlier_mask],
                   color='red', s=50, zorder=5)
    
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('$w_t$', fontsize=12)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Observation Weights', fontsize=12)
    
    upper_bound = np.sqrt((nu + 1) / nu)
    ax2.set_ylim([0, max(upper_bound * 1.05, weights.max() * 1.05)])
    
    if title is None:
        title = f'Robust Cointegration Analysis (ν = {nu})'
    fig.suptitle(title, fontsize=14, y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def cointegration_summary(result: RobustCointegrationTest,
                          print_output: bool = True) -> str:
    """
    Generate a publication-quality summary of cointegration results.
    
    Parameters
    ----------
    result : RobustCointegrationTest
        Results from sequential PLR testing.
    print_output : bool, optional
        Whether to print the summary. Default is True.
        
    Returns
    -------
    str
        Formatted summary string.
    """
    summary = result.summary
    
    if print_output:
        print(summary)
    
    return summary


def diagnostic_report(y: np.ndarray, p: int, nu: float = 5,
                      variable_names: Optional[List[str]] = None,
                      dates: Optional[np.ndarray] = None,
                      significance_level: float = 0.05,
                      save_path: Optional[str] = None,
                      show_plots: bool = True) -> Dict:
    """
    Generate a comprehensive diagnostic report.
    
    This function performs the complete analysis recommended in
    Franses & Lucas (1998), including:
    1. Comparison of robust and non-robust tests
    2. Weight analysis and outlier detection
    3. Visualization
    
    Parameters
    ----------
    y : np.ndarray
        Data array of shape (T, k).
    p : int
        VAR lag order.
    nu : float, optional
        Degrees of freedom. Default is 5.
    variable_names : List[str], optional
        Variable names.
    dates : np.ndarray, optional
        Time indices.
    significance_level : float, optional
        Significance level. Default is 0.05.
    save_path : str, optional
        Path prefix for saving outputs.
    show_plots : bool, optional
        Whether to display plots. Default is True.
        
    Returns
    -------
    dict
        Dictionary containing all analysis results.
        
    Examples
    --------
    >>> from robcointeg import diagnostic_report
    >>> import numpy as np
    >>> 
    >>> # Load data
    >>> y = np.random.randn(100, 2).cumsum(axis=0)
    >>> 
    >>> # Run complete analysis
    >>> report = diagnostic_report(y, p=2, nu=5)
    >>> print(report['summary'])
    """
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    
    T, k = y.shape
    
    if variable_names is None:
        variable_names = [f'Variable {i+1}' for i in range(k)]
    
    if dates is None:
        dates = np.arange(1, T + 1)
    
    # Compare robust and non-robust tests
    comparison = compare_tests(y, p, nu=nu, significance_level=significance_level)
    
    # Print comparison summary
    print(comparison['summary'])
    
    # Create visualizations
    figures = {}
    
    if HAS_MATPLOTLIB:
        # Weight plot
        fig_weights = plot_weights(
            comparison['weights'], nu, k,
            dates=dates[-len(comparison['weights']):],
            title=f'Observation Weights (ν={nu})',
            save_path=f"{save_path}_weights.png" if save_path else None,
            show=show_plots
        )
        figures['weights'] = fig_weights
        
        # Series with outliers
        fig_series = plot_series_with_outliers(
            y, comparison['outlier_indices'],
            dates=dates,
            variable_names=variable_names,
            title='Time Series with Detected Outliers',
            save_path=f"{save_path}_series.png" if save_path else None,
            show=show_plots
        )
        figures['series'] = fig_series
        
        # Combined panel
        fig_panel = plot_comparison_panel(
            y, comparison['weights'], comparison['outlier_indices'],
            nu, k,
            dates=dates,
            variable_names=variable_names,
            title=f'Robust Cointegration Analysis',
            save_path=f"{save_path}_panel.png" if save_path else None,
            show=show_plots
        )
        figures['panel'] = fig_panel
    
    # Generate text report
    report_lines = []
    report_lines.append("\n" + "=" * 80)
    report_lines.append("ROBUST COINTEGRATION ANALYSIS - DIAGNOSTIC REPORT")
    report_lines.append("Based on Franses & Lucas (1998)")
    report_lines.append("=" * 80)
    
    report_lines.append("\n1. DATA DESCRIPTION")
    report_lines.append("-" * 40)
    report_lines.append(f"   Sample size: {T}")
    report_lines.append(f"   Number of variables: {k}")
    report_lines.append(f"   VAR order: {p}")
    report_lines.append(f"   Variable names: {', '.join(variable_names)}")
    
    report_lines.append("\n2. ESTIMATION SETTINGS")
    report_lines.append("-" * 40)
    report_lines.append(f"   Robust method: Student-t pseudolikelihood")
    report_lines.append(f"   Degrees of freedom (ν): {nu}")
    report_lines.append(f"   Significance level: {significance_level:.0%}")
    
    report_lines.append("\n3. COINTEGRATION TEST RESULTS")
    report_lines.append("-" * 40)
    report_lines.append(f"   Gaussian (Johansen) selected rank: {comparison['gaussian_rank']}")
    report_lines.append(f"   Robust (Student-t) selected rank: {comparison['robust_rank']}")
    report_lines.append(f"   Conflict: {'Yes' if comparison['conflict'] else 'No'}")
    
    report_lines.append("\n4. OUTLIER ANALYSIS")
    report_lines.append("-" * 40)
    n_outliers = len(comparison['outlier_indices'])
    threshold = weight_threshold(nu, k, 0.005)
    report_lines.append(f"   Weight threshold (α=0.005): {threshold:.4f}")
    report_lines.append(f"   Number of outliers detected: {n_outliers}")
    report_lines.append(f"   Outlier fraction: {n_outliers/len(comparison['weights']):.2%}")
    
    if n_outliers > 0:
        report_lines.append(f"   Outlier time indices: {comparison['outlier_indices'][:10].tolist()}")
    
    report_lines.append("\n5. INTERPRETATION")
    report_lines.append("-" * 40)
    report_lines.append(f"   {comparison['recommendation']}")
    
    report_lines.append("\n" + "=" * 80)
    
    full_report = "\n".join(report_lines)
    print(full_report)
    
    return {
        'comparison': comparison,
        'figures': figures,
        'summary': full_report,
        'robust_rank': comparison['robust_rank'],
        'gaussian_rank': comparison['gaussian_rank'],
        'conflict': comparison['conflict'],
        'weights': comparison['weights'],
        'outlier_indices': comparison['outlier_indices'],
        'eigenvalues': comparison['eigenvalues_robust'],
    }


def create_latex_table(result: RobustCointegrationTest,
                       caption: str = "Cointegration Tests",
                       label: str = "tab:coint_tests") -> str:
    """
    Create a LaTeX table of cointegration test results.
    
    Parameters
    ----------
    result : RobustCointegrationTest
        Test results.
    caption : str, optional
        Table caption.
    label : str, optional
        LaTeX label.
        
    Returns
    -------
    str
        LaTeX table code.
    """
    nu_str = f"{result.nu}" if result.nu < np.inf else r"$\infty$"
    method = f"Student-$t$ ($\\nu = {nu_str}$)" if result.nu < np.inf else "Gaussian"
    
    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(f"\\caption{{{caption}}}")
    lines.append(f"\\label{{{label}}}")
    lines.append(r"\begin{tabular}{cccccc}")
    lines.append(r"\hline\hline")
    lines.append(r"$H_0$ & Statistic & 10\% CV & 5\% CV & 1\% CV & Decision \\")
    lines.append(r"\hline")
    
    for tr in result.test_results:
        h0 = f"$r \\leq {tr.rank_tested}$"
        stat = f"{tr.test_statistic:.2f}"
        cv10 = f"{tr.critical_values[0.10]:.2f}"
        cv05 = f"{tr.critical_values[0.05]:.2f}"
        cv01 = f"{tr.critical_values[0.01]:.2f}"
        
        if tr.reject[0.01]:
            decision = "Reject$^{***}$"
        elif tr.reject[0.05]:
            decision = "Reject$^{**}$"
        elif tr.reject[0.10]:
            decision = "Reject$^{*}$"
        else:
            decision = "Accept"
        
        lines.append(f"{h0} & {stat} & {cv10} & {cv05} & {cv01} & {decision} \\\\")
    
    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\begin{tablenotes}")
    lines.append(r"\small")
    lines.append(f"\\item Method: {method}. ")
    lines.append(f"\\item $*$, $**$, $***$ denote significance at 10\\%, 5\\%, and 1\\% levels.")
    lines.append(f"\\item Selected rank: $r = {result.selected_rank}$.")
    lines.append(r"\end{tablenotes}")
    lines.append(r"\end{table}")
    
    return "\n".join(lines)
