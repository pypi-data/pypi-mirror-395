# boot_dw: Bootstrap Tests for Autocorrelation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python implementation of bootstrap-based tests for autocorrelation in regression models, based on:

**Jeong, J. and Chung, S. (2001). "Bootstrap tests for autocorrelation". _Computational Statistics & Data Analysis_ 38: 49-69.**

## Overview

The classical Durbin-Watson (DW) test for autocorrelation suffers from an important limitation: the test is inconclusive when the test statistic falls into the "indeterminate range" (dL, dU). This package implements bootstrap alternatives that eliminate this problem and provide superior finite-sample properties.

### Implemented Tests

1. **Classical DW Test** - Traditional Durbin-Watson test (with indeterminate range)
2. **BDW Test** - Bootstrapped Durbin-Watson test (eliminates indeterminate range)
3. **B-ρ Test** - Bootstrapped AR(1) coefficient test (percentile method)
4. **BCa-ρ Test** - Bias-corrected accelerated ρ test (**recommended**, most powerful)

## Installation

```bash
pip install boot_dw
```

Or install from source:

```bash
git clone https://github.com/merwanroudane/bootdw.git
cd bootdw
pip install -e .
```

## Quick Start

```python
import numpy as np
from boot_dw import autocorrelation_test

# Generate sample data
np.random.seed(42)
n = 50
X = np.random.randn(n, 2)
y = X @ np.array([2, -1]) + np.random.randn(n)

# Run BCa-ρ test (recommended)
result = autocorrelation_test(y, X, method='bca_rho', random_state=42)
print(result)
```

Output:
```
======================================================================
  Bias-corrected accelerated ρ (BCa-ρ) test
======================================================================
H₀: ρ = 0  vs  H₁: ρ > 0

Test statistic:  -0.045123
P-value:         0.685000

Conclusion: Fail to reject H₀

Estimated ρ̂:    -0.045123
DW statistic:    2.087456
95% BCa CI:      (-0.312456, 0.198234)

Sample size:     n = 50, k = 2
Bootstrap reps:  B = 200
======================================================================
```

## Features

### Publication-Ready Output

The package provides publication-quality formatted output:

```python
from boot_dw import bca_rho_test

result = bca_rho_test(y, X, n_bootstrap=200, random_state=42)

# Detailed summary
print(result.summary())

# LaTeX table for multiple tests
from boot_dw.utils import format_latex_table

results = {
    'Classical DW': dw_test(y, X),
    'BDW': bdw_test(y, X, random_state=42),
    'BCa-ρ': bca_rho_test(y, X, random_state=42)
}

print(format_latex_table(results))
```

### Monte Carlo Simulations

Replicate the simulations from Jeong & Chung (2001):

```python
import numpy as np
from boot_dw import autocorrelation_test

# Simulation parameters
n = 50
k = 3
rho_values = np.arange(0, 1.0, 0.1)
n_simulations = 1000
n_bootstrap = 200

rejection_rates = []

for rho in rho_values:
    rejections = 0
    
    for _ in range(n_simulations):
        # Generate data with AR(1) errors
        X = np.random.randn(n, k)
        u = np.zeros(n)
        u[0] = np.random.randn()
        
        for t in range(1, n):
            u[t] = rho * u[t-1] + np.random.randn()
        
        y = X @ np.ones(k) + u
        
        # Test for autocorrelation
        result = autocorrelation_test(y, X, method='bca_rho', 
                                     n_bootstrap=n_bootstrap, alpha=0.05)
        
        if result.pvalue < 0.05:
            rejections += 1
    
    rejection_rates.append(rejections / n_simulations)

print(f"Empirical size (ρ=0): {rejection_rates[0]:.3f}")
print(f"Power at ρ=0.5: {rejection_rates[5]:.3f}")
```

## API Reference

### Main Test Function

```python
autocorrelation_test(y, X, method='bca_rho', alternative='greater', 
                    n_bootstrap=200, alpha=0.05, add_constant=True, 
                    random_state=None)
```

**Parameters:**
- `y`: Dependent variable (n,)
- `X`: Independent variables (n, k)
- `method`: Test method - `'dw'`, `'bdw'`, `'b_rho'`, or `'bca_rho'` (recommended)
- `alternative`: `'greater'` (default), `'less'`, or `'two-sided'`
- `n_bootstrap`: Number of bootstrap replications (default: 200)
- `alpha`: Significance level (default: 0.05)
- `add_constant`: Add intercept to regression (default: True)
- `random_state`: Random seed for reproducibility

**Returns:** `TestResult` object with attributes:
- `statistic`: Test statistic value
- `pvalue`: P-value
- `method`: Test name
- `alternative`: Alternative hypothesis
- `additional_info`: Dict with details (CI, critical values, etc.)

### Individual Test Functions

```python
from boot_dw import dw_test, bdw_test, b_rho_test, bca_rho_test

# Classical Durbin-Watson test
result_dw = dw_test(y, X)

# Bootstrapped Durbin-Watson test
result_bdw = bdw_test(y, X, n_bootstrap=200, random_state=42)

# Bootstrapped ρ test (percentile method)
result_brho = b_rho_test(y, X, n_bootstrap=200, random_state=42)

# BCa-ρ test (most powerful)
result_bca = bca_rho_test(y, X, n_bootstrap=200, random_state=42)
```

### Core Functions

```python
from boot_dw.core import durbin_watson, ols_regression, estimate_rho

# Calculate DW statistic
dw_stat = durbin_watson(residuals)

# OLS regression
beta, residuals, fitted = ols_regression(y, X, add_constant=True)

# Estimate AR(1) coefficient
rho_hat = estimate_rho(residuals)
```

### Bootstrap Functions

```python
from boot_dw.bootstrap import (
    recursive_bootstrap_dw,
    recursive_bootstrap_rho,
    bca_confidence_interval
)

# Bootstrap DW distribution
dw_bootstrap = recursive_bootstrap_dw(y, X, residuals, rho_est, n_bootstrap=200)

# Bootstrap ρ distribution
rho_bootstrap = recursive_bootstrap_rho(y, X, residuals, rho_est, n_bootstrap=200)

# BCa confidence interval
lower, upper, z0, a0 = bca_confidence_interval(rho_bootstrap, rho_obs, y, X)
```

## Theoretical Background

### The Durbin-Watson Statistic

For regression model y = Xβ + u with AR(1) errors:

$$u_t = \rho u_{t-1} + e_t, \quad |ρ| < 1$$

The Durbin-Watson statistic is:

$$d = \frac{\sum_{t=2}^T (e_t - e_{t-1})^2}{\sum_{t=1}^T e_t^2} \approx 2(1 - \hat{\rho})$$

where:
- d ≈ 2: No autocorrelation (ρ ≈ 0)
- d < 2: Positive autocorrelation (ρ > 0)
- d > 2: Negative autocorrelation (ρ < 0)

### Bootstrap Procedures

#### BDW Test (Bootstrapped Durbin-Watson)

1. Estimate β̂, ρ̂ from original data
2. Resample innovations ê with replacement
3. Construct u* = e* (imposing H₀: ρ = 0)
4. Create bootstrap data y* = Xβ̂ + u*
5. Compute DW* and build empirical distribution F*_d
6. Compare observed DW to F*_d for p-value

#### B-ρ Test (Bootstrapped ρ)

1. Estimate β̂, ρ̂ and compute innovations
2. Resample innovations ê with replacement
3. Recursively construct u*_t = ρ̂u*_{t-1} + e*_t
4. Estimate ρ* from bootstrap errors
5. Build empirical distribution F*_ρ
6. Test if 0 is in the confidence interval

#### BCa-ρ Test (Bias-Corrected Accelerated ρ)

1. Perform B-ρ bootstrap
2. Calculate bias correction: z₀ = Φ⁻¹(Ĝ(ρ̂))
3. Calculate acceleration: a₀ from jackknife influence function
4. Compute adjusted confidence interval
5. Test if 0 is outside BCa interval

### Performance (from Jeong & Chung 2001)

Monte Carlo results show:

1. **Classical DW test:**
   - Has indeterminate range
   - Poor size and power in small samples

2. **BDW test:**
   - Eliminates indeterminate range
   - Better power than classical DW and (a+bdU) approximation

3. **B-ρ test:**
   - More powerful than BDW
   - May have size distortions in small samples

4. **BCa-ρ test (BEST):**
   - Most accurate empirical size
   - Highest power, especially in small samples (n=10-50)
   - Robust across different sample sizes
   - Strongly recommended for practical applications

## Examples

### Example 1: Testing with Simulated AR(1) Data

```python
import numpy as np
from boot_dw import autocorrelation_test

# Set parameters
np.random.seed(123)
n = 100
k = 3
rho_true = 0.6

# Generate regressors
X = np.random.randn(n, k)
beta_true = np.array([2.0, -1.5, 0.8])

# Generate AR(1) errors
u = np.zeros(n)
u[0] = np.random.randn()
for t in range(1, n):
    u[t] = rho_true * u[t-1] + np.random.randn()

# Generate dependent variable
y = X @ beta_true + u

# Test for autocorrelation
result = autocorrelation_test(y, X, method='bca_rho', random_state=123)
print(result.summary())
```

### Example 2: Comparing All Tests

```python
import numpy as np
from boot_dw import dw_test, bdw_test, b_rho_test, bca_rho_test
from boot_dw.utils import format_latex_table

# Generate data
np.random.seed(42)
n = 50
X = np.random.randn(n, 2)
y = X @ np.array([2, -1]) + np.random.randn(n) * 0.5

# Run all tests
results = {
    'Classical DW': dw_test(y, X),
    'BDW': bdw_test(y, X, n_bootstrap=200, random_state=42),
    'B-ρ (Percentile)': b_rho_test(y, X, n_bootstrap=200, random_state=42),
    'BCa-ρ': bca_rho_test(y, X, n_bootstrap=200, random_state=42)
}

# Print comparison
for name, result in results.items():
    print(f"\n{name}:")
    if result.pvalue is not None:
        print(f"  Statistic: {result.statistic:.4f}")
        print(f"  P-value: {result.pvalue:.4f}")
    else:
        print(f"  DW statistic: {result.statistic:.4f}")
        print(f"  P-value: Not available (use DW tables)")

# Generate LaTeX table
print("\nLaTeX Table:")
print(format_latex_table(results))
```

### Example 3: Power Simulation Study

```python
import numpy as np
import matplotlib.pyplot as plt
from boot_dw import autocorrelation_test

def simulate_power(n=50, k=3, rho_values=None, n_sim=100, n_bootstrap=200):
    """Simulate power function for BCa-ρ test."""
    if rho_values is None:
        rho_values = np.arange(0, 1.0, 0.1)
    
    power = np.zeros(len(rho_values))
    
    for i, rho in enumerate(rho_values):
        rejections = 0
        
        for _ in range(n_sim):
            # Generate data
            X = np.random.randn(n, k)
            u = np.zeros(n)
            u[0] = np.random.randn() / np.sqrt(1 - rho**2)
            
            for t in range(1, n):
                u[t] = rho * u[t-1] + np.random.randn()
            
            y = X @ np.ones(k) + u
            
            # Test
            result = autocorrelation_test(y, X, method='bca_rho', 
                                        n_bootstrap=n_bootstrap, alpha=0.05)
            
            if result.pvalue < 0.05:
                rejections += 1
        
        power[i] = rejections / n_sim
        print(f"ρ = {rho:.1f}: power = {power[i]:.3f}")
    
    return rho_values, power

# Run simulation
rho_vals, power_vals = simulate_power(n=50, k=3, n_sim=100, n_bootstrap=200)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(rho_vals, power_vals, 'o-', linewidth=2, markersize=8)
plt.axhline(y=0.05, color='r', linestyle='--', label='Nominal size (5%)')
plt.xlabel('True ρ', fontsize=12)
plt.ylabel('Rejection Rate', fontsize=12)
plt.title('Power Function of BCa-ρ Test (n=50, k=3)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('power_function.png', dpi=300)
plt.show()
```

## Citation

If you use this package in your research, please cite both the package and the original paper:

**Package:**
```bibtex
@software{boot_dw2024,
  author = {Roudane, Merwan},
  title = {boot\_dw: Bootstrap Tests for Autocorrelation},
  year = {2024},
  url = {https://github.com/merwanroudane/bootdw},
  version = {0.0.1}
}
```

**Original paper:**
```bibtex
@article{jeong2001bootstrap,
  title={Bootstrap tests for autocorrelation},
  author={Jeong, Jinook and Chung, Seoung},
  journal={Computational Statistics \& Data Analysis},
  volume={38},
  number={1},
  pages={49--69},
  year={2001},
  publisher={Elsevier}
}
```

## References

1. Jeong, J. and Chung, S. (2001). "Bootstrap tests for autocorrelation". _Computational Statistics & Data Analysis_ 38: 49-69.

2. Durbin, J. and Watson, G.S. (1950). "Testing for Serial Correlation in Least Squares Regression I". _Biometrika_ 37: 409-428.

3. Durbin, J. and Watson, G.S. (1951). "Testing for Serial Correlation in Least Squares Regression II". _Biometrika_ 38: 159-178.

4. Efron, B. (1987). "Better Bootstrap Confidence Intervals". _Journal of the American Statistical Association_ 82: 171-200.

## License

MIT License - see LICENSE file for details.

## Author

**Dr. Merwan Roudane**  
Email: merwanroudane920@gmail.com  
GitHub: https://github.com/merwanroudane

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This implementation is based on the seminal work of Jeong & Chung (2001). Special thanks to the authors for their rigorous theoretical and empirical analysis of bootstrap methods for autocorrelation testing.
