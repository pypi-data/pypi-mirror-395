import pandas as pd
from typing import Optional, List
from .base import BaseTransformer

class DatetimeFeatureExtractor(BaseTransformer):
    """
    Extracts date and time features from datetime columns.

    This transformer identifies columns that are of a datetime type (or can be
    converted to it) and extracts specified features, such as year, month, day,
    etc., into new columns. The original datetime column is dropped after extraction.
    """

    def __init__(self, features: Optional[List[str]] = None, columns: Optional[List[str]] = None, name: Optional[str] = None):
        """
        Initializes the DatetimeFeatureExtractor.

        Parameters
        ----------
        features : list of str, optional
            A list of datetime attributes to extract. Defaults to ['year', 'month', 'day', 'dayofweek'].
            Supported features include any valid pandas `.dt` accessor attribute (e.g., 'year', 'month', 'day', 'hour', 'minute', 'dayofweek', 'week').
        columns : list of str, optional
            The specific columns to process. If None, the transformer will attempt to
            process all object or datetime64 columns.
        """
        super().__init__(name=name or "DatetimeFeatureExtractor")
        self.features = features or ['year', 'month', 'day', 'dayofweek']
        self.columns = columns
        self._fitted_params = {"datetime_columns": []}

    def _fit(self, X: pd.DataFrame, y=None):
        """Identifies the datetime columns to be processed."""
        if self.columns:
            cols_to_process = self.columns
        else:
            # Auto-detect object or datetime columns
            cols_to_process = X.select_dtypes(include=['object', 'datetime64[ns]']).columns

        # Further filter to find columns that are convertible to datetime
        datetime_cols = []
        for col in cols_to_process:
            if pd.api.types.is_datetime64_any_dtype(X[col]) or pd.to_datetime(X[col], errors='coerce').notna().any():
                datetime_cols.append(col)

        self._fitted_params["datetime_columns"] = datetime_cols

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Extracts features from the datetime columns and drops the original."""
        X_out = X.copy()
        datetime_cols = self._fitted_params.get("datetime_columns", [])
        new_cols_created = []

        for col in datetime_cols:
            # Ensure column is in datetime format
            datetime_series = pd.to_datetime(X_out[col], errors='coerce')
            for feature in self.features:
                new_col_name = f"{col}_{feature}"
                if feature == 'week':
                    X_out[new_col_name] = datetime_series.dt.isocalendar().week
                else:
                    X_out[new_col_name] = getattr(datetime_series.dt, feature)
                new_cols_created.append(new_col_name)
            X_out = X_out.drop(columns=col)

        # Log the transform event with details for the reporter
        self._log("transform", {
            "input_shape": X.shape,
            "output_shape": X_out.shape,
            "new_columns_created": new_cols_created,
            "fitted_params": self.fitted_params  # Pass datetime_columns for reporter
        })
        return X_out