from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import joblib
from .base import BaseTransformer


class Pipeline(BaseTransformer):
    """
    A pipeline that chains multiple transformers sequentially.

    Example:
    --------
    >>> from transfory.base import ExampleScaler
    >>> from transfory.pipeline import Pipeline
    >>> from transfory.imputer import Imputer
    >>> from transfory.encoder import Encoder
    >>> pipe = Pipeline([
    ...     ("imputer", Imputer(strategy="mean")),
    ...     ("encoder", Encoder(method="label")),
    ...     ("scaler", ExampleScaler())
    ... ])
    >>> pipe.fit(df_train)
    >>> df_transformed = pipe.transform(df_test)
    """

    def __init__(self, steps: List[Tuple[str, BaseTransformer]], name: Optional[str] = None,
                 logging_callback: Optional[callable] = None):
        super().__init__(name=name or "Pipeline", logging_callback=logging_callback)
        self.steps: List[Tuple[str, BaseTransformer]] = steps
        self._validate_steps() # This remains

    # ------------------------------
    # Validation
    # ------------------------------
    def _validate_steps(self) -> None:
        """Ensure all steps are valid (name, BaseTransformer instance)."""
        if not isinstance(self.steps, list):
            raise TypeError("Pipeline steps must be a list of (name, transformer) tuples.")

        for step in self.steps:
            if not isinstance(step, tuple) or len(step) != 2:
                raise ValueError("Each step must be a (name, transformer) tuple.")
            name, transformer = step
            if not isinstance(transformer, BaseTransformer):
                raise TypeError(f"Step '{name}' must inherit from BaseTransformer.")

    # ------------------------------
    # Core fitting logic
    # ------------------------------
    def _fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> None:
        current_data = X
        last_step_idx = len(self.steps) - 1
        for i, (name, transformer) in enumerate(self.steps):
            # Pass the pipeline's callback and the step name to the transformer
            # The lambda now correctly uses the step_name from the child, which is crucial for ColumnTransformer
            if self._logging_callback:
                # This lambda captures the pipeline's step name (`name`) but passes the child's
                # own `step_name` to the callback. This preserves nested names like "ct::imputer".
                # We now prepend the pipeline step name to create a nested name.
                transformer._logging_callback = lambda child_step_name, payload, pipeline_step_name=name: self._logging_callback(
                    f"{pipeline_step_name}::{child_step_name}", payload
                )

            self._log("fit_step_start", {"step": name, "shape": current_data.shape})
            if i < last_step_idx:
                current_data = transformer.fit_transform(current_data, y)
            else: # For the last step, just fit.
                transformer.fit(current_data, y)

            self._log("fit_end", {"step": name, "output_shape": current_data.shape})

        self._fitted_params = {
            "step_names": [n for n, _ in self.steps],
            "n_steps": len(self.steps),
        }

    # ------------------------------
    # Core transformation logic
    # ------------------------------
    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        current_data = X
        for name, transformer in self.steps:
            # Pass the pipeline's callback to the transformer
            if self._logging_callback:
                transformer._logging_callback = lambda child_step_name, payload, pipeline_step_name=name: self._logging_callback(
                    f"{pipeline_step_name}::{child_step_name}", payload
                )

            self._log("transform_step", {"step": name, "input_shape": current_data.shape})
            current_data = transformer.transform(current_data)

            self._log("transform_done", {"step": name, "output_shape": current_data.shape})
        return current_data

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Fit all transformers and transform the data.

        This overrides the base `fit_transform` to provide a more efficient
        implementation for pipelines, avoiding a redundant final transform.
        """
        if self._frozen:
            raise FrozenTransformerError(f"Transformer {self.name} is frozen and cannot be refit.")

        self._validate_input(X)
        current_data = X
        for name, transformer in self.steps:
            # Pass the pipeline's callback to the transformer
            if self._logging_callback:
                transformer._logging_callback = lambda child_step_name, payload, pipeline_step_name=name: self._logging_callback(
                    f"{pipeline_step_name}::{child_step_name}", payload
                )

            self._log("fit_transform_step", {"step": name, "input_shape": current_data.shape})
            current_data = transformer.fit_transform(current_data, y)

            self._log("fit_transform_done", {"step": name, "output_shape": current_data.shape})

        self._is_fitted = True
        return current_data

    # ------------------------------
    # Step management
    # ------------------------------
    def add_step(self, name: str, transformer: BaseTransformer) -> None:
        """Add a new transformer at the end of the pipeline."""
        if not isinstance(transformer, BaseTransformer):
            raise TypeError("New step must inherit from BaseTransformer.")
        self.steps.append((name, transformer))
        self._validate_steps()

    def remove_step(self, name: str) -> None:
        """Remove a transformer by name."""
        before = len(self.steps)
        self.steps = [(n, t) for (n, t) in self.steps if n != name]
        after = len(self.steps)
        if before == after:
            raise ValueError(f"No step named '{name}' found.")

    def get_step(self, name: str) -> Optional[BaseTransformer]:
        """Retrieve a transformer by name."""
        for n, t in self.steps:
            if n == name:
                return t
        return None

    # ------------------------------
    # Persistence
    # ------------------------------
    def save(self, filepath: str) -> None:
        """Save the entire pipeline (and all transformers) to disk."""
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "Pipeline":
        """Load a previously saved pipeline."""
        obj = joblib.load(filepath)
        if not isinstance(obj, Pipeline):
            raise TypeError("Loaded object is not a Pipeline.")
        return obj

    # ------------------------------
    # Representation
    # ------------------------------
    def __repr__(self) -> str:
        step_names = " → ".join([name for name, _ in self.steps])
        return f"<Pipeline ({len(self.steps)} steps): {step_names}>"
