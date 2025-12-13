import pytest
import pandas as pd
from transfory.datetime import DatetimeFeatureExtractor
from transfory.pipeline import Pipeline
from transfory.insight import InsightReporter

# Mark all tests in this file to ignore the specific UserWarning from pandas
pytestmark = pytest.mark.filterwarnings("ignore:Could not infer format:UserWarning")

@pytest.fixture
def sample_df_with_dates():
    """DataFrame with a datetime column and other data types."""
    data = {
        'event_date': ['2023-01-15 10:30:00', '2024-07-22 20:00:00', None],
        'value': [100, 200, 300],
        'category': ['A', 'B', 'A']
    }
    return pd.DataFrame(data)

def test_datetime_extractor_defaults(sample_df_with_dates):
    """Test default feature extraction ('year', 'month', 'day', 'dayofweek')."""
    extractor = DatetimeFeatureExtractor()
    transformed_df = extractor.fit_transform(sample_df_with_dates)

    # Check if original column is dropped and new ones are created
    assert 'event_date' not in transformed_df.columns
    expected_new_cols = ['event_date_year', 'event_date_month', 'event_date_day', 'event_date_dayofweek']
    assert all(col in transformed_df.columns for col in expected_new_cols)

    # Check values for the first row
    assert transformed_df.loc[0, 'event_date_year'] == 2023
    assert transformed_df.loc[0, 'event_date_month'] == 1
    assert transformed_df.loc[0, 'event_date_day'] == 15
    assert transformed_df.loc[0, 'event_date_dayofweek'] == 6  # Sunday

def test_datetime_extractor_custom_features(sample_df_with_dates):
    """Test extraction of a custom list of features."""
    custom_features = ['hour', 'minute', 'week']
    extractor = DatetimeFeatureExtractor(features=custom_features)
    transformed_df = extractor.fit_transform(sample_df_with_dates)

    assert all(f'event_date_{feat}' in transformed_df.columns for feat in custom_features)
    assert transformed_df.loc[0, 'event_date_hour'] == 10
    assert transformed_df.loc[1, 'event_date_minute'] == 0

def test_datetime_in_pipeline_with_reporter(sample_df_with_dates):
    """Test the extractor in a pipeline and check the reporter's output."""
    reporter = InsightReporter()
    pipeline = Pipeline(steps=[("extract_dates", DatetimeFeatureExtractor())], logging_callback=reporter.get_callback())
    pipeline.fit_transform(sample_df_with_dates)
    report_summary = reporter.summary()

    assert "identified 1 datetime column(s) to process: ['event_date']" in report_summary
    assert "extracted features from 1 column(s)" in report_summary