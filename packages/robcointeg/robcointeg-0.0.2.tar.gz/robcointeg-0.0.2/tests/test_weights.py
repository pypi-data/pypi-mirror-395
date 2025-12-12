"""
Tests for weights computation and outlier detection.

These tests verify the weight computation methodology from
Franses & Lucas (1998), particularly Equations (6) and (8).
"""

import numpy as np
import pytest
from numpy.testing import assert_allclose

from robcointeg import compute_weights, detect_outliers, weight_threshold
from robcointeg.weights import (
    compute_squared_weights,
    classify_outlier_type,
    outlier_adjusted_data,
    weight_based_diagnostics,
)


class TestComputeWeights:
    """Tests for weight computation (Equation 8)."""
    
    def test_weights_shape(self):
        """Test that weights have correct shape."""
        T, k = 100, 2
        residuals = np.random.randn(T, k)
        V = np.eye(k)
        
        weights = compute_weights(residuals, V, nu=5)
        
        assert weights.shape == (T,)
    
    def test_weights_positive(self):
        """Test that weights are positive."""
        residuals = np.random.randn(100, 2)
        V = np.eye(2)
        
        weights = compute_weights(residuals, V, nu=5)
        
        assert np.all(weights > 0)
    
    def test_weights_upper_bound(self):
        """Test that weights satisfy upper bound (ν+1)/ν.
        
        From the paper (p. 461): 'Note that w_t is not bounded from above
        by 1 but by (ν+1)/ν.'
        """
        nu = 5
        residuals = np.random.randn(100, 2)
        V = np.eye(2)
        
        weights = compute_weights(residuals, V, nu=nu)
        
        upper_bound = np.sqrt((nu + 1) / nu)
        assert np.all(weights <= upper_bound + 1e-10)
    
    def test_weights_decrease_with_outliers(self):
        """Test that weights decrease for outlying observations."""
        T, k = 100, 2
        np.random.seed(42)
        residuals = np.random.randn(T, k) * 0.5
        
        # Add outlier at position 50
        residuals[50, :] = np.array([10, 10])
        
        V = np.cov(residuals.T)
        weights = compute_weights(residuals, V, nu=5)
        
        # Weight at outlier should be among the lowest
        assert weights[50] < np.mean(weights)
    
    def test_weights_approach_one_for_normal_data(self):
        """Test that weights are close to 1 for normally distributed data."""
        np.random.seed(42)
        residuals = np.random.randn(1000, 2)
        V = np.cov(residuals.T)
        
        weights = compute_weights(residuals, V, nu=5)
        
        # Mean weight should be close to 1 for normal data
        # (actual value depends on nu)
        assert 0.5 < np.mean(weights) < 1.5
    
    def test_weights_formula_equation_8(self):
        """Test that weights follow Equation (8): w_t = (ν/(ν + ε'V⁻¹ε))^0.5."""
        nu = 5
        k = 2
        residuals = np.array([[1.0, 0.5], [0.2, 0.3]])
        V = np.eye(k)
        
        weights = compute_weights(residuals, V, nu)
        
        # Manual calculation
        V_inv = np.linalg.inv(V)
        for t in range(2):
            eps = residuals[t, :]
            quad_form = eps @ V_inv @ eps
            expected_w = np.sqrt(nu / (nu + quad_form))
            assert_allclose(weights[t], expected_w, rtol=1e-10)


class TestSquaredWeights:
    """Tests for squared weights (Equation 6)."""
    
    def test_squared_weights_equal_weights_squared(self):
        """Test that squared weights equal the square of weights."""
        residuals = np.random.randn(100, 2)
        V = np.eye(2)
        
        weights = compute_weights(residuals, V, nu=5)
        weights_sq = compute_squared_weights(residuals, V, nu=5)
        
        assert_allclose(weights_sq, weights ** 2, rtol=1e-10)


class TestWeightThreshold:
    """Tests for weight threshold computation."""
    
    def test_threshold_positive(self):
        """Test that threshold is positive."""
        threshold = weight_threshold(nu=5, k=2, alpha=0.005)
        assert threshold > 0
    
    def test_threshold_less_than_one(self):
        """Test that threshold is less than 1."""
        threshold = weight_threshold(nu=5, k=2, alpha=0.005)
        assert threshold < 1
    
    def test_threshold_matches_paper(self):
        """Test threshold matches paper example.
        
        From p. 462: 'For example, for ν = 5 and k = 2, this means that
        observations with weights smaller than approximately .67 deserve
        a closer inspection.'
        """
        threshold = weight_threshold(nu=5, k=2, alpha=0.005)
        assert 0.65 < threshold < 0.70
    
    def test_threshold_increases_with_alpha(self):
        """Test that threshold increases with larger alpha (less stringent)."""
        threshold_005 = weight_threshold(nu=5, k=2, alpha=0.005)
        threshold_05 = weight_threshold(nu=5, k=2, alpha=0.05)
        
        assert threshold_05 > threshold_005
    
    def test_threshold_decreases_with_k(self):
        """Test that threshold decreases with larger k."""
        threshold_k2 = weight_threshold(nu=5, k=2, alpha=0.005)
        threshold_k5 = weight_threshold(nu=5, k=5, alpha=0.005)
        
        assert threshold_k5 < threshold_k2


class TestDetectOutliers:
    """Tests for outlier detection."""
    
    def test_detect_outliers_returns_correct_type(self):
        """Test that detect_outliers returns correct result type."""
        weights = np.random.rand(100) * 0.8 + 0.2
        
        result = detect_outliers(weights, nu=5, k=2)
        
        assert hasattr(result, 'weights')
        assert hasattr(result, 'outlier_indices')
        assert hasattr(result, 'threshold')
        assert hasattr(result, 'n_outliers')
    
    def test_detect_outliers_identifies_low_weights(self):
        """Test that detect_outliers identifies low weights as outliers."""
        np.random.seed(42)
        weights = np.ones(100) * 0.9
        
        # Add some low weights
        weights[10] = 0.3
        weights[50] = 0.4
        weights[90] = 0.2
        
        result = detect_outliers(weights, nu=5, k=2, alpha=0.005)
        
        # These low weights should be detected as outliers
        # (depending on threshold)
        if result.threshold > 0.4:
            assert 10 in result.outlier_indices
            assert 90 in result.outlier_indices
    
    def test_detect_outliers_no_false_positives_clean_data(self):
        """Test that clean data doesn't have too many false positives."""
        np.random.seed(42)
        
        # All weights above threshold
        threshold = weight_threshold(nu=5, k=2, alpha=0.005)
        weights = np.ones(100) * (threshold + 0.1)
        
        result = detect_outliers(weights, nu=5, k=2, alpha=0.005)
        
        assert result.n_outliers == 0
    
    def test_detect_outliers_with_dates(self):
        """Test outlier detection with dates provided."""
        weights = np.random.rand(100) * 0.8 + 0.2
        dates = np.arange(1900, 2000)
        
        result = detect_outliers(weights, nu=5, k=2, dates=dates)
        
        assert 'outlier_dates' in dir(result)


class TestClassifyOutlierType:
    """Tests for outlier type classification."""
    
    def test_classify_empty_outliers(self):
        """Test classification with no outliers."""
        weights = np.ones(100)
        outlier_indices = np.array([])
        
        result = classify_outlier_type(weights, outlier_indices, p=1)
        
        assert all(len(v) == 0 for v in result.values())
    
    def test_classify_single_outlier_as_innovative(self):
        """Test that single outlier is classified as innovative."""
        weights = np.ones(100)
        weights[50] = 0.3
        outlier_indices = np.array([50])
        
        result = classify_outlier_type(weights, outlier_indices, p=1)
        
        assert 50 in result['innovative']
    
    def test_classify_consecutive_as_additive(self):
        """Test that p+1 consecutive outliers are classified as additive.
        
        From the paper (p. 463): 'This generalizes to VAR models of order p,
        in which case a patch of p + 1 low weights can be expected in case
        of an AO.'
        """
        weights = np.ones(100)
        weights[50] = 0.3
        weights[51] = 0.3
        outlier_indices = np.array([50, 51])
        
        result = classify_outlier_type(weights, outlier_indices, p=1)
        
        # p=1, so p+1=2 consecutive outliers should be AO
        assert 50 in result['additive'] or 50 in result['level_shift']


class TestOutlierAdjustedData:
    """Tests for outlier adjustment methods."""
    
    def test_interpolate_method(self):
        """Test interpolation method for outlier adjustment."""
        y = np.array([[1.0, 2.0], [2.0, 3.0], [10.0, 20.0], [4.0, 5.0], [5.0, 6.0]])
        outlier_indices = np.array([2])
        
        y_adj = outlier_adjusted_data(y, outlier_indices, method='interpolate')
        
        # Position 2 should be interpolated as average of positions 1 and 3
        expected = 0.5 * (y[1, :] + y[3, :])
        assert_allclose(y_adj[2, :], expected)
    
    def test_winsorize_method(self):
        """Test winsorization method."""
        y = np.random.randn(100, 2)
        y[50, :] = np.array([100, -100])  # Extreme values
        outlier_indices = np.array([50])
        
        y_adj = outlier_adjusted_data(y, outlier_indices, method='winsorize')
        
        # Extreme values should be reduced
        assert np.abs(y_adj[50, 0]) < 100
        assert np.abs(y_adj[50, 1]) < 100
    
    def test_remove_method(self):
        """Test removal method."""
        y = np.random.randn(100, 2)
        outlier_indices = np.array([50, 60])
        
        y_adj = outlier_adjusted_data(y, outlier_indices, method='remove')
        
        assert y_adj.shape[0] == 98  # Two observations removed


class TestWeightBasedDiagnostics:
    """Tests for weight-based diagnostics."""
    
    def test_diagnostics_returns_dict(self):
        """Test that diagnostics returns a dictionary."""
        weights = np.random.rand(100) * 0.8 + 0.2
        
        stats = weight_based_diagnostics(weights, nu=5, k=2)
        
        assert isinstance(stats, dict)
    
    def test_diagnostics_contains_key_stats(self):
        """Test that diagnostics contains key statistics."""
        weights = np.random.rand(100) * 0.8 + 0.2
        
        stats = weight_based_diagnostics(weights, nu=5, k=2)
        
        assert 'mean_weight' in stats
        assert 'min_weight' in stats
        assert 'max_weight' in stats
        assert 'n_below_threshold' in stats
    
    def test_diagnostics_values_reasonable(self):
        """Test that diagnostic values are reasonable."""
        weights = np.random.rand(100) * 0.5 + 0.5
        
        stats = weight_based_diagnostics(weights, nu=5, k=2)
        
        assert 0 < stats['mean_weight'] < 2
        assert stats['min_weight'] <= stats['max_weight']
        assert 0 <= stats['n_below_threshold'] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
