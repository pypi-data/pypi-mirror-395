import pytest
import pandas as pd
import json
import os
from datetime import datetime

from transfory.insight import InsightReporter
from transfory.base import ExampleScaler  # Using a simple transformer for testing callbacks


@pytest.fixture
def reporter():
    """Provides a clean InsightReporter instance for each test."""
    return InsightReporter()


@pytest.fixture
def sample_payload():
    """Provides a sample event payload for logging."""
    return {
        "event": "fit",
        "details": {"input_shape": (10, 3), "params_set": ["A", "B"]}
    }


@pytest.fixture
def sample_dataframe():
    """Provides a simple DataFrame for transformers to use."""
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})


def test_reporter_initialization(reporter):
    """Tests that the reporter initializes in a clean, empty state."""
    assert isinstance(reporter._logs, list)
    assert len(reporter._logs) == 0
    assert isinstance(reporter._start_time, datetime)
    assert "No transformation logs recorded" in reporter.summary()


def test_reporter_log_event(reporter, sample_payload):
    """Tests the direct logging of a single event."""
    reporter.log_event("test_step", sample_payload)

    assert len(reporter._logs) == 1
    log_entry = reporter._logs[0]

    assert "timestamp" in log_entry
    assert log_entry["step"] == "test_step"
    assert log_entry["event"] == "fit"
    assert log_entry["details"] == {"input_shape": (10, 3), "params_set": ["A", "B"]}


def test_reporter_get_callback_and_integration(reporter, sample_dataframe):
    """
    Tests that the callback mechanism correctly logs events from a transformer.
    """
    # Create a transformer and pass the reporter's callback to it
    scaler = ExampleScaler(logging_callback=reporter.get_callback())
    scaler.fit(sample_dataframe)

    assert len(reporter._logs) == 1
    log_entry = reporter._logs[0]

    assert log_entry["step"] == "ExampleScaler"
    assert log_entry["event"] == "fit"
    assert log_entry["details"]["input_shape"] == (3, 2)
    assert "fitted_params" in log_entry["details"]


def test_reporter_summary_output(reporter, sample_payload):
    """Tests the different output formats of the summary method."""
    reporter.log_event("step1", sample_payload)

    # Test string summary
    summary_str = reporter.summary()
    assert isinstance(summary_str, str)
    assert "Transfory Insight Report" in summary_str
    assert "Step 'step1'" in summary_str
    assert "completed a 'fit' event" in summary_str

    # Test DataFrame summary
    summary_df = reporter.summary(as_dataframe=True)
    assert isinstance(summary_df, pd.DataFrame)
    assert len(summary_df) == 1
    assert "step" in summary_df.columns
    assert summary_df.iloc[0]["step"] == "step1"


def test_reporter_clear(reporter, sample_payload):
    """Tests that the clear method resets the logs."""
    reporter.log_event("step1", sample_payload)
    assert len(reporter._logs) == 1

    reporter.clear()
    assert len(reporter._logs) == 0
    assert "No transformation logs recorded" in reporter.summary()


def test_reporter_export(reporter, sample_payload, tmp_path):
    """Tests exporting logs to JSON and CSV formats."""
    reporter.log_event("step1", sample_payload)
    reporter.log_event("step2", {"event": "transform", "details": {"shape": (10, 2)}})

    # Test JSON export
    json_path = os.path.join(tmp_path, "report.json")
    reporter.export(json_path, format="json")
    assert os.path.exists(json_path)
    with open(json_path, "r") as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]["step"] == "step1"

    # Test CSV export
    csv_path = os.path.join(tmp_path, "report.csv")
    reporter.export(csv_path, format="csv")
    assert os.path.exists(csv_path)
    df = pd.read_csv(csv_path)
    assert len(df) == 2
    assert df.iloc[1]["step"] == "step2"


def test_reporter_export_errors(reporter, tmp_path):
    """Tests error handling for the export method."""
    # Test exporting with no logs
    with pytest.raises(ValueError, match="No logs to export"):
        reporter.export(os.path.join(tmp_path, "report.json"))

    # Add a log
    reporter.log_event("step1", {})

    # Test unsupported format
    with pytest.raises(ValueError, match="Unsupported format"):
        reporter.export(os.path.join(tmp_path, "report.txt"), format="txt")


def test_reporter_repr(reporter, sample_payload):
    """Tests the __repr__ method for a concise representation."""
    assert repr(reporter) == "<InsightReporter logs=0>"

    reporter.log_event("step1", sample_payload)
    assert repr(reporter) == "<InsightReporter logs=1>"


def test_callback_is_robust_to_errors(sample_dataframe):
    """Ensures a faulty callback does not crash the transformer."""
    def faulty_callback(step_name, payload):
        raise ValueError("This callback is broken!")

    scaler = ExampleScaler(logging_callback=faulty_callback)

    # The fit method should complete successfully without raising an error,
    # as the BaseTransformer is designed to suppress logging exceptions.
    try:
        scaler.fit(sample_dataframe)
    except Exception as e:
        pytest.fail(f"Transformer should not fail due to a bad callback. Raised: {e}")

    assert scaler.is_fitted, "Transformer should still be fitted even if logging fails."