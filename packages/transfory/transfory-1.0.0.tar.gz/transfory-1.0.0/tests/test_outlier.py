import pytest
import pandas as pd
import numpy as np

from transfory.outlier import OutlierHandler
from transfory.pipeline import Pipeline
from transfory.insight import InsightReporter

@pytest.fixture
def sample_df_with_outliers():
    """DataFrame with obvious outliers for testing."""
    data = {
        'feature1': [1, 10, 11, 12, 13, 14, 15, 100],  # 100 is an upper outlier
        'feature2': [-50, 8, 9, 10, 11, 12, 13, 14],  # -50 is a lower outlier
        'category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    }
    return pd.DataFrame(data)

def test_outlier_handler_iqr_method(sample_df_with_outliers):
    """Test if the IQR method correctly caps outliers."""
    handler = OutlierHandler(method='iqr', factor=1.5, quantile_interpolation='midpoint')
    transformed_df = handler.fit_transform(sample_df_with_outliers)

    # For 'feature1' with 'midpoint': Q1=10.5, Q3=14.5, IQR=4.0. Upper bound = 14.5 + 1.5*4.0 = 20.5.
    # The value 100 should be capped at 20.5.
    assert transformed_df['feature1'].max() == 20.5

    # For 'feature2' with 'midpoint': Q1=8.5, Q3=12.5, IQR=4.0. Lower bound = 8.5 - 1.5*4.0 = 2.5.
    # The value -50 should be capped at 2.5.
    assert transformed_df['feature2'].min() == 2.5

def test_outlier_handler_percentile_method(sample_df_with_outliers):
    """Test if the percentile method correctly caps outliers."""
    # Use percentiles that will clip the single outlier on each end
    handler = OutlierHandler(method='percentile', lower_quantile=0.15, upper_quantile=0.85)
    transformed_df = handler.fit_transform(sample_df_with_outliers)

    # The max value should be the 85th percentile of the original data
    assert transformed_df['feature1'].max() == sample_df_with_outliers['feature1'].quantile(0.85)
    # The min value should be the 15th percentile of the original data
    assert transformed_df['feature2'].min() == sample_df_with_outliers['feature2'].quantile(0.15)

def test_outlier_handler_invalid_method_raises_error():
    """Test that an invalid method raises a ValueError."""
    with pytest.raises(ValueError, match="Method 'invalid_method' is not supported"):
        OutlierHandler(method='invalid_method')

def test_outlier_handler_in_pipeline_with_reporter(sample_df_with_outliers):
    """Test the OutlierHandler within a Pipeline and check the InsightReporter's output."""
    reporter = InsightReporter()
    pipeline = Pipeline(
        steps=[
            ("handle_outliers", OutlierHandler(method="iqr"))
        ],
        logging_callback=reporter.get_callback()
    )

    pipeline.fit_transform(sample_df_with_outliers)
    report_summary = reporter.summary()

    # Check for the specific, user-friendly text from the InsightReporter
    assert "learned capping bounds using 'iqr' for 2 column(s)" in report_summary
    assert "will be capped between" in report_summary
    assert "applied capping to 2 column(s)" in report_summary