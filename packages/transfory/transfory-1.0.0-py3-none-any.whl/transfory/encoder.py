import pandas as pd
from typing import Optional
from .base import BaseTransformer

class Encoder(BaseTransformer):
    def __init__(self, method="onehot", handle_unseen="ignore", name: Optional[str] = None):
        super().__init__(name=name or f"Encoder(method='{method}')")
        
        supported_methods = ["label", "onehot"]
        if method not in supported_methods:
            raise ValueError(f"Method '{method}' is not supported. Use one of {supported_methods}.")

        supported_unseen = ["ignore", "error"]
        if handle_unseen not in supported_unseen:
            raise ValueError(f"handle_unseen='{handle_unseen}' is not supported. Use one of {supported_unseen}.")
            
        self.method = method
        self.handle_unseen = handle_unseen
        self._fitted_params = {"mappings": {}}

    def _fit(self, X: pd.DataFrame, y=None):
        self._fitted_params["mappings"] = {}
        cat_cols = X.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            # Store unique categories found during fitting
            unique_cats = X[col].dropna().unique()
            if self.method == "label":
                self._fitted_params["mappings"][col] = {cat: i for i, cat in enumerate(unique_cats)}
            elif self.method == "onehot":
                self._fitted_params["mappings"][col] = list(unique_cats)

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        mappings = self._fitted_params.get("mappings", {})
        original_cols = X.columns.tolist()
        out = X.copy()

        if self.method == "label":
            for col, mapping in mappings.items():
                if col in out.columns:
                    # Unseen values will become NaN after mapping
                    unseen_mask = ~out[col].isin(mapping.keys()) & out[col].notna()
                    if unseen_mask.any() and self.handle_unseen == "error":
                        unseen_values = out[col][unseen_mask].unique()
                        raise ValueError(f"Unseen categories in column '{col}': {list(unseen_values)}")
                    
                    # Map known categories, fill unseen with -1
                    out[col] = out[col].map(mapping).fillna(-1).astype(int)

            self._log("transform", {"columns_encoded": list(mappings.keys())})

        elif self.method == "onehot":
            for col, known_cats in mappings.items():
                if col in out.columns:
                    unseen_mask = ~out[col].isin(known_cats) & out[col].notna()
                    if unseen_mask.any() and self.handle_unseen == "error":
                        unseen_values = out[col][unseen_mask].unique()
                        raise ValueError(f"Unseen categories in column '{col}': {list(unseen_values)}")

                    for cat in known_cats:
                        # Create column for each known category
                        out[f"{col}_{cat}"] = (out[col] == cat).astype(int)
                    # Drop original column after encoding
                    out.drop(columns=[col], inplace=True)
            
            new_cols = [c for c in out.columns if c not in original_cols]
            self._log("transform", {
                "input_shape": (out.shape[0], len(original_cols)),
                "new_columns_added": new_cols,
                "output_shape": out.shape
            })

        return out

    def __repr__(self):
        return f"Encoder(method='{self.method}', handle_unseen='{self.handle_unseen}')"

