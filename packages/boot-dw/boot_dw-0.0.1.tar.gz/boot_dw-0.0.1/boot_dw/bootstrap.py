"""
Bootstrap procedures for autocorrelation testing.

This module implements recursive bootstrap methods for the Durbin-Watson
statistic and AR(1) coefficient, following Jeong & Chung (2001).
"""

import numpy as np
from typing import Tuple, Optional
from numpy.typing import NDArray
from scipy import stats

from .core import durbin_watson, ols_regression, estimate_rho, recursive_ar1_errors


def recursive_bootstrap_dw(y: NDArray[np.float64], 
                           X: NDArray[np.float64],
                           residuals: NDArray[np.float64],
                           rho_est: float,
                           n_bootstrap: int = 200,
                           random_state: Optional[int] = None) -> NDArray[np.float64]:
    """
    Perform recursive bootstrap for Durbin-Watson statistic.
    
    This implements the BDW test procedure from Jeong & Chung (2001), Section 3:
    
    1. Resample residuals ê to construct bootstrap residual vector e*
    2. Recursively construct bootstrap residual u* imposing H₀: ρ = 0
    3. Create "fake" data y* = Xβ̂ + u*
    4. Re-compute DW statistic d* from (X, y*)
    5. Repeat to construct empirical distribution F*_d
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable
    X : ndarray, shape (n, k)
        Design matrix (independent variables, possibly with constant)
    residuals : ndarray, shape (n,)
        OLS residuals from original regression
    rho_est : float
        Estimated AR(1) coefficient from original residuals
    n_bootstrap : int, default=200
        Number of bootstrap replications
    random_state : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    dw_bootstrap : ndarray, shape (n_bootstrap,)
        Bootstrap distribution of DW statistics under H₀: ρ = 0
        
    Notes
    -----
    Under the null hypothesis H₀: ρ = 0, the errors are i.i.d., so u* = e*.
    This forces the null distribution for the bootstrap procedure.
    
    The empirical distribution F*_d can be used to obtain critical values
    that eliminate the indeterminate range of the classical DW test.
    
    References
    ----------
    .. [1] Jeong & Chung (2001), Section 3, pp. 55-56
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import recursive_bootstrap_dw, ols_regression
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> beta, resid, fitted = ols_regression(y, X)
    >>> rho = estimate_rho(resid)
    >>> dw_boot = recursive_bootstrap_dw(y, X, resid, rho, n_bootstrap=100)
    >>> print(f"Bootstrap mean: {np.mean(dw_boot):.4f}")
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    n = len(residuals)
    dw_bootstrap = np.zeros(n_bootstrap)
    
    # Get fitted values from original regression
    beta_ols, _, fitted = ols_regression(y, X, add_constant=False)
    
    # Estimate innovations: ê_t
    # For the BDW test, we impose H₀: ρ = 0 in bootstrap
    # So we directly use residuals as innovations
    innovations = residuals.copy()
    
    for b in range(n_bootstrap):
        # Step 3: Resample innovations with replacement
        e_star = np.random.choice(innovations, size=n, replace=True)
        
        # Step 4: Under H₀: ρ = 0, u* = e* (no recursive construction needed)
        u_star = e_star.copy()
        
        # Step 5: Create bootstrap data y* = Xβ̂ + u*
        y_star = fitted + u_star
        
        # Step 6: Re-compute DW statistic
        _, resid_star, _ = ols_regression(y_star, X, add_constant=False)
        dw_bootstrap[b] = durbin_watson(resid_star)
    
    return dw_bootstrap


def recursive_bootstrap_rho(y: NDArray[np.float64],
                            X: NDArray[np.float64], 
                            residuals: NDArray[np.float64],
                            rho_est: float,
                            n_bootstrap: int = 200,
                            random_state: Optional[int] = None) -> NDArray[np.float64]:
    """
    Perform recursive bootstrap for AR(1) coefficient ρ.
    
    This implements the B-ρ test procedure from Jeong & Chung (2001), Section 3:
    
    1. Estimate ρ̂ and compute innovations ê_t
    2. Resample innovations to get e*
    3. Recursively construct u* using estimated ρ̂ (NOT imposing H₀)
    4. Compute ρ* from u*
    5. Repeat to construct empirical distribution F*_ρ
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable
    X : ndarray, shape (n, k)
        Design matrix  
    residuals : ndarray, shape (n,)
        OLS residuals from original regression
    rho_est : float
        Estimated AR(1) coefficient from original residuals
    n_bootstrap : int, default=200
        Number of bootstrap replications
    random_state : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    rho_bootstrap : ndarray, shape (n_bootstrap,)
        Bootstrap distribution of ρ̂ conditional on the sample
        
    Notes
    -----
    Unlike BDW, this test constructs the bootstrap distribution under the
    alternative hypothesis (conditional on the sample), not under H₀.
    
    The test compares the null value ρ = 0 to the empirical distribution F*_ρ.
    If the α-level left tail of F*_ρ is greater than 0, reject H₀.
    
    References
    ----------
    .. [1] Jeong & Chung (2001), Section 3, pp. 56-57
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import recursive_bootstrap_rho, ols_regression, estimate_rho
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> u = np.zeros(n)
    >>> u[0] = np.random.randn()
    >>> for t in range(1, n):
    ...     u[t] = 0.5 * u[t-1] + np.random.randn()
    >>> y = X @ np.array([2, -1]) + u
    >>> beta, resid, fitted = ols_regression(y, X)
    >>> rho = estimate_rho(resid)
    >>> rho_boot = recursive_bootstrap_rho(y, X, resid, rho, n_bootstrap=100)
    >>> print(f"Bootstrap mean: {np.mean(rho_boot):.4f}")
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    n = len(residuals)
    rho_bootstrap = np.zeros(n_bootstrap)
    
    # Get fitted values from original regression
    beta_ols, _, fitted = ols_regression(y, X, add_constant=False)
    
    # Estimate innovations from residuals
    # For AR(1): u_t = ρu_{t-1} + e_t, so e_t = u_t - ρu_{t-1}
    u_t = residuals[1:]
    u_t_1 = residuals[:-1]
    innovations = u_t - rho_est * u_t_1
    
    for b in range(n_bootstrap):
        # Step 3: Resample innovations
        e_star = np.random.choice(innovations, size=n-1, replace=True)
        
        # Step 4: Recursively construct u* using AR(1) with ρ̂
        # Pick initial u*_1 from innovations to ensure stationarity
        e1_star = np.random.choice(innovations, size=1)[0]
        u_star = np.zeros(n)
        u_star[0] = e1_star / np.sqrt(1 - rho_est**2)
        
        # Recursive construction: u*_t = ρ̂u*_{t-1} + e*_t
        for t in range(1, n):
            u_star[t] = rho_est * u_star[t-1] + e_star[t-1]
        
        # Step 5: Compute ρ* from bootstrap errors
        rho_bootstrap[b] = estimate_rho(u_star)
    
    return rho_bootstrap


def bca_confidence_interval(statistic_bootstrap: NDArray[np.float64],
                           statistic_observed: float,
                           y: NDArray[np.float64],
                           X: NDArray[np.float64],
                           alpha: float = 0.05) -> Tuple[float, float, float, float]:
    """
    Calculate bias-corrected and accelerated (BCa) confidence interval.
    
    This implements the BCa method from Efron (1987) as used in Jeong & Chung
    (2001) for the BCa-ρ test. The BCa method corrects for both bias and skewness
    in the bootstrap distribution.
    
    Parameters
    ----------
    statistic_bootstrap : ndarray, shape (n_bootstrap,)
        Bootstrap distribution of the statistic
    statistic_observed : float
        Observed value of the statistic from the original sample
    y : ndarray, shape (n,)
        Dependent variable (for jackknife calculations)
    X : ndarray, shape (n, k)
        Design matrix (for jackknife calculations)
    alpha : float, default=0.05
        Significance level for confidence interval
        
    Returns
    -------
    lower : float
        Lower confidence bound
    upper : float
        Upper confidence bound
    z0 : float
        Bias correction constant
    a0 : float
        Acceleration constant
        
    Notes
    -----
    The BCa interval is calculated as:
        θ ∈ [Ĝ⁻¹(Φ(z[α])), Ĝ⁻¹(Φ(z[1-α]))]
    
    where:
        z[i] = z₀ + (z₀ + z^(i)) / (1 - a₀(z₀ + z^(i)))
        
    The bias constant z₀ and acceleration constant a₀ correct for:
    - z₀: Bias in the bootstrap distribution
    - a₀: Skewness in the bootstrap distribution
    
    References
    ----------
    .. [1] Efron, B. (1987). "Better Bootstrap Confidence Intervals".
           Journal of the American Statistical Association 82: 171-200.
    .. [2] Jeong & Chung (2001), Section 3, pp. 57
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import bca_confidence_interval, recursive_bootstrap_rho
    >>> from boot_dw import ols_regression, estimate_rho
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> beta, resid, fitted = ols_regression(y, X)
    >>> rho = estimate_rho(resid)
    >>> rho_boot = recursive_bootstrap_rho(y, X, resid, rho, n_bootstrap=200)
    >>> lower, upper, z0, a0 = bca_confidence_interval(rho_boot, rho, y, X)
    >>> print(f"95% BCa CI: [{lower:.4f}, {upper:.4f}]")
    """
    n = len(y)
    
    # Calculate bias correction constant z0
    # z₀ = Φ⁻¹(Ĝ(θ̂))
    # This measures how far the bootstrap distribution is from the observed value
    prop_less = np.mean(statistic_bootstrap <= statistic_observed)
    z0 = stats.norm.ppf(np.clip(prop_less, 0.001, 0.999))
    
    # Calculate acceleration constant a0 using jackknife
    # a₀ = (1/6) * Σθ̇ᵢ³ / (Σθ̇ᵢ²)^(3/2)
    # where θ̇ᵢ is the empirical influence function
    
    # Compute jackknife estimates (leave-one-out)
    theta_jack = np.zeros(n)
    for i in range(n):
        # Leave out observation i
        y_jack = np.delete(y, i)
        X_jack = np.delete(X, i, axis=0)
        
        # Compute statistic on jackknife sample
        _, resid_jack, _ = ols_regression(y_jack, X_jack, add_constant=False)
        theta_jack[i] = estimate_rho(resid_jack)
    
    # Mean of jackknife estimates
    theta_jack_mean = np.mean(theta_jack)
    
    # Empirical influence function
    # θ̇ᵢ = (n-1)(θ̄_jack - θ_i)
    theta_dot = (n - 1) * (theta_jack_mean - theta_jack)
    
    # Acceleration constant
    numerator = np.sum(theta_dot**3)
    denominator = 6.0 * (np.sum(theta_dot**2)**(3/2))
    
    if denominator == 0:
        a0 = 0.0
    else:
        a0 = numerator / denominator
    
    # Calculate adjusted percentiles
    # z[i] = z₀ + (z₀ + z^(i)) / (1 - a₀(z₀ + z^(i)))
    z_alpha = stats.norm.ppf(alpha)
    z_1_alpha = stats.norm.ppf(1 - alpha)
    
    # Adjusted lower percentile
    z_lower = z0 + (z0 + z_alpha) / (1 - a0 * (z0 + z_alpha))
    p_lower = stats.norm.cdf(z_lower)
    
    # Adjusted upper percentile  
    z_upper = z0 + (z0 + z_1_alpha) / (1 - a0 * (z0 + z_1_alpha))
    p_upper = stats.norm.cdf(z_upper)
    
    # Clip percentiles to valid range
    p_lower = np.clip(p_lower, 0.001, 0.999)
    p_upper = np.clip(p_upper, 0.001, 0.999)
    
    # Get confidence bounds from bootstrap distribution
    lower = np.percentile(statistic_bootstrap, p_lower * 100)
    upper = np.percentile(statistic_bootstrap, p_upper * 100)
    
    return lower, upper, z0, a0
