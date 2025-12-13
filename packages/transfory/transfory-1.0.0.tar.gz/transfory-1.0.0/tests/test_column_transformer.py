import pytest
import pandas as pd
import numpy as np

from transfory.column_transformer import ColumnTransformer
from transfory.missing import MissingValueHandler
from transfory.encoder import Encoder
from transfory.scaler import Scaler
from transfory.featuregen import FeatureGenerator
from transfory.insight import InsightReporter
from transfory.pipeline import Pipeline # To test pipelines within ColumnTransformer
from transfory.base import NotFittedError

@pytest.fixture
def sample_df_for_ct():
    """DataFrame for ColumnTransformer testing."""
    return pd.DataFrame({
        'num_col1': [1, 2, 3, 4, np.nan],
        'num_col2': [10, 20, np.nan, 40, 50],
        'cat_col1': ['A', 'B', 'A', 'C', 'B'],
        'cat_col2': ['X', 'Y', 'X', 'Z', None],
        'id_col': [101, 102, 103, 104, 105]
    })

def test_column_transformer_initialization():
    """Test basic initialization and validation."""
    with pytest.raises(ValueError, match="`transformers` must be a list of"):
        ColumnTransformer(transformers="not_a_list")
    
    with pytest.raises(ValueError, match="`remainder` must be 'drop' or 'passthrough'"):
        ColumnTransformer(transformers=[], remainder="invalid")

    ct = ColumnTransformer(transformers=[
        ("num_imputer", MissingValueHandler(strategy="mean"), ['num_col1']),
        ("cat_encoder", Encoder(method="onehot"), ['cat_col1'])
    ])
    assert len(ct.transformers) == 2
    assert ct.remainder == 'drop'
    assert ct.name == "ColumnTransformer"

def test_column_transformer_fit_transform_drop_remainder(sample_df_for_ct):
    """Test fit_transform with 'drop' remainder."""
    ct = ColumnTransformer(
        transformers=[
            ("num_imputer", MissingValueHandler(strategy="mean"), ['num_col1', 'num_col2']),
            ("cat_encoder", Encoder(method="onehot"), ['cat_col1'])
        ],
        remainder='drop'
    )
    transformed_df = ct.fit_transform(sample_df_for_ct)

    # Check for expected columns
    assert 'num_col1' in transformed_df.columns
    assert 'num_col2' in transformed_df.columns
    assert 'cat_col1_A' in transformed_df.columns
    assert 'cat_col1_B' in transformed_df.columns
    assert 'cat_col1_C' in transformed_df.columns
    
    # Original categorical and id_col should be dropped
    assert 'cat_col1' not in transformed_df.columns
    assert 'cat_col2' not in transformed_df.columns
    assert 'id_col' not in transformed_df.columns

    # Check for no NaNs in transformed numeric columns
    assert not transformed_df[['num_col1', 'num_col2']].isnull().any().any()
    
    # Check shape (2 numeric + 3 one-hot encoded)
    assert transformed_df.shape[1] == 2 + 3

def test_column_transformer_fit_transform_passthrough_remainder(sample_df_for_ct):
    """Test fit_transform with 'passthrough' remainder."""
    ct = ColumnTransformer(
        transformers=[
            ("num_imputer", MissingValueHandler(strategy="mean"), ['num_col1']),
            ("cat_encoder", Encoder(method="onehot"), ['cat_col1'])
        ],
        remainder='passthrough'
    )
    transformed_df = ct.fit_transform(sample_df_for_ct)

    # Check for expected columns
    assert 'num_col1' in transformed_df.columns
    assert 'cat_col1_A' in transformed_df.columns
    
    # Remainder columns should be present
    assert 'num_col2' in transformed_df.columns # Not explicitly handled, so passed through
    assert 'cat_col2' in transformed_df.columns # Not explicitly handled, so passed through
    assert 'id_col' in transformed_df.columns   # Not explicitly handled, so passed through

    # Check shape (1 numeric + 3 one-hot encoded + 3 remainder)
    assert transformed_df.shape[1] == 1 + 3 + 3

def test_column_transformer_with_numeric_selector(sample_df_for_ct):
    """Test column selection using 'numeric' string."""
    ct = ColumnTransformer(
        transformers=[
            ("num_scaler", Scaler(method="zscore"), 'numeric')
        ],
        remainder='drop'
    )
    transformed_df = ct.fit_transform(sample_df_for_ct)
    
    # Should have scaled num_col1, num_col2, and id_col (all are numeric)
    assert 'num_col1' in transformed_df.columns
    assert 'num_col2' in transformed_df.columns
    assert 'id_col' in transformed_df.columns
    assert 'cat_col1' not in transformed_df.columns # Categorical columns dropped

    # Check scaling (mean close to 0, std close to 1)
    assert np.isclose(transformed_df['num_col1'].mean(), 0, atol=1e-9)
    assert np.isclose(transformed_df['num_col1'].std(ddof=0), 1, atol=1e-9)

def test_column_transformer_with_categorical_selector(sample_df_for_ct):
    """Test column selection using 'categorical' string."""
    ct = ColumnTransformer(
        transformers=[
            ("cat_encoder", Encoder(method="onehot"), 'categorical')
        ],
        remainder='drop'
    )
    transformed_df = ct.fit_transform(sample_df_for_ct)
    
    # Should have encoded cat_col1 and cat_col2
    assert 'cat_col1_A' in transformed_df.columns
    assert 'cat_col2_X' in transformed_df.columns
    assert 'num_col1' not in transformed_df.columns # Numeric columns dropped

def test_column_transformer_with_pipeline_as_transformer(sample_df_for_ct):
    """Test using a Pipeline as a sub-transformer."""
    num_pipeline = Pipeline([
        ("impute", MissingValueHandler(strategy="mean")),
        ("scale", Scaler(method="zscore"))
    ])
    ct = ColumnTransformer(
        transformers=[
            ("num_pipe", num_pipeline, ['num_col1', 'num_col2'])
        ],
        remainder='drop'
    )
    transformed_df = ct.fit_transform(sample_df_for_ct)
    
    assert 'num_col1' in transformed_df.columns
    assert 'num_col2' in transformed_df.columns
    assert not transformed_df[['num_col1', 'num_col2']].isnull().any().any()
    assert np.isclose(transformed_df['num_col1'].mean(), 0, atol=1e-9)

def test_column_transformer_with_explicit_passthrough(sample_df_for_ct):
    """Test explicit 'passthrough' transformer."""
    ct = ColumnTransformer(
        transformers=[
            ("num_imputer", MissingValueHandler(strategy="mean"), ['num_col1']),
            ("pass_id", "passthrough", ['id_col']) # Explicit passthrough
        ],
        remainder='drop' # Remainder 'num_col2', 'cat_col1', 'cat_col2' should be dropped
    )
    transformed_df = ct.fit_transform(sample_df_for_ct)

    assert 'num_col1' in transformed_df.columns
    assert 'id_col' in transformed_df.columns
    assert 'num_col2' not in transformed_df.columns
    assert 'cat_col1' not in transformed_df.columns
    assert 'cat_col2' not in transformed_df.columns
    pd.testing.assert_series_equal(sample_df_for_ct['id_col'], transformed_df['id_col'])

def test_column_transformer_not_fitted_error(sample_df_for_ct):
    """Test that transform raises NotFittedError if not fitted."""
    ct = ColumnTransformer(transformers=[
        ("num_imputer", MissingValueHandler(strategy="mean"), ['num_col1'])
    ])
    with pytest.raises(NotFittedError):
        ct.transform(sample_df_for_ct)

def test_column_transformer_with_insight_reporter(sample_df_for_ct):
    """Test ColumnTransformer logging with InsightReporter."""
    reporter = InsightReporter()
    ct = ColumnTransformer(
        transformers=[
            ("num_imputer", MissingValueHandler(strategy="mean"), ['num_col1']),
            ("cat_encoder", Encoder(method="onehot"), ['cat_col1']),
            ("pass_id", "passthrough", ['id_col'])
        ],
        remainder='passthrough',
        logging_callback=reporter.get_callback()
    )
    ct.fit_transform(sample_df_for_ct)
    report_summary = reporter.summary()

    # Check for overall ColumnTransformer events
    assert "ColumnTransformer" in report_summary
    
    # Check for sub-transformer events
    assert "[num_imputer] Step 'MissingValueHandler' (MissingValueHandler) learned imputation values using 'mean' for 1 column(s). Values: num_col1: 2.50." in report_summary
    assert "[cat_encoder] Step 'Encoder' (Encoder) fitted for 'onehot' encoding on 1 column(s). This will create 3 new columns." in report_summary
    
    # Check for specific messages
    assert "started fitting sub-transformer 'MissingValueHandler' on 1 column(s): ['num_col1']" in report_summary
    assert "finished fitting sub-transformer 'MissingValueHandler'" in report_summary
    assert "started transforming with sub-transformer 'Encoder' on 1 column(s): ['cat_col1']" in report_summary
    assert "applied 'onehot' encoding, creating 3 new columns and removing originals." in report_summary # From Encoder's own log
    assert "passed through 1 column(s) unchanged: ['id_col']" in report_summary # Explicit passthrough
    assert "passed through 2 remainder column(s) unchanged: ['num_col2', 'cat_col2']" in report_summary # Remainder passthrough

def test_column_transformer_empty_columns_for_transformer(sample_df_for_ct):
    """Test that a transformer is skipped if its column selector yields no columns."""
    reporter = InsightReporter()
    ct = ColumnTransformer(
        transformers=[
            ("non_existent_col_imputer", MissingValueHandler(strategy="mean"), ['non_existent_col']),
            ("cat_encoder", Encoder(method="onehot"), ['cat_col1'])
        ],
        logging_callback=reporter.get_callback()
    )
    transformed_df = ct.fit_transform(sample_df_for_ct)
    report_summary = reporter.summary()

    assert "skipped sub-transformer 'MissingValueHandler': No columns selected for transformation." in report_summary
    assert 'cat_col1_A' in transformed_df.columns
    assert 'num_col1' not in transformed_df.columns # Dropped by default remainder='drop'
    assert 'non_existent_col' not in transformed_df.columns # Should not be created