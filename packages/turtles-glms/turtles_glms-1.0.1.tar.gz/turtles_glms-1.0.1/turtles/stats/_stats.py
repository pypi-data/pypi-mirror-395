"""
Various statistical functions.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.sparse.linalg import eigs
from scipy.stats import pearsonr

from .._utils import _add_intercept, _shape_check, _validate_args


def calculate_errors(
    y_true: np.ndarray, y_pred: np.ndarray, m: Optional[int] = None
) -> Dict[str, float]:
    """
    Calculate errors for arrays containing continuous values. Not suitable
    for classification cases.

        1. Sum of Squared Errors (or Residual Sum of Squares)
        2. Mean Squared Error
        3. Root Mean Squared Error

    Parameters
    ----------
    y_true : np.ndarray
        True target array. Must be the same shape as y_pred and have 1 dimension
        or be flattened.
    y_pred : np.ndarray
        Predicted values target array. Must be the same shape as y_true and have
        1 dimension or be flattened.
    m : int
        Number of observations. If using this function to calculate model fit
        statistics, 'm' should be the degrees of freedom.

    Returns
    -------
    Dict[str, float]
        Dictionary where {key:value} is {"error name": value}.
    """

    m = m or max(y_true.shape)

    _validate_args(
        {"y_true": (y_true, np.ndarray), "y_pred": (y_pred, np.ndarray), "m": (m, int)}
    )

    errors = y_true - y_pred
    sse = np.sum(errors**2).item()
    mse = sse / m
    rmse = np.sqrt(mse).item()

    response = {
        "Sum of Squared Errors": sse,
        "Mean Squared Error": mse,
        "Root Mean Squared Error": rmse,
    }

    return response


def variance_inflation_factor(
    X: np.ndarray, var_names: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate Variance Inflation Factor (VIF) for all predictors in the
    input matrix.

    Fits one linear model for each dimension, where that single dimension
    is the dependent variable, and all other dimensions (including an intercept)
    are the independent variables.

    Parameters
    ----------
    X : np.ndarray, shape (m, n)
        Design matrix. Should not include an intercept.
    var_names : Optional[List[str]]
        Variable names. If not passed, defaults to `x_i` where `i` is the order
        of the dimension in the input matrix. Names must appear in the order
        that they do in the input matrix.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame containing the Coefficient (str), R-squared (float),
        VIF (float).
    """

    _validate_args({"X": (X, np.ndarray)})
    _shape_check(X, "X", 1)

    vifs = {"Coefficient": [], "R-squared": [], "VIF": []}

    for idx in range(X.shape[1]):
        # create design matrix -- all except one predictor
        exog = np.delete(X, idx, axis=1)
        # target -- the one predictor
        endog = X[:, idx]

        # add intercept to design matrix
        exog = _add_intercept(exog)

        # fit model -- one predictor vs all others
        coefs = np.linalg.inv(exog.T @ exog) @ exog.T @ endog

        # calculate residuals
        fitted_vals = exog @ coefs.T
        residuals = endog - fitted_vals

        # Redisual Sum of Squares and Sum of Squares Total
        rss = np.sum(residuals**2)
        sst = np.sum((endog - np.mean(endog)) ** 2)

        # R-squared
        r2 = 1 - rss / sst
        vifs["R-squared"].append(r2.item())

        # VIF
        vif = 1 / (1 - r2)
        vifs["VIF"].append(vif.item())

        vifs["Coefficient"].append(f"x{idx}")

    if var_names is not None:
        vifs["Coefficient"] = var_names

    return pd.DataFrame(vifs)


def pearson_corr(
    x: np.ndarray,
    y: np.ndarray,
) -> Tuple[float, float]:
    """
    Calculate the Pearson Correlation Coefficient.

    This is basically a wrapper around the SciPy function.

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html

    Parameters
    ----------
    x : np.ndarray
        First input array. Usually a single independent variable.
    y : np.ndarray
        Second input array. A single independent or dependent variable.

    Returns
    -------
    Tuple[float, float]
        Tuple containing the correlation coefficient in position [0],
        and the p-value in position [1].
    """

    _validate_args({"x": (x, np.ndarray), "y": (y, np.ndarray)})

    result = pearsonr(x=x.flatten(), y=y.flatten())
    return (result.statistic.item(), result.pvalue.item())


def covariance_matrix(X: np.ndarray, return_xc=False) -> np.ndarray:
    """
    Calculate the covariance between variables in a matrix.

    Parameters
    ----------
    X : np.ndarray
        Design matrix of shape (M, N).
    return_xc : bool, defaults to False
        Optionally return the centered matrix.

    Returns
    -------
    C : np.ndarray
        Covariance matrix of size (N, N).
    X_c : np.ndarray
        Centered input matrix.
    """

    _validate_args({"X": (X, np.ndarray), "return_xc": (return_xc, bool)})
    _shape_check(X, "X", 2)

    # estimate mean for each variable / column
    m = X.shape[0]
    X_t = X.T
    avg = np.mean(X_t, axis=1)

    # 'center' the matrix
    X_c = X_t - avg[:, None]

    # covariance matrix
    C = (X_c @ X_c.T) / m

    if return_xc:
        return C, X_c

    return C


def pca(X: np.ndarray, p: int) -> np.ndarray:
    """
    Principal Component Analysis.

    Parameters
    ----------
    X : np.ndarray, shape (M, N)
        Input data (design matrix) for calculating pricipal components.
    p : int
        Number of principle components to return. Must be less than or
        equal to the number of dimensions in X.

    Raises
    ------
    ValueError
        If the requested number of principal components exceeds the number
        of dimensions in the input matrix.

    Returns
    -------
    np.ndarray, shape (M, p)
        Matrix with p dimensions.
    """

    _validate_args({"X": (X, np.ndarray), "p": (p, int)})
    _shape_check(X, "X", 2)

    if p > X.shape[1]:
        raise ValueError("'p' must be <= 'X' dimensions.")

    # get covariance matrix
    C, X_c = covariance_matrix(X, return_xc=True)

    # calculate eigenvalues, eigenvectors
    s, w = eigs(C, p)
    s = s.real
    s = np.reshape(s, (p, 1))
    w = w.real
    pca = w.T @ X_c

    return pca.T
