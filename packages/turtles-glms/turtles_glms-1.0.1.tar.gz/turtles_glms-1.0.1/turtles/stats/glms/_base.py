"""
Base GLM class.

This class is used to create child classes for various GLMs, such as Logistic 
Regression and Poisson Regression.

When creating a child class, any class instance method can technically be 
overwritten. However, the GLM parent class implements certain features that all 
child classes should have (like performing optimization), so the child classes 
don't need to duplicate the code. Other methods in the parent class are left empty 
and MUST be imlpemented in the child class for the child class to work properly. 
These are:

    1. `_link_func(self)`: The function to be applied to the linear combination 
       of input variables and coefficients to produce the expected response. In 
       Logistic Regression, for example, this would be the sigmoid function.

    2. `_grad_func(self)`: The Gradient (first derivative) of the GLMs loss 
       function used during model fitting.

    3. `_hess_func(self)`: The Hessian (second derivative) of the GLMs loss 
       function used during model fitting in second-order optimization methods.

    4. `_objective_func(self)`: The objective function we want to minimize when 
       optimizing. This function is used by the scipy L-BFGS solver. The first 
       derivative of this function is the Gradient, and the second derivative 
       is the Hessian.

Each of these must be implemented separately, because the optimization procedure 
differs between GLMs since they have different loss functions. Different loss 
functions means different derivatives, different distributions, etc.

The other functions implemented in this class are common across child classes. 
As previously mentioned, they can be overwritten by the child class if needed.

    1. `_is_fit(self)`: Checks if the model has been fit. This is used to control 
       access to instance attributes and methods the require the model first be 
       fit.

    2. `_get_hessian_inv(self)`: Computes the inverse of a Hessian matrix. This 
       is a simple linear algebra operation with a try/except construct.

    3. `_optimization(self)`: Implements the optimization algorithm using the 
       child class implementation of the derivative methods and objective function.

    4. `_get_coef_stats(self)`:`: Calculates basic stats for coefficients from 
       model fitting, such as std errors, p-values, confidence intervals, etc.

    5. `_get_std_errors(self)`: Calculates std errors for model coefficients using 
       the Coveriance matrix (inverse Hessian).

    6. `fit(self)`: Fits the child class instance using the input `method` for 
       optimization. Also computes the model coefficient statistics.

    7. `predict(self)`: Predict outcome(s) using a linear combination of input 
       variables and the fitted model coefficients. Uses the child classes link 
       function to produce the appropriate response.

    8. `summary(self)`: Produces a summary table for the model after fitting. 
       Displays the estimated model coefficients and their statistics.

Child classes can contain as many additional class methods, instance methods, 
instance attributes, etc. as needed, as long as they don't conlfict with what's 
described above.
"""

import warnings
from typing import List, Literal, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import fmin_l_bfgs_b
from scipy.stats import norm

from ..._utils import _add_intercept, _validate_args
from ._warnings import SingularityWarning

_supported_methods = ["newton", "grad", "lbfgs"]


class GLM:
    """
    Parent class for GLM implementations.

    Class Attributes and Methods are described in each child class
    implementation.
    """

    def __init__(
        self,
        max_iter: int = 1000,
        learning_rate: float = 0.1,
        tolerance: float = 0.000001,
        beta_momentum: float = 0.9,
        method: Literal["newton", "grad", "lbfgs"] = "lbfgs",
    ):
        """
        Initialize the GLM with the specified hyperparameters.

        Parameters
        ----------
        max_iter : Optional[int], default=1000
            The maximum number of iterations for the fitting algorithm.
        learning_rate : Optional[float], default=0.1
            The learning rate (step size) used to update the model parameters
            during the fitting algorithm. Only applicable for `grad` and `newton`.
        tolerance : float, default=0.000001
            The tolerance for stopping the fitting algorithm when the change in
            model parameters is below this value. Only applicable for `grad`
            and `newton`.
        beta_momentum : float, default=0.9
            Momentum hyperparameter for the gradient descent update. Only used
            and required when method = 'grad'. A value of 0 is equivalent to
            standard gradient descent.
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
        """

        _validate_args(
            {
                "max_iter": (max_iter, int),
                "learning_rate": (learning_rate, float),
                "tolerance": (tolerance, float),
                "method": (method, str),
                "beta_momentum": (beta_momentum, (float, int)),
            }
        )

        # additional input checks
        for args in [
            ("max_iter", max_iter),
            ("learning_rate", learning_rate),
            ("tolerance", tolerance),
            ("beta_momentum", beta_momentum),
        ]:
            if args[0] == "tolerance" and (args[1] <= 0) and (args[1] >= 1):
                raise ValueError(
                    (
                        f"tolerance must be greater than 0 and less than 1. "
                        f"Received {args[1]}"
                    )
                )
            elif args[1] <= 0 and args[0] != "beta_momentum":
                raise ValueError(
                    f"{args[0]} must be greater than 0. Recevied {args[1]}"
                )

        if method not in ["newton", "grad", "lbfgs"]:
            raise ValueError(
                f"method must be one of {_supported_methods}. Received {method}"
            )

        self.max_iter = max_iter
        self.learning_rate = learning_rate
        self.tolerance = tolerance
        self.method = method
        self.beta_momentum = beta_momentum

        self.variable_names = None

        self._iterations = 0
        self._fitted = False
        self._velocity = None
        self._gradient = None

        # set exposure using property
        # this can be overwritten in child classes if exposure is applicable
        self.has_exposure

    @property
    def has_exposure(self):
        self._has_exposure = False
        return self._has_exposure

    @property
    def observations(self) -> float:
        self._is_fit()
        return self._m

    @property
    def dimensions(self) -> float:
        self._is_fit()
        return self._n

    @property
    def degrees_of_freedom(self) -> int:
        self._is_fit()
        return self._dof

    @property
    def betas(self) -> np.ndarray:
        self._is_fit()
        return self._betas

    @property
    def iterations(self) -> float:
        self._is_fit()
        return self._iterations

    @property
    def last_gradient(self) -> np.ndarray:
        self._is_fit()
        return self._gradient

    @property
    def last_velocity(self) -> np.ndarray:
        self._is_fit()
        return self._velocity

    @property
    def std_error_betas(self) -> np.ndarray:
        self._is_fit()
        return self._std_error_betas

    @property
    def z_stat_betas(self) -> np.ndarray:
        self._is_fit()
        return self._z_stat_betas

    @property
    def p_values(self) -> np.ndarray:
        self._is_fit()
        return self._p_values

    @property
    def critical_z(self) -> float:
        self._is_fit()
        return self._critical_z

    @property
    def confidence_interval(self) -> Tuple[np.ndarray, np.ndarray]:
        self._is_fit()
        return self._confidence_interval

    # ----- CHILD CLASS INSTANCE METHODS -----

    def _objective_func(
        self, betas: np.ndarray, X: np.ndarray, y: np.ndarray
    ) -> float:  # pragma: no cover
        """
        Compute the negative log-likelihood for the GLM. This is the objective
        function we want to minimize in the scipy L-BFGS solver.

        The function parameters MUST be in the specified order: betas, X, y.
        These are ALWAYS required. The L-BFGS solver passes positional arguments
        to this function in this exact order. If the child class requires a
        parameter like exposure, it must be placed last to maintain the proper
        order.

        This instance method must be implemented in the child class.
        """
        pass

    def _link_func(self, y: np.ndarray) -> np.ndarray:  # pragma: no cover
        """
        Link function for the GLM child class.

        This instance method must be implemented in the child class.
        """
        pass

    def _grad_func(
        self, betas: np.ndarray, X: np.ndarray, y: np.ndarray
    ) -> np.ndarray:  # pragma: no cover
        """
        Gradient calculation function for the GLM child class (i.e., the first
        derivative of the loss function with respect to the model parameters).

        The function parameters MUST be in the specified order: betas, X, y.
        These are ALWAYS required. The L-BFGS solver passes positional arguments
        to this function in this exact order. If the child class requires a
        parameter like exposure, it must be placed last to maintain the proper
        order.

        This instance method must be implemented in the child class.
        """
        pass

    def _hess_func(self, X: np.ndarray) -> np.ndarray:  # pragma: no cover
        """
        Hessian calculation function for the GLM child class (i.e., the second
        derivative of the loss function with respect to the model parameters).

        This instance method must be implemented in the child class.
        """
        pass

    # ----- IMPLEMENTED INSTANCE METHODS -----

    def _is_fit(self):
        """
        Check if the model is fit by calling a property that's only
        set in the 'fit()' method.

        This is used to help ensure the model has been fit before the
        user can call certain instance methods and attributes.

        Raises
        ------
        Warning
            If the class instance has not been fit.
        """
        if not self._fitted:
            raise Warning("Please fit the model before calling this method/property.")

    def _get_hessian_inv(self, H: np.ndarray) -> np.ndarray:
        """
        Compute the inverse of the Hessian matrix.

        Parameters
        ----------
        X : np.ndarray, shape (N, N)
            A Hessian matrix. Must be square.

        Raises
        ------
        SingularityWarning
            If the Hessian matrix is singular and the inverse cannot be computed.
            This may happen if the hyperparameters are not tuned properly, or
            multicollinearity exists.

        Returns
        -------
        np.ndarray, shape (N, N)
            The inverse of the Hessian matrix.
        """
        try:
            hessian_inv = np.linalg.inv(H)
        except np.linalg.LinAlgError:
            warnings.warn(
                "Hessian matrix is singular, cannot compute standard inverse. "
                "Falling back to the Moore-Penrose Pseudoinverse (np.linalg.pinv)."
                "This often indicates perfect collinearity in the design matrix.",
                SingularityWarning,
                stacklevel=2,
            )
            hessian_inv = np.linalg.pinv(H)
        return hessian_inv

    def _gradient_descent(self, **kwargs):
        """
        Momentum-based Gradient Descent for updating betas. Uses the child class
        implementation of the Gradient, `_grad_func()`.

        Parameters
        ----------
        **kwargs
            X : np.ndarray, shape (M, N)
                The input design matrix, where M is the number of samples and N
                is the number of features.
            y : np.ndarray, shape (M, 1)
                The true target values for each sample in the dataset.
            exposure : Optional[np.ndarray], shape (M, 1)
                The exposure values for each sample. Only applicable for GLMs
                that use exposure.

        Returns
        -------
        None
        """
        # send kwargs to child class _grad_func(), which may
        # contain varying parameters
        self._gradient = self._grad_func(self._betas, **kwargs)
        self._velocity = (
            self.beta_momentum * self._velocity
            + (1 - self.beta_momentum) * self._gradient
        )
        self._betas -= self.learning_rate * self._velocity

    def _newtons_method(self, **kwargs):
        """
        Newtons Method for updating betas. Uses the child class implementation
        of the Gradient and Hessian, `_grad_func()` and `_hess_func()`.

        Parameters
        ----------
        **kwargs
            X : np.ndarray, shape (M, N)
                The input design matrix, where M is the number of samples and
                N is the number of features.
            y : np.ndarray, shape (M, 1)
                The true target values for each sample in the dataset.
            exposure : Optional[np.ndarray], shape (M, 1)
                The exposure values for each sample. Only applicable for GLMs
                that use exposure.

        Returns
        -------
        None
        """
        self._gradient = self._grad_func(self._betas, **kwargs)
        H = self._hess_func(kwargs["X"])
        H_inv = self._get_hessian_inv(H)
        self._betas += self.learning_rate * self._gradient @ H_inv

    def _l_bfgs(self, **kwargs):
        """
        Performs optimization using the L-BFGS-B algorithm.

        This method uses the L-BFGS-B (Limited-memory Broyden-Fletcher-Goldfarb-
        Shanno with Box constraints) algorithm from `scipy.optimize` to minimize
        an objective function and estimate the optimal coefficients.

        This method is good for large datasets because it typically converges
        quickly.

        NOTE: The L-BFGS solver implements its own procedure internally; thus
        we set the `_iterations` and `_betas` attributes based on its results.
        We also mark the model as "fitted" to terminate the `_optimization()`
        method.

        https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin_l_bfgs_b.html

        Parameters
        ----------
        **kwargs
            X : np.ndarray, shape (M, N)
                The input design matrix, where M is the number of samples and
                N is the
                number of features.
            y : np.ndarray, shape (M, 1)
                The true target values for each sample in the dataset.
            exposure : Optional[np.ndarray], shape (M, 1)
                The exposure values for each sample. Only applicable for GLMs
                that use exposure.

        Returns
        -------
        None
        """

        # set up args so we include the correct arguments
        X = kwargs.get("X")
        y = kwargs.get("y").flatten()
        exposure = kwargs.get("exposure", None)
        args = (X, y, exposure.flatten()) if exposure is not None else (X, y)

        result = fmin_l_bfgs_b(
            func=self._objective_func,
            x0=self._betas.flatten(),
            fprime=self._grad_func,
            args=args,
            approx_grad=False,
            maxiter=self.max_iter,
        )

        # extract results
        self._betas = result[0].reshape(1, self._n + 1)
        self._fitted = True
        self._iterations = result[2]["nit"]

    def _optimization(self, **kwargs):
        """
        Perform the specified algorithm to estimate model parameters.

        This method iteratively updates the model parameters (betas) with the
        goal of minimizing the loss function. The process continues until
        convergence criteria are met: either the maximum number of iterations
        or a change in the betas below a specified tolerance.

        The **kwargs passed to this function are passed to the appropriate
        algorithm function.

        NOTE: The L-BFGS solver implements its own procedure internally. We
        terminate the `_optimization()` function once its complete, using the
        `_fitted` attribute.

        Parameters
        ----------
        **kwargs
            X : np.ndarray, shape (M, N)
                The input design matrix, where M is the number of samples and
                N is the number of features.
            y : np.ndarray, shape (M, 1)
                The true target values for each sample in the dataset.

        Returns
        -------
        None
        """

        # get appropriate algorithm func based on 'method'
        algo_map = {
            "grad": self._gradient_descent,
            "newton": self._newtons_method,
            "lbfgs": self._l_bfgs,
        }
        update_betas = algo_map.get(self.method)

        while self._iterations < self.max_iter:

            prev_betas = self._betas.copy()

            # perform algo to update betas
            update_betas(**kwargs)

            # strict convergence check
            if (
                np.max(np.abs(self._betas - prev_betas)) < self.tolerance
            ) or self._fitted:
                break

            self._iterations += 1

        self._fitted = True

    def _get_std_errors(self, X: np.ndarray):
        """
        Calculate the Standard Error for the estimated model coefficients.

        The Covariance Matrix is equal to the inverse of the Hessian matrix,
        and the Standard Errors of the estimated model coefficients are equal
        to the square root of the Covariance Matrix diagonals.

        Parameters
        ----------
        X : np.ndarray, shape (M, N+1)
            Design matrix, including the intercept.

        Returns
        -------
        None
        """

        H = self._hess_func(X)
        # covariance matrix is the hessian inverse
        self._covariance = self._get_hessian_inv(H)
        # std errors are the square roots of the diagonal elements
        self._std_error_betas = np.sqrt(np.diagonal(np.abs(self._covariance))).reshape(
            1, self._n + 1
        )

    def _get_coef_stats(self, X: np.ndarray, y: np.ndarray):
        """
        Calculate statistics for the model coefficient estimates.

            1. Std Errors
            2. Z-statistics
            3. P-values
            4. Critical Z-value
            5. 95% confidence intervals

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
        # get std errors
        self._get_std_errors(X)

        # coefficient z-stats -- (1, N+1)
        self._z_stat_betas = self._betas / self._std_error_betas

        # use norm-dist CDF to get p-values -- (1, N+1)
        self._p_values = 2 * (1 - norm.cdf(np.abs(self._z_stat_betas)))

        # use norm-dist PPF to get critical z-value at 95% confidence
        self._critical_z = norm.ppf(1 - 0.05 / 2)

        # confidence interval
        self._confidence_interval = (
            self._betas - (self._critical_z * self._std_error_betas),
            self._betas + (self._critical_z * self._std_error_betas),
        )

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        exposure: Optional[np.ndarray] = None,
        var_names: Optional[List[str]] = [],
    ):
        """
        Fit the model using the optimization 'method' specified during class
        instantiation.

        Parameters
        ----------
        X : np.ndarray, shape (M, N)
            The input design matrix, where M is the number of samples and N
            is the number of features. This should not include the intercept.
        y : np.ndarray, shape (M, 1)
            The true target values for each sample in the dataset.
        exposure : Optional[np.ndarray], shape (M, 1)
            The exposure values for each sample. These represent the varying
            exposure times, population sizes, or different rates of observation,
            which are used to scale the predicted values. It is a vector of size
            M containing the exposure values. Not applicable for all GLMs.
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
            {
                "X": (X, np.ndarray),
                "y": (y, np.ndarray),
                "var_names": (var_names, list),
                "exposure": (exposure, (np.ndarray, type(None))),
            }
        )

        self._m, self._n = X.shape

        if var_names and len(var_names) != self._n:
            raise ValueError(
                "'var_names' length must be equal to the design matrix dimensions."
            )

        # set instance attributes
        self.variable_names = var_names
        self._dof = self._m - self._n - 1

        # initialize
        X = _add_intercept(X)
        self._betas = np.zeros((1, self._n + 1))

        if self.method == "grad":
            self._velocity = np.zeros_like(self._betas)

        # deliver args for optimization; pass exposure, if needed
        package = {"X": X, "y": y}
        if self._has_exposure:
            exposure = exposure if exposure is not None else np.ones_like(y)
            package["exposure"] = exposure

        # fit model
        self._optimization(**package)

        # calculate coefficient stats
        self._get_coef_stats(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict the target values for the given input data.

        The model makes predictions using the learned intercept and coefficients.
        Predicted values are transformed into the appropriate response using
        the child class implementation of the `_link_func()`.

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
        return self._link_func(X @ self._betas.T)

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
            4. z-statistic
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
            "z-statistic": self._z_stat_betas[0],
            "p-value": self._p_values[0],
            "[0.025": self._confidence_interval[0][0],
            "0.075]": self._confidence_interval[1][0],
        }
        return pd.DataFrame(stats).round(4)
