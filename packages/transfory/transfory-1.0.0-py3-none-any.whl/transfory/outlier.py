import pandas as pd
from typing import Optional, List
from .base import BaseTransformer

class OutlierHandler(BaseTransformer):
    """
    Handles outliers in numerical columns using capping methods.

    Methods:
    - 'iqr': Caps outliers based on the Interquartile Range (IQR).
             Values below Q1 - factor * IQR or above Q3 + factor * IQR are capped.
    - 'percentile': Caps outliers at specified lower and upper percentiles.
    """

    def __init__(self, method: str = "iqr", factor: float = 1.5,
                 lower_quantile: float = 0.01, upper_quantile: float = 0.99,
                 quantile_interpolation: str = 'linear',
                 columns: Optional[List[str]] = None, name: Optional[str] = None):
        super().__init__(name=name or f"OutlierHandler(method='{method}')")

        supported_methods = ["iqr", "percentile"]
        if method not in supported_methods:
            raise ValueError(f"Method '{method}' is not supported. Use one of {supported_methods}.")

        if method == 'iqr' and factor <= 0:
            raise ValueError("Factor for 'iqr' method must be positive.")

        if method == 'percentile' and not (0 <= lower_quantile < upper_quantile <= 1):
            raise ValueError("Percentiles must be between 0 and 1, and lower_quantile must be less than upper_quantile.")

        self.method = method
        self.factor = factor
        self.lower_quantile = lower_quantile
        self.upper_quantile = upper_quantile
        self.quantile_interpolation = quantile_interpolation
        self.columns = columns
        self._fitted_params = {"bounds": {}}

    def _fit(self, X: pd.DataFrame, y=None):
        """Calculate the upper and lower bounds for capping."""
        bounds = {}
        cols_to_process = self.columns or X.select_dtypes(include="number").columns

        for col in cols_to_process:
            if self.method == "iqr":
                Q1 = X[col].quantile(0.25, interpolation=self.quantile_interpolation)
                Q3 = X[col].quantile(0.75, interpolation=self.quantile_interpolation)
                IQR = Q3 - Q1
                lower_bound = Q1 - self.factor * IQR
                upper_bound = Q3 + self.factor * IQR
            elif self.method == "percentile":
                lower_bound = X[col].quantile(self.lower_quantile, interpolation=self.quantile_interpolation)
                upper_bound = X[col].quantile(self.upper_quantile, interpolation=self.quantile_interpolation)
            bounds[col] = (lower_bound, upper_bound)

        self._fitted_params["bounds"] = bounds

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Cap the values in the DataFrame based on the fitted bounds."""
        X_out = X.copy()
        bounds = self._fitted_params.get("bounds", {})
        for col, (lower, upper) in bounds.items():
            X_out[col] = X_out[col].clip(lower=lower, upper=upper)

        # Log the transform event with details for the reporter
        self._log("transform", {
            "input_shape": X.shape,
            "output_shape": X_out.shape,
            "fitted_params": self.fitted_params # Pass bounds for reporter to use
        })
        return X_out