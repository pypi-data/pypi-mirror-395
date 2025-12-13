"""
Unit tests for boot_dw package.

Tests all core functionality including DW statistic, OLS regression,
bootstrap procedures, and all test functions.
"""

import numpy as np
import pytest
from boot_dw.core import durbin_watson, ols_regression, estimate_rho, recursive_ar1_errors
from boot_dw.bootstrap import recursive_bootstrap_dw, recursive_bootstrap_rho, bca_confidence_interval
from boot_dw.tests import dw_test, bdw_test, b_rho_test, bca_rho_test, autocorrelation_test


class TestDurbinWatson:
    """Tests for Durbin-Watson statistic."""
    
    def test_dw_no_autocorrelation(self):
        """Test DW statistic with no autocorrelation (should be near 2)."""
        np.random.seed(42)
        residuals = np.random.randn(100)
        dw = durbin_watson(residuals)
        assert 1.5 < dw < 2.5, "DW should be near 2 for no autocorrelation"
    
    def test_dw_positive_autocorrelation(self):
        """Test DW statistic with positive autocorrelation (should be < 2)."""
        np.random.seed(42)
        n = 100
        rho = 0.7
        u = np.zeros(n)
        u[0] = np.random.randn()
        for t in range(1, n):
            u[t] = rho * u[t-1] + np.random.randn()
        
        dw = durbin_watson(u)
        assert dw < 2, "DW should be < 2 for positive autocorrelation"
    
    def test_dw_negative_autocorrelation(self):
        """Test DW statistic with negative autocorrelation (should be > 2)."""
        np.random.seed(42)
        n = 100
        rho = -0.5
        u = np.zeros(n)
        u[0] = np.random.randn()
        for t in range(1, n):
            u[t] = rho * u[t-1] + np.random.randn()
        
        dw = durbin_watson(u)
        assert dw > 2, "DW should be > 2 for negative autocorrelation"
    
    def test_dw_range(self):
        """Test that DW statistic is always between 0 and 4."""
        np.random.seed(42)
        for _ in range(10):
            residuals = np.random.randn(50)
            dw = durbin_watson(residuals)
            assert 0 <= dw <= 4, "DW must be in [0, 4]"


class TestOLSRegression:
    """Tests for OLS regression."""
    
    def test_ols_simple(self):
        """Test OLS with simple linear relationship."""
        np.random.seed(42)
        n = 100
        X = np.random.randn(n, 2)
        beta_true = np.array([2, -1])
        y = X @ beta_true + np.random.randn(n) * 0.1
        
        beta, residuals, fitted = ols_regression(y, X, add_constant=False)
        
        # Check coefficient estimates are close to true values
        np.testing.assert_allclose(beta, beta_true, atol=0.5)
        
        # Check residuals
        assert len(residuals) == n
        assert np.abs(np.mean(residuals)) < 0.1
    
    def test_ols_with_constant(self):
        """Test OLS with constant term."""
        np.random.seed(42)
        n = 100
        X = np.random.randn(n, 1)
        y = 3 + 2*X.flatten() + np.random.randn(n) * 0.1
        
        beta, residuals, fitted = ols_regression(y, X, add_constant=True)
        
        assert len(beta) == 2, "Should have 2 coefficients (constant + slope)"
        assert np.abs(beta[0] - 3) < 0.5, "Constant should be near 3"
        assert np.abs(beta[1] - 2) < 0.5, "Slope should be near 2"
    
    def test_ols_residuals_sum_zero(self):
        """Test that OLS residuals sum to zero (with constant)."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([1, -1]) + np.random.randn(n)
        
        beta, residuals, fitted = ols_regression(y, X, add_constant=True)
        
        assert np.abs(np.mean(residuals)) < 1e-10, "Residuals should sum to ~0"


class TestEstimateRho:
    """Tests for AR(1) coefficient estimation."""
    
    def test_estimate_rho_zero(self):
        """Test ρ estimation with white noise (should be near 0)."""
        np.random.seed(42)
        u = np.random.randn(100)
        rho = estimate_rho(u)
        assert np.abs(rho) < 0.3, "ρ should be near 0 for white noise"
    
    def test_estimate_rho_positive(self):
        """Test ρ estimation with known positive autocorrelation."""
        np.random.seed(42)
        n = 200
        rho_true = 0.7
        u = np.zeros(n)
        u[0] = np.random.randn()
        for t in range(1, n):
            u[t] = rho_true * u[t-1] + np.random.randn()
        
        rho_est = estimate_rho(u)
        assert np.abs(rho_est - rho_true) < 0.2, f"Estimated ρ should be near {rho_true}"
    
    def test_estimate_rho_negative(self):
        """Test ρ estimation with negative autocorrelation."""
        np.random.seed(42)
        n = 200
        rho_true = -0.5
        u = np.zeros(n)
        u[0] = np.random.randn()
        for t in range(1, n):
            u[t] = rho_true * u[t-1] + np.random.randn()
        
        rho_est = estimate_rho(u)
        assert rho_est < 0, "Estimated ρ should be negative"


class TestRecursiveAR1:
    """Tests for recursive AR(1) error generation."""
    
    def test_recursive_ar1_shape(self):
        """Test that recursive AR(1) returns correct shape."""
        np.random.seed(42)
        innovations = np.random.randn(100)
        errors = recursive_ar1_errors(innovations, rho=0.5)
        assert len(errors) == 100
    
    def test_recursive_ar1_stationarity(self):
        """Test that stationary initialization works."""
        np.random.seed(42)
        innovations = np.random.randn(1000)
        rho = 0.7
        errors = recursive_ar1_errors(innovations, rho=rho)
        
        # Theoretical variance for stationary AR(1): σ²/(1-ρ²)
        theoretical_var = 1.0 / (1 - rho**2)
        empirical_var = np.var(errors)
        
        # Should be reasonably close
        assert np.abs(empirical_var - theoretical_var) < 0.5


class TestBootstrapProcedures:
    """Tests for bootstrap procedures."""
    
    def test_bootstrap_dw_shape(self):
        """Test that bootstrap DW returns correct number of replications."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        beta, residuals, fitted = ols_regression(y, X, add_constant=True)
        rho = estimate_rho(residuals)
        X_full = np.column_stack([np.ones(n), X])
        
        dw_boot = recursive_bootstrap_dw(y, X_full, residuals, rho, n_bootstrap=100, random_state=42)
        
        assert len(dw_boot) == 100
        assert np.all((dw_boot >= 0) & (dw_boot <= 4)), "All DW values should be in [0,4]"
    
    def test_bootstrap_rho_shape(self):
        """Test that bootstrap ρ returns correct number of replications."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        beta, residuals, fitted = ols_regression(y, X, add_constant=True)
        rho = estimate_rho(residuals)
        X_full = np.column_stack([np.ones(n), X])
        
        rho_boot = recursive_bootstrap_rho(y, X_full, residuals, rho, n_bootstrap=100, random_state=42)
        
        assert len(rho_boot) == 100
        assert np.all(np.abs(rho_boot) < 1), "All ρ values should be in (-1,1) for stationarity"
    
    def test_bca_confidence_interval(self):
        """Test BCa confidence interval calculation."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        beta, residuals, fitted = ols_regression(y, X, add_constant=True)
        rho_obs = estimate_rho(residuals)
        X_full = np.column_stack([np.ones(n), X])
        
        rho_boot = recursive_bootstrap_rho(y, X_full, residuals, rho_obs, n_bootstrap=100, random_state=42)
        
        lower, upper, z0, a0 = bca_confidence_interval(rho_boot, rho_obs, y, X_full, alpha=0.05)
        
        assert lower < upper, "Lower bound should be less than upper bound"
        assert -1 < lower < 1, "Bounds should be valid ρ values"
        assert -1 < upper < 1, "Bounds should be valid ρ values"


class TestAutocorrelationTests:
    """Tests for main test functions."""
    
    def test_dw_test(self):
        """Test classical DW test."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        result = dw_test(y, X)
        
        assert hasattr(result, 'statistic')
        assert hasattr(result, 'pvalue')
        assert hasattr(result, 'method')
        assert 0 <= result.statistic <= 4
    
    def test_bdw_test(self):
        """Test bootstrapped DW test."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        result = bdw_test(y, X, n_bootstrap=100, random_state=42)
        
        assert hasattr(result, 'statistic')
        assert hasattr(result, 'pvalue')
        assert result.pvalue is not None
        assert 0 <= result.pvalue <= 1
    
    def test_b_rho_test(self):
        """Test bootstrapped ρ test."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        result = b_rho_test(y, X, n_bootstrap=100, random_state=42)
        
        assert hasattr(result, 'statistic')
        assert hasattr(result, 'pvalue')
        assert result.pvalue is not None
        assert 0 <= result.pvalue <= 1
        assert -1 < result.statistic < 1
    
    def test_bca_rho_test(self):
        """Test BCa-ρ test."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        result = bca_rho_test(y, X, n_bootstrap=100, random_state=42)
        
        assert hasattr(result, 'statistic')
        assert hasattr(result, 'pvalue')
        assert result.pvalue is not None
        assert 0 <= result.pvalue <= 1
        assert 'bca_interval' in result.additional_info
        assert 'bias_constant_z0' in result.additional_info
        assert 'acceleration_constant_a0' in result.additional_info
    
    def test_autocorrelation_test_methods(self):
        """Test unified interface with different methods."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        methods = ['dw', 'bdw', 'b_rho', 'bca_rho']
        
        for method in methods:
            result = autocorrelation_test(y, X, method=method, n_bootstrap=50, random_state=42)
            assert hasattr(result, 'statistic')
            assert hasattr(result, 'method')
    
    def test_alternative_hypotheses(self):
        """Test different alternative hypotheses."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        alternatives = ['greater', 'less', 'two-sided']
        
        for alt in alternatives:
            result = bca_rho_test(y, X, alternative=alt, n_bootstrap=50, random_state=42)
            assert result.alternative == alt
            assert 0 <= result.pvalue <= 1
    
    def test_reproducibility(self):
        """Test that random_state ensures reproducibility."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n, 2)
        y = X @ np.array([2, -1]) + np.random.randn(n)
        
        result1 = bca_rho_test(y, X, n_bootstrap=100, random_state=123)
        result2 = bca_rho_test(y, X, n_bootstrap=100, random_state=123)
        
        assert result1.pvalue == result2.pvalue
        assert result1.statistic == result2.statistic


class TestInputValidation:
    """Tests for input validation and edge cases."""
    
    def test_1d_X_array(self):
        """Test that 1-D X array is handled correctly."""
        np.random.seed(42)
        n = 50
        X = np.random.randn(n)  # 1-D array
        y = 2 + 3*X + np.random.randn(n)
        
        result = bca_rho_test(y, X, n_bootstrap=50, random_state=42)
        assert hasattr(result, 'statistic')
    
    def test_small_sample(self):
        """Test with very small sample size."""
        np.random.seed(42)
        n = 15  # Small sample
        X = np.random.randn(n, 1)
        y = X.flatten() + np.random.randn(n)
        
        result = bca_rho_test(y, X, n_bootstrap=50, random_state=42)
        assert hasattr(result, 'statistic')


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=boot_dw', '--cov-report=html'])
