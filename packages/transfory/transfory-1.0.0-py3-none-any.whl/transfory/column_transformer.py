import pandas as pd
import numpy as np
import copy
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from .base import BaseTransformer, NotFittedError

class ColumnTransformer(BaseTransformer):
    """
    Applies different transformers to different columns of a DataFrame.

    This transformer allows for parallel application of multiple transformers,
    each to a specific subset of columns. The results are then concatenated
    into a single output DataFrame.

    Parameters
    ----------
    transformers : list of (str, BaseTransformer, Union[str, List[str], Callable])
        List of (name, transformer, columns) tuples.
        - name (str): A unique name for the transformer.
        - transformer (BaseTransformer or "passthrough"): An instance of a Transfory transformer
          (or a Pipeline of Transfory transformers), or the string "passthrough" to include
          columns without transformation.
        - columns (Union[str, List[str], Callable]): Specifies the columns to
          which the transformer should be applied.
            - If a list of strings: These columns will be selected.
            - If 'numeric': All numerical columns (int, float) will be selected.
            - If 'categorical': All object or category columns will be selected.
            - If a callable: The callable will be applied to the DataFrame's columns
              and should return a list of column names.
    remainder : {'drop', 'passthrough'}, default='drop'
        Strategy for handling columns not specified in `transformers`.
        - 'drop': Columns not specified will be dropped.
        - 'passthrough': Columns not specified will be included in the output
          DataFrame without any transformation.
    name : str, optional
        A human-readable name for this ColumnTransformer instance.
    logging_callback : callable, optional
        A callback function for logging events, typically from an InsightReporter.
    """

    def __init__(self,
                 transformers: List[Tuple[str, Union[BaseTransformer, str], Union[str, List[str], Callable]]],
                 remainder: str = 'drop',
                 name: Optional[str] = None,
                 logging_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None):
        super().__init__(name=name or "ColumnTransformer", logging_callback=logging_callback)

        if not isinstance(transformers, list) or not all(isinstance(t, tuple) and len(t) == 3 for t in transformers):
            raise ValueError("`transformers` must be a list of (name, transformer, columns) tuples.")
        
        if remainder not in ['drop', 'passthrough']:
            raise ValueError("`remainder` must be 'drop' or 'passthrough'.")

        self.transformers = transformers
        self.remainder = remainder
        self._fitted_params['processed_transformers'] = [] # Stores (name, fitted_transformer, actual_cols)
        self._fitted_params['passthrough_columns'] = [] # Stores columns explicitly passed through
        self._fitted_params['remainder_columns'] = [] # Stores columns implicitly passed through

    def _get_columns_by_selector(self, X: pd.DataFrame, selector: Union[str, List[str], Callable]) -> List[str]:
        """Helper to resolve column selectors."""
        if isinstance(selector, list):
            return [col for col in selector if col in X.columns]
        elif isinstance(selector, str):
            if selector == 'numeric':
                return X.select_dtypes(include=np.number).columns.tolist()
            elif selector == 'categorical':
                return X.select_dtypes(include=['object', 'category']).columns.tolist()
            else:
                raise ValueError(f"Unknown string selector '{selector}'. Use 'numeric', 'categorical', or a list of column names.")
        elif callable(selector):
            selected_cols = selector(X.columns)
            if not isinstance(selected_cols, list):
                raise TypeError("Callable column selector must return a list of column names.")
            return [col for col in selected_cols if col in X.columns]
        else:
            raise TypeError(f"Invalid column selector type: {type(selector)}. Must be list, str, or callable.")

    def _fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> None:
        processed_transformers_info = []
        all_selected_cols = set()
        explicit_passthrough_cols = set()

        for t_name, t_instance, col_selector in self.transformers:
            if t_instance == 'passthrough':
                if isinstance(col_selector, list):
                    explicit_passthrough_cols.update(col_selector)
                else:
                    raise ValueError(f"When transformer is 'passthrough', columns must be a list of column names, not '{col_selector}'.")
                continue # Skip fitting for passthrough

            actual_cols = self._get_columns_by_selector(X, col_selector)
            if not actual_cols:
                self._log("fit_skip_transformer", {"transformer_name": t_instance.name if isinstance(t_instance, BaseTransformer) else t_name, "reason": "No columns selected for transformation."})
                continue

            # Create a deep copy of the transformer to ensure isolation
            cloned_transformer = copy.deepcopy(t_instance)

            # Route sub-transformer's logs through this ColumnTransformer's logger
            cloned_transformer._logging_callback = lambda sub_step_name, payload: self._log(
                event=payload.get("event", "unknown"),
                details=payload.get("details", {}),
                transformer_name=payload.get("transformer_name"), # Pass sub-transformer's name
                config=payload.get("config"), # Pass sub-transformer's config
                step_name=f"{t_name}::{sub_step_name}" # Prefix sub-step name
            )

            self._log("fit_sub_transformer_start", {"transformer_name": cloned_transformer.name, "columns": actual_cols, "input_shape": X[actual_cols].shape})
            cloned_transformer.fit(X[actual_cols], y)
            self._log("fit_sub_transformer_end", {"transformer_name": cloned_transformer.name, "columns": actual_cols})

            processed_transformers_info.append((t_name, cloned_transformer, actual_cols))
            all_selected_cols.update(actual_cols)
        
        self._fitted_params['processed_transformers'] = processed_transformers_info
        self._fitted_params['passthrough_columns'] = list(explicit_passthrough_cols.intersection(X.columns))

        # Determine remainder columns
        # Preserve original column order by iterating through X.columns
        # instead of using set operations which lose order.
        handled_cols = all_selected_cols.union(explicit_passthrough_cols)
        self._fitted_params['remainder_columns'] = [
            col for col in X.columns if col not in handled_cols
        ]


    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.is_fitted:
            raise NotFittedError(f"Transformer {self.name} is not fitted. Call .fit() first.")

        transformed_parts = []
        
        # Process each fitted transformer
        for t_name, fitted_transformer, actual_cols in self._fitted_params['processed_transformers']:
            # Route sub-transformer's logs through this ColumnTransformer's logger
            fitted_transformer._logging_callback = lambda sub_step_name, payload: self._log(
                event=payload.get("event", "unknown"),
                details=payload.get("details", {}),
                transformer_name=payload.get("transformer_name"), # Pass sub-transformer's name
                config=payload.get("config"), # Pass sub-transformer's config
                step_name=f"{t_name}::{sub_step_name}" # Prefix sub-step name
            )
            self._log("transform_sub_transformer_start", {"transformer_name": fitted_transformer.name, "columns": actual_cols, "input_shape": X[actual_cols].shape})
            transformed_subset = fitted_transformer.transform(X[actual_cols])
            self._log("transform_sub_transformer_end", {"transformer_name": fitted_transformer.name, "columns": actual_cols, "output_shape": transformed_subset.shape})
            transformed_parts.append(transformed_subset)

        # Handle explicit passthrough columns
        if self._fitted_params['passthrough_columns']:
            passthrough_df = X[self._fitted_params['passthrough_columns']].copy()
            transformed_parts.append(passthrough_df)
            self._log("transform_passthrough", {"columns": self._fitted_params['passthrough_columns'], "reason": "Explicitly passed through."})

        # Handle remainder columns
        if self.remainder == 'passthrough' and self._fitted_params['remainder_columns']:
            remainder_df = X[self._fitted_params['remainder_columns']].copy()
            transformed_parts.append(remainder_df)
            self._log("transform_remainder", {"columns": self._fitted_params['remainder_columns'], "reason": "Remainder columns passed through."})

        if not transformed_parts:
            # If no transformers ran and no passthrough/remainder, return an empty DataFrame
            return pd.DataFrame(index=X.index)
        
        # Concatenate all parts
        X_out = pd.concat(transformed_parts, axis=1)
        return X_out

    def __repr__(self) -> str:
        status = "fitted" if self._is_fitted else "unfitted"
        num_transformers = len(self.transformers)
        return f"<ColumnTransformer ({num_transformers} transformers) status={status}>"