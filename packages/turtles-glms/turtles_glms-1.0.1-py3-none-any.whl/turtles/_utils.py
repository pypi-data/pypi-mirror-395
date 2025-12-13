"""
General utility functions.
"""

from typing import Any, Dict, Tuple, Union

import numpy as np


def _shape_check(x: np.ndarray, var_name: str, dim: int = 1):
    """
    Check if numpy array has at least `dim` dimensions.

    x : np.ndarray
        Numpy matrix.
    var_name : str
        The variable name to return in the error message.
    dim : int, default 2
        The min number of dimensions in the array.

    Raises
    ------
    ValueError
        If the array has less than `dim` dimensions.

    Returns
    -------
    None
    """

    if np.ndim(x) == 1 or x.shape[1] < dim:
        raise ValueError(f"'{var_name}' must contain more than {dim} dimensions.")


def _validate_args(map: Dict[str, Tuple[Any, Union[type, Tuple[type, ...]]]]):
    """
    Simple type validation of a set of input arguments.

    Parameters
    ----------
    map : Dict[str, Tuple[Any, Union[type, Tuple[type, ...]]]]
        A dictionary where keys are the argument names and the values are
        tuples containing:
        - the object to check
        - the expected type or a tuple of types

    Raises
    ------
    TypeError
        If the type of an argument does not match the expected type.

    Example
    -------
    _validate_args(
        {
            'X': (X, np.array),
            'Y': (Y, (int, float))
        }
    )
    """
    for key, (obj, expected_type) in map.items():
        if isinstance(expected_type, tuple):
            if not any(isinstance(obj, t) for t in expected_type):
                raise TypeError(
                    f"Parameter '{key}' must be one of the types {expected_type}; "
                    f"received {type(obj)}"
                )
        else:
            if not isinstance(obj, expected_type):
                raise TypeError(
                    f"Parameter '{key}' must be of type {expected_type}; "
                    f"received {type(obj)}"
                )


def _add_intercept(X: np.ndarray) -> np.ndarray:
    """
    Add intercept to the design matrix. The intercept is simply
    a column of ones.

    Parameters
    ----------
    X : np.ndarray, shape (M, N)
        Design matrix with M rows (samples) and N columns (features).

    Returns
    -------
    np.ndarray, shape (M, N+1)
        Design matrix with the intercept as the first column.
    """

    _validate_args({"X": (X, np.ndarray)})

    m = X.shape[0]
    intercept = np.ones(m).reshape(m, 1)
    X = np.concatenate((intercept, X), axis=1)
    return X
