import pytest
import pandas as pd
import os

from transfory.base import ExampleScaler
from transfory.pipeline import Pipeline
from transfory.insight import InsightReporter
from transfory.base import NotFittedError, FrozenTransformerError

@pytest.fixture
def sample_dataframe():
    """Provides a simple DataFrame for pipeline tests."""
    return pd.DataFrame({"A": [1.0, 2.0, 3.0], "B": [10.0, 20.0, 30.0]})


def test_pipeline_basic(sample_dataframe):
    """Basic pipeline test with a single ExampleScaler."""
    pipe = Pipeline([
        ("scaler", ExampleScaler())
    ])

    # Fit and transform
    pipe.fit(sample_dataframe)
    df_out = pipe.transform(sample_dataframe)

    assert not df_out.equals(sample_dataframe), "Pipeline output should differ from input after scaling."
    assert pipe.is_fitted, "Pipeline should be marked as fitted."


def test_pipeline_multiple_steps(sample_dataframe):
    """Test pipeline with multiple ExampleScaler steps."""
    pipe = Pipeline([
        ("scaler1", ExampleScaler()),
        ("scaler2", ExampleScaler())
    ])

    df_out = pipe.fit_transform(sample_dataframe)
    assert isinstance(df_out, pd.DataFrame), "Output should be a DataFrame."
    assert len(pipe.steps) == 2


def test_pipeline_add_remove_steps(sample_dataframe):
    """Ensure add_step and remove_step methods work."""
    pipe = Pipeline([
        ("scaler", ExampleScaler())
    ])

    # Add step
    pipe.add_step("scaler2", ExampleScaler())
    assert len(pipe.steps) == 2 and pipe.steps[1][0] == "scaler2"

    # Remove step
    pipe.remove_step("scaler")
    assert len(pipe.steps) == 1 and pipe.steps[0][0] == "scaler2"


def test_pipeline_repr():
    """Check string representation."""
    pipe = Pipeline([
        ("scaler", ExampleScaler())
    ])
    rep = repr(pipe)
    assert "Pipeline" in rep and "scaler" in rep


def test_pipeline_not_fitted_error(sample_dataframe):
    """Tests that transform raises an error if the pipeline is not fitted."""
    pipe = Pipeline([("scaler", ExampleScaler())])
    with pytest.raises(NotFittedError):
        pipe.transform(sample_dataframe)


def test_pipeline_freezing(sample_dataframe):
    """Tests the freeze/unfreeze functionality for the pipeline."""
    pipe = Pipeline([("scaler", ExampleScaler())])
    pipe.fit(sample_dataframe)
    pipe.freeze()

    with pytest.raises(FrozenTransformerError):
        pipe.fit(sample_dataframe)

    # Unfreezing should allow fitting again
    pipe.unfreeze()
    pipe.fit(sample_dataframe)  # Should not raise an error
    assert pipe.is_fitted


def test_pipeline_persistence(sample_dataframe, tmp_path):
    """Tests saving and loading a fitted pipeline."""
    filepath = os.path.join(tmp_path, "pipeline.joblib")

    # Fit and save the pipeline
    pipe_original = Pipeline([("scaler1", ExampleScaler()), ("scaler2", ExampleScaler())])
    pipe_original.fit(sample_dataframe)
    pipe_original.save(filepath)

    assert os.path.exists(filepath)

    # Load the pipeline and check its state
    pipe_loaded = Pipeline.load(filepath)
    assert pipe_loaded.is_fitted
    assert len(pipe_loaded.steps) == 2
    assert pipe_loaded.steps[0][0] == "scaler1"

    # Ensure the loaded pipeline produces the same result
    transformed_original = pipe_original.transform(sample_dataframe)
    transformed_loaded = pipe_loaded.transform(sample_dataframe)
    pd.testing.assert_frame_equal(transformed_original, transformed_loaded)


def test_pipeline_with_insight_reporter(sample_dataframe):
    """Tests that a pipeline correctly logs events to an InsightReporter."""
    reporter = InsightReporter()
    pipe = Pipeline([("scaler", ExampleScaler())], logging_callback=reporter.get_callback())
    pipe.fit_transform(sample_dataframe)

    # The pipeline itself logs fit_start/end and transform_step/done for each step
    assert len(reporter._logs) > 0
    assert "Pipeline" in reporter.summary()
