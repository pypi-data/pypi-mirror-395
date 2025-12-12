"""
robcointeg: Outlier-Robust Cointegration Analysis
==================================================

A Python implementation of outlier-robust cointegration testing based on
Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis",
Journal of Business & Economic Statistics, 16:4, 459-468.

This package provides:
- Robust cointegration testing using Student-t pseudolikelihood
- Observation weights for outlier detection
- Standard Johansen cointegration tests for comparison
- Diagnostic tools and visualization

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
GitHub: https://github.com/merwanroudane/robcointeg

License: MIT
"""

__version__ = "0.0.1"
__author__ = "Dr Merwan Roudane"
__email__ = "merwanroudane920@gmail.com"

from .core import (
    RobustVAR,
    robust_var_estimate,
    student_t_pseudolikelihood,
    gaussian_likelihood,
)

from .tests import (
    RobustCointegrationTest,
    plr_test,
    johansen_trace_test,
    compare_tests,
)

from .weights import (
    compute_weights,
    detect_outliers,
    weight_threshold,
)

from .critical_values import (
    get_critical_value,
    CriticalValueTable,
)

from .diagnostics import (
    cointegration_summary,
    plot_weights,
    plot_series_with_outliers,
    diagnostic_report,
)

from .utils import (
    vec_ar_to_vecm,
    difference_matrix,
    lag_matrix,
    akaike_criterion,
    schwarz_criterion,
    select_lag_order,
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Core
    "RobustVAR",
    "robust_var_estimate",
    "student_t_pseudolikelihood",
    "gaussian_likelihood",
    # Tests
    "RobustCointegrationTest",
    "plr_test",
    "johansen_trace_test",
    "compare_tests",
    # Weights
    "compute_weights",
    "detect_outliers",
    "weight_threshold",
    # Critical values
    "get_critical_value",
    "CriticalValueTable",
    # Diagnostics
    "cointegration_summary",
    "plot_weights",
    "plot_series_with_outliers",
    "diagnostic_report",
    # Utils
    "vec_ar_to_vecm",
    "difference_matrix",
    "lag_matrix",
    "akaike_criterion",
    "schwarz_criterion",
    "select_lag_order",
]
