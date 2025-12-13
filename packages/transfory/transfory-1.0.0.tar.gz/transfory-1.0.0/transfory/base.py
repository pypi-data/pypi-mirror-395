from __future__ import annotations
import abc
import pickle
import joblib
from typing import Any, Callable, Dict, Iterable, List, Optional
import pandas as pd
import os


class NotFittedError(RuntimeError):
    """Raised when transform is called before fit."""
    pass


class FrozenTransformerError(RuntimeError):
    """Raised when attempting to fit a frozen transformer."""
    pass


class BaseTransformer(abc.ABC):
    """
    Abstract base class for all transformers in Transfory.

    Key responsibilities:
      - provide fit/transform/fit_transform interface
      - validate input types (pandas.DataFrame)
      - record fitted parameters into `_fitted_params`
      - support freezing (prevent re-fitting)
      - support saving / loading state to disk
      - optionally call a logging callback (for InsightReporter)
    """

    def __init__(self, name: Optional[str] = None, logging_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None):
        """
        Parameters
        ----------
        name:
            Optional human-readable name for the transformer. If None, class name is used.
        logging_callback:
            Optional callable with signature (step_name: str, details: dict) that will be invoked
            after fit/transform to allow external loggers (e.g., InsightReporter) to record results.
        """
        self.name: str = name or self.__class__.__name__
        self._is_fitted: bool = False
        self._fitted_params: Dict[str, Any] = {}
        self._frozen: bool = False
        self._last_input_columns: Optional[List[str]] = None
        self._logging_callback = logging_callback

    # ------------------------------
    # Abstract methods subclasses must implement
    # ------------------------------
    @abc.abstractmethod
    def _fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> None:
        """
        Subclass-specific fitting logic must save learned parameters into self._fitted_params.
        Called by fit() after validation.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Subclass-specific transform logic. Must use parameters from self._fitted_params.
        Called by transform() after validation.
        """
        raise NotImplementedError

    # ------------------------------
    # Public API
    # ------------------------------
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "BaseTransformer":
        """
        Fit the transformer to X (and optional y). Records input columns and fitted params.
        Raises FrozenTransformerError if transformer is frozen.
        """
        if self._frozen:
            raise FrozenTransformerError(f"Transformer {self.name} is frozen and cannot be refit.")

        X = self._validate_input(X)

        # let subclass do its work
        self._fit(X, y)

        # record fitted metadata
        self._is_fitted = True
        self._last_input_columns = list(X.columns)
        # call logging hook
        self._log("fit", {"input_shape": X.shape, "fitted_params": dict(self._fitted_params)})
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform X using the fitted parameters.
        Raises NotFittedError if not fitted.
        """
        if not self._is_fitted:
            raise NotFittedError(f"Transformer {self.name} is not fitted. Call .fit() first.")

        X = self._validate_input(X, require_same_columns=True)

        transformed = self._transform(X)

        # call logging hook
        self._log("transform", {"input_shape": X.shape, "output_shape": transformed.shape})
        return transformed

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Convenience: fit then transform.
        """
        self.fit(X, y)
        return self.transform(X)

    # ------------------------------
    # Utility / Metadata
    # ------------------------------
    @property
    def is_fitted(self) -> bool:
        return self._is_fitted

    @property
    def fitted_params(self) -> Dict[str, Any]:
        return dict(self._fitted_params)

    def freeze(self) -> None:
        """Prevent further calls to fit() — useful after saving a trained pipeline."""
        self._frozen = True

    def unfreeze(self) -> None:
        """Allow fit() again."""
        self._frozen = False

    # ------------------------------
    # Persistence
    # ------------------------------
    def save(self, filepath: str) -> None:
        """
        Save transformer to disk using joblib for speed and compatibility.
        """
        dirpath = os.path.dirname(filepath)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "BaseTransformer":
        """
        Load transformer from disk (may be subclass).
        """
        obj = joblib.load(filepath)
        if not isinstance(obj, BaseTransformer):
            raise TypeError("Loaded object is not a BaseTransformer.")
        return obj

    # ------------------------------
    # Validation and helpers
    # ------------------------------
    def _validate_input(self, X: pd.DataFrame, require_same_columns: bool = False) -> pd.DataFrame:
        """
        Ensure X is a pandas DataFrame and optionally ensure columns match those seen during fit.
        Returns a shallow copy for safety.
        """
        if not isinstance(X, pd.DataFrame):
            raise TypeError(f"{self.name} expects a pandas.DataFrame, got {type(X)}")

        # Optionally check columns match training
        if require_same_columns and self._last_input_columns is not None:
            # Check that all columns from `fit` are present in `transform`'s X.
            # This is more flexible than an exact match, allowing extra columns.
            fit_cols_set = set(self._last_input_columns)
            transform_cols_set = set(X.columns)

            if not fit_cols_set.issubset(transform_cols_set):
                missing_cols = fit_cols_set - transform_cols_set
                raise ValueError(
                    f"Missing columns for {self.name}. Transformer was fitted on {self._last_input_columns}, "
                    f"but the following columns are missing: {list(missing_cols)}."
                )

        # return a shallow copy to avoid accidental in-place edits by subclasses
        return X.copy()

    def _log(self, event: str, details: Dict[str, Any], step_name: Optional[str] = None, config: Optional[Dict[str, Any]] = None, transformer_name: Optional[str] = None) -> None:
        """
        Internal logging hook. If a logging_callback is set, call it with standardized payload.
        """
        if not callable(self._logging_callback):
            return

        # If a config is passed directly (e.g., from a ColumnTransformer forwarding a sub-log),
        # use it. Otherwise, generate a config from the transformer's own public attributes.
        try:
            if config is not None:
                config_params = config
            else:
                config_params = {
                    k: v for k, v in self.__dict__.items()
                    if not k.startswith('_') and not callable(v)
                }

            payload = {
                # Use the forwarded name if provided, otherwise use self.name
                "transformer_name": transformer_name if transformer_name is not None else self.name,
                "event": event,
                "details": details,
                "config": config_params,
            }
            # Use the provided step_name (from a pipeline) or the transformer's own name.
            self._logging_callback(step_name or self.name, payload)
        except Exception:
            # Logging should never break pipeline execution. Silently ignore logging errors.
            # In development you may want to raise or print a warning.
            pass

    def __getstate__(self) -> Dict[str, Any]:
        """
        Customize serialization. Exclude the logging callback, which is not serializable.
        """
        state = self.__dict__.copy()
        state["_logging_callback"] = None  # Exclude non-serializable callback
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """
        Customize deserialization.
        """
        self.__dict__.update(state)

    # ------------------------------
    # Dunder & convenience
    # ------------------------------
    def __repr__(self) -> str:
        status = "fitted" if self._is_fitted else "unfitted"
        return f"<{self.__class__.__name__} name={self.name} status={status} params={list(self._fitted_params.keys())}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseTransformer):
            return False
        return (self.__class__ == other.__class__
                and self.name == other.name
                and self._fitted_params == other._fitted_params)

    def __len__(self) -> int:
        """Return a measure (number of stored fitted params) for convenience."""
        return len(self._fitted_params)


# ------------------------------
# Minimal example subclass for demonstration / testing
# ------------------------------
class ExampleScaler(BaseTransformer):
    """
    Minimal example implementation of a scaler transformer using BaseTransformer.
    This is just to demonstrate how subclasses should implement _fit/_transform.
    """

    def __init__(self, columns: Optional[Iterable[str]] = None, name: Optional[str] = None, logging_callback: Optional[Callable[[str, Dict[str, Any]], None]] = None):
        super().__init__(name=name, logging_callback=logging_callback)
        self.columns = list(columns) if columns is not None else None

    def _fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> None:
        numeric = X.select_dtypes(include="number")
        cols = self.columns or list(numeric.columns)
        means = {}
        stds = {}
        for c in cols:
            means[c] = float(X[c].mean())
            stds[c] = float(X[c].std(ddof=0)) or 1.0
        self._fitted_params = {"means": means, "stds": stds, "columns": cols}

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if "means" not in self._fitted_params:
            raise NotFittedError("ExampleScaler was not fitted.")
        out = X.copy()
        cols = self._fitted_params["columns"]
        for c in cols:
            out[c] = (out[c] - self._fitted_params["means"][c]) / self._fitted_params["stds"][c]
        return out