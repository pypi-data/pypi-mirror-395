![CI](https://github.com/adammotzel/pyglms/actions/workflows/ci.yaml/badge.svg)
![coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%20--%203.13-blue)
![License](https://img.shields.io/github/license/adammotzel/pyglms)
 ![PyPI](https://img.shields.io/pypi/v/turtles-glms.svg)


# PyGLMs (Turtles) 🐢

An implementation of various Generalized Linear Models (GLMs), written in Python.

I created this package as a refresher on GLMs and the underlying optimization techniques. It's intended as a learning tool and a reference for building and understanding these models from the ground up.


## Overview

The code is packaged as a Python library named `turtles` ([I like turtles](https://www.youtube.com/watch?v=CMNry4PE93Y)), making the code easy to integrate into your own projects.

The package is written using `numpy` for linear algebra operations, `scipy` for (some) optimization, `pandas` for displaying tabular results, and `matplotlib` for plots.

The following models have been implemented:

1. Multiple Linear Regression (`turtles.stats.glms.MLR` class)
2. Logistic Regression (`turtles.stats.glms.LogReg` class, uses `GLM` parent class)
3. Poisson Regression (`turtles.stats.glms.PoissonReg` class, uses `GLM` parent class)

The `GLM` parent class supports three optimization methods for parameter estimation: Momentum-based Gradient Descent for first-order optimization, Newton's Method for second-order optimization, and Limited-memory Broyden–Fletcher–Goldfarb–Shanno (L-BFGS). The user can specify the desired optimization `method` during class instantiation.

Momentum-based Gradient Descent and Newton's Method are implemented in Python as part of the `turtles` distribution. L-BFGS is implemented using `scipy.optimize`; it's a quasi-Newton method that approximates the Hessian (instead of fully computing it, like Newton's Method), so it's quite fast.


## Usage

You can pip install the package from PyPI:

```bash
pip install turtles-glms
```

See `examples/` in the [GitHub repo](https://github.com/adammotzel/pyglms) for example usage of the GLM classes and statistical functions.

### Fitting GLMs

You can fit GLMs by instantiating a GLM class and calling its `fit()` method.

```python
model = PoissonReg(
    method="newton",
    learning_rate=0.01
)
n_model.fit(
    X=X, 
    y=y, 
    exposure=exposure
)
```

A few important notes about fitting `turtles` GLMs:
1. The `fit()` method parameters `X`, `y`, and (for Poisson) `exposure` must be `numpy` arrays. Parameters `y` and `exposure` must be of shape `(M, 1)`, where `M` is the number of rows in the data. The package does not support `pandas` or `polars` dataframes at this time. See class / instance method docstrings for exact requirements.
2. Each GLM class has a `learning_rate` parameter, applicable to Gradient Descent and Newton's optimization methods. The learning rate (or step size) is a hyperparameter that controls the magnitude of parameter updates during the optimization process. If it's too large, the Hessian matrix may become singular, in which case the learning rate should be decreased. This is typically part of the tuning process.
3. There are currently no regularization methods implemented in the package. Future versions may include L1, L2, and Elastic Net methods.


## Contributing

To run (and edit) this project locally, clone the repo and create your virtual environment from project root using your global (or local) Python version. This project requires Python 3.10+.

```bash
python -m venv
```

Activate the env (`source .venv/Scripts/activate` for Windows OS, `source .venv/bin/activate` for Linux) and install dependencies:

```bash
pip install -e .[dev]
```

Optionally, you can execute `scripts/env.sh` to create and activate a virtual environment using `uv`. The `uv` package manager must be installed for this to work.


### Adding GLMs

To add more GLM classes, use the `GLM` parent class for inheritence (see `PoissonReg` and `LogReg` as examples). The GLM parent class provides a solid framework for implementing new child classes and should be used whenever possible. Unimplemented GLMs include Negative Binomial, Gamma, and Tweedie.


## Testing

All tests are contained within `tests` directories for each module. You can simply execute the `pytest` command from project root to run all unit tests.

```bash
pytest
```

**Notes on Test Coverage:**
- Plotting functions from `turtles.plotting` are tested, but plotting methods in GLM classes 
(like `MLR`) are ignored. Those class methods are essentially just wrappers around `matplotlib` 
and `turtles.plotting` functions.
- `GLM` class methods that are meant to be implemented by child classes are ignored.
