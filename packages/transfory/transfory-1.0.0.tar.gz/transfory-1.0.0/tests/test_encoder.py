import pandas as pd
import pytest
import re

from transfory.encoder import Encoder

@pytest.fixture
def sample_df():
    """Fixture to create a sample DataFrame for testing."""
    return pd.DataFrame({
        'city': ['New York', 'London', 'London', 'Paris'],
        'weather': ['Sunny', 'Cloudy', 'Sunny', 'Cloudy']
    })

@pytest.fixture
def unseen_df():
    """Fixture for a DataFrame with categories not seen during fitting."""
    return pd.DataFrame({
        'city': ['London', 'Dubai'],  # 'Dubai' is unseen
        'weather': ['Rainy', 'Sunny'] # 'Rainy' is unseen
    })

# --- Tests for handle_unseen='ignore' (default behavior) ---

def test_onehot_encoder_ignore_unseen(sample_df, unseen_df):
    """Test that one-hot encoder with 'ignore' creates zero-vectors for unseen categories."""
    encoder = Encoder(method='onehot', handle_unseen='ignore')
    encoder.fit(sample_df)
    transformed = encoder.transform(unseen_df)

    # Expected columns from fitting on sample_df
    expected_cols = ['city_New York', 'city_London', 'city_Paris', 'weather_Sunny', 'weather_Cloudy']
    assert all(col in transformed.columns for col in expected_cols)

    # The 'Dubai' row should have all city columns as 0
    dubai_row = transformed.iloc[1]
    assert dubai_row['city_New York'] == 0
    assert dubai_row['city_London'] == 0
    assert dubai_row['city_Paris'] == 0

    # The 'Rainy' row should have all weather columns as 0
    rainy_row = transformed.iloc[0]
    assert rainy_row['weather_Sunny'] == 0
    assert rainy_row['weather_Cloudy'] == 0

def test_label_encoder_ignore_unseen(sample_df, unseen_df):
    """Test that label encoder with 'ignore' maps unseen categories to -1."""
    encoder = Encoder(method='label', handle_unseen='ignore')
    encoder.fit(sample_df)
    transformed = encoder.transform(unseen_df)

    # The 'Dubai' value in 'city' should be mapped to -1
    assert transformed.loc[1, 'city'] == -1
    # The 'Rainy' value in 'weather' should be mapped to -1
    assert transformed.loc[0, 'weather'] == -1
    # A known value should be mapped correctly
    assert transformed.loc[0, 'city'] != -1

# --- Tests for handle_unseen='error' ---

def test_onehot_encoder_error_unseen(sample_df, unseen_df):
    """Test that one-hot encoder with 'error' raises a ValueError for unseen categories."""
    encoder = Encoder(method='onehot', handle_unseen='error')
    encoder.fit(sample_df)

    with pytest.raises(ValueError, match=re.escape("Unseen categories in column 'city': ['Dubai']")):
        encoder.transform(unseen_df)

def test_label_encoder_error_unseen(sample_df, unseen_df):
    """Test that label encoder with 'error' raises a ValueError for unseen categories."""
    encoder = Encoder(method='label', handle_unseen='error')
    encoder.fit(sample_df)

    with pytest.raises(ValueError, match=re.escape("Unseen categories in column 'city': ['Dubai']")):
        encoder.transform(unseen_df)