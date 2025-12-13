import pandas as pd
from itertools import combinations
from typing import Optional
from .base import BaseTransformer

class FeatureGenerator(BaseTransformer):
    def __init__(self, degree=2, include_interactions=True, name: Optional[str] = None, logging_callback: Optional[callable] = None):
        super().__init__(
            name=name or f"FeatureGenerator(degree={degree})",
            logging_callback=logging_callback
        )
        self.degree = degree
        self.include_interactions = include_interactions

    def _fit(self, X: pd.DataFrame, y=None):
        # Only select numeric columns
        numeric_cols = list(X.select_dtypes(include="number").columns)
        self._fitted_params["columns_to_process"] = numeric_cols

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        columns_to_process = self._fitted_params.get("columns_to_process", [])
        new_feature_names = []

        # Polynomial features
        for col in columns_to_process:
            for p in range(2, self.degree + 1):
                new_col_name = f"{col}^{p}"
                X[new_col_name] = X[col] ** p
                new_feature_names.append(new_col_name)

        # Interaction terms
        if self.include_interactions:
            for col1, col2 in combinations(columns_to_process, 2):
                new_col_name = f"{col1}_x_{col2}"
                X[new_col_name] = X[col1] * X[col2]
                new_feature_names.append(new_col_name)

        # Log the newly created features for better insight
        self._log("transform", {
            "input_shape": X.shape,
            "new_features_created": new_feature_names,
            "output_shape": (X.shape[0], X.shape[1] + len(new_feature_names))
        })

        return X

    def __repr__(self):
        return f"FeatureGenerator(degree={self.degree}, include_interactions={self.include_interactions})"
