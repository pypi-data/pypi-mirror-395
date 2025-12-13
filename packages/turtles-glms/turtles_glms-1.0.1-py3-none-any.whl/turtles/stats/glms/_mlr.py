"""
Multiple Linear Regression.

MLR does not use the GLM parent class because we calculate  
the model coefficients using Ordinary Least Squares (OLS), which 
is pure linear algebra and does not require optimization.
"""

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import probplot, t

from ..._utils import _add_intercept, _validate_args
from ...plotting import plot_y_vs_x


class MLR:
    """
    Multiple Linear Regression using Oridinary Least Squares (OLS).

    As a reminder, simple Multiple Linear Regression requires the following
    assumptions:

        1. Linearity / Mean Zero:
            The relationship between the dependent and each independent variable
            is linear, and the residuals (errors) have a mean of zero.
        2. Constant Variance (Homoscedasticity):
            The variance of the residuals (errors) is constant, i.e., all errors
            have the same variance.
        3. Independence (Uncorrelated Errors):
            The residuals are independent random variables of each other. This
            implies that there is no autocorrelation, meaning the error term at
            any given observation should not be correlated with the error term
            at any other observation.
        4. Normality of Errors:
            The residuals of the model are approximately normally distributed.

    The design matrix used to fit the model, X, has M rows and N dimensions,
    excluding the intercept.

    Regularization is not currently supported.

    Attributes
    ----------
    variable_names : List[str]
        List of variable names passed during model fit.
    observations : int
        Number of observations in the design matrix.
    dimensions : int
        Number of dimensions in the design matrix, excluding the intercept.
    degrees_of_freedom : int
        Degrees of Freedom. Calculated as (observations - dimensions - 1).
    betas : np.ndarray
        The estimated model coefficients, including the intercept (first element).
    intercept : float
        The intercept term (the first element of betas).
    residuals : np.ndarray
        The residuals from the fitted model.
    variance : float
        The estimated sample variance from the fitted model.
    rss : float
        The Residual Sum of Squares (RSS) value from the fitted model.
    mse : float
        The Mean Squared Error (MSE) value from the fitted model.
    rmse : float
        The Root Mean Squared Error (RMSE) value from the fitted model.
        Also the std deviation of the residuals.
    std_residuals : np.ndarray
        Standardized residuals from the fitted model.
    covariance : np.ndarray
        The covariance matrix of the estimated model coefficients.
    std_error_betas : np.ndarray
        The standard errors of the estimated model coefficients.
    t_stat_betas : np.ndarray
        The t-statistic of each model coefficient.
    p_values : np.ndarray
        Model coefficient p-values.
    critical_t : float
        Critical t-value at 95% confidence from the fitted model.
    confidence_interval : Tuple[np.ndarray, np.ndarray]
        95% confidence interval for the estimated model coefficients.
    sst : float
        Sum of Squares Total from the fitted model.
    r2 : float
        R-squared from the fitted model. Interpreted as the proportion of
        total variability in the dependent variable that can be explained
        by the model.
    r2_adj : float
        Adjusted R-squared from the fitted model. R-squared with a 'penalty'
        for models with a higher number of predictors.

    Methods
    -------
    fit(X, y)
        Fit a Multiple Linear Regression model to the given data.
    predict(X)
        Predict the target values for the given input data.
    summary()
        Generate a model summary table.
    plot_residuals_hist()
        Generates a simple histogram plot of the residuals. Useful
        for checking the normality assumption. If you want to create
        your own plot, you can use the self.residuals instance property.
    plot_residuals_vs_ind()
        Generates a scattor plot of the standardized residuals vs an
        independent variable.
    plot_residuals_vs_fitted()
        Generates a scattor plot of the standardized residuals vs the
        fitted values.
    qq_plot()
        Generates a QQ plot using the standardized residuals.
    """

    def __init__(self):
        self.variable_names = None

        self._fitted = False

    @property
    def observations(self):
        self._is_fit()
        return self._m

    @property
    def dimensions(self):
        self._is_fit()
        return self._n

    @property
    def degrees_of_freedom(self):
        self._is_fit()
        return self._dof

    @property
    def betas(self):
        self._is_fit()
        return self._betas

    @property
    def intercept(self):
        self._is_fit()
        return self._intercept

    @property
    def residuals(self):
        self._is_fit()
        return self._residuals

    @property
    def variance(self):
        self._is_fit()
        return self._variance

    @property
    def rss(self):
        self._is_fit()
        return self._rss

    @property
    def mse(self):
        self._is_fit()
        return self._mse

    @property
    def rmse(self):
        self._is_fit()
        return self._rmse

    @property
    def std_residuals(self):
        self._is_fit()
        return self._std_residuals

    @property
    def covariance(self):
        self._is_fit()
        return self._covariance

    @property
    def std_error_betas(self):
        self._is_fit()
        return self._std_error_betas

    @property
    def t_stat_betas(self):
        self._is_fit()
        return self._t_stat_betas

    @property
    def p_values(self):
        self._is_fit()
        return self._p_values

    @property
    def critical_t(self):
        self._is_fit()
        return self._critical_t

    @property
    def confidence_interval(self):
        self._is_fit()
        return self._confidence_interval

    @property
    def sst(self):
        self._is_fit()
        return self._sst

    @property
    def r2(self):
        self._is_fit()
        return self._r2

    @property
    def r2_adj(self):
        self._is_fit()
        return self._r2_adj

    def _is_fit(self):
        """
        Check if the model is fit by calling a property that's only
        set in the 'fit()' method.

        This is used to help ensure the model has been fit before the
        user can call instance methods and attributes.

        Raises
        ------
        Warning
            If the class instance has not been fit.

        Returns
        -------
        None
        """
        if not self._fitted:
            raise Warning("Please fit the model before calling this method/property.")

    def fit(self, X: np.ndarray, y: np.ndarray, var_names: Optional[List[str]] = []):
        """
        Fit a Multiple Linear Regression model.

        This method fits the model to the given design matrix `X` and true
        target values `y` using Ordinary Least Squares (OLS).

        Parameters
        ----------
        X : np.ndarray, shape (M, N)
            Design matrix with M rows (samples) and N columns (features). Intercept
            is added during model fit.
        y : np.ndarray, shape (M, 1)
            True target values, where M is the number of samples.
        var_names : Optional[List[Union[str, None]]]
            Optional list of variable names. List must be in the same order that
            the variables appear in the design matrix. 'Intercept' should not
            be included in the list.

        Raises
        ------
        ValueError
            If the length of `var_names` does not equal the number of dimensions
            in the input matrix.

        Returns
        -------
        None
        """

        _validate_args(
            {"X": (X, np.ndarray), "y": (y, np.ndarray), "var_names": (var_names, list)}
        )

        # rows, columns, degrees of freedom
        self._m, self._n = X.shape
        self._dof = self._m - self._n - 1

        if var_names and len(var_names) != self._n:
            raise ValueError(
                "'var_names' length must be equal to the design matrix dimensions."
            )

        self.variable_names = var_names

        # add intercept to design matrix
        X = _add_intercept(X)

        # fit model and get betas
        self._betas = np.linalg.inv(X.T @ X) @ X.T @ y  # (N+1, 1)
        self._betas = self._betas.reshape(1, self._n + 1)  # (1, N+1)
        self._intercept = self._betas[0][0]

        # residuals are (M, 1)
        self._fitted = True
        self._fitted_values = self.predict(X[:, 1:])
        self._residuals = y - self._fitted_values

        # Residual Sum of Squares, aka SSE
        self._rss = np.sum(self._residuals**2)

        # Mean Squared Error
        # MSE is an estimate of variance in MLR, so they should be equal
        self._mse = self._rss / self._dof

        # Root Mean Squared Error, aka std deviation of residuals
        self._rmse = np.sqrt(self._mse)

        # r-squared
        self._sst = np.sum((y - np.mean(y)) ** 2)
        self._r2 = 1 - self._rss / self._sst
        self._r2_adj = 1 - (self._m - 1) * (1 - self._r2) / self._dof

        # standardized residuals
        self._std_residuals = self._residuals / self._rmse

        # estimate sample variance
        self._variance = ((self._residuals.T @ self._residuals) / self._dof)[0][0]

        # Variance-Covariance matrix -- (N+1, N+1)
        self._covariance = self._mse * np.linalg.inv(X.T @ X)

        # std error of betas
        self._std_error_betas = np.sqrt(np.diag(self._covariance)).reshape(
            1, self._n + 1
        )

        # coefficient t-stats -- (1, N+1)
        self._t_stat_betas = self._betas / self._std_error_betas

        # use t-dist CDF to get p-values -- (1, N+1)
        self._p_values = (1 - t.cdf(np.abs(self._t_stat_betas), self._dof)) * 2

        # use t-dist PPF to get critical t-value at 95% confidence
        self._critical_t = t.ppf(1 - 0.05 / 2, self._dof)

        # confidence interval
        self._confidence_interval = (
            self._betas - (self._critical_t * self._std_error_betas),
            self._betas + (self._critical_t * self._std_error_betas),
        )

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict the target values for the given input data.

        The model makes predictions using the learned intercept and coefficients.

        Parameters
        ----------
        X : np.ndarray, shape (M, N)
            Design matrix with N rows (samples) and N columns (features).
            The number of columns (N) must match the number of coefficients.
            The design matrix should not include the intercept; it is added
            within this class method.

        Returns
        -------
        np.ndarray, shape (M, 1)
            The predicted target values.
        """

        self._is_fit()

        _validate_args({"X": (X, np.ndarray)})

        X = _add_intercept(X)
        return X @ self._betas.T

    def summary(self) -> pd.DataFrame:
        """
        Generate a model summary table.

        Returns
        -------
        pd.DataFrame
            DataFrame with the following columns:

            1. Variable
            2. Coefficient
            3. Std Error
            4. t-statistic
            5. p-value
            6. [0.025 (confidence interval)
            7. 0.075] (confidence interval)

        """

        self._is_fit()

        names = self.variable_names or [f"x{i}" for i in range(self._n)]
        stats = {
            "Variable": ["Intercept"] + names,
            "Coefficient": self._betas[0],
            "Std Error": self._std_error_betas[0],
            "t-statistic": self._t_stat_betas[0],
            "p-value": self._p_values[0],
            "[0.025": self._confidence_interval[0][0],
            "0.075]": self._confidence_interval[1][0],
        }
        return pd.DataFrame(stats).round(4)

    def plot_residuals_hist(self, bins: Optional[int] = 20):  # pragma: no cover
        """
        A simple histogram plot of the residuals. Useful for checking
        the Normality assumption.

        Parameters
        ----------
        bins : Optional[int]
            The number of bins to use for the histogram. Default is 20.

        Returns
        -------
        None
            Displays histogram plot.
        """

        self._is_fit()

        _validate_args({"bins": (bins, int)})

        plt.hist(self._residuals, bins=bins, color="blue", edgecolor="black")
        plt.title("Residuals Distribution")
        plt.show()

    def plot_residuals_vs_ind(
        self,
        x: np.ndarray,
        title: Optional[str] = "Residuals vs. Independent",
        xlabel: Optional[str] = "Independent",
    ):  # pragma: no cover
        """
        Plot standardized residuals against an independent variable.
        Useful for checking the Linearity assumption.

        Parameters
        ----------
        x : np.ndarray
            Independent variable.
        title : Optional[str]
            Plot title. Defaults to 'Residuals vs. Independent'.
        xlabel : Optional[str]
            Plot label for x-axis. Defaults to 'Independent'.

        Returns
        -------
        None
            Displays scatter plot.
        """

        self._is_fit()

        # input vars validated in plot function
        plot_y_vs_x(
            x=x, y=self._std_residuals, title=title, xlabel=xlabel, ylabel="Residuals"
        )

    def plot_residuals_vs_fitted(
        self,
        title: Optional[str] = "Residuals vs. Fitted Values",
        xlabel: Optional[str] = "Fitted Values",
    ):  # pragma: no cover
        """
        Plot standardized residuals against fitted values. Useful for checking
        the Constant Variance and Uncorrelated Errors assumptions.

        Parameters
        ----------
        title : Optional[str]
            Plot title. Defaults to 'Residuals vs. Fitted Values'.
        xlabel : Optional[str]
            Plot label for x-axis. Defaults to 'Fitted Values'.

        Returns
        -------
        None
            Displays scatter plot.
        """

        self._is_fit()

        # input vars validated in plot function
        plot_y_vs_x(
            x=self._fitted_values,
            y=self._std_residuals,
            title=title,
            xlabel=xlabel,
            ylabel="Residuals",
        )

    def qq_plot(self):  # pragma: no cover
        """
        Generate a QQ Plot using the standardized residuals. Useful
        for checking the Normality assumption.

        Returns
        -------
        None
            Displays QQ Plot.
        """

        self._is_fit()

        probplot(np.sort(self._std_residuals).flatten(), dist="norm", plot=plt)
        plt.title("QQ Plot")
        plt.show()
