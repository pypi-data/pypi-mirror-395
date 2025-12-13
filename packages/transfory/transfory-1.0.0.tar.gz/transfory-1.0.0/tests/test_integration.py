import pytest
import pandas as pd
import numpy as np

from transfory.missing import MissingValueHandler
from transfory.encoder import Encoder
from transfory.featuregen import FeatureGenerator
from transfory.scaler import Scaler
from transfory.pipeline import Pipeline
from transfory.insight import InsightReporter


@pytest.fixture
def raw_dataframe():
    """Provides a raw, messy DataFrame for integration testing."""
    return pd.DataFrame({
        "age": [20, 25, 30, np.nan, 22],
        "income": [50000, 60000, np.nan, 55000, 52000],
        "city": ["Manila", "Cebu", "Manila", "Davao", None],
        "gender": ["M", "F", "F", None, "M"]
    })


def test_full_pipeline_integration(raw_dataframe):
    """
    Tests a full data transformation pipeline from start to finish,
    verifying the interaction between different transformers.
    """
    # Create an InsightReporter to capture events
    reporter = InsightReporter()

    # 1. Define the full pipeline
    pipeline = Pipeline([
        ("imputer", MissingValueHandler(strategy="mean")),
        ("encoder", Encoder(method="onehot")),
        ("feature_generator", FeatureGenerator(degree=2, include_interactions=True)),
        ("scaler", Scaler(method="zscore"))
    ], logging_callback=reporter.get_callback())

    # 2. Fit and transform the data
    transformed_df = pipeline.fit_transform(raw_dataframe)

    # 3. Assertions to verify the outcome
    assert isinstance(transformed_df, pd.DataFrame), "Output should be a DataFrame."
    assert not transformed_df.isnull().values.any(), "There should be no missing values after the pipeline."

    # Check for one-hot encoded columns
    assert "city_Manila" in transformed_df.columns
    assert "gender_M" in transformed_df.columns

    # Check for generated features
    assert "age^2" in transformed_df.columns
    assert "age_x_income" in transformed_df.columns

    # Check that numeric columns are scaled (mean ~0)
    assert np.allclose(transformed_df["age"].mean(), 0), "Scaled 'age' column should have a mean close to 0."

    # 4. Assert that the InsightReporter captured the events
    summary = reporter.summary()
    assert "imputer" in summary
    assert "encoder" in summary
    assert "feature_generator" in summary
    assert "scaler" in summary
    assert len(reporter._logs) > 0, "InsightReporter should have logged pipeline events."