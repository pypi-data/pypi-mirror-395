"""
GLMs submodule.
"""

from ._mlr import MLR
from ._logreg import LogReg
from ._poisson import PoissonReg


__all__ = [
    "MLR",
    "LogReg",
    "PoissonReg"
]
