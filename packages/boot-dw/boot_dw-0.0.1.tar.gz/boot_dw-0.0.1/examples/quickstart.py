"""
Quick Start Example for boot_dw package.

This script provides a minimal working example to get started.
"""

import numpy as np
from boot_dw import autocorrelation_test

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data (n=50, k=2 regressors)
n = 50
X = np.random.randn(n, 2)
y = X @ np.array([2, -1]) + np.random.randn(n)

print("Quick Start Example: Testing for Autocorrelation")
print("="*60)
print(f"Data: n={n} observations, k=2 regressors")
print(f"Model: y = β₀ + β₁X₁ + β₂X₂ + u")
print(f"Null hypothesis: H₀: ρ = 0 (no autocorrelation)")
print("="*60)

# Perform BCa-ρ test (recommended, most powerful test)
result = autocorrelation_test(y, X, method='bca_rho', 
                              n_bootstrap=200, random_state=42)

# Display results
print("\nTest Results:")
print(result)

# Interpretation
print("\nInterpretation:")
if result.pvalue < 0.001:
    print("*** Highly significant evidence of autocorrelation (p < 0.001)")
elif result.pvalue < 0.01:
    print("**  Strong evidence of autocorrelation (p < 0.01)")
elif result.pvalue < 0.05:
    print("*   Evidence of autocorrelation (p < 0.05)")
elif result.pvalue < 0.10:
    print("†   Weak evidence of autocorrelation (p < 0.10)")
else:
    print("    No significant evidence of autocorrelation (p >= 0.10)")

print(f"\nEstimated AR(1) coefficient: ρ̂ = {result.statistic:.4f}")
print(f"95% BCa confidence interval: {result.additional_info['bca_interval']}")
