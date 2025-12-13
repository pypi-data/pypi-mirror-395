import pandas as pd
import numpy as np
from .base import BaseTransformer as Transformer

class MissingValueHandler(Transformer):
    """
    Handles missing values in a DataFrame using various strategies.

    Strategies:
    - 'mean': Fills missing values with the mean of the column (numeric only).
    - 'median': Fills missing values with the median of the column (numeric only).
    - 'mode': Fills missing values with the mode of the column (numeric or categorical).
    - 'constant': Fills missing values with a provided `fill_value`.
    """
    def __init__(self, strategy="mean", fill_value=None, name: str = None):
        super().__init__(name=name or f"MissingValueHandler(strategy='{strategy}')")
        
        supported_strategies = ["mean", "median", "mode", "constant"]
        if strategy not in supported_strategies:
            raise ValueError(f"Strategy '{strategy}' is not supported. Use one of {supported_strategies}.")
        if strategy == "constant" and fill_value is None:
            raise ValueError("`fill_value` must be provided when strategy is 'constant'.")

        self.strategy = strategy
        self.fill_value = fill_value
        self._fill_values = {}  # stored during fit

    def _fit(self, X: pd.DataFrame, y=None):
        """Calculate the imputation values for each column based on the strategy."""
        self._fill_values = {}
        for col in X.columns:
            if X[col].isna().any():
                if self.strategy == "mean":
                    if pd.api.types.is_numeric_dtype(X[col]):
                        self._fill_values[col] = X[col].mean()
                elif self.strategy == "median":
                    if pd.api.types.is_numeric_dtype(X[col]):
                        self._fill_values[col] = X[col].median()
                elif self.strategy == "mode":
                    self._fill_values[col] = X[col].mode().iloc[0]
                elif self.strategy == "constant":
                    self._fill_values[col] = self.fill_value
        
        # Store fitted params for logging and persistence
        self._fitted_params["fill_values"] = self._fill_values

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values using the stored imputation values."""
        X = X.copy()
        # The fillna method can take a dictionary, which is more efficient
        # than iterating and filling one column at a time.
        if self._fill_values:
            X.fillna(self._fill_values, inplace=True)
        return X

    def __repr__(self):
        if self.strategy == 'constant':
            return f"MissingValueHandler(strategy='{self.strategy}', fill_value={self.fill_value})"
        return f"MissingValueHandler(strategy='{self.strategy}')"
