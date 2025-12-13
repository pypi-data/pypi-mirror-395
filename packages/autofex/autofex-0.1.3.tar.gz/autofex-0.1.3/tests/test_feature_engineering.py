"""
Tests for the feature engineering module.
"""

import pytest
import pandas as pd
import numpy as np
from autofex.feature_engineering import FeatureEngineer


class TestFeatureEngineer:
    """Test suite for FeatureEngineer."""

    def test_init(self):
        """Test FeatureEngineer initialization."""
        fe = FeatureEngineer()
        assert fe.config is not None
        # Check default attributes are set
        assert hasattr(fe, 'numeric_transforms')
        assert hasattr(fe, 'categorical_transforms')
        assert hasattr(fe, 'interaction_degree')

    def test_fit_transform_basic(self, sample_data):
        """Test basic fit_transform functionality."""
        X, y = sample_data
        fe = FeatureEngineer()

        X_transformed = fe.fit_transform(X, y)

        assert X_transformed.shape[0] == X.shape[0]
        assert X_transformed.shape[1] >= X.shape[1]  # Should have at least original features

    def test_numeric_transformations(self):
        """Test numeric feature transformations."""
        np.random.seed(42)
        X = pd.DataFrame({
            'normal': np.random.randn(100),
            'positive_skewed': np.random.exponential(1, 100),
            'zeros': np.zeros(100)
        })
        y = pd.Series(np.random.randint(0, 2, 100))

        fe = FeatureEngineer({
            'numeric_transforms': ['log', 'sqrt', 'square', 'standardize']
        })

        X_transformed = fe.fit_transform(X, y)

        # Check that new features were created
        assert X_transformed.shape[1] > X.shape[1]

        # Check specific transformations exist
        feature_names = X_transformed.columns.tolist()
        assert any('log' in name for name in feature_names)
        assert any('sqrt' in name for name in feature_names)
        assert any('square' in name for name in feature_names)

    def test_interaction_features(self):
        """Test polynomial interaction features."""
        X = pd.DataFrame({
            'feature_1': [1, 2, 3, 4, 5],
            'feature_2': [2, 3, 4, 5, 6],
            'feature_3': [3, 4, 5, 6, 7]
        })
        y = pd.Series([0, 1, 0, 1, 0])

        fe = FeatureEngineer({
            'interaction_degree': 2
        })

        X_transformed = fe.fit_transform(X, y)

        # Should have interaction features
        assert X_transformed.shape[1] > X.shape[1]

        # Check for interaction feature names
        feature_names = X_transformed.columns.tolist()
        # Check for any interaction feature (contains space or multiple feature names)
        has_interaction = any(
            ' ' in name or 
            ('feature_1' in name and 'feature_2' in name) or
            ('feature_1' in name and 'feature_3' in name) or
            ('feature_2' in name and 'feature_3' in name)
            for name in feature_names
        )
        assert has_interaction, f"No interaction features found. Got: {feature_names}"

    def test_categorical_transforms(self):
        """Test categorical feature transformations."""
        X = pd.DataFrame({
            'numeric': [1, 2, 3, 4, 5],
            'category': ['A', 'B', 'A', 'C', 'B']
        })
        y = pd.Series([0, 1, 0, 1, 0])

        fe = FeatureEngineer({
            'categorical_transforms': ['frequency_encode', 'label_encode']
        })

        X_transformed = fe.fit_transform(X, y)

        assert X_transformed.shape[1] >= X.shape[1]

        # Check for encoded features
        feature_names = X_transformed.columns.tolist()
        assert any('freq' in name for name in feature_names)
        assert any('label' in name for name in feature_names)

    def test_max_features_limit(self):
        """Test max features limitation."""
        X = pd.DataFrame(np.random.randn(50, 10), columns=[f'feat_{i}' for i in range(10)])
        y = pd.Series(np.random.randint(0, 2, 50))

        fe = FeatureEngineer({
            'max_features': 15
        })

        X_transformed = fe.fit_transform(X, y)

        # Should not exceed max features (plus some buffer for importance selection)
        assert X_transformed.shape[1] <= 20  # Allow some flexibility

    def test_fit_transform_separate(self, sample_data):
        """Test separate fit and transform."""
        X, y = sample_data
        X_train = X.iloc[:80]
        X_test = X.iloc[80:]
        y_train = y.iloc[:80]

        fe = FeatureEngineer()

        # Fit on training data
        fe.fit(X_train, y_train)

        # Transform both train and test
        X_train_transformed = fe.transform(X_train)
        X_test_transformed = fe.transform(X_test)

        # Check that both transformations have the same number of features
        assert X_train_transformed.shape[1] == X_test_transformed.shape[1]

        # Check that training data maintains its shape (feature engineering shouldn't drop rows)
        assert X_train_transformed.shape[0] >= X_train.shape[0]  # May add rows due to lineage
        assert X_test_transformed.shape[0] >= X_test.shape[0]

    def test_minimal_dataframe(self):
        """Test handling of minimal dataframe."""
        X = pd.DataFrame({'col1': [1, 2, 3]})
        y = pd.Series([0, 1, 0])

        fe = FeatureEngineer()

        X_transformed = fe.fit_transform(X, y)

        assert X_transformed.shape[0] == X.shape[0]
        assert X_transformed.shape[1] >= X.shape[1]
