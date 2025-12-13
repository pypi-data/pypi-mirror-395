"""
boot_dw: Bootstrap Tests for Autocorrelation
=============================================

A Python implementation of bootstrap-based tests for autocorrelation in regression 
models, based on Jeong & Chung (2001) "Bootstrap tests for autocorrelation", 
Computational Statistics & Data Analysis 38: 49-69.

This package implements:
- Classical Durbin-Watson test
- Bootstrapped Durbin-Watson (BDW) test
- Bootstrapped ρ (B-ρ) test  
- Bias-corrected accelerated ρ (BCa-ρ) test

Author: Dr. Merwan Roudane
Email: merwanroudane920@gmail.com
Version: 0.0.1
"""

from .core import durbin_watson, ols_regression
from .tests import (
    dw_test,
    bdw_test, 
    b_rho_test,
    bca_rho_test,
    autocorrelation_test
)
from .bootstrap import (
    recursive_bootstrap_dw,
    recursive_bootstrap_rho,
    bca_confidence_interval
)
from .utils import TestResult, format_test_output

__version__ = "0.0.1"
__author__ = "Dr. Merwan Roudane"
__email__ = "merwanroudane920@gmail.com"

__all__ = [
    # Core functions
    'durbin_watson',
    'ols_regression',
    # Test functions
    'dw_test',
    'bdw_test',
    'b_rho_test',
    'bca_rho_test',
    'autocorrelation_test',
    # Bootstrap functions
    'recursive_bootstrap_dw',
    'recursive_bootstrap_rho',
    'bca_confidence_interval',
    # Utilities
    'TestResult',
    'format_test_output',
]
