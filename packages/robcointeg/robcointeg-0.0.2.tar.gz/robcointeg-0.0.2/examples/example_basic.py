"""
Example: Robust Cointegration Analysis with Outlier Detection

This script demonstrates the complete workflow for robust cointegration
testing as described in Franses & Lucas (1998).

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
"""

import numpy as np

# Import from robcointeg
from robcointeg import (
    RobustVAR,
    compare_tests,
    detect_outliers,
    diagnostic_report,
)
from robcointeg.data import (
    generate_franses_lucas_dgp,
    generate_data_with_outliers,
)


def example_basic_usage():
    """Basic usage example: fit robust VAR model."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Robust VAR Estimation")
    print("=" * 70)
    
    # Generate sample data
    np.random.seed(42)
    T = 100
    y = np.cumsum(np.random.randn(T, 2), axis=0)
    
    # Fit robust VAR model with nu=5 (recommended in the paper)
    model = RobustVAR(p=2, nu=5)
    model.fit(y)
    
    # Print summary
    print(model.summary())
    
    # Access individual components
    print("\nEigenvalues:", model.eigenvalues)
    print("Min weight:", model.weights.min())
    print("Max weight:", model.weights.max())


def example_compare_robust_and_gaussian():
    """Compare robust and non-robust cointegration tests."""
    print("\n" + "=" * 70)
    print("Example 2: Comparing Robust and Gaussian Tests")
    print("=" * 70)
    
    np.random.seed(42)
    
    # Generate clean data
    y_clean = np.cumsum(np.random.randn(100, 2), axis=0)
    
    print("\n--- Analysis of Clean Data ---")
    comparison_clean = compare_tests(y_clean, p=2, nu=5)
    print(comparison_clean['summary'])
    
    # Add outliers
    y_outlier = y_clean.copy()
    y_outlier[50, 0] += 8  # Large additive outlier
    y_outlier[51, 0] += 8
    
    print("\n--- Analysis of Data with Outliers ---")
    comparison_outlier = compare_tests(y_outlier, p=2, nu=5)
    print(comparison_outlier['summary'])
    
    # Demonstrate the key diagnostic feature
    if comparison_outlier['conflict']:
        print("\n⚠️  The tests give different results!")
        print("This indicates the standard results may be driven by outliers.")
    else:
        print("\n✓ The tests agree - results likely robust to outliers.")


def example_outlier_detection():
    """Demonstrate outlier detection using observation weights."""
    print("\n" + "=" * 70)
    print("Example 3: Outlier Detection")
    print("=" * 70)
    
    np.random.seed(42)
    
    # Generate data with known outliers
    y, true_outliers, info = generate_data_with_outliers(
        T=100, k=2,
        outlier_type="additive",
        outlier_size=6.0,
        outlier_fraction=0.05,
        seed=42
    )
    
    print(f"\nTrue outlier indices: {true_outliers}")
    
    # Fit robust model
    model = RobustVAR(p=1, nu=5)
    model.fit(y)
    
    # Detect outliers from weights
    result = detect_outliers(model.weights, nu=5, k=2, p=1)
    print(result.summary)
    
    print(f"\nDetected outlier indices: {result.outlier_indices}")


def example_franses_lucas_dgp():
    """Analyze data from the DGP used in the paper."""
    print("\n" + "=" * 70)
    print("Example 4: Franses & Lucas (1998) DGP")
    print("=" * 70)
    
    # Generate data from the paper's DGP (Equation 10)
    y, params = generate_franses_lucas_dgp(T=100, seed=42)
    
    print("\nData generating process parameters (from p. 462):")
    print(f"  α = {params['alpha'].flatten()}")
    print(f"  Σ = \n{params['Sigma']}")
    
    # Fit model
    model = RobustVAR(p=1, nu=5)
    model.fit(y)
    
    print(model.summary())


def example_monte_carlo_demonstration():
    """Demonstrate Monte Carlo properties (simplified version of Table 2)."""
    print("\n" + "=" * 70)
    print("Example 5: Monte Carlo Demonstration (Table 2 replication)")
    print("=" * 70)
    
    n_sim = 100  # Use more for accurate results (paper used 1000)
    T = 100
    k = 2
    outlier_size = 5
    
    # Count rejections for clean and contaminated data
    gaussian_clean_reject = 0
    robust_clean_reject = 0
    gaussian_outlier_reject = 0
    robust_outlier_reject = 0
    
    np.random.seed(42)
    
    for i in range(n_sim):
        # Generate random walk (no cointegration under null)
        y = np.cumsum(np.random.randn(T, k), axis=0)
        
        # Test on clean data
        try:
            from robcointeg import plr_test
            gauss_result = plr_test(y, p=1, nu=np.inf, r=0)
            robust_result = plr_test(y, p=1, nu=5, r=0)
            
            if gauss_result.reject[0.05]:
                gaussian_clean_reject += 1
            if robust_result.reject[0.05]:
                robust_clean_reject += 1
        except:
            continue
        
        # Add outliers
        y_ao = y.copy()
        outlier_idx = np.random.randint(10, T - 10)
        y_ao[outlier_idx, :] += outlier_size * np.random.randn(k)
        
        # Test on contaminated data
        try:
            gauss_result_ao = plr_test(y_ao, p=1, nu=np.inf, r=0)
            robust_result_ao = plr_test(y_ao, p=1, nu=5, r=0)
            
            if gauss_result_ao.reject[0.05]:
                gaussian_outlier_reject += 1
            if robust_result_ao.reject[0.05]:
                robust_outlier_reject += 1
        except:
            continue
    
    print(f"\nResults from {n_sim} simulations:")
    print(f"\nClean data (should be ~5% rejection under null):")
    print(f"  Gaussian rejection rate: {100*gaussian_clean_reject/n_sim:.1f}%")
    print(f"  Robust (ν=5) rejection rate: {100*robust_clean_reject/n_sim:.1f}%")
    
    print(f"\nData with outliers:")
    print(f"  Gaussian rejection rate: {100*gaussian_outlier_reject/n_sim:.1f}%")
    print(f"  Robust (ν=5) rejection rate: {100*robust_outlier_reject/n_sim:.1f}%")
    
    print("\nNote: The Gaussian test should show inflated rejection rates")
    print("with outliers, while the robust test should be more stable.")


def main():
    """Run all examples."""
    print("\n" + "#" * 70)
    print("# ROBCOINTEG: Robust Cointegration Analysis Examples")
    print("# Based on Franses & Lucas (1998)")
    print("#" * 70)
    
    example_basic_usage()
    example_compare_robust_and_gaussian()
    example_outlier_detection()
    example_franses_lucas_dgp()
    example_monte_carlo_demonstration()
    
    print("\n" + "#" * 70)
    print("# Examples completed!")
    print("#" * 70)


if __name__ == "__main__":
    main()
