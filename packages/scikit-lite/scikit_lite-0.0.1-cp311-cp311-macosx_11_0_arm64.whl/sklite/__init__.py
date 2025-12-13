"""scikit-lite: Lightweight ML library with scikit-learn compatible API."""

__version__ = "0.0.1a0"

import warnings

try:
    from sklite._core import rust_health_check
except ImportError:
    warnings.warn(
        "Rust extensions not available.",
        category=ImportWarning,
        stacklevel=2,
    )

    def rust_health_check():
        return "Rust extensions not available."


from sklite.cluster import KMeans
from sklite.linear_model import LinearRegression, LogisticRegression, SGDRegressor
from sklite.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    root_mean_squared_error,
)

__all__ = [
    "LinearRegression",
    "LogisticRegression",
    "KMeans",
    "SGDRegressor",
    "accuracy_score",
    "mean_absolute_error",
    "mean_squared_error",
    "r2_score",
    "root_mean_squared_error",
    "rust_health_check",
]

warnings.warn(
    "This library is in pre-alpha stage. APIs may change without notice.",
    category=UserWarning,
    stacklevel=2,
)
