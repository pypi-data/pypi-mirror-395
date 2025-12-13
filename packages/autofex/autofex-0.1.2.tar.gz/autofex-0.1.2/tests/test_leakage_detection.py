"""
Tests for the leakage detection module.
"""

import pytest
import pandas as pd
import numpy as np
from autofex.leakage_detection import LeakageDetector


class TestLeakageDetector:
    """Test suite for LeakageDetector."""

    def test_init(self):
        """Test LeakageDetector initialization."""
        detector = LeakageDetector()
        assert detector.config is not None
        # Check default attributes are set
        assert hasattr(detector, 'leakage_threshold')
        assert hasattr(detector, 'perfect_prediction_threshold')

    def test_detect_basic(self, sample_data):
        """Test basic leakage detection."""
        X, y = sample_data
        detector = LeakageDetector()

        report = detector.detect(X, y)

        # Check report structure
        expected_keys = [
            'target_leakage', 'statistical_anomalies', 'feature_perfection',
            'duplicate_features', 'overall_assessment'
        ]

        for key in expected_keys:
            assert key in report

    def test_target_leakage_detection(self, sample_data):
        """Test target leakage detection."""
        X, y = sample_data
        detector = LeakageDetector()

        report = detector.detect(X, y)
        target_leakage = report['target_leakage']

        assert 'leakage_candidates' in target_leakage
        assert 'threshold' in target_leakage
        assert 'total_candidates' in target_leakage

    def test_perfect_features_detection(self, sample_data):
        """Test perfect feature detection."""
        X, y = sample_data
        detector = LeakageDetector()

        report = detector.detect(X, y)
        perfection = report['feature_perfection']

        assert 'perfect_features' in perfection
        assert 'threshold' in perfection
        assert 'total_perfect_features' in perfection

    def test_duplicate_features_detection(self, sample_data):
        """Test duplicate features detection."""
        X, y = sample_data
        detector = LeakageDetector()

        report = detector.detect(X, y)
        duplicates = report['duplicate_features']

        assert 'duplicate_features' in duplicates
        assert 'total_duplicates' in duplicates

    def test_overall_assessment(self, sample_data):
        """Test overall leakage assessment."""
        X, y = sample_data
        detector = LeakageDetector()

        report = detector.detect(X, y)
        assessment = report['overall_assessment']

        assert 'risk_level' in assessment
        assert 'risk_score' in assessment
        assert 'risk_factors' in assessment
        assert 'recommendations' in assessment

        assert assessment['risk_level'] in ['low', 'medium', 'high']

    def test_train_test_contamination(self, sample_data):
        """Test train-test contamination detection."""
        X, y = sample_data
        # Create artificial test data (subset of training)
        X_test = X.iloc[:20].copy()
        y_test = y.iloc[:20]

        detector = LeakageDetector()
        report = detector.detect(X, y, X_test)

        assert 'train_test_contamination' in report
        contamination = report['train_test_contamination']

        assert 'contamination_indicators' in contamination
        assert 'risk_level' in contamination

    def test_custom_config(self):
        """Test LeakageDetector with custom configuration."""
        config = {
            'leakage_threshold': 0.9,
            'perfect_prediction_threshold': 0.95,
            'cv_folds': 5
        }

        detector = LeakageDetector(config)

        assert detector.leakage_threshold == 0.9
        assert detector.perfect_prediction_threshold == 0.95
        assert detector.cv_folds == 5
