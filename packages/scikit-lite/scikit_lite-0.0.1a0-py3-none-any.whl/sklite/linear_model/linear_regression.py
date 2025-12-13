import numpy as np

from sklite.base import RegressorMixin

from ._base import LinearModel


class SGDRegressor(LinearModel, RegressorMixin):
    """Linear regression model using gradient descent.

    Parameters
    ----------
    learning_rate : float, default=0.01
        Learning rate for gradient descent optimization.
    max_iter : int, default=10000
        Maximum number of iterations for gradient descent.

    Attributes
    ----------
    weights_ : ndarray of shape (n_features,)
        Coefficients of the linear model.
    bias_ : float
        Bias/intercept term of the linear model.
    n_features_in_ : int
        Number of features seen during fit.
    """

    def __init__(self, learning_rate=0.01, max_iter=10000):
        if learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if max_iter <= 0:
            raise ValueError("max_iter must be positive")
        self.learning_rate = learning_rate
        self.max_iter = max_iter

    def fit(self, X, y):
        """Fit linear regression model using gradient descent.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        # Convert to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)

        # Validate shapes
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.ndim != 2:
            raise ValueError(f"X must be 2D array, got {X.ndim}D")
        if y.ndim != 1:
            raise ValueError(f"y must be 1D array, got {y.ndim}D")
        if X.shape[0] != y.shape[0]:
            raise ValueError(f"X and y have incompatible shapes: {X.shape[0]} vs {y.shape[0]}")

        n_samples, n_features = X.shape
        self.n_features_in_ = n_features
        self.weights_ = np.zeros(n_features)
        self.bias_ = 0

        for _ in range(self.max_iter):
            y_hat = np.dot(X, self.weights_) + self.bias_
            grad_w = (1 / n_samples) * np.dot(X.T, (y_hat - y))
            grad_b = (1 / n_samples) * np.sum(y_hat - y)

            self.weights_ -= self.learning_rate * grad_w
            self.bias_ -= self.learning_rate * grad_b

        return self

    def predict(self, X):
        """Predict using the linear model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to predict.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted values.
        """
        # Check if fitted
        if not hasattr(self, "weights_"):
            raise ValueError(
                "This LinearRegression instance is not fitted yet. "
                "Call 'fit' before using this method."
            )

        # Convert and validate input
        X = np.asarray(X)

        if X.ndim == 1:
            X = X.reshape(-1, 1)

        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {X.shape[1]} features, but model was fitted "
                f"with {self.n_features_in_} features"
            )

        return np.dot(X, self.weights_) + self.bias_


class LinearRegression(LinearModel, RegressorMixin):
    """Ordinary least squares Linear Regression.

    This class implements the ordinary least squares linear regression
    using the closed-form solution.

    Attributes
    ----------
    weights_ : ndarray of shape (n_features,)
        Coefficients of the linear model.
    bias_ : float
        Bias/intercept term of the linear model.
    n_features_in_ : int
        Number of features seen during fit.
    """

    def __init__(self):
        pass  # TODO: fit_intercept

    def fit(self, X, y):
        """Fit linear regression model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        # Convert to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)

        # Validate shapes
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.ndim != 2:
            raise ValueError(f"X must be 2D array, got {X.ndim}D")
        if y.ndim != 1:
            raise ValueError(f"y must be 1D array, got {y.ndim}D")
        if X.shape[0] != y.shape[0]:
            raise ValueError(f"X and y have incompatible shapes: {X.shape[0]} vs {y.shape[0]}")

        n_samples, n_features = X.shape
        self.n_features_in_ = n_features

        X_with_intercept = np.c_[np.ones(n_samples), X]
        # Solve using lstsq (handles singular matrices)
        params, _, _, _ = np.linalg.lstsq(X_with_intercept, y, rcond=None)
        self.bias_ = params[0]
        self.weights_ = params[1:]

        return self

    def predict(self, X):
        """Predict using the linear model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to predict.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted values.
        """
        # Check if fitted
        if not hasattr(self, "weights_"):
            raise ValueError(
                "This LinearRegression instance is not fitted yet. "
                "Call 'fit' before using this method."
            )

        # Convert and validate input
        X = np.asarray(X)

        if X.ndim == 1:
            X = X.reshape(-1, 1)

        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {X.shape[1]} features, but model was fitted "
                f"with {self.n_features_in_} features"
            )

        return np.dot(X, self.weights_) + self.bias_
