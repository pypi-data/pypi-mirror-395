import numpy as np

from sklite.base import ClassifierMixin

from ._base import LinearModel


class LogisticRegression(LinearModel, ClassifierMixin):
    """Logistic Regression classifier using gradient descent.

    This class implements binary logistic regression using gradient descent
    optimization with the sigmoid activation function and cross-entropy loss.

    Parameters
    ----------
    learning_rate : float, default=0.01
        Learning rate for gradient descent optimization.
    max_iter : int, default=1000
        Maximum number of iterations for gradient descent.

    Attributes
    ----------
    weights_ : ndarray of shape (n_features,)
        Coefficients of the logistic model.
    bias_ : float
        Bias/intercept term of the logistic model.
    n_features_in_ : int
        Number of features seen during fit.
    """

    def __init__(self, learning_rate=0.01, max_iter=1000):
        if learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if max_iter <= 0:
            raise ValueError("max_iter must be positive")
        self.learning_rate = learning_rate
        self.max_iter = max_iter

    def _sigmoid(self, z):
        """Sigmoid activation function.

        Parameters
        ----------
        z : ndarray
            Linear combination of inputs.

        Returns
        -------
        ndarray
            Sigmoid activation of z.
        """
        # Clip to prevent overflow in exp
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        """Fit logistic regression model using gradient descent.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values (binary: 0 or 1).

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

        # Check for binary classification
        unique_classes = np.unique(y)
        if len(unique_classes) != 2:
            raise ValueError(
                f"LogisticRegression currently only supports binary classification. "
                f"Got {len(unique_classes)} classes: {unique_classes}"
            )
        if not np.array_equal(unique_classes, [0, 1]):
            raise ValueError(
                f"Target values must be 0 and 1 for binary classification. Got: {unique_classes}"
            )

        n_samples, n_features = X.shape
        self.n_features_in_ = n_features

        self.weights_ = np.zeros(n_features)
        self.bias_ = 0

        # Gradient descent
        for _ in range(self.max_iter):
            # Forward pass
            z = np.dot(X, self.weights_) + self.bias_
            y_pred = self._sigmoid(z)

            # Compute gradients
            grad_w = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            grad_b = (1 / n_samples) * np.sum(y_pred - y)

            # Update parameters
            self.weights_ -= self.learning_rate * grad_w
            self.bias_ -= self.learning_rate * grad_b

        return self

    def predict_proba(self, X):
        """Predict class probabilities for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to predict.

        Returns
        -------
        proba : ndarray of shape (n_samples,)
            Probability of the positive class (class 1).
        """
        # Check if fitted
        if not hasattr(self, "weights_"):
            raise ValueError(
                "This LogisticRegression instance is not fitted yet. "
                "Call 'fit' before using this method."
            )

        X = np.asarray(X)

        if X.ndim == 1:
            X = X.reshape(-1, 1)

        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {X.shape[1]} features, but model was fitted "
                f"with {self.n_features_in_} features"
            )

        z = np.dot(X, self.weights_) + self.bias_
        return self._sigmoid(z)

    def predict(self, X):
        """Predict class labels for samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples to predict.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted class labels (0 or 1).
        """
        proba = self.predict_proba(X)
        return (proba >= 0.5).astype(int)
