"""
Tests for the data profiling module.
"""

import pytest
import pandas as pd
import numpy as np
from autofex.data_profiling import DataProfiler


class TestDataProfiler:
    """Test suite for DataProfiler."""

    def test_init(self):
        """Test DataProfiler initialization."""
        profiler = DataProfiler()
        assert profiler.config is not None
        # Check default attributes are set
        assert hasattr(profiler, 'missing_threshold')
        assert hasattr(profiler, 'outlier_method')

    def test_analyze_basic(self, sample_data):
        """Test basic data analysis."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)

        # Check report structure
        expected_keys = [
            'overview', 'missing_values', 'data_types', 'distributions',
            'outliers', 'correlations', 'duplicates', 'cardinality', 'target_analysis'
        ]

        for key in expected_keys:
            assert key in report

    def test_overview_stats(self, sample_data):
        """Test overview statistics calculation."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        overview = report['overview']

        assert overview['n_rows'] == len(X)
        assert overview['n_features'] == len(X.columns)
        assert overview['memory_usage'] > 0
        assert overview['target_type'] in ['classification', 'regression']

    def test_missing_values_analysis(self, sample_data_with_missing):
        """Test missing values analysis."""
        X, y = sample_data_with_missing
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        missing = report['missing_values']

        assert 'missing_counts' in missing
        assert 'missing_percentages' in missing
        assert 'total_missing_cells' in missing
        assert missing['total_missing_cells'] > 0

    def test_data_types_analysis(self, sample_data):
        """Test data types analysis."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        dtypes_info = report['data_types']

        assert 'dtypes' in dtypes_info
        assert 'inferred_types' in dtypes_info
        assert len(dtypes_info['dtypes']) == len(X.columns)

    def test_distributions_analysis(self, sample_data):
        """Test distributions analysis."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        distributions = report['distributions']

        assert len(distributions) == len(X.columns)

        # Check numeric feature stats
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col_stats = distributions[numeric_cols[0]]
            assert 'mean' in col_stats
            assert 'std' in col_stats
            assert 'min' in col_stats
            assert 'max' in col_stats

    def test_outliers_detection(self, sample_data):
        """Test outliers detection."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        outliers = report['outliers']

        assert len(outliers) == len(X.columns)

        # Check outlier stats for numeric columns
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col_outliers = outliers[numeric_cols[0]]
            assert 'outlier_count' in col_outliers
            assert 'outlier_percentage' in col_outliers
            assert 'method' in col_outliers

    def test_correlations_analysis(self, sample_data):
        """Test correlations analysis."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        correlations = report['correlations']

        # Should have correlation matrices for numeric data
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            assert 'pearson_correlation' in correlations
            assert 'spearman_correlation' in correlations
        else:
            assert correlations.get('insufficient_numeric_features')

    def test_duplicates_analysis(self, sample_data):
        """Test duplicates analysis."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        duplicates = report['duplicates']

        assert 'duplicate_rows' in duplicates
        assert 'duplicate_columns' in duplicates

    def test_cardinality_analysis(self, sample_data):
        """Test cardinality analysis."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        cardinality = report['cardinality']

        assert len(cardinality) == len(X.columns)

        for col, stats in cardinality.items():
            assert 'unique_values' in stats
            assert 'total_values' in stats
            assert 'uniqueness_ratio' in stats

    def test_target_relationships(self, sample_data):
        """Test target relationship analysis."""
        X, y = sample_data
        profiler = DataProfiler()

        report = profiler.analyze(X, y)
        target_analysis = report['target_analysis']

        assert 'target_type' in target_analysis
        assert 'feature_target_relationships' in target_analysis

    def test_custom_config(self):
        """Test DataProfiler with custom configuration."""
        config = {
            'missing_threshold': 0.2,
            'outlier_method': 'zscore',
            'correlation_threshold': 0.9
        }

        profiler = DataProfiler(config)

        assert profiler.missing_threshold == 0.2
        assert profiler.outlier_method == 'zscore'
        assert profiler.correlation_threshold == 0.9
