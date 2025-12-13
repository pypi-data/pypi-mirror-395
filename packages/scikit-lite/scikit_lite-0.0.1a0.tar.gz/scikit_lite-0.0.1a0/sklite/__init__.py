"""scikit-lite: Lightweight ML library with scikit-learn compatible API."""

__version__ = "0.0.1a0"

from sklite.linear_model import LinearRegression, SGDRegressor
from sklite.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    root_mean_squared_error,
)

__all__ = [
    "LinearRegression",
    "SGDRegressor",
    "mean_absolute_error",
    "mean_squared_error",
    "r2_score",
    "root_mean_squared_error",
]
