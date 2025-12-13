import numpy as np

from sklite.base import BaseEstimator, ClusterMixin


class KMeans(ClusterMixin, BaseEstimator):
    """K-means clustering.

    Parameters
    ----------
    n_clusters : int
        Number of clusters, number of centroids to be created.
    max_iter : int, default=500
        Maximum number of iterations.
    tol : float, default=1e-4
        Tolerance to declare convergence.
    random_state : int or None, default=None
        Random seed for centroid initialization.

    Attributes
    ----------
    cluster_centers_ : ndarray of shape (n_clusters, n_features)
        Coordinates of cluster centers.
    labels_ : ndarray of shape (n_samples,)
        Labels of each point.
    n_features_in_ : int
        Number of features seen during fit.
    inertia_ : float
        Sum of squared distances of samples to their closest cluster center.
    """

    def __init__(self, n_clusters, max_iter=500, tol=1e-4, random_state=None):
        if n_clusters <= 0:
            raise ValueError("n_clusters must be positive")
        if max_iter <= 0:
            raise ValueError("max_iter must be positive")
        if tol <= 0:
            raise ValueError("tol must be positive")
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state

    def fit(self, X):
        """Fit K-means clustering.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        # Convert to numpy array
        X = np.asarray(X)

        # Validate shapes
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.ndim != 2:
            raise ValueError(f"X must be 2D array, got {X.ndim}D")

        n_samples, n_features = X.shape
        rng = np.random.default_rng(self.random_state)

        # Initialize centroids randomly from the data points
        random_indices = rng.choice(n_samples, size=self.n_clusters, replace=False)
        centroids = X[random_indices]

        for i in range(self.max_iter):
            # Assign clusters based on closest centroid
            distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
            labels = np.argmin(distances, axis=1)

            # Compute new centroids
            new_centroids = np.array(
                [
                    X[labels == k].mean(axis=0) if np.any(labels == k) else centroids[k]
                    for k in range(self.n_clusters)
                ]
            )

            # Check for convergence
            if np.linalg.norm(new_centroids - centroids) < self.tol:
                break

            centroids = new_centroids

        self.cluster_centers_ = centroids
        self.labels_ = labels
        self.n_features_in_ = n_features

        # Calculate inertia (sum of squared distances to closest cluster center)
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        min_distances = np.min(distances, axis=1)
        self.inertia_ = np.sum(min_distances**2)

        return self

    def predict(self, X):
        """Predict the closest cluster each sample in X belongs to.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            New data to predict.

        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Index of the cluster each sample belongs to.
        """
        # Check if fitted
        if not hasattr(self, "cluster_centers_"):
            raise ValueError(
                "This KMeans instance is not fitted yet. Call 'fit' before using this method."
            )

        # Convert to numpy array
        X = np.asarray(X)

        # Validate shapes
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.ndim != 2:
            raise ValueError(f"X must be 2D array, got {X.ndim}D")
        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {X.shape[1]} features, but model was fitted "
                f"with {self.n_features_in_} features"
            )

        distances = np.linalg.norm(X[:, np.newaxis] - self.cluster_centers_, axis=2)
        labels = np.argmin(distances, axis=1)

        return labels
