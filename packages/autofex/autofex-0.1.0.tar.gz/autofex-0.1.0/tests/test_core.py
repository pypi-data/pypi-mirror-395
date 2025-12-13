"""
Tests for the core AutoFEX class.
"""

import pytest
import pandas as pd
import numpy as np
from autofex import AutoFEX


class TestAutoFEX:
    """Test suite for AutoFEX main class."""

    def test_init(self):
        """Test AutoFEX initialization."""
        afx = AutoFEX()
        assert afx.feature_engineer is not None
        assert afx.data_profiler is not None
        assert afx.leakage_detector is not None
        assert afx.benchmarker is not None
        assert afx.lineage_tracker is not None

    def test_process_basic(self, sample_data):
        """Test basic AutoFEX pipeline processing."""
        X, y = sample_data
        afx = AutoFEX(enable_cache=False)

        result = afx.process(X, y)

        # Check result structure
        assert hasattr(result, 'original_data')
        assert hasattr(result, 'engineered_features')
        assert hasattr(result, 'data_quality_report')
        assert hasattr(result, 'leakage_report')
        assert hasattr(result, 'benchmark_results')
        assert hasattr(result, 'feature_lineage')
        assert hasattr(result, 'processing_time')

        # Check that features were engineered
        assert result.engineered_features.shape[0] == X.shape[0]
        assert result.engineered_features.shape[1] >= X.shape[1]

        # Check processing time is reasonable
        assert result.processing_time > 0
        assert result.processing_time < 60  # Should complete within 1 minute

    def test_process_without_target(self, sample_data):
        """Test AutoFEX pipeline without target variable."""
        X, y = sample_data
        afx = AutoFEX(enable_cache=False)

        # Process without target (unsupervised)
        result = afx.process(X)

        assert result.engineered_features.shape[0] == X.shape[0]
        assert result.engineered_features.shape[1] >= X.shape[1]
        # Leakage and benchmark results might be empty without target
        assert isinstance(result.leakage_report, dict)
        assert isinstance(result.benchmark_results, dict)

    def test_process_with_test_data(self, sample_data):
        """Test AutoFEX pipeline with separate test data."""
        X, y = sample_data
        # Split into train/test
        X_train = X.iloc[:80]
        X_test = X.iloc[80:]
        y_train = y.iloc[:80]
        y_test = y.iloc[80:]

        afx = AutoFEX(enable_cache=False)
        result = afx.process(X_train, y_train, X_test)

        assert result.original_data.shape == X_train.shape
        assert result.engineered_features.shape[0] == X_train.shape[0]

    def test_suggest_feature_transformations(self, sample_data):
        """Test feature transformation suggestions."""
        X, y = sample_data
        afx = AutoFEX()

        suggestions = afx.suggest_feature_transformations(X, y)

        assert isinstance(suggestions, list)
        if len(suggestions) > 0:
            suggestion = suggestions[0]
            assert 'column' in suggestion
            assert 'transformation' in suggestion
            assert 'reason' in suggestion
            assert 'expected_impact' in suggestion

    def test_custom_config(self):
        """Test AutoFEX with custom configuration."""
        config = {
            'feature_engineering_config': {'max_features': 50},
            'profiling_config': {'missing_threshold': 0.3},
            'leakage_config': {'leakage_threshold': 0.8},
            'benchmarking_config': {'cv_folds': 3},
            'lineage_config': {}
        }

        afx = AutoFEX(**config)
        assert afx.feature_engineer.config.get('max_features') == 50
