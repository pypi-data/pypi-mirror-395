"""
Comprehensive examples for boot_dw package.

This script demonstrates all features of the boot_dw package with
publication-ready output.
"""

import numpy as np
import matplotlib.pyplot as plt
from boot_dw import (
    dw_test,
    bdw_test,
    b_rho_test,
    bca_rho_test,
    autocorrelation_test
)
from boot_dw.utils import format_latex_table


def example_1_basic_usage():
    """Example 1: Basic usage of all tests."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    # Generate sample data
    np.random.seed(42)
    n = 50
    X = np.random.randn(n, 2)
    y = X @ np.array([2, -1]) + np.random.randn(n)
    
    print("\nData: n = 50, k = 2 regressors")
    print("Model: y = β₁ + β₂X₁ + β₃X₂ + u")
    print("H₀: ρ = 0 (no autocorrelation)")
    
    # Test using all methods
    print("\n" + "-"*80)
    print("1. Classical Durbin-Watson Test:")
    print("-"*80)
    result_dw = dw_test(y, X)
    print(result_dw)
    
    print("\n" + "-"*80)
    print("2. Bootstrapped Durbin-Watson (BDW) Test:")
    print("-"*80)
    result_bdw = bdw_test(y, X, n_bootstrap=200, random_state=42)
    print(result_bdw)
    
    print("\n" + "-"*80)
    print("3. Bootstrapped ρ (B-ρ) Test:")
    print("-"*80)
    result_brho = b_rho_test(y, X, n_bootstrap=200, random_state=42)
    print(result_brho)
    
    print("\n" + "-"*80)
    print("4. BCa-ρ Test (RECOMMENDED):")
    print("-"*80)
    result_bca = bca_rho_test(y, X, n_bootstrap=200, random_state=42)
    print(result_bca.summary())


def example_2_ar1_data():
    """Example 2: Testing with known AR(1) autocorrelation."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Data with AR(1) Autocorrelation")
    print("="*80)
    
    # Parameters
    np.random.seed(123)
    n = 100
    k = 3
    rho_true = 0.6
    
    print(f"\nData: n = {n}, k = {k} regressors")
    print(f"True AR(1) coefficient: ρ = {rho_true}")
    
    # Generate regressors
    X = np.random.randn(n, k)
    beta_true = np.array([2.0, -1.5, 0.8])
    
    # Generate AR(1) errors
    u = np.zeros(n)
    u[0] = np.random.randn() / np.sqrt(1 - rho_true**2)
    for t in range(1, n):
        u[t] = rho_true * u[t-1] + np.random.randn()
    
    # Generate dependent variable
    y = X @ beta_true + u
    
    # Test for autocorrelation
    print("\nTesting with BCa-ρ test:")
    result = bca_rho_test(y, X, n_bootstrap=200, random_state=123)
    print(result.summary())
    
    print(f"\nTrue ρ = {rho_true:.4f}")
    print(f"Estimated ρ̂ = {result.statistic:.4f}")
    print(f"95% BCa CI = {result.additional_info['bca_interval']}")
    print(f"\nConclusion: {'Reject H₀' if result.pvalue < 0.05 else 'Fail to reject H₀'} at 5% level")


def example_3_comparison_table():
    """Example 3: Compare all tests in a LaTeX table."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Comparison Table (LaTeX Format)")
    print("="*80)
    
    # Generate data
    np.random.seed(42)
    n = 50
    X = np.random.randn(n, 2)
    y = X @ np.array([2, -1]) + np.random.randn(n) * 0.5
    
    # Run all tests
    results = {
        'Classical DW': dw_test(y, X),
        'BDW': bdw_test(y, X, n_bootstrap=200, random_state=42),
        'B-ρ': b_rho_test(y, X, n_bootstrap=200, random_state=42),
        'BCa-ρ': bca_rho_test(y, X, n_bootstrap=200, random_state=42)
    }
    
    # Generate LaTeX table
    latex_code = format_latex_table(
        results,
        caption="Comparison of Autocorrelation Tests (n=50, k=2)",
        label="tab:comparison"
    )
    
    print("\nLaTeX Table Code:")
    print(latex_code)
    
    # Also print summary
    print("\n\nSummary of Results:")
    print("-"*80)
    print(f"{'Test':<20} {'Statistic':>12} {'P-value':>12} {'Conclusion':>20}")
    print("-"*80)
    for name, result in results.items():
        if result.pvalue is not None:
            conclusion = "Reject H₀" if result.pvalue < 0.05 else "Fail to reject H₀"
            print(f"{name:<20} {result.statistic:12.4f} {result.pvalue:12.4f} {conclusion:>20}")
        else:
            print(f"{name:<20} {result.statistic:12.4f} {'N/A':>12} {'See DW tables':>20}")
    print("-"*80)


def example_4_power_simulation():
    """Example 4: Small-scale power simulation."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Power Simulation (Monte Carlo Study)")
    print("="*80)
    
    # Parameters
    n = 50
    k = 3
    rho_values = np.arange(0, 1.0, 0.2)
    n_simulations = 50  # Small number for demo (use 1000+ for real study)
    n_bootstrap = 100   # Small number for demo (use 200+ for real study)
    alpha = 0.05
    
    print(f"\nSimulation parameters:")
    print(f"  Sample size: n = {n}")
    print(f"  Regressors: k = {k}")
    print(f"  AR(1) values: ρ = {list(rho_values)}")
    print(f"  Simulations per ρ: {n_simulations}")
    print(f"  Bootstrap replications: {n_bootstrap}")
    print(f"  Significance level: α = {alpha}")
    
    print("\nRunning simulations...")
    power = np.zeros(len(rho_values))
    
    for i, rho in enumerate(rho_values):
        rejections = 0
        
        for sim in range(n_simulations):
            # Generate data
            X = np.random.randn(n, k)
            u = np.zeros(n)
            
            if rho == 0:
                u = np.random.randn(n)
            else:
                u[0] = np.random.randn() / np.sqrt(1 - rho**2)
                for t in range(1, n):
                    u[t] = rho * u[t-1] + np.random.randn()
            
            y = X @ np.ones(k) + u
            
            # Test
            result = autocorrelation_test(
                y, X, method='bca_rho', 
                n_bootstrap=n_bootstrap, 
                alpha=alpha
            )
            
            if result.pvalue < alpha:
                rejections += 1
        
        power[i] = rejections / n_simulations
        print(f"  ρ = {rho:.1f}: rejection rate = {power[i]:.3f}")
    
    # Summary
    print("\n" + "-"*80)
    print("Results Summary:")
    print("-"*80)
    print(f"Empirical size (ρ=0.0): {power[0]:.3f}")
    print(f"  Expected: {alpha:.3f}")
    print(f"  Size distortion: {abs(power[0] - alpha):.3f}")
    print(f"\nPower at ρ=0.6: {power[3] if len(power) > 3 else 'N/A':.3f}")
    print(f"Power at ρ=0.8: {power[4] if len(power) > 4 else 'N/A':.3f}")
    print("-"*80)
    
    # Plot power function
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(rho_values, power, 'o-', linewidth=2, markersize=8, label='BCa-ρ test')
        plt.axhline(y=alpha, color='r', linestyle='--', linewidth=1.5, label=f'Nominal size ({alpha})')
        plt.xlabel('True ρ', fontsize=12)
        plt.ylabel('Rejection Rate', fontsize=12)
        plt.title(f'Power Function of BCa-ρ Test\n(n={n}, k={k}, B={n_bootstrap}, simulations={n_simulations})', 
                 fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig('power_function_example.png', dpi=300, bbox_inches='tight')
        print("\nPower function plot saved as: power_function_example.png")
        # plt.show()
    except Exception as e:
        print(f"\nNote: Could not create plot: {e}")


def example_5_different_alternatives():
    """Example 5: Testing different alternatives."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Different Alternative Hypotheses")
    print("="*80)
    
    # Generate data with positive autocorrelation
    np.random.seed(999)
    n = 50
    X = np.random.randn(n, 2)
    rho = 0.5
    u = np.zeros(n)
    u[0] = np.random.randn() / np.sqrt(1 - rho**2)
    for t in range(1, n):
        u[t] = rho * u[t-1] + np.random.randn()
    y = X @ np.array([2, -1]) + u
    
    print("\nData generated with ρ = 0.5 (positive autocorrelation)")
    
    # Test with different alternatives
    alternatives = ['greater', 'less', 'two-sided']
    
    for alt in alternatives:
        print(f"\n{'-'*80}")
        print(f"Testing H₀: ρ = 0  vs  H₁: ρ {alt.replace('greater', '> 0').replace('less', '< 0').replace('two-sided', '≠ 0')}")
        print(f"{'-'*80}")
        
        result = bca_rho_test(y, X, alternative=alt, n_bootstrap=200, random_state=999)
        print(f"\nStatistic: {result.statistic:.4f}")
        print(f"P-value:   {result.pvalue:.4f}")
        print(f"Conclusion: {'Reject H₀' if result.pvalue < 0.05 else 'Fail to reject H₀'} at 5% level")


def main():
    """Run all examples."""
    print("\n")
    print("="*80)
    print(" "*20 + "boot_dw Package Examples")
    print(" "*15 + "Bootstrap Tests for Autocorrelation")
    print("="*80)
    
    # Run examples
    example_1_basic_usage()
    example_2_ar1_data()
    example_3_comparison_table()
    example_4_power_simulation()
    example_5_different_alternatives()
    
    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
