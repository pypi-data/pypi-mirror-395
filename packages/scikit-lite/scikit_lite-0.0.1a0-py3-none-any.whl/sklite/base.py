from abc import ABCMeta

__all__ = ["BaseEstimator", "RegressorMixin"]


class BaseEstimator(metaclass=ABCMeta):
    def get_params(self, deep=True):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def set_params(self, **params):
        valid_params = self.get_params(deep=False)
        for k, v in params.items():
            if k not in valid_params:
                raise ValueError(
                    f"Invalid parameter {k!r} for estimator {self.__class__.__name__}. "
                    f"Valid parameters are: {list(valid_params.keys())}"
                )
            setattr(self, k, v)
        return self

    def __repr__(self):
        params = self.get_params()
        params_str = ", ".join(f"{k}={v!r}" for k, v in params.items())
        return f"{self.__class__.__name__}({params_str})"


class RegressorMixin:
    def score(self, X, y):
        from .metrics import r2_score

        y_pred = self.predict(X)
        return r2_score(y, y_pred)
