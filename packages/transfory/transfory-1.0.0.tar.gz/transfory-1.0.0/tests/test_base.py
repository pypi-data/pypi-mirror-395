# tests/test_base.py
import pytest
import pandas as pd
from transfory.base import ExampleScaler


@pytest.fixture
def sample_dataframe():
    """Provides a simple DataFrame for testing."""
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 6]
    })
    return df

def test_example_scaler(sample_dataframe):
    scaler = ExampleScaler()
    result = scaler.fit_transform(sample_dataframe)
    assert isinstance(result, pd.DataFrame)
    assert not result.equals(sample_dataframe), "fit_transform should modify the DataFrame."