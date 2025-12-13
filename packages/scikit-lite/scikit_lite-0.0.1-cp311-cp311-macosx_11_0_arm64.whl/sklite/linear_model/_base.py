from abc import ABCMeta, abstractmethod

from sklite.base import BaseEstimator, ClassifierMixin


class LinearModel(BaseEstimator, metaclass=ABCMeta):
    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass


class LinearClassifier(LinearModel, ClassifierMixin, metaclass=ABCMeta):
    """Base class for linear classifiers.

    Inherits from LinearModel and ClassifierMixin to provide
    a common interface for linear classification algorithms.
    """

    pass
