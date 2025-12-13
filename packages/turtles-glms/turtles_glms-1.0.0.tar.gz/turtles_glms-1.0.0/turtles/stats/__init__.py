"""
Stats module.

These functions support various statistical tasks.
"""

from ._stats import (
    calculate_errors,
    variance_inflation_factor,
    pearson_corr,
    covariance_matrix,
    pca
)


__all__ = [
    "glms",  # submodule
    "calculate_errors",
    "variance_inflation_factor",
    "pearson_corr",
    "covariance_matrix",
    "pca"
]
