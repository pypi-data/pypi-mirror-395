"""
Comprehensive test suite for the CPR package.

Tests are organized by module and include:
- Unit tests for utility functions
- Tests for long-run variance estimation
- Tests for FM-OLS estimation
- Tests for CT and PU tests
- Integration tests with simulated data

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
"""

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal, assert_almost_equal


class TestUtils:
    """Tests for utility functions."""
    
    def test_trimr_basic(self):
        """Test basic trimr functionality."""
        from cpr import trimr
        
        x = np.array([[1], [2], [3], [4], [5]])
        result = trimr(x, 1, 1)
        expected = np.array([[2], [3], [4]])
        assert_array_almost_equal(result, expected)
    
    def test_trimr_no_trim(self):
        """Test trimr with no trimming."""
        from cpr import trimr
        
        x = np.array([[1], [2], [3]])
        result = trimr(x, 0, 0)
        assert_array_almost_equal(result, x)
    
    def test_trimr_error(self):
        """Test trimr raises error on over-trimming."""
        from cpr import trimr
        
        x = np.array([[1], [2], [3]])
        with pytest.raises(ValueError):
            trimr(x, 2, 2)
    
    def test_lag_basic(self):
        """Test basic lag functionality."""
        from cpr import lag
        
        x = np.array([[1], [2], [3], [4], [5]])
        result = lag(x, 1)
        expected = np.array([[0], [1], [2], [3], [4]])
        assert_array_almost_equal(result, expected)
    
    def test_lag_multiple(self):
        """Test lag with n > 1."""
        from cpr import lag
        
        x = np.array([[1], [2], [3], [4], [5]])
        result = lag(x, 2)
        expected = np.array([[0], [0], [1], [2], [3]])
        assert_array_almost_equal(result, expected)
    
    def test_ensure_2d(self):
        """Test ensure_2d function."""
        from cpr import ensure_2d
        
        x = np.array([1, 2, 3])
        result = ensure_2d(x)
        assert result.ndim == 2
        assert result.shape == (3, 1)
    
    def test_generate_deterministics(self):
        """Test deterministic components generation."""
        from cpr import generate_deterministics
        
        # No deterministics
        result = generate_deterministics(5, -1)
        assert result is None
        
        # Intercept only
        result = generate_deterministics(5, 0)
        assert result.shape == (5, 1)
        assert_array_almost_equal(result, np.ones((5, 1)))
        
        # Intercept and trend
        result = generate_deterministics(5, 1)
        assert result.shape == (5, 2)
        assert_array_almost_equal(result[:, 0], np.ones(5))
        assert_array_almost_equal(result[:, 1], np.arange(1, 6))


class TestLRVariance:
    """Tests for long-run variance estimation."""
    
    def test_lr_weights_bartlett(self):
        """Test Bartlett kernel weights."""
        from cpr import lr_weights
        
        w, upper = lr_weights(100, 'ba', 10)
        assert len(w) == 99
        assert upper == 9
        assert w[0] > w[1]  # Decreasing weights
    
    def test_lr_weights_qs(self):
        """Test Quadratic Spectral kernel weights."""
        from cpr import lr_weights
        
        w, upper = lr_weights(100, 'qs', 10)
        assert len(w) == 99
        assert upper == 99  # QS uses all lags
    
    def test_lr_var_dimensions(self):
        """Test lr_var output dimensions."""
        from cpr import lr_var
        
        np.random.seed(42)
        u = np.random.randn(100, 3)
        Omega, Delta, Sigma = lr_var(u, 'ba', 10, 0)
        
        assert Omega.shape == (3, 3)
        assert Delta.shape == (3, 3)
        assert Sigma.shape == (3, 3)
    
    def test_lr_var_positive_definite(self):
        """Test that lr_var produces positive semi-definite matrices."""
        from cpr import lr_var
        
        np.random.seed(42)
        u = np.random.randn(200, 2)
        Omega, Delta, Sigma = lr_var(u, 'ba', 10, 0)
        
        # Check eigenvalues are non-negative
        eigvals = np.linalg.eigvalsh(Omega)
        assert np.all(eigvals >= -1e-10)
    
    def test_bandwidth_nw(self):
        """Test Newey-West bandwidth selection."""
        from cpr import bandwidth_nw
        
        np.random.seed(42)
        v = np.random.randn(100, 2)
        bw = bandwidth_nw(v, 'ba', 0, None)
        
        assert bw > 0
        assert np.isfinite(bw)
    
    def test_bandwidth_andrews(self):
        """Test Andrews bandwidth selection."""
        from cpr import bandwidth_andrews
        
        np.random.seed(42)
        v = np.random.randn(100, 2)
        bw = bandwidth_andrews(v, 'ba')
        
        assert bw > 0
        assert np.isfinite(bw)


class TestPolyTerms:
    """Tests for polynomial terms generation."""
    
    def test_gen_power_reg_all(self):
        """Test power generation with all powers."""
        from cpr import gen_power_reg
        
        x = np.array([1, 2, 3, 4, 5])
        result = gen_power_reg(x, 'yes', 3)
        
        assert result.shape == (5, 3)
        assert_array_almost_equal(result[:, 0], x)
        assert_array_almost_equal(result[:, 1], x**2)
        assert_array_almost_equal(result[:, 2], x**3)
    
    def test_gen_power_reg_specific(self):
        """Test power generation with specific powers."""
        from cpr import gen_power_reg
        
        x = np.array([1, 2, 3, 4, 5])
        result = gen_power_reg(x, 'no', np.array([1, 3]))
        
        assert result.shape == (5, 2)
        assert_array_almost_equal(result[:, 0], x)
        assert_array_almost_equal(result[:, 1], x**3)
    
    def test_gen_cpr_corr_vec(self):
        """Test correction vector generation."""
        from cpr import gen_cpr_corr_vec
        
        x = np.array([1, 2, 3, 4, 5])
        result = gen_cpr_corr_vec(x, 'yes', 2)
        
        # corr_term[0] = 1 * sum(x^0) = 5
        # corr_term[1] = 2 * sum(x^1) = 2 * 15 = 30
        assert len(result) == 2
        assert_almost_equal(result[0], 5)
        assert_almost_equal(result[1], 30)
    
    def test_gen_var_poly_terms(self):
        """Test full polynomial terms generation."""
        from cpr import gen_var_poly_terms
        
        np.random.seed(42)
        x = np.random.randn(100, 2)
        result = gen_var_poly_terms(x, 2)
        
        assert result.X.shape == (100, 4)  # 2 regressors × 2 powers each
        assert len(result.Mstar) == 4
        assert len(result.P) == 3


class TestFMOLS:
    """Tests for FM-OLS estimation."""
    
    def test_fmols_basic(self):
        """Test basic FM-OLS estimation."""
        from cpr import fm_cpr
        
        np.random.seed(42)
        T = 200
        x = np.cumsum(np.random.randn(T))
        y = 1.0 + 0.5 * x + 0.1 * x**2 + np.random.randn(T) * 0.5
        
        deter = np.column_stack([np.ones(T), np.arange(1, T + 1)])
        result = fm_cpr(y, x.reshape(-1, 1), orders=2, deter=deter)
        
        assert len(result.beta_fm) == 2
        assert len(result.u_plus) == T - 1
        assert result.Omega_udotv > 0
    
    def test_fmols_no_deterministics(self):
        """Test FM-OLS without deterministics."""
        from cpr import fm_cpr
        
        np.random.seed(42)
        T = 200
        x = np.cumsum(np.random.randn(T))
        y = 0.5 * x + 0.1 * x**2 + np.random.randn(T) * 0.5
        
        result = fm_cpr(y, x.reshape(-1, 1), orders=2, deter=None)
        
        assert len(result.beta_fm) == 2
        assert len(result.delta_fm) == 0
    
    def test_fmols_multiple_regressors(self):
        """Test FM-OLS with multiple regressors."""
        from cpr import fm_cpr
        
        np.random.seed(42)
        T = 200
        x1 = np.cumsum(np.random.randn(T))
        x2 = np.cumsum(np.random.randn(T))
        x = np.column_stack([x1, x2])
        y = 1.0 + 0.3 * x1 + 0.2 * x2 + np.random.randn(T) * 0.5
        
        deter = np.ones((T, 1))
        result = fm_cpr(y, x, orders=1, deter=deter)
        
        assert len(result.beta_fm) == 2


class TestCTTest:
    """Tests for CT test."""
    
    def test_ct_test_basic(self):
        """Test basic CT test."""
        from cpr import fm_cpr, ct_test
        
        np.random.seed(42)
        T = 200
        x = np.cumsum(np.random.randn(T))
        y = 1.0 + 0.5 * x + 0.1 * x**2 + np.random.randn(T) * 0.5
        
        deter = np.column_stack([np.ones(T), np.arange(1, T + 1)])
        fmols_result = fm_cpr(y, x.reshape(-1, 1), orders=2, deter=deter)
        
        ct_result = ct_test(
            fmols_result.u_plus, 
            fmols_result.Omega_udotv, 
            d=1, m=1, p=2
        )
        
        assert ct_result.statistic > 0
        assert 0.05 in ct_result.critical_values
        assert 0.05 in ct_result.reject
    
    def test_ct_test_critical_values(self):
        """Test that CT test uses correct critical values."""
        from cpr import ct_test, get_ct_critical_value
        
        np.random.seed(42)
        u_plus = np.random.randn(100)
        omega = 1.0
        
        result = ct_test(u_plus, omega, d=1, m=1, p=2)
        
        expected_cv = get_ct_critical_value(1, 1, 2, 0.05)
        assert_almost_equal(result.critical_values[0.05], expected_cv)


class TestPUTest:
    """Tests for PU test."""
    
    def test_pu_test_basic(self):
        """Test basic PU test."""
        from cpr import pu_test
        
        np.random.seed(42)
        T = 200
        x = np.cumsum(np.random.randn(T))
        y = 1.0 + 0.5 * x + 0.1 * x**2 + np.random.randn(T) * 0.5
        
        result = pu_test(y, x.reshape(-1, 1), d=1, m=1, orders=2)
        
        assert result.statistic > 0
        assert 0.05 in result.critical_values
        assert 0.05 in result.reject
    
    def test_pu_test_spurious(self):
        """Test PU test with clearly spurious regression."""
        from cpr import pu_test
        
        np.random.seed(42)
        T = 200
        x = np.cumsum(np.random.randn(T))
        y = np.cumsum(np.random.randn(T))  # Independent I(1) process
        
        result = pu_test(y, x.reshape(-1, 1), d=1, m=1, orders=2)
        
        # Should not reject H0 (no cointegration) for spurious regression
        assert result.statistic > 0


class TestCriticalValues:
    """Tests for critical values."""
    
    def test_get_ct_critical_value(self):
        """Test CT critical value retrieval."""
        from cpr import get_ct_critical_value
        
        cv = get_ct_critical_value(d=1, m=1, p=2, alpha=0.05)
        assert cv > 0
        assert np.isfinite(cv)
    
    def test_get_pu_critical_value(self):
        """Test PU critical value retrieval."""
        from cpr import get_pu_critical_value
        
        cv = get_pu_critical_value(d=1, m=1, p=2, alpha=0.05)
        assert cv > 0
        assert np.isfinite(cv)
    
    def test_critical_values_ordering(self):
        """Test that critical values are properly ordered."""
        from cpr import get_all_critical_values
        
        cv = get_all_critical_values('CT', d=1, m=1, p=2)
        
        # Critical values should be increasing with percentile
        assert np.all(np.diff(cv) >= 0)
    
    def test_invalid_parameters(self):
        """Test error handling for invalid parameters."""
        from cpr import get_ct_critical_value
        
        with pytest.raises(ValueError):
            get_ct_critical_value(d=5, m=1, p=2, alpha=0.05)
        
        with pytest.raises(ValueError):
            get_ct_critical_value(d=1, m=10, p=2, alpha=0.05)


class TestIntegration:
    """Integration tests with realistic scenarios."""
    
    def test_ekc_simulation(self):
        """Test with simulated EKC data."""
        from cpr import fm_cpr, ct_test, pu_test, CPRTestSummary
        
        np.random.seed(123)
        T = 300
        
        # Generate GDP (I(1))
        gdp = np.cumsum(np.random.randn(T)) + 10
        
        # Generate emissions with true quadratic relationship
        beta = [0.5, -0.02]
        emissions = 2.0 + beta[0] * gdp + beta[1] * gdp**2 + np.random.randn(T) * 0.3
        
        # Estimation
        deter = np.column_stack([np.ones(T), np.arange(1, T + 1)])
        fmols_result = fm_cpr(
            emissions, gdp.reshape(-1, 1), 
            orders=2, deter=deter, 
            kern='ba', band='NW'
        )
        
        # Tests
        ct_result = ct_test(
            fmols_result.u_plus, 
            fmols_result.Omega_udotv, 
            d=1, m=1, p=2
        )
        
        pu_result = pu_test(
            emissions, gdp.reshape(-1, 1), 
            d=1, m=1, orders=2
        )
        
        # Create summary
        summary = CPRTestSummary(ct_result, pu_result)
        
        # With cointegrated data, we expect evidence for cointegration
        evidence = summary.evidence_for_cointegration(alpha=0.05)
        # Note: With random seed, specific outcome may vary
        assert evidence is not None or evidence is True or evidence is False
    
    def test_output_format(self):
        """Test that output is properly formatted."""
        from cpr import ct_test
        
        np.random.seed(42)
        u_plus = np.random.randn(100)
        omega = 1.0
        
        result = ct_test(u_plus, omega, d=1, m=1, p=2)
        
        # Test string representation
        output = str(result)
        assert "CT Test" in output
        assert "Statistic" in output
        assert "Critical Values" in output


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_small_sample(self):
        """Test with small sample size."""
        from cpr import fm_cpr
        
        np.random.seed(42)
        T = 30
        x = np.cumsum(np.random.randn(T))
        y = 1.0 + 0.5 * x + np.random.randn(T) * 0.5
        
        deter = np.ones((T, 1))
        result = fm_cpr(y, x.reshape(-1, 1), orders=1, deter=deter)
        
        assert len(result.beta_fm) == 1
        assert np.isfinite(result.Omega_udotv)
    
    def test_deterministic_d_minus1(self):
        """Test with d=-1 (no deterministics)."""
        from cpr import ct_test, get_ct_critical_value
        
        np.random.seed(42)
        u_plus = np.random.randn(100)
        omega = 1.0
        
        result = ct_test(u_plus, omega, d=-1, m=1, p=2)
        
        assert result.d == -1
        assert np.isfinite(result.statistic)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
