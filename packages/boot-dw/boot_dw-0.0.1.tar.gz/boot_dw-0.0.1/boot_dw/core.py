"""
Core functions for Durbin-Watson statistics and regression.

This module implements the fundamental statistical functions needed for 
autocorrelation testing, following Jeong & Chung (2001).
"""

import numpy as np
from typing import Tuple, Optional
from numpy.typing import NDArray


def durbin_watson(residuals: NDArray[np.float64], axis: int = 0) -> float:
    """
    Calculate the Durbin-Watson statistic.
    
    The Durbin-Watson test statistic is defined as:
    
    .. math::
        d = \\frac{\\sum_{t=2}^{T}(e_t - e_{t-1})^2}{\\sum_{t=1}^{T}e_t^2}
    
    This is approximately equal to 2(1-ρ) where ρ is the sample autocorrelation
    of the residuals.
    
    Parameters
    ----------
    residuals : ndarray
        Residuals from regression model (OLS residuals ê)
    axis : int, optional
        Axis to use if data has more than 1 dimension, default is 0
        
    Returns
    -------
    dw : float
        The Durbin-Watson statistic
        
    Notes
    -----
    The test statistic will always be between 0 and 4:
    - Values near 2 indicate no autocorrelation
    - Values near 0 indicate positive autocorrelation  
    - Values near 4 indicate negative autocorrelation
    
    References
    ----------
    .. [1] Durbin, J. and Watson, G.S. (1950). "Testing for Serial Correlation 
           in Least Squares Regression I". Biometrika 37: 409-428.
    .. [2] Jeong, J. and Chung, S. (2001). "Bootstrap tests for autocorrelation".
           Computational Statistics & Data Analysis 38: 49-69.
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import durbin_watson
    >>> residuals = np.array([0.1, -0.2, 0.3, -0.1, 0.2])
    >>> dw = durbin_watson(residuals)
    >>> print(f"DW statistic: {dw:.4f}")
    """
    residuals = np.asarray(residuals)
    diff_resids = np.diff(residuals, 1, axis=axis)
    dw = np.sum(diff_resids**2, axis=axis) / np.sum(residuals**2, axis=axis)
    return float(dw)


def ols_regression(y: NDArray[np.float64], X: NDArray[np.float64], 
                   add_constant: bool = True) -> Tuple[NDArray[np.float64], 
                                                        NDArray[np.float64],
                                                        NDArray[np.float64]]:
    """
    Perform Ordinary Least Squares regression.
    
    Estimates the linear regression model:
        y = Xβ + u
    
    Parameters
    ----------
    y : ndarray, shape (n,)
        Dependent variable (n observations)
    X : ndarray, shape (n, k) or (n,)
        Independent variables (n observations, k regressors)
        If 1-dimensional, will be reshaped to (n, 1)
    add_constant : bool, default=True
        If True, add a constant term to X
        
    Returns
    -------
    beta : ndarray, shape (k,) or (k+1,)
        OLS coefficient estimates
    residuals : ndarray, shape (n,)
        OLS residuals ê = y - Xβ̂  
    fitted : ndarray, shape (n,)
        Fitted values ŷ = Xβ̂
        
    Notes
    -----
    The OLS estimator is:
        β̂ = (X'X)⁻¹X'y
        
    Residuals are calculated as:
        ê = y - Xβ̂ = (I - X(X'X)⁻¹X')y = My
        
    where M is the residual maker matrix.
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import ols_regression
    >>> np.random.seed(42)
    >>> n = 100
    >>> X = np.random.randn(n, 2)
    >>> y = 2 + 3*X[:, 0] - 1.5*X[:, 1] + np.random.randn(n)*0.5
    >>> beta, residuals, fitted = ols_regression(y, X)
    >>> print(f"Coefficients: {beta}")
    """
    y = np.asarray(y).flatten()
    X = np.asarray(X)
    
    # Ensure X is 2-dimensional
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    
    # Add constant if requested
    if add_constant:
        X = np.column_stack([np.ones(len(y)), X])
    
    # OLS estimation: β̂ = (X'X)⁻¹X'y
    XtX = X.T @ X
    Xty = X.T @ y
    beta = np.linalg.solve(XtX, Xty)
    
    # Calculate fitted values and residuals
    fitted = X @ beta
    residuals = y - fitted
    
    return beta, residuals, fitted


def estimate_rho(residuals: NDArray[np.float64]) -> float:
    """
    Estimate the AR(1) coefficient ρ from residuals.
    
    For the AR(1) model:
        u_t = ρu_{t-1} + e_t
    
    The OLS estimator is:
        ρ̂ = Σu_t u_{t-1} / Σu²_{t-1}
    
    Parameters
    ----------
    residuals : ndarray, shape (n,)
        Residuals from regression
        
    Returns
    -------
    rho : float
        Estimated AR(1) coefficient
        
    Notes
    -----
    This is the sample autocorrelation coefficient at lag 1,
    calculated using OLS on the AR(1) model.
    
    Examples
    --------
    >>> import numpy as np
    >>> from boot_dw import estimate_rho
    >>> # Simulate AR(1) process
    >>> np.random.seed(42)
    >>> n = 100
    >>> rho_true = 0.7
    >>> u = np.zeros(n)
    >>> u[0] = np.random.randn()
    >>> for t in range(1, n):
    ...     u[t] = rho_true * u[t-1] + np.random.randn()
    >>> rho_hat = estimate_rho(u)
    >>> print(f"True ρ: {rho_true}, Estimated ρ: {rho_hat:.4f}")
    """
    residuals = np.asarray(residuals).flatten()
    
    # Calculate ρ̂ = Σu_t u_{t-1} / Σu²_{t-1}
    u_t = residuals[1:]
    u_t_1 = residuals[:-1]
    
    rho = np.sum(u_t * u_t_1) / np.sum(u_t_1**2)
    
    return float(rho)


def recursive_ar1_errors(innovations: NDArray[np.float64], rho: float,
                         u0: Optional[float] = None) -> NDArray[np.float64]:
    """
    Generate AR(1) errors recursively from innovations.
    
    For AR(1) model:
        u_t = ρu_{t-1} + e_t, |ρ| < 1
        
    Starting from u_0, recursively construct the full error series.
    
    Parameters
    ----------
    innovations : ndarray, shape (n,)
        White noise innovations e_t
    rho : float
        AR(1) coefficient, must satisfy |ρ| < 1
    u0 : float, optional
        Initial value for u_0. If None, uses e_0/√(1-ρ²) for stationarity
        
    Returns
    -------
    errors : ndarray, shape (n,)
        AR(1) error series u_t
        
    Notes
    -----
    For a stationary AR(1) process, the initial value should be:
        u_0 ~ N(0, σ²/(1-ρ²))
        
    This function implements the recursive construction described in
    Jeong & Chung (2001), step 4 of the B-ρ test procedure.
    
    Examples
    --------
    >>> import numpy as np  
    >>> from boot_dw import recursive_ar1_errors
    >>> np.random.seed(42)
    >>> e = np.random.randn(100)
    >>> u = recursive_ar1_errors(e, rho=0.7)
    >>> print(f"Variance of u: {np.var(u):.4f}")
    """
    innovations = np.asarray(innovations).flatten()
    n = len(innovations)
    errors = np.zeros(n)
    
    # Set initial value
    if u0 is None:
        # For stationarity: u_0 = e_0/√(1-ρ²)
        errors[0] = innovations[0] / np.sqrt(1 - rho**2)
    else:
        errors[0] = u0
    
    # Recursive construction: u_t = ρu_{t-1} + e_t
    for t in range(1, n):
        errors[t] = rho * errors[t-1] + innovations[t]
    
    return errors
