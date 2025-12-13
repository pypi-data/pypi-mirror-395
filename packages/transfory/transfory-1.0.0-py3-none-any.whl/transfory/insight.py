from __future__ import annotations
import pandas as pd
import re
import json
from datetime import datetime
from typing import Any, Dict, List, Optional


class InsightReporter:
    """
    Collects and summarizes events emitted by transformers.

    The InsightReporter acts as a lightweight event logger.
    Each transformer calls it via `logging_callback(name, payload)`,
    and the reporter records what transformations were performed.

    Example usage
    -------------
    >>> reporter = InsightReporter()
    >>> callback = reporter.get_callback()
    >>> scaler = ExampleScaler(logging_callback=callback)
    >>> scaler.fit_transform(df)
    >>> print(reporter.summary())
    """

    def __init__(self):
        # Store logs as list of dicts
        self._logs: List[Dict[str, Any]] = []
        self._start_time: datetime = datetime.now()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_callback(self):
        """
        Returns a callable that transformers can use for logging.
        This allows the reporter to be plugged into a pipeline easily.
        """
        def _callback(step_name: str, payload: Dict[str, Any]) -> None:
            self.log_event(step_name, payload)
        return _callback

    def log_event(self, step_name: str, payload: Dict[str, Any]) -> None:
        """
        Append a transformation event to the log.
        Automatically timestamps each entry.
        """
        # Unpack the received payload for richer, more structured logs.
        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "step": step_name,
            **payload,
        }
        self._logs.append(event)

    def _format_log_entry(self, log: Dict[str, Any]) -> str:
        """Generates a human-readable explanation for a single log entry."""
        step_name = log.get("step", "Unknown Step")
        event = log.get("event", "unknown")
        details = log.get("details", {})
        # Get the original transformer name for display, and a lowercase version for logic.
        raw_display_name = log.get("transformer_name", step_name)
        display_transformer_name = str(raw_display_name).split('(')[0]
        logic_transformer_name = display_transformer_name.lower()
        config = log.get("config", {})

        # Handle nested step names (e.g., "ColumnTransformer_step::SubTransformer_step")
        nested_step_match = re.match(r"(.+)::(.+)", step_name)
        if nested_step_match:
            parent_step_name = nested_step_match.group(1)
            sub_step_name = nested_step_match.group(2)
            # For nested steps, the 'transformer_name' in the log IS the sub-transformer's name.
            # Use it to drive the logic for formatting the sub-step's explanation.
            sub_raw_display_name = log.get("transformer_name", sub_step_name)
            sub_display_transformer_name = str(sub_raw_display_name).split('(')[0]
            sub_explanation = self._format_log_entry_for_transformer(
                sub_display_transformer_name, event, details, sub_display_transformer_name, sub_display_transformer_name.lower(), config
            )
            return f"[{parent_step_name}] {sub_explanation}"
        


        
        # For top-level steps, use the dedicated helper
        return self._format_log_entry_for_transformer(
            step_name, event, details, display_transformer_name, logic_transformer_name, config
        )

    def _format_log_entry_for_transformer(self, step_name: str, event: str, details: Dict[str, Any],
                                          display_transformer_name: str, logic_transformer_name: str,
                                          config: Dict[str, Any]) -> str:
        # --- Custom Explanations for Container Transformers ---
        # These are checked first because they have their own event types.

        # ColumnTransformer
        if "columntransformer" in logic_transformer_name:
            # These are events from the ColumnTransformer itself, so we create simpler messages.
            if event == "fit_sub_transformer_start":
                sub_transformer_name = str(details.get("transformer_name", "Unknown")).split('(')[0]
                columns = details.get("columns", [])
                return f"started fitting sub-transformer '{sub_transformer_name}' on {len(columns)} column(s): {columns}."
            if event == "fit_sub_transformer_end":
                sub_transformer_name = str(details.get("transformer_name", "Unknown")).split('(')[0]
                return f"finished fitting sub-transformer '{sub_transformer_name}'."
            if event == "transform_passthrough":
                columns = details.get("columns", [])
                return f"passed through {len(columns)} column(s) unchanged: {columns}."
            if event == "transform_remainder":
                columns = details.get("columns", [])
                return f"passed through {len(columns)} remainder column(s) unchanged: {columns}."
            if event == "fit_skip_transformer":
                sub_transformer_name = str(details.get("transformer_name", "Unknown")).split('(')[0]
                reason = details.get("reason", "No columns selected for transformation.")
                return f"skipped sub-transformer '{sub_transformer_name}': {reason}"
            if event == "transform_sub_transformer_start":
                sub_transformer_name = str(details.get("transformer_name", "Unknown")).split('(')[0]
                columns = details.get("columns", [])
                return f"started transforming with sub-transformer '{sub_transformer_name}' on {len(columns)} column(s): {columns}."

        # --- Custom Explanations for Different Transformers ---

        # MissingValueHandler
        if "missingvaluehandler" in logic_transformer_name:
            if event == "fit":
                fill_values = details.get("fitted_params", {}).get("fill_values", {})
                if fill_values:
                    strategy = config.get("strategy", "unknown")
                    # Create a more descriptive summary of values, e.g., "age: 29.7, embarked: 'S'"
                    value_summary = ", ".join([f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: '{v}'" for k, v in fill_values.items()])
                    return f"Step '{step_name}' (MissingValueHandler) learned imputation values using '{strategy}' for {len(fill_values)} column(s). Values: {value_summary}."
                return f"Step '{step_name}' (MissingValueHandler) fitted, but no missing values were found to handle."
            if event == "transform":
                # This assumes the transform log will include which columns were affected.
                # The current MissingValueHandler does not log this, but we can make the text generic.
                return f"Step '{step_name}' (MissingValueHandler) applied imputation to the data."

        # Encoder
        if "encoder" in logic_transformer_name:
            if event == "fit":
                mappings = details.get("fitted_params", {}).get("mappings", {})
                if mappings:
                    cols = list(mappings.keys())
                    method = config.get("method", "unknown")
                    if method == 'onehot':
                        total_new_cols = sum(len(v) for v in mappings.values())
                        return f"Step '{step_name}' (Encoder) fitted for 'onehot' encoding on {len(cols)} column(s). This will create {total_new_cols} new columns."
                    return f"Step '{step_name}' (Encoder) fitted for '{method}' encoding on {len(cols)} column(s): {cols}."
                return f"Step '{step_name}' (Encoder) fitted, but no categorical columns were found to encode."
            if event == "transform" and config.get("method") == 'onehot':
                new_cols = details.get("new_columns_added", [])
                if new_cols:
                    return f"Step '{step_name}' (Encoder) applied 'onehot' encoding, creating {len(new_cols)} new columns and removing originals."

        # Scaler
        if "scaler" in logic_transformer_name:
            if event == "fit":
                cols = self._get_fitted_columns(details, "columns")
                if cols:
                    method = config.get("method", "unknown")
                    return f"Step '{step_name}' (Scaler) fitted. It will apply '{method}' scaling to {len(cols)} numeric column(s)."
                return f"Step '{step_name}' (Scaler) fitted, but no numeric columns were found to scale."
            if event == "transform":
                cols = details.get("fitted_params", {}).get("columns", [])
                if len(cols) > 0:
                    return f"Step '{step_name}' (Scaler) applied scaling to {len(cols)} column(s): {list(cols)}."

        # FeatureGenerator
        if "featuregenerator" in logic_transformer_name:
            if event == "fit":
                cols = self._get_fitted_columns(details, "columns_to_process")
                strategy = config.get("strategy", "unknown")
                return f"Step '{step_name}' (FeatureGenerator) fitted. It will generate features from {len(cols)} numeric column(s)."
            if event == "transform":
                new_features = details.get("new_features_created", [])
                if new_features:
                    return f"Step '{step_name}' (FeatureGenerator) created {len(new_features)} new features (e.g., '{new_features[0]}', '{new_features[1]}'...). The DataFrame now has {details.get('output_shape', [0,0])[1]} columns."
                return f"Step '{step_name}' (FeatureGenerator) ran but created no new features."

        # OutlierHandler
        if "outlierhandler" in logic_transformer_name:
            if event == "fit":
                bounds = details.get("fitted_params", {}).get("bounds", {})
                if bounds:
                    method = config.get("method", "unknown")
                    # Show an example bound to be more descriptive
                    example_col, (lower, upper) = next(iter(bounds.items()))
                    return f"Step '{step_name}' (OutlierHandler) learned capping bounds using '{method}' for {len(bounds)} column(s). (e.g., '{example_col}' will be capped between {lower:.2f} and {upper:.2f})."
                return f"Step '{step_name}' (OutlierHandler) fitted, but no numeric columns were found to process."
            if event == "transform":
                bounds = details.get("fitted_params", {}).get("bounds", {})
                if bounds:
                    return f"Step '{step_name}' (OutlierHandler) applied capping to {len(bounds)} column(s)."

        # DatetimeFeatureExtractor
        if "datetimefeatureextractor" in logic_transformer_name:
            if event == "fit":
                dt_cols = details.get("fitted_params", {}).get("datetime_columns", [])
                features_to_extract = config.get("features", [])
                if dt_cols:
                    return f"Step '{step_name}' (DatetimeFeatureExtractor) identified {len(dt_cols)} datetime column(s) to process: {dt_cols}. It will extract {len(features_to_extract)} features: {features_to_extract}."
                return f"Step '{step_name}' (DatetimeFeatureExtractor) fitted, but no datetime columns were found to process."
            if event == "transform":
                # This requires the transformer to log more details, but we can make a generic message.
                # A more advanced version would log the new columns created.
                dt_cols = details.get("fitted_params", {}).get("datetime_columns", [])
                return f"Step '{step_name}' (DatetimeFeatureExtractor) extracted features from {len(dt_cols)} column(s) and dropped the originals."


        # Default message if no specific handler matched
        explanation = f"Step '{step_name}' ({display_transformer_name}) completed a '{event}' event."
        if step_name.lower() == logic_transformer_name:
             explanation = f"Step '{step_name}' completed a '{event}' event."
        return explanation

    def _get_fitted_columns(self, details: Dict[str, Any], param_key: str) -> List[str]:
        """Helper to extract fitted column names from a log's details."""
        params = details.get("fitted_params", {})
        values = params.get(param_key, {})
        if isinstance(values, dict):
            return list(values.keys())
        if isinstance(values, (list, pd.Index)):
            return list(values)
        return []

    def summary(self, as_dataframe: bool = False) -> Any:
        """
        Summarize logged transformations in a readable format.

        Parameters
        ----------
        as_dataframe : bool
            If True, return a pandas.DataFrame. Otherwise, return a formatted string.
        """
        if not self._logs:
            return "No transformation logs recorded."

        if as_dataframe:
            return pd.DataFrame(self._logs)

        # Format as readable text
        lines = [
            f"=== Transfory Insight Report ===",
            f"Session started: {self._start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total steps logged: {len(self._logs)}",
            "",
        ]
        for log in self._logs:
            lines.append(f"[{log['timestamp']}] {self._format_log_entry(log)}")
        return "\n".join(lines)

    def clear(self) -> None:
        """Reset all stored logs."""
        self._logs.clear()

    def export(self, filepath: str, format: str = "json") -> None:
        """
        Export logs to a file (JSON or CSV).

        Parameters
        ----------
        filepath : str
            Destination path.
        format : str
            "json" or "csv"
        """
        if not self._logs:
            raise ValueError("No logs to export.")

        if format == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self._logs, f, indent=2)
        elif format == "csv":
            df = pd.DataFrame(self._logs)
            df.to_csv(filepath, index=False)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'csv'.")

    def __repr__(self) -> str:
        return f"<InsightReporter logs={len(self._logs)}>"
