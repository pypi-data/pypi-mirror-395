"""
Functions to support preprocessing/transformations.
"""

from typing import List, Tuple, Union

import numpy as np
import pandas as pd

from .._utils import _validate_args


def one_hot_encode(
    df: pd.DataFrame,
    columns: List[str],
    drop_first: bool = True,
    return_df: bool = True,
) -> Union[pd.DataFrame, Tuple[np.ndarray, List[str]]]:
    """
    One Hot Encode categorical variables in a Pandas DataFrame, also known
    as dummy variables or indicator variables.

    This is essentially just a wrapper around the Pandas `get_dummies()`
    function, but it optioanlly returns a Numpy matrix, making the resulting
    object immediately compatible with the `turtles` GLM classes.

    https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html

    Parameters
    ----------
    df : pd.DataFrame, shape (M, N)
        Pandas DataFrame containing data to be encoded.
    columns : List[str]
        List of column names in `df` to be encoded. Column values must be
        strings or categorical.
    drop_first : bool, default True
        Whether to drop the first category from the resulting table. Dropping
        the first category is useful when building a GLM, because the dropped
        category will then be treated as the 'base case' or 'reference category'
        for model coefficient interpretation.
    return_df : bool, default True
        Optionally return a pandas DataFrame. If False, a Tuple of a numpy
        matrix and resulting column names is returned.

    Returns
    -------
    Union[pd.DataFrame, Tuple[np.ndarray, List[str]]]

        If `return_df` = True, a pandas DataFrame is returned, containing the
        encoded columns.

        If `return_df` = False, a Tuple is returned, where the new matrix is
        in position [0] and the list of new column names in position [1].
    """

    _validate_args(
        {
            "df": (df, pd.DataFrame),
            "columns": (columns, list),
            "drop_first": (drop_first, bool),
            "return_df": (return_df, bool),
        }
    )

    temp = df.copy()

    one_hot_encoded_df = pd.get_dummies(
        temp, columns=columns, drop_first=drop_first, dtype=int
    )

    if return_df:
        return one_hot_encoded_df

    column_names = list(one_hot_encoded_df.columns)

    return one_hot_encoded_df.to_numpy(), column_names
