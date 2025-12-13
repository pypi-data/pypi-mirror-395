"""
Logistic Regression.
"""

import numpy as np

from ._base import GLM


class LogReg(GLM):
    """
    Logistic Regression using Maximum Likelihood Estimation (MLE).

    As a reminder, Logistic Regression requires the following assumptions:

        1. Linearity:
            Linearity of independent variables and log odds (target).
        2. Independence:
            [y_i, y_i+1, ..., y_n] are independent random variables.
        3. Logit Link Function:
            We link the probability of success to the predicting variables via
            the 'logit' link function.

    The design matrix used to fit the model, X, has M rows and N dimensions,
    excluding the intercept. I.e., it has shape (M, N), or (M, N+1) with the
    intercept.

    Regularization is not currently supported.

    Attributes
    ----------
    max_iter : Optional[int], default=1000
        The maximum number of iterations for the fitting algorithm.
    learning_rate : Optional[float], default=0.01
        The learning rate (step size) used to update the model parameters during
        the fitting algorithm. Only applicable for `grad` and `newton`.
    tolerance : float, default=0.001
        The tolerance for stopping the fitting algorithm when the change in model
        parameters is below this value. Only applicable for `grad` and `newton`.
    beta_momentum : float, default=0.9
        Momentum hyperparameter for the gradient descent update. Only used and
        required when method = 'grad'. A value of 0 is equivalent to standard
        gradient descent.
    method : Literal['newton', 'grad', 'lbfgs'], default 'lbfgs'.
        Optimization method for fitting the model. Currently supported algorithms
        are:
            - `grad`: Gradient Descent (first-order). Requires hyperparameter
              tuning (`learning_rate`, `tolerance`, `beta_momentum`, `max_iter`).
            - `newton`: Newton's Method (second-order). Requires hyperparameter
              tuning (`learning_rate`, `tolerance`, `max_iter`).
            - `lbfgs`: Low-memory Broyden-Fletcher-Goldfarb-Shanno algorithm
              (quasi-Newton). Does not require hyperparameter tuning; only uses
              `max_iter`.
    iterations : int
        The number of iterations performed by the optimization algorithm.
    betas : np.ndarray, shape (1, N+1)
        The model parameters (coefficients) learned during the fitting process,
        where N is the number of features. The element is position [0] is the
        intercept.
    observations : int
        Number of observations in the design matrix.
    dimensions : int
        Number of dimensions in the design matrix, excluding the intercept.
    std_error_betas : np.ndarray, shape (1, N+1)
        The standard errors of the estimated model coefficients.
    last_gradient : np.ndarray, shape (1, N+1)
        The gradient vector from the last iteration of the optimization algorithm.
        Not applicable for the L-BFGS algorithm.
    last_velocity : np.ndarray, shape (1, N+1)
        The velocity vector from the last iteration of the optimization algorithm.
        Only used in momentum-based optimization methods like gradient descent.
    z_stat_betas : np.ndarray, shape (1, N+1)
        The z-statistics for the estimated model coefficients.
    p_values : np.ndarray, shape (1, N+1)
        The p-values corresponding to the z-statistics for the estimated model
        coefficients.
    critical_z : float
        The critical z-value for the estimated model coefficients, based on a
        95% confidence level.
    confidence_interval : Tuple[np.ndarray, np.ndarray]
        95% confidence interval for the estimated model coefficients.
    degrees_of_freedom : int
        Degrees of Freedom. Calculated as (observations - dimensions - 1).

    Methods
    -------
    fit(X, y)
        Fit the Poisson regression model to the input data.
    predict(X)
        Predict the target values (counts) for the input data based on the
        fitted model coefficients.
    summary()
        Generate a model summary table.
    """

    def _objective_func(self, betas: np.ndarray, X: np.ndarray, y: np.ndarray) -> float:
        """
        Compute the negative log-likelihood for Logistic regression. This is
        the objective function we want to minimize in the scipy L-BFGS solver.

        Parameters
        ----------
        betas : np.ndarray, shape (1, N+1)
            The estimated model coefficients including the intercept (position [0]).
        X : np.ndarray, shape (M, N)
            The input design matrix, where M is the number of samples and N is
            the number of features.
        y : np.ndarray, shape (M, 1)
            The true target values for each sample in the dataset. It is a vector
            of size M containing the counts.

        Returns
        -------
        float
            The negative log-likelihood value.
        """
        p = self._link_func(X @ betas.T)
        return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))

    def _link_func(self, y: np.ndarray) -> np.ndarray:
        """
        Compute the sigmoid (logistic) function applied to a linear
        combination of features.

        Parameters
        ----------
        y : np.ndarray, shape (M, 1)
            Fitted values, computed as the dot product of the design matrix
            and the estimated model coefficients.

        Returns
        -------
        np.ndarray, shape (M, 1)
            The output of the sigmoid function applied to the fitted values,
            where each element represents a probability.
        """
        return 1 / (1 + np.exp(-y))

    def _grad_func(self, betas: np.ndarray, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Compute the Gradient (first derivative) of the log-likelihood loss function
        with respect to the model parameters.

        Calculating the Gradient is the first step of each iteration during model
        fitting. As such, we set the 'self._current_sigmoid' instance attribute
        so it can be used by second-order methods during each iteration.

        Parameters
        ----------
        betas : np.ndarray, shape (1, N+1)
            The estimated model coefficients including the intercept (position [0]).
        X : np.ndarray, shape (M, N)
            The input design matrix, where M is the number of samples and N is
            the number of features.
        y : np.ndarray, shape (M, 1)
            The true target values for each sample in the dataset. It is a vector
            of size M containing the counts.

        Returns
        -------
        np.ndarray, shape (1, N)
            The Gradient of the loss function with respect to the model parameters
            (betas), which will be used to update the model parameters during
            model fitting.
        """
        # sigmoid (M, 1), gradient (N, 1)
        self._current_sigmoid = self._link_func(X @ betas.T)
        gradient = X.T @ (y - self._current_sigmoid)
        return -gradient.T

    def _hess_func(self, X: np.ndarray) -> np.ndarray:
        """
        Compute the Hessian (second derivative) of the log-likelihood loss function
        with respect to the model parameters.

        Parameters
        ----------
        X : np.ndarray, shape (M, N)
            The input design matrix, where M is the number of samples and N is
            the number of features.

        Returns
        -------
        np.ndarray, shape (N, N)
            The Hessian matrix.
        """
        diag_elements = self._current_sigmoid * (1 - self._current_sigmoid)
        return -X.T * diag_elements.flatten() @ X
