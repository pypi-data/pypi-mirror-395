"""
Poisson Regression.
"""

import numpy as np

from ._base import GLM


class PoissonReg(GLM):
    """
    Poisson Regression using Maximum Likelihood Estimation (MLE).

    Assumptions for Poisson Regression:

        1. Linearity:
            The log of the expected count is a linear combination of the
        predictors.
        2. Independence:
            The observations are independent of one another.
        3. Poisson Distribution:
            The target variable, which is a count of events
            or occurrences, follows a Poisson distribution.
        4. Equidispersion:
            The variance is equal to the mean, i.e., there is no over or
            under dispersion.

    The design matrix used to fit the model, X, has M rows and N dimensions,
    excluding the intercept.

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
    deviance : float
        Deviance statistic; a goodness-of-fit measurement.
    dispersion : float
        Dispersion statistic. In Poisson Regression, dispersion is expected to
        be 1.0. This is calculated as (deviance / degrees_of_freedom).

    Methods
    -------
    fit(X, y, exposure)
        Fit the Poisson regression model to the input data. If exposure is not
        provided, an array of ones is used (i.e., we assume equal exposure).
    predict(X)
        Predict the target values (counts) for the input data based on the
        fitted model coefficients.
    summary()
        Generate a model summary table.
    """

    # overwrite property to trigger exposure
    @property
    def has_exposure(self):
        self._has_exposure = True
        return self._has_exposure

    @property
    def deviance(self) -> float:
        self._is_fit()
        return self._deviance

    @property
    def dispersion(self) -> float:
        self._is_fit()
        return self._dispersion

    def _objective_func(
        self, betas: np.ndarray, X: np.ndarray, y: np.ndarray, exposure: np.ndarray
    ) -> float:
        """
        Compute the negative log-likelihood for Poisson regression. This is the
        objective function we want to minimize in the scipy L-BFGS solver.

        The exposure parameter is used to scale the predicted values (lambdas),
        typically when the count data is related to a varying exposure or
        different observation periods across the samples.

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
        exposure : np.ndarray, shape (M, 1)
            The exposure values for each sample. These represent the varying
            exposure times, population sizes, or different rates of observation,
            which are used to scale the predicted lambdas. It is a vector of size
            M containing the exposure values.

        Returns
        -------
        float
            The negative log-likelihood value.
        """
        lambda_ = self._link_func(X @ betas.T) * exposure
        return -np.sum(y * np.log(lambda_) - lambda_)

    def _link_func(self, y: np.ndarray) -> np.ndarray:
        """
        Compute the exponential of a linear combination of features.

        Parameters
        ----------
        y : np.ndarray, shape (M, 1)
            Fitted values, computed as the dot product of the design matrix
            and the estimated model coefficients.

        Returns
        -------
        np.ndarray, shape (M, 1)
            The output where each element represents a count of events.
        """
        return np.exp(y)

    def _grad_func(
        self, betas: np.ndarray, X: np.ndarray, y: np.ndarray, exposure: np.ndarray
    ) -> np.ndarray:
        """
        Compute the Gradient (first derivative) of the loss function with respect
        to the model parameters.

        Calculating the Gradient is the first step of each iteration during model
        fitting. As such, we set the 'self._current_lambdas' instance attribute
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
        exposure : np.ndarray, shape (M, 1)
            The exposure values for each sample. These represent the varying
            exposure times, population sizes, or different rates of observation,
            which are used to scale the predicted lambdas. It is a vector of size
            M containing the exposure values.

        Returns
        -------
        np.ndarray, shape (1, N)
            The Gradient of the loss function with respect to the model parameters
            (betas), which will be used to update the model parameters during
            model fitting.
        """
        # lambdas is (M, 1), gradient (N, 1)
        self._current_lambdas = self._link_func(X @ betas.T) * exposure
        gradient = X.T @ (y - self._current_lambdas)
        return -gradient.T

    def _hess_func(self, X: np.ndarray) -> np.ndarray:
        """
        Compute the Hessian (second derivative) of the loss function
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
        return -X.T * self._current_lambdas.flatten() @ X

    def _get_coef_stats(self, X: np.ndarray, y: np.ndarray):
        """
        Execute GLM parent class `_get_coef_stats(self)` instance method,
        then calculate additional custom stats for Poisson reg:

            - Deviance
            - Degrees of Freedom
            - Dispersion statistic

        Parameters
        ----------
        X : np.ndarray, shape (M, N+1)
            Design matrix, including the intercept.
        y : np.ndarray, shape (M, 1)
            Target values.

        Returns
        -------
        None
        """
        # ensure parent method still executes
        super()._get_coef_stats(X, y)

        fitted_values = self.predict(X[:, 1:])

        # resolve div by 0 errors
        new_fitted = np.where(fitted_values == 0, 1, fitted_values)
        new_y = np.where(y == 0, 1, y)
        multiplier = np.where((y == 0) | (fitted_values == 0), 0, y)

        # calculate deviance
        term_one = multiplier * np.log(new_y / new_fitted)
        deviances = 2 * (term_one - (y - fitted_values))
        self._deviance = np.sum(deviances)

        # calculate dispersion statistic
        self._dispersion = self._deviance / self._dof
