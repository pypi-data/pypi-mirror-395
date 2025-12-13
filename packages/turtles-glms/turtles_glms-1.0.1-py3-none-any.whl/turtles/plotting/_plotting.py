"""
Plotting functions.
"""

import matplotlib.pyplot as plt
import numpy as np

from .._utils import _validate_args


def plot_y_vs_x(
    x: np.ndarray,
    y: np.ndarray,
    title: str = "Dependent vs. Independent",
    xlabel: str = "Independent",
    ylabel: str = "Dependent",
):
    """
    Scatter plot of a variable (y) against another variable (x).

    Input arrays must be the same shape.

    Parameters
    ----------
    x : np.ndarray
        Input array for x-axis.
    y : np.ndarray
        Input aray for y-axis.
    title : str
        Plot title. Defaults to 'Dependent vs. Independent'.
    xlabel : str
        Plot label for x-axis. Defaults to 'Independent'.
    ylabel : str
        Plot label for y axis. Defaults to 'Dependent'.

    Returns
    -------
    None
        Displays scatter plot.
    """

    _validate_args(
        {
            "x": (x, np.ndarray),
            "y": (y, np.ndarray),
            "title": (title, str),
            "xlabel": (xlabel, str),
            "ylabel": (ylabel, str),
        }
    )

    plt.scatter(x=x, y=y, color="blue", edgecolor="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
