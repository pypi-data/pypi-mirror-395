import numpy as np


def mean_absolute_error(y_true, y_pred):
    """Mean absolute error regression metric.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    mae : float
        Mean absolute error.
    """
    return np.mean(np.abs(y_true - y_pred))


def mean_squared_error(y_true, y_pred):
    """Mean squared error regression metric.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    mse : float
        Mean squared error.
    """
    return np.mean((y_true - y_pred) ** 2)


def root_mean_squared_error(y_true, y_pred):
    """Root mean squared error regression metric.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    rmse : float
        Root mean squared error.
    """
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def r2_score(y_true, y_pred):
    """R² (coefficient of determination) regression score.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    r2 : float
        R² score. Returns nan if fewer than 2 samples.
        Returns 0.0 for perfect prediction when variance is 0.
        Returns -inf for non-zero error when variance is 0.
    """
    if len(y_true) < 2:
        return np.nan

    numerator = np.sum((y_true - y_pred) ** 2)
    denominator = np.sum((y_true - np.mean(y_true)) ** 2)

    if denominator == 0:
        return 0.0 if numerator == 0 else -np.inf

    return 1 - numerator / denominator
