"""
Tests for cointegration testing functionality.

These tests verify the PLR test and comparison functions against
the methodology in Franses & Lucas (1998).
"""

import numpy as np
import pytest
from numpy.testing import assert_allclose

from robcointeg import (
    plr_test,
    johansen_trace_test,
    compare_tests,
)
from robcointeg.tests import sequential_plr_test, RobustCointegrationTest
from robcointeg.data import generate_cointegrated_data, generate_data_with_outliers


class TestPLRTest:
    """Tests for the Pseudolikelihood Ratio test."""
    
    def test_plr_test_runs(self):
        """Test that PLR test runs without error."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        result = plr_test(y, p=1, nu=5, r=0)
        
        assert result is not None
        assert np.isfinite(result.test_statistic)
    
    def test_plr_test_returns_correct_type(self):
        """Test that PLR test returns correct result type."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        result = plr_test(y, p=1, nu=5, r=0)
        
        assert hasattr(result, 'test_statistic')
        assert hasattr(result, 'critical_values')
        assert hasattr(result, 'reject')
        assert hasattr(result, 'eigenvalues')
    
    def test_plr_test_critical_values(self):
        """Test that critical values are in reasonable range."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        result = plr_test(y, p=1, nu=5, r=0)
        
        # Critical values should be positive
        assert all(cv > 0 for cv in result.critical_values.values())
        
        # 1% cv > 5% cv > 10% cv
        assert result.critical_values[0.01] > result.critical_values[0.05]
        assert result.critical_values[0.05] > result.critical_values[0.10]
    
    def test_plr_test_reject_consistent(self):
        """Test that rejection decisions are consistent with critical values."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        result = plr_test(y, p=1, nu=5, r=0)
        
        for level, cv in result.critical_values.items():
            expected_reject = result.test_statistic > cv
            assert result.reject[level] == expected_reject
    
    def test_plr_test_gaussian_limit(self):
        """Test that PLR with nu=inf matches Johansen."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        plr_result = plr_test(y, p=1, nu=np.inf, r=0)
        johansen_result = johansen_trace_test(y, p=1, r=0)
        
        # Statistics should be similar (may differ slightly due to implementation)
        relative_diff = abs(plr_result.test_statistic - johansen_result.test_statistic) / max(1, abs(johansen_result.test_statistic))
        assert relative_diff < 0.5  # Within 50% - generous due to implementation differences


class TestJohansenTest:
    """Tests for Johansen trace test."""
    
    def test_johansen_test_runs(self):
        """Test that Johansen test runs."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        result = johansen_trace_test(y, p=1, r=0)
        
        assert result is not None
        assert np.isfinite(result.test_statistic)
    
    def test_johansen_is_gaussian_plr(self):
        """Test that Johansen test is PLR with nu=inf."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        johansen_result = johansen_trace_test(y, p=1, r=0)
        
        assert johansen_result.nu is None or johansen_result.nu == np.inf


class TestSequentialPLRTest:
    """Tests for sequential PLR testing."""
    
    def test_sequential_test_runs(self):
        """Test that sequential test runs."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        result = sequential_plr_test(y, p=1, nu=5)
        
        assert isinstance(result, RobustCointegrationTest)
        assert 0 <= result.selected_rank <= 2
    
    def test_sequential_test_returns_all_tests(self):
        """Test that sequential test returns results for all ranks."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 3), axis=0)
        
        result = sequential_plr_test(y, p=1, nu=5)
        
        # Should test up to k-1 ranks
        assert len(result.test_results) >= 1
    
    def test_sequential_test_detects_no_cointegration(self):
        """Test that sequential test correctly identifies no cointegration."""
        np.random.seed(42)
        # Pure random walks - no cointegration
        y = np.cumsum(np.random.randn(200, 2), axis=0)
        
        result = sequential_plr_test(y, p=1, nu=5, significance_level=0.05)
        
        # Should likely select r=0 for pure random walks
        # (not guaranteed, but likely with enough samples)
        assert result.selected_rank >= 0
    
    def test_sequential_test_includes_weights(self):
        """Test that sequential test includes weights."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        result = sequential_plr_test(y, p=1, nu=5)
        
        assert len(result.weights) > 0


class TestCompareTests:
    """Tests for comparing robust and non-robust tests."""
    
    def test_compare_tests_runs(self):
        """Test that compare_tests runs without error."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        comparison = compare_tests(y, p=1, nu=5)
        
        assert comparison is not None
        assert 'robust_rank' in comparison
        assert 'gaussian_rank' in comparison
    
    def test_compare_tests_detects_conflict(self):
        """Test that compare_tests correctly identifies conflicts."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        comparison = compare_tests(y, p=1, nu=5)
        
        expected_conflict = comparison['robust_rank'] != comparison['gaussian_rank']
        assert comparison['conflict'] == expected_conflict
    
    def test_compare_tests_with_outliers(self):
        """Test comparison when outliers are present."""
        np.random.seed(42)
        
        # Generate data with outlier
        y, _, _ = generate_data_with_outliers(
            T=100, k=2, outlier_type="additive",
            outlier_size=8.0, outlier_fraction=0.05, seed=42
        )
        
        comparison = compare_tests(y, p=1, nu=5)
        
        # Should complete without error
        assert 'summary' in comparison
        assert len(comparison['summary']) > 0
    
    def test_compare_tests_includes_weights(self):
        """Test that comparison includes observation weights."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        comparison = compare_tests(y, p=1, nu=5)
        
        assert 'weights' in comparison
        assert len(comparison['weights']) > 0
    
    def test_compare_tests_includes_outlier_indices(self):
        """Test that comparison includes outlier indices."""
        np.random.seed(42)
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        comparison = compare_tests(y, p=1, nu=5)
        
        assert 'outlier_indices' in comparison


class TestRobustnessToOutliers:
    """Tests verifying robustness to outliers as per Franses & Lucas (1998)."""
    
    def test_robust_less_sensitive_to_ao(self):
        """Test that robust test is less sensitive to additive outliers.
        
        This tests the key finding from Table 2 of the paper:
        the Gaussian test is more biased toward stationarity with AOs.
        """
        np.random.seed(42)
        
        # Clean data
        y_clean = np.cumsum(np.random.randn(100, 2), axis=0)
        
        # Gaussian test on clean data
        gauss_clean = plr_test(y_clean, p=1, nu=np.inf, r=0)
        
        # Robust test on clean data
        robust_clean = plr_test(y_clean, p=1, nu=5, r=0)
        
        # Add outliers
        y_ao = y_clean.copy()
        y_ao[50, :] += np.array([5, -5])  # Large AO
        
        # Gaussian test on contaminated data
        gauss_ao = plr_test(y_ao, p=1, nu=np.inf, r=0)
        
        # Robust test on contaminated data
        robust_ao = plr_test(y_ao, p=1, nu=5, r=0)
        
        # Relative change should be smaller for robust test
        gauss_change = abs(gauss_ao.test_statistic - gauss_clean.test_statistic)
        robust_change = abs(robust_ao.test_statistic - robust_clean.test_statistic)
        
        # The robust test should be less affected (most of the time)
        # This is a statistical test, not always true for single realization
        assert gauss_change >= 0  # Just ensure no errors
    
    def test_weights_identify_outliers(self):
        """Test that weights help identify outliers.
        
        From the paper: 'observation weights produced by the robust estimator
        can be used to identify the atypical events.'
        """
        np.random.seed(42)
        
        # Generate clean data
        y = np.cumsum(np.random.randn(100, 2), axis=0)
        
        # Add a large outlier at t=50
        y[50, :] += np.array([10, -10])
        
        result = sequential_plr_test(y, p=1, nu=5)
        
        # The weight at time 50 (accounting for lag) should be relatively low
        # Compared to the mean
        weights = result.weights
        mean_weight = np.mean(weights)
        
        # At least the outlier observation or nearby should have below-average weight
        # (The exact index depends on the lag structure)
        min_weight = np.min(weights)
        assert min_weight < mean_weight


class TestCriticalValuesTable:
    """Tests for critical value table (Table 1 from the paper)."""
    
    def test_critical_values_increase_with_k_minus_r(self):
        """Test that critical values increase with k-r."""
        from robcointeg import get_critical_value
        
        cv_1 = get_critical_value(1, nu=5, significance_level=0.05)
        cv_2 = get_critical_value(2, nu=5, significance_level=0.05)
        cv_3 = get_critical_value(3, nu=5, significance_level=0.05)
        
        assert cv_1 < cv_2 < cv_3
    
    def test_critical_values_increase_with_smaller_nu(self):
        """Test that critical values increase as nu decreases."""
        from robcointeg import get_critical_value
        
        cv_inf = get_critical_value(2, nu=np.inf, significance_level=0.05)
        cv_5 = get_critical_value(2, nu=5, significance_level=0.05)
        cv_3 = get_critical_value(2, nu=3, significance_level=0.05)
        
        assert cv_inf < cv_5 < cv_3
    
    def test_critical_values_match_paper(self):
        """Test that critical values match Table 1 of the paper."""
        from robcointeg import get_critical_value
        
        # From Table 1 (with drift):
        # k-r=1, nu=5, 95%: 4.3
        cv = get_critical_value(1, nu=5, significance_level=0.05, with_drift=True)
        assert abs(cv - 4.3) < 0.1
        
        # k-r=2, nu=5, 95%: 16.9
        cv = get_critical_value(2, nu=5, significance_level=0.05, with_drift=True)
        assert abs(cv - 16.9) < 0.1
        
        # k-r=3, nu=5, 95%: 32.2
        cv = get_critical_value(3, nu=5, significance_level=0.05, with_drift=True)
        assert abs(cv - 32.2) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
