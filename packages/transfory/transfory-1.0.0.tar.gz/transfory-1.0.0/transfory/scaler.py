import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from .base import BaseTransformer as Transformer


class Scaler(Transformer):
    """
    A wrapper for scikit-learn's scaling transformers.

    Applies a specified scaling method to all numerical columns in a DataFrame.

    Methods:
    - 'minmax':  Wraps sklearn.preprocessing.MinMaxScaler.
    - 'zscore': Wraps sklearn.preprocessing.StandardScaler.
    """

    def __init__(self, method="minmax"):
        super().__init__(name=f"Scaler(method='{method}')")
        self.method = method

        # Map method names to scikit-learn scaler classes
        scaler_map = {
            "minmax": MinMaxScaler,
            "zscore": StandardScaler,
        }

        if method not in scaler_map:
            raise ValueError(f"Method '{method}' is not supported. Available methods: {list(scaler_map.keys())}")

        # The internal scikit-learn scaler instance
        self._scaler = scaler_map[method]()
        self._columns_to_scale = None

    def _fit(self, X: pd.DataFrame, y=None):
        """Fit the scaler on the numerical columns of X."""
        self._columns_to_scale = X.select_dtypes(include="number").columns
        if not self._columns_to_scale.empty:
            self._scaler.fit(X[self._columns_to_scale])

        # Store the fitted scaler for persistence and inspection, per BaseTransformer design
        self._fitted_params["scaler_instance"] = self._scaler
        self._fitted_params["columns"] = self._columns_to_scale

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform the numerical columns of X using the fitted scaler."""
        if self._columns_to_scale is not None and not self._columns_to_scale.empty:
            X[self._columns_to_scale] = self._scaler.transform(X[self._columns_to_scale])
        return X
