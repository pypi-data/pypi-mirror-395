"""
Statistical tests for autocorrelation.

This module implements various tests for autocorrelation in regression models,
including classical and bootstrap-based methods from Jeong & Chung (2001).
"""

import numpy as np
from typing import Optional, Literal
from numpy.typing import NDArray
from scipy import stats

from .core import durbin_watson, ols_regression, estimate_rho
from .bootstrap import (
    recursive_bootstrap_dw,
    recursive_bootstrap_rho,
    bca_confidence_interval
)
from .utils import TestResult


def dw_test(y: NDArray[np.float64],
            X: NDArray[np.float64],
            alternative: Literal['two-sided', 'greater', 'less'] = 'greater',
            add_constant: bool = True) -> TestResult:
    """
    Classical Durbin-Watson test for autocorrelation.
    
    Tests H₀: ρ = 0 against H₁: ρ > 0 (default), ρ ≠ 0, or ρ < 0.
    
    Note: This implementation provides the DW statistic but does not include
    the indeterminate range (dL, dU). Users should refer to DW tables or use
    the bootstrap tests (BDW, B-ρ, BCa-ρ) which eliminate this issue.
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable
    X : ndarray, shape (n, k) or (n,)
        Independent variables
    alternative : {'two-sided', 'greater', 'less'}, default='greater'
        Alternative hypothesis:
        - 'greater': H₁: ρ > 0 (positive autocorrelation)
        - 'less': H₁: ρ < 0 (negative autocorrelation)
        - 'two-sided': H₁: ρ ≠ 0
    add_constant : bool, default=True
        If True, add constant term to regression
        
    Returns
    -------
    result : TestResult
        Object containing test results with attributes:
        - statistic: DW test statistic
        - pvalue: None (requires DW tables)
        - method: Description of test
        - alternative: Alternative hypothesis
        - additional_info: Dictionary with ρ estimate and sample size
        
    Notes
    -----
    The Durbin-Watson statistic is approximately 2(1-ρ̂), where:
    - DW ≈ 2 indicates no autocorrelation (ρ ≈ 0)
    - DW < 2 indicates positive autocorrelation (ρ > 0)
    - DW > 2 indicates negative autocorrelation (ρ < 0)
    
    The classical DW test has an indeterminate range (dL, dU). Values
    in this range lead to inconclusive results. Bootstrap tests eliminate
    this problem.
    
    References
    ----------
    .. [1] Durbin & Watson (1950, 1951)
    .. [2] Jeong & Chung (2001), Section 2
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import dw_test
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> result = dw_test(y, X)
    >>> print(result)
    """
    # Perform OLS regression
    beta, residuals, fitted = ols_regression(y, X, add_constant=add_constant)
    
    # Calculate DW statistic
    dw_stat = durbin_watson(residuals)
    
    # Estimate ρ
    rho_est = estimate_rho(residuals)
    
    # Note: Classical DW test doesn't have exact p-values
    # Users should compare to DW tables or use bootstrap tests
    
    result = TestResult(
        statistic=dw_stat,
        pvalue=None,
        method="Durbin-Watson test",
        alternative=alternative,
        additional_info={
            'rho_estimate': rho_est,
            'n': len(y),
            'k': X.shape[1] if X.ndim > 1 else 1,
            'note': 'Classical DW test requires comparison with tabulated critical values (dL, dU). '
                   'Consider using bdw_test(), b_rho_test(), or bca_rho_test() for exact p-values.'
        }
    )
    
    return result


def bdw_test(y: NDArray[np.float64],
             X: NDArray[np.float64],
             alternative: Literal['two-sided', 'greater', 'less'] = 'greater',
             n_bootstrap: int = 200,
             alpha: float = 0.05,
             add_constant: bool = True,
             random_state: Optional[int] = None) -> TestResult:
    """
    Bootstrapped Durbin-Watson (BDW) test for autocorrelation.
    
    This test eliminates the indeterminate range of the classical DW test by
    using bootstrap to construct the empirical null distribution F*_d.
    
    Procedure (Jeong & Chung 2001, Section 3):
    1. Estimate β̂, ρ̂ from original data
    2. Bootstrap innovations imposing H₀: ρ = 0
    3. Construct empirical distribution of DW statistics
    4. Compare observed DW to bootstrap critical values
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable
    X : ndarray, shape (n, k) or (n,)
        Independent variables
    alternative : {'two-sided', 'greater', 'less'}, default='greater'
        Alternative hypothesis
    n_bootstrap : int, default=200
        Number of bootstrap replications (200 used in paper)
    alpha : float, default=0.05
        Significance level
    add_constant : bool, default=True
        If True, add constant term to regression
    random_state : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    result : TestResult
        Object containing test results with attributes:
        - statistic: Observed DW statistic
        - pvalue: Bootstrap p-value
        - method: Description of test
        - alternative: Alternative hypothesis
        - additional_info: Dictionary with bootstrap details
        
    Notes
    -----
    The BDW test constructs the null distribution F*_d by:
    - Resampling residuals to get e*
    - Setting u* = e* (imposing H₀: ρ = 0)
    - Computing DW* from bootstrap samples
    
    The p-value is the proportion of bootstrap DW* values more extreme
    than the observed DW statistic.
    
    References
    ----------
    .. [1] Jeong & Chung (2001), Section 3, pp. 55-56
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import bdw_test
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> result = bdw_test(y, X, n_bootstrap=200, random_state=42)
    >>> print(result)
    """
    # Perform OLS regression
    beta, residuals, fitted = ols_regression(y, X, add_constant=add_constant)
    
    # Calculate observed DW statistic
    dw_obs = durbin_watson(residuals)
    
    # Estimate ρ
    rho_est = estimate_rho(residuals)
    
    # Prepare X for bootstrap (remove constant if it was added)
    X_boot = X if not add_constant else np.column_stack([np.ones(len(y)), X])
    
    # Perform recursive bootstrap
    dw_boot = recursive_bootstrap_dw(y, X_boot, residuals, rho_est, 
                                     n_bootstrap=n_bootstrap,
                                     random_state=random_state)
    
    # Calculate p-value based on alternative hypothesis
    if alternative == 'greater':
        # H₁: ρ > 0, so reject if DW < critical value
        # P-value = P(DW* < DW_obs)
        pvalue = np.mean(dw_boot <= dw_obs)
    elif alternative == 'less':
        # H₁: ρ < 0, so reject if DW > critical value
        # P-value = P(DW* > DW_obs)
        pvalue = np.mean(dw_boot >= dw_obs)
    else:  # two-sided
        # P-value = 2 * min(P(DW* < DW_obs), P(DW* > DW_obs))
        p_left = np.mean(dw_boot <= dw_obs)
        p_right = np.mean(dw_boot >= dw_obs)
        pvalue = 2 * min(p_left, p_right)
    
    # Calculate critical value
    if alternative == 'greater':
        critical_value = np.percentile(dw_boot, alpha * 100)
    elif alternative == 'less':
        critical_value = np.percentile(dw_boot, (1 - alpha) * 100)
    else:  # two-sided
        critical_value_lower = np.percentile(dw_boot, alpha/2 * 100)
        critical_value_upper = np.percentile(dw_boot, (1 - alpha/2) * 100)
        critical_value = (critical_value_lower, critical_value_upper)
    
    result = TestResult(
        statistic=dw_obs,
        pvalue=pvalue,
        method="Bootstrapped Durbin-Watson (BDW) test",
        alternative=alternative,
        additional_info={
            'rho_estimate': rho_est,
            'n_bootstrap': n_bootstrap,
            'critical_value': critical_value,
            'bootstrap_mean': np.mean(dw_boot),
            'bootstrap_std': np.std(dw_boot),
            'n': len(y),
            'k': X.shape[1] if X.ndim > 1 else 1
        }
    )
    
    return result


def b_rho_test(y: NDArray[np.float64],
               X: NDArray[np.float64],
               alternative: Literal['two-sided', 'greater', 'less'] = 'greater',
               n_bootstrap: int = 200,
               alpha: float = 0.05,
               add_constant: bool = True,
               random_state: Optional[int] = None) -> TestResult:
    """
    Bootstrapped ρ (B-ρ) test for autocorrelation.
    
    This test directly bootstraps the AR(1) coefficient ρ rather than the
    DW statistic, potentially providing better power.
    
    Procedure (Jeong & Chung 2001, Section 3):
    1. Estimate β̂, ρ̂ from original data
    2. Estimate innovations ê_t
    3. Bootstrap innovations and recursively construct u* using ρ̂
    4. Compute ρ* from bootstrap errors
    5. Compare null value ρ = 0 to empirical distribution F*_ρ
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable
    X : ndarray, shape (n, k) or (n,)
        Independent variables
    alternative : {'two-sided', 'greater', 'less'}, default='greater'
        Alternative hypothesis
    n_bootstrap : int, default=200
        Number of bootstrap replications
    alpha : float, default=0.05
        Significance level
    add_constant : bool, default=True
        If True, add constant term to regression
    random_state : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    result : TestResult
        Object containing test results with attributes:
        - statistic: Estimated ρ̂ from original sample
        - pvalue: Bootstrap p-value
        - method: Description of test
        - alternative: Alternative hypothesis  
        - additional_info: Dictionary with bootstrap details
        
    Notes
    -----
    Unlike BDW, the B-ρ test constructs the bootstrap distribution F*_ρ
    conditional on the sample (under the alternative), not under H₀.
    
    The test rejects H₀: ρ = 0 if the α-level confidence interval from
    F*_ρ does not contain 0.
    
    References
    ----------
    .. [1] Jeong & Chung (2001), Section 3, pp. 56-57
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import b_rho_test
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> result = b_rho_test(y, X, n_bootstrap=200, random_state=42)
    >>> print(result)
    """
    # Perform OLS regression
    beta, residuals, fitted = ols_regression(y, X, add_constant=add_constant)
    
    # Estimate ρ from original sample
    rho_obs = estimate_rho(residuals)
    
    # Prepare X for bootstrap
    X_boot = X if not add_constant else np.column_stack([np.ones(len(y)), X])
    
    # Perform recursive bootstrap
    rho_boot = recursive_bootstrap_rho(y, X_boot, residuals, rho_obs,
                                       n_bootstrap=n_bootstrap,
                                       random_state=random_state)
    
    # Calculate p-value using percentile method
    # Test H₀: ρ = 0 by checking if 0 is in the confidence interval
    
    if alternative == 'greater':
        # H₁: ρ > 0
        # Reject if α-level lower tail > 0
        critical_value = np.percentile(rho_boot, alpha * 100)
        pvalue = np.mean(rho_boot <= 0)
    elif alternative == 'less':
        # H₁: ρ < 0
        # Reject if α-level upper tail < 0
        critical_value = np.percentile(rho_boot, (1 - alpha) * 100)
        pvalue = np.mean(rho_boot >= 0)
    else:  # two-sided
        # Reject if 0 is outside (α/2, 1-α/2) interval
        critical_value_lower = np.percentile(rho_boot, alpha/2 * 100)
        critical_value_upper = np.percentile(rho_boot, (1 - alpha/2) * 100)
        critical_value = (critical_value_lower, critical_value_upper)
        
        # Two-tailed p-value
        p_left = np.mean(rho_boot <= 0)
        p_right = np.mean(rho_boot >= 0)
        pvalue = 2 * min(p_left, p_right)
    
    result = TestResult(
        statistic=rho_obs,
        pvalue=pvalue,
        method="Bootstrapped ρ (B-ρ) test (percentile method)",
        alternative=alternative,
        additional_info={
            'n_bootstrap': n_bootstrap,
            'critical_value': critical_value,
            'bootstrap_mean': np.mean(rho_boot),
            'bootstrap_std': np.std(rho_boot),
            'dw_statistic': durbin_watson(residuals),
            'n': len(y),
            'k': X.shape[1] if X.ndim > 1 else 1
        }
    )
    
    return result


def bca_rho_test(y: NDArray[np.float64],
                 X: NDArray[np.float64],
                 alternative: Literal['two-sided', 'greater', 'less'] = 'greater',
                 n_bootstrap: int = 200,
                 alpha: float = 0.05,
                 add_constant: bool = True,
                 random_state: Optional[int] = None) -> TestResult:
    """
    Bias-corrected accelerated ρ (BCa-ρ) test for autocorrelation.
    
    This is the most powerful test from Jeong & Chung (2001), combining
    the B-ρ test with BCa corrections for bias and skewness.
    
    Procedure:
    1. Perform B-ρ bootstrap to get F*_ρ
    2. Apply BCa corrections using:
       - Bias constant z₀ (from bootstrap vs observed)
       - Acceleration constant a₀ (from jackknife)
    3. Compute adjusted confidence interval
    4. Test if 0 is outside the BCa interval
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable
    X : ndarray, shape (n, k) or (n,)
        Independent variables
    alternative : {'two-sided', 'greater', 'less'}, default='greater'
        Alternative hypothesis
    n_bootstrap : int, default=200
        Number of bootstrap replications
    alpha : float, default=0.05
        Significance level
    add_constant : bool, default=True
        If True, add constant term to regression
    random_state : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    result : TestResult
        Object containing test results with attributes:
        - statistic: Estimated ρ̂ from original sample
        - pvalue: Bootstrap p-value
        - method: Description of test
        - alternative: Alternative hypothesis
        - additional_info: Dictionary with BCa details
        
    Notes
    -----
    The BCa method (Efron 1987) corrects the percentile method for:
    - Bias: z₀ = Φ⁻¹(Ĝ(ρ̂))
    - Skewness: a₀ computed from jackknife influence function
    
    Monte Carlo results (Jeong & Chung 2001, Table 1 and Figs 1-16) show
    this test has:
    - Most accurate empirical size
    - Highest power, especially in small samples
    - Robust performance across sample sizes
    
    References
    ----------
    .. [1] Jeong & Chung (2001), Section 3, pp. 57
    .. [2] Efron (1987), JASA 82: 171-200
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import bca_rho_test
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> result = bca_rho_test(y, X, n_bootstrap=200, random_state=42)
    >>> print(result)
    """
    # Perform OLS regression
    beta, residuals, fitted = ols_regression(y, X, add_constant=add_constant)
    
    # Estimate ρ from original sample
    rho_obs = estimate_rho(residuals)
    
    # Prepare X and y for bootstrap
    X_boot = X if not add_constant else np.column_stack([np.ones(len(y)), X])
    
    # Perform recursive bootstrap
    rho_boot = recursive_bootstrap_rho(y, X_boot, residuals, rho_obs,
                                       n_bootstrap=n_bootstrap,
                                       random_state=random_state)
    
    # Calculate BCa confidence interval
    ci_lower, ci_upper, z0, a0 = bca_confidence_interval(
        rho_boot, rho_obs, y, X_boot, alpha=alpha
    )
    
    # Determine rejection based on alternative
    if alternative == 'greater':
        # H₁: ρ > 0
        # Reject if BCa lower bound > 0
        reject = ci_lower > 0
        critical_value = ci_lower
        # Approximate p-value
        pvalue = np.mean(rho_boot <= 0)
    elif alternative == 'less':
        # H₁: ρ < 0  
        # Reject if BCa upper bound < 0
        reject = ci_upper < 0
        critical_value = ci_upper
        pvalue = np.mean(rho_boot >= 0)
    else:  # two-sided
        # Reject if 0 is outside BCa interval
        reject = (0 < ci_lower) or (0 > ci_upper)
        critical_value = (ci_lower, ci_upper)
        p_left = np.mean(rho_boot <= 0)
        p_right = np.mean(rho_boot >= 0)
        pvalue = 2 * min(p_left, p_right)
    
    result = TestResult(
        statistic=rho_obs,
        pvalue=pvalue,
        method="Bias-corrected accelerated ρ (BCa-ρ) test",
        alternative=alternative,
        additional_info={
            'n_bootstrap': n_bootstrap,
            'bca_interval': (ci_lower, ci_upper),
            'bias_constant_z0': z0,
            'acceleration_constant_a0': a0,
            'critical_value': critical_value,
            'reject_H0': reject,
            'bootstrap_mean': np.mean(rho_boot),
            'bootstrap_std': np.std(rho_boot),
            'dw_statistic': durbin_watson(residuals),
            'n': len(y),
            'k': X.shape[1] if X.ndim > 1 else 1
        }
    )
    
    return result


def autocorrelation_test(y: NDArray[np.float64],
                         X: NDArray[np.float64],
                         method: Literal['dw', 'bdw', 'b_rho', 'bca_rho'] = 'bca_rho',
                         alternative: Literal['two-sided', 'greater', 'less'] = 'greater',
                         n_bootstrap: int = 200,
                         alpha: float = 0.05,
                         add_constant: bool = True,
                         random_state: Optional[int] = None) -> TestResult:
    """
    Unified interface for autocorrelation tests.
    
    This function provides a single entry point for all autocorrelation tests
    implemented in this package.
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable
    X : ndarray, shape (n, k) or (n,)
        Independent variables
    method : {'dw', 'bdw', 'b_rho', 'bca_rho'}, default='bca_rho'
        Test method to use:
        - 'dw': Classical Durbin-Watson test
        - 'bdw': Bootstrapped Durbin-Watson test
        - 'b_rho': Bootstrapped ρ test (percentile method)
        - 'bca_rho': BCa-ρ test (recommended, most powerful)
    alternative : {'two-sided', 'greater', 'less'}, default='greater'
        Alternative hypothesis
    n_bootstrap : int, default=200
        Number of bootstrap replications (ignored for 'dw')
    alpha : float, default=0.05
        Significance level
    add_constant : bool, default=True
        If True, add constant term to regression
    random_state : int, optional
        Random seed for reproducibility (bootstrap methods only)
        
    Returns
    -------
    result : TestResult
        Test results object
        
    See Also
    --------
    dw_test : Classical Durbin-Watson test
    bdw_test : Bootstrapped Durbin-Watson test
    b_rho_test : Bootstrapped ρ test
    bca_rho_test : BCa-ρ test
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import autocorrelation_test
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> 
    >>> # Use recommended BCa-ρ test
    >>> result = autocorrelation_test(y, X, method='bca_rho', random_state=42)
    >>> print(result)
    >>> 
    >>> # Compare with classical DW test
    >>> result_dw = autocorrelation_test(y, X, method='dw')
    >>> print(result_dw)
    """
    if method == 'dw':
        return dw_test(y, X, alternative=alternative, add_constant=add_constant)
    elif method == 'bdw':
        return bdw_test(y, X, alternative=alternative, n_bootstrap=n_bootstrap,
                       alpha=alpha, add_constant=add_constant, random_state=random_state)
    elif method == 'b_rho':
        return b_rho_test(y, X, alternative=alternative, n_bootstrap=n_bootstrap,
                         alpha=alpha, add_constant=add_constant, random_state=random_state)
    elif method == 'bca_rho':
        return bca_rho_test(y, X, alternative=alternative, n_bootstrap=n_bootstrap,
                           alpha=alpha, add_constant=add_constant, random_state=random_state)
    else:
        raise ValueError(f"Unknown method: {method}. Must be one of: 'dw', 'bdw', 'b_rho', 'bca_rho'")
