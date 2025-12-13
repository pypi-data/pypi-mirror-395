"""
Preprocess module.

Functions support common data transformation tasks to prep datasets
for GLMs.
"""

from .._utils import _add_intercept as add_intercept
from ._transform import one_hot_encode

__all__ = ["one_hot_encode", "add_intercept"]
