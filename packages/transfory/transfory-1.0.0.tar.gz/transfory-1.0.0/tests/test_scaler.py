import pytest
import pandas as pd
import numpy as np
import os

from transfory.scaler import Scaler
from transfory.base import NotFittedError, FrozenTransformerError


@pytest.fixture
def sample_dataframe():
    """Provides a sample DataFrame for testing."""
    return pd.DataFrame({
        'numeric_1': np.array([10, 20, 30, 40, 50]),
        'numeric_2': np.array([-1, 0, 1, 2, 3], dtype=float),
        'category': ['A', 'B', 'A', 'C', 'B'],
        'all_zeros': np.zeros(5)
    })


@pytest.fixture
def new_dataframe():
    """Provides a new DataFrame to test transformation on unseen data."""
    return pd.DataFrame({
        'numeric_1': np.array([15, 25, 55]),
        'numeric_2': np.array([-2, 0.5, 1.5]),
        'category': ['A', 'B', 'C'],
        'all_zeros': np.zeros(3)
    })


def test_scaler_initialization():
    """Tests the initialization of the Scaler."""
    # Test default method
    scaler = Scaler()
    assert scaler.method == "minmax"
    assert "minmax" in scaler.name

    # Test zscore method
    scaler = Scaler(method="zscore")
    assert scaler.method == "zscore"
    assert "zscore" in scaler.name

    # Test invalid method
    with pytest.raises(ValueError, match="is not supported"):
        Scaler(method="invalid_method")


def test_scaler_fit(sample_dataframe):
    """Tests the fit method."""
    scaler = Scaler()
    assert not scaler.is_fitted

    scaler.fit(sample_dataframe)

    assert scaler.is_fitted
    assert "scaler_instance" in scaler.fitted_params
    assert "columns" in scaler.fitted_params
    assert list(scaler.fitted_params["columns"]) == ['numeric_1', 'numeric_2', 'all_zeros']


def test_transform_not_fitted(sample_dataframe):
    """Tests that transform raises an error if not fitted."""
    scaler = Scaler()
    with pytest.raises(NotFittedError):
        scaler.transform(sample_dataframe)


def test_minmax_scaler_transform(sample_dataframe):
    """Tests the min-max scaling transformation."""
    scaler = Scaler(method="minmax")
    transformed_df = scaler.fit_transform(sample_dataframe)

    # Check that numeric columns are scaled between 0 and 1
    assert np.allclose(transformed_df['numeric_1'].min(), 0.0)
    assert np.allclose(transformed_df['numeric_1'].max(), 1.0)
    assert np.allclose(transformed_df['numeric_2'].min(), 0.0)
    assert np.allclose(transformed_df['numeric_2'].max(), 1.0)

    # Check that a column with zero variance is handled correctly (all zeros)
    assert np.allclose(transformed_df['all_zeros'], 0.0)

    # Check that non-numeric column is untouched
    pd.testing.assert_series_equal(sample_dataframe['category'], transformed_df['category'])


def test_zscore_scaler_transform(sample_dataframe):
    """Tests the z-score standardization transformation."""
    scaler = Scaler(method="zscore")
    transformed_df = scaler.fit_transform(sample_dataframe)

    # Check that scaled columns have mean ~0 and std ~1
    assert np.allclose(transformed_df['numeric_1'].mean(), 0.0)
    assert np.allclose(transformed_df['numeric_1'].std(ddof=0), 1.0)
    assert np.allclose(transformed_df['numeric_2'].mean(), 0.0)
    assert np.allclose(transformed_df['numeric_2'].std(ddof=0), 1.0)

    # Check that a column with zero variance is handled correctly (all zeros)
    assert np.allclose(transformed_df['all_zeros'], 0.0)

    # Check that non-numeric column is untouched
    pd.testing.assert_series_equal(sample_dataframe['category'], transformed_df['category'])


def test_scaler_on_new_data(sample_dataframe, new_dataframe):
    """Tests that a fitted scaler can transform new data correctly."""
    scaler = Scaler(method="minmax")
    scaler.fit(sample_dataframe)
    transformed_new_df = scaler.transform(new_dataframe)

    # Test scaling on a value within the original range: (15-10)/(50-10) = 0.125
    assert np.allclose(transformed_new_df['numeric_1'][0], 0.125)

    # Test scaling on a value outside the original range. scikit-learn's MinMaxScaler does not clip by default.
    # The calculation is (55-10)/(50-10) = 45/40 = 1.125
    assert np.allclose(transformed_new_df['numeric_1'][2], 1.125)


def test_scaler_persistence(sample_dataframe, new_dataframe, tmp_path):
    """Tests saving and loading a fitted scaler."""
    filepath = os.path.join(tmp_path, "scaler.joblib")

    # Fit and save the scaler
    scaler_original = Scaler(method="zscore")
    scaler_original.fit(sample_dataframe)
    scaler_original.save(filepath)

    assert os.path.exists(filepath)

    # Load the scaler and transform new data
    scaler_loaded = Scaler.load(filepath)
    assert scaler_loaded.is_fitted
    assert scaler_loaded.method == "zscore"

    # Check that the loaded scaler produces the same result
    transformed_original = scaler_original.transform(new_dataframe)
    transformed_loaded = scaler_loaded.transform(new_dataframe)
    pd.testing.assert_frame_equal(transformed_original, transformed_loaded)


def test_scaler_freezing(sample_dataframe):
    """Tests the freeze functionality from the base class."""
    scaler = Scaler()
    scaler.fit(sample_dataframe)
    scaler.freeze()

    with pytest.raises(FrozenTransformerError):
        scaler.fit(sample_dataframe)

    # Unfreezing should allow fitting again
    scaler.unfreeze()
    scaler.fit(sample_dataframe) # Should not raise an error
    assert scaler.is_fitted