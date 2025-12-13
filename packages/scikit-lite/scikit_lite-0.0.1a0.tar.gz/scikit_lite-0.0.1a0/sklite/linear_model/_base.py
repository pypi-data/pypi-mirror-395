from abc import ABCMeta, abstractmethod

from sklite.base import BaseEstimator


class LinearModel(BaseEstimator, metaclass=ABCMeta):
    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass
