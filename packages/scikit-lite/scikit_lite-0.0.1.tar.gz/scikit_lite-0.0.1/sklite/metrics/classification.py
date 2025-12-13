import numpy as np


def accuracy_score(y_true, y_pred):
    """Accuracy sore classification metric.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    accuracy : float
        Accuracy score.
    """
    return np.mean(y_true == y_pred)


def precision_score(y_true, y_pred):
    """Precision score classification metric.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    precision : float
        Precision score.
    """
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    predicted_positives = np.sum(y_pred == 1)
    if predicted_positives == 0:
        return 0.0

    return true_positives / predicted_positives


def recall_score(y_true, y_pred):
    """Recall score classification metric.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    recall : float
        Recall score.
    """
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    actual_positives = np.sum(y_true == 1)
    if actual_positives == 0:
        return 0.0

    return true_positives / actual_positives


def f1_score(y_true, y_pred):
    """F1 score classification metric.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth target values.
    y_pred : array-like of shape (n_samples,)
        Predicted values.

    Returns
    -------
    f1 : float
        F1 score.
    """
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    if (precision + recall) == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)
