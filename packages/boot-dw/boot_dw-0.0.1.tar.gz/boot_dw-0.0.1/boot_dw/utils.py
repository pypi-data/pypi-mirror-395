"""
Utility functions and classes for bootstrap autocorrelation tests.
"""

import numpy as np
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass, field


@dataclass
class TestResult:
    """
    Container for statistical test results.
    
    This class provides a standardized format for reporting test results,
    similar to scipy.stats test result objects.
    
    Attributes
    ----------
    statistic : float
        The test statistic value
    pvalue : float or None
        The p-value of the test (None if not available)
    method : str
        Name/description of the test method
    alternative : str
        The alternative hypothesis tested
    additional_info : dict
        Additional information specific to the test
    """
    statistic: float
    pvalue: Optional[float]
    method: str
    alternative: str
    additional_info: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """Format test results for display."""
        return format_test_output(self)
    
    def __repr__(self) -> str:
        """Representation of test result."""
        if self.pvalue is not None:
            return (f"TestResult(statistic={self.statistic:.6f}, "
                   f"pvalue={self.pvalue:.6f}, method='{self.method}')")
        else:
            return (f"TestResult(statistic={self.statistic:.6f}, "
                   f"pvalue=None, method='{self.method}')")
    
    def summary(self) -> str:
        """
        Get detailed summary of test results.
        
        Returns
        -------
        str
            Formatted string with complete test details
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"  {self.method}")
        lines.append("=" * 70)
        lines.append(f"Alternative hypothesis: {self.alternative}")
        lines.append("")
        lines.append(f"Test statistic: {self.statistic:.6f}")
        
        if self.pvalue is not None:
            lines.append(f"P-value:        {self.pvalue:.6f}")
            lines.append("")
            if self.pvalue < 0.01:
                lines.append("*** Highly significant (p < 0.01)")
            elif self.pvalue < 0.05:
                lines.append("**  Significant (p < 0.05)")
            elif self.pvalue < 0.10:
                lines.append("*   Marginally significant (p < 0.10)")
            else:
                lines.append("    Not significant (p >= 0.10)")
        else:
            lines.append("P-value:        Not available")
            lines.append(f"Note:           {self.additional_info.get('note', '')}")
        
        lines.append("")
        lines.append("Additional Information:")
        lines.append("-" * 70)
        
        # Display key additional info
        important_keys = ['rho_estimate', 'dw_statistic', 'n', 'k', 
                         'n_bootstrap', 'critical_value', 'bca_interval',
                         'bias_constant_z0', 'acceleration_constant_a0',
                         'bootstrap_mean', 'bootstrap_std', 'reject_H0']
        
        for key in important_keys:
            if key in self.additional_info:
                value = self.additional_info[key]
                if isinstance(value, float):
                    lines.append(f"  {key:25s}: {value:.6f}")
                elif isinstance(value, tuple):
                    if len(value) == 2:
                        lines.append(f"  {key:25s}: ({value[0]:.6f}, {value[1]:.6f})")
                    else:
                        lines.append(f"  {key:25s}: {value}")
                else:
                    lines.append(f"  {key:25s}: {value}")
        
        lines.append("=" * 70)
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert test result to dictionary.
        
        Returns
        -------
        dict
            Dictionary containing all test information
        """
        return {
            'statistic': self.statistic,
            'pvalue': self.pvalue,
            'method': self.method,
            'alternative': self.alternative,
            **self.additional_info
        }


def format_test_output(result: TestResult, decimal_places: int = 6) -> str:
    """
    Format test result for publication-quality output.
    
    Parameters
    ----------
    result : TestResult
        Test result object to format
    decimal_places : int, default=6
        Number of decimal places for numeric values
        
    Returns
    -------
    str
        Formatted test output
        
    Examples
    --------
    >>> from boot_dw import TestResult, format_test_output
    >>> result = TestResult(statistic=1.8234, pvalue=0.0234, 
    ...                     method="BCa-ρ test", alternative="greater")
    >>> print(format_test_output(result))
    """
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append(f"  {result.method}")
    lines.append("=" * 70)
    lines.append(f"H₀: ρ = 0  vs  H₁: ρ {result.alternative.replace('greater', '> 0').replace('less', '< 0').replace('two-sided', '≠ 0')}")
    lines.append("")
    
    stat_str = f"{result.statistic:.{decimal_places}f}"
    lines.append(f"Test statistic:  {stat_str}")
    
    if result.pvalue is not None:
        pval_str = f"{result.pvalue:.{decimal_places}f}"
        lines.append(f"P-value:         {pval_str}")
        lines.append("")
        
        # Significance stars
        if result.pvalue < 0.001:
            lines.append("Conclusion: Reject H₀ at 0.1% level (***)")
        elif result.pvalue < 0.01:
            lines.append("Conclusion: Reject H₀ at 1% level (**)")
        elif result.pvalue < 0.05:
            lines.append("Conclusion: Reject H₀ at 5% level (*)")
        elif result.pvalue < 0.10:
            lines.append("Conclusion: Reject H₀ at 10% level (†)")
        else:
            lines.append("Conclusion: Fail to reject H₀")
    else:
        lines.append("P-value:         Not available (refer to DW tables)")
    
    # Add important additional information
    if 'rho_estimate' in result.additional_info:
        rho = result.additional_info['rho_estimate']
        lines.append(f"\nEstimated ρ̂:    {rho:.{decimal_places}f}")
    
    if 'dw_statistic' in result.additional_info:
        dw = result.additional_info['dw_statistic']
        lines.append(f"DW statistic:    {dw:.{decimal_places}f}")
    
    if 'bca_interval' in result.additional_info:
        ci_lower, ci_upper = result.additional_info['bca_interval']
        lines.append(f"95% BCa CI:      ({ci_lower:.{decimal_places}f}, {ci_upper:.{decimal_places}f})")
    
    if 'critical_value' in result.additional_info:
        cv = result.additional_info['critical_value']
        if isinstance(cv, tuple):
            lines.append(f"Critical values: ({cv[0]:.{decimal_places}f}, {cv[1]:.{decimal_places}f})")
        else:
            lines.append(f"Critical value:  {cv:.{decimal_places}f}")
    
    if 'n' in result.additional_info and 'k' in result.additional_info:
        n = result.additional_info['n']
        k = result.additional_info['k']
        lines.append(f"\nSample size:     n = {n}, k = {k}")
    
    if 'n_bootstrap' in result.additional_info:
        B = result.additional_info['n_bootstrap']
        lines.append(f"Bootstrap reps:  B = {B}")
    
    lines.append("=" * 70 + "\n")
    return "\n".join(lines)


def format_latex_table(results: Dict[str, TestResult], 
                       caption: str = "Autocorrelation Test Results",
                       label: str = "tab:autocorr") -> str:
    """
    Format multiple test results as a publication-ready LaTeX table.
    
    Parameters
    ----------
    results : dict
        Dictionary mapping test names to TestResult objects
    caption : str, default="Autocorrelation Test Results"
        Table caption
    label : str, default="tab:autocorr"
        LaTeX label for cross-referencing
        
    Returns
    -------
    str
        LaTeX table code
        
    Examples
    --------
    >>> from boot_dw import autocorrelation_test, format_latex_table
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> n = 50
    >>> X = np.random.randn(n, 2)
    >>> y = X @ np.array([2, -1]) + np.random.randn(n)
    >>> 
    >>> results = {
    ...     'Classical DW': autocorrelation_test(y, X, method='dw'),
    ...     'BDW': autocorrelation_test(y, X, method='bdw', random_state=42),
    ...     'BCa-ρ': autocorrelation_test(y, X, method='bca_rho', random_state=42)
    ... }
    >>> print(format_latex_table(results))
    """
    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("  \\centering")
    lines.append(f"  \\caption{{{caption}}}")
    lines.append(f"  \\label{{{label}}}")
    lines.append("  \\begin{tabular}{lcccc}")
    lines.append("    \\toprule")
    lines.append("    Test & Statistic & P-value & $\\hat{\\rho}$ & DW \\\\")
    lines.append("    \\midrule")
    
    for name, result in results.items():
        stat = f"{result.statistic:.4f}"
        
        if result.pvalue is not None:
            if result.pvalue < 0.001:
                pval = f"{result.pvalue:.4f}***"
            elif result.pvalue < 0.01:
                pval = f"{result.pvalue:.4f}**"
            elif result.pvalue < 0.05:
                pval = f"{result.pvalue:.4f}*"
            else:
                pval = f"{result.pvalue:.4f}"
        else:
            pval = "---"
        
        rho = result.additional_info.get('rho_estimate', None)
        rho_str = f"{rho:.4f}" if rho is not None else "---"
        
        dw = result.additional_info.get('dw_statistic', result.statistic if 'DW' in result.method else None)
        dw_str = f"{dw:.4f}" if dw is not None else "---"
        
        lines.append(f"    {name} & {stat} & {pval} & {rho_str} & {dw_str} \\\\")
    
    lines.append("    \\bottomrule")
    lines.append("  \\end{tabular}")
    lines.append("  \\begin{tablenotes}")
    lines.append("    \\footnotesize")
    lines.append("    \\item Note: *, **, *** denote significance at 5\\%, 1\\%, 0.1\\% levels, respectively.")
    lines.append("  \\end{tablenotes}")
    lines.append("\\end{table}")
    
    return "\n".join(lines)


def generate_monte_carlo_table(results_dict: Dict[str, Dict[str, Any]],
                               caption: str = "Monte Carlo Simulation Results",
                               label: str = "tab:mc") -> str:
    """
    Generate LaTeX table for Monte Carlo simulation results.
    
    Useful for replicating tables like Table 1 in Jeong & Chung (2001).
    
    Parameters
    ----------
    results_dict : dict
        Nested dictionary with structure:
        {scenario: {test_name: {'size': float, 'power': dict}}}
    caption : str
        Table caption
    label : str
        LaTeX label
        
    Returns
    -------
    str
        LaTeX table code
    """
    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("  \\centering")
    lines.append(f"  \\caption{{{caption}}}")
    lines.append(f"  \\label{{{label}}}")
    lines.append("  \\begin{tabular}{lcccccc}")
    lines.append("    \\toprule")
    lines.append("    & \\multicolumn{6}{c}{Test Method} \\\\")
    lines.append("    \\cmidrule(lr){2-7}")
    lines.append("    Scenario & DW & $(a+bd_U)$ & BDW & B-$\\rho$ & BCa-$\\rho$ & True \\\\")
    lines.append("    \\midrule")
    
    for scenario, tests in results_dict.items():
        row = [scenario]
        for test in ['DW', 'a+bdU', 'BDW', 'B-rho', 'BCa-rho']:
            if test in tests:
                value = tests[test].get('rejection_rate', tests[test].get('size', 0))
                row.append(f"{value:.3f}")
            else:
                row.append("---")
        lines.append("    " + " & ".join(row) + " \\\\")
    
    lines.append("    \\bottomrule")
    lines.append("  \\end{tabular}")
    lines.append("\\end{table}")
    
    return "\n".join(lines)


def significance_stars(pvalue: float) -> str:
    """
    Return significance stars based on p-value.
    
    Parameters
    ----------
    pvalue : float
        P-value from statistical test
        
    Returns
    -------
    str
        Significance stars: '***', '**', '*', '†', or ''
        
    Examples
    --------
    >>> from boot_dw.utils import significance_stars
    >>> print(significance_stars(0.0001))
    ***
    >>> print(significance_stars(0.03))
    *
    >>> print(significance_stars(0.15))
    <BLANKLINE>
    """
    if pvalue < 0.001:
        return "***"
    elif pvalue < 0.01:
        return "**"
    elif pvalue < 0.05:
        return "*"
    elif pvalue < 0.10:
        return "†"
    else:
        return ""
