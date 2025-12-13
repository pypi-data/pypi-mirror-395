# tests/test_insight.py
import pytest
import pandas as pd
from transfory.base import ExampleScaler
from transfory.pipeline import Pipeline
from transfory.insight import InsightReporter


@pytest.fixture
def sample_dataframe():
    """Provides a simple DataFrame for testing."""
    return pd.DataFrame({
        "age": [20, 30, 40],
        "income": [1000, 2000, 3000]
    })

def test_pipeline_with_insight_reporter(sample_dataframe):
    """Tests that a pipeline correctly logs events to an InsightReporter."""
    # Create an InsightReporter
    reporter = InsightReporter()

    # Build a pipeline and attach the reporter's callback
    pipe = Pipeline(
        [("scale", ExampleScaler())],
        logging_callback=reporter.get_callback()
    )

    # Run the pipeline
    pipe.fit_transform(sample_dataframe)
    summary = reporter.summary()
    assert "ExampleScaler" in summary
    assert "fit" in summary
    assert "transform" in summary
    assert len(reporter._logs) == 4  # Pipeline logs start/end, and the transformer logs fit/transform
