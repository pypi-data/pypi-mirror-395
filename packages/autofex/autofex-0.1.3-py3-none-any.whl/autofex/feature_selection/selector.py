"""
Feature Selection Module

NextGen feature selection with multiple strategies:
- L1 regularization (Lasso)
- Recursive Feature Elimination (RFE)
- Genetic algorithms
- Correlation-based selection
- Variance threshold
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from sklearn.feature_selection import (
    SelectFromModel,
    RFE,
    RFECV,
    VarianceThreshold,
    SelectKBest,
    f_classif,
    f_regression,
    mutual_info_classif,
    mutual_info_regression,
)
from sklearn.linear_model import LassoCV, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import warnings


class FeatureSelector:
    """
    Feature selection with multiple strategies and ensemble methods.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize feature selector.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.strategies = self.config.get(
            "strategies", ["l1", "rfe", "variance", "correlation"]
        )
        self.n_features = self.config.get("n_features", "auto")
        self.cv_folds = self.config.get("cv_folds", 5)
        self.random_state = self.config.get("random_state", 42)

    def select_features_l1(
        self, X: pd.DataFrame, y: pd.Series, alpha: Optional[float] = None
    ) -> List[str]:
        """
        Select features using L1 regularization (Lasso).

        Args:
            X: Features
            y: Target
            alpha: Regularization strength (if None, uses CV)

        Returns:
            List of selected feature names
        """
        is_classification = self._is_classification_target(y)

        if is_classification:
            if alpha is None:
                model = LogisticRegression(
                    penalty="l1",
                    solver="liblinear",
                    random_state=self.random_state,
                    max_iter=1000,
                )
            else:
                model = LogisticRegression(
                    C=1 / alpha,
                    penalty="l1",
                    solver="liblinear",
                    random_state=self.random_state,
                    max_iter=1000,
                )
        else:
            if alpha is None:
                model = LassoCV(cv=self.cv_folds, random_state=self.random_state)
            else:
                from sklearn.linear_model import Lasso

                model = Lasso(alpha=alpha, random_state=self.random_state)

        X_filled = X.fillna(X.mean())
        model.fit(X_filled, y)

        selector = SelectFromModel(model, prefit=True)
        selected_features = X.columns[selector.get_support()].tolist()

        return list(selected_features)  # type: ignore[no-any-return]

    def select_features_rfe(
        self, X: pd.DataFrame, y: pd.Series, n_features: Optional[int] = None
    ) -> List[str]:
        """
        Select features using Recursive Feature Elimination.

        Args:
            X: Features
            y: Target
            n_features: Number of features to select

        Returns:
            List of selected feature names
        """
        is_classification = self._is_classification_target(y)

        if is_classification:
            estimator = RandomForestClassifier(
                n_estimators=50, random_state=self.random_state
            )
        else:
            estimator = RandomForestRegressor(
                n_estimators=50, random_state=self.random_state
            )

        if n_features is None:
            # Use RFECV for automatic selection
            selector = RFECV(
                estimator,
                step=1,
                cv=self.cv_folds,
                scoring="accuracy" if is_classification else "r2",
            )
        else:
            selector = RFE(estimator, n_features_to_select=n_features, step=1)

        X_filled = X.fillna(X.mean())
        selector.fit(X_filled, y)

        selected_features = X.columns[selector.get_support()].tolist()

        return list(selected_features)  # type: ignore[no-any-return]

    def select_features_variance(
        self, X: pd.DataFrame, threshold: float = 0.01
    ) -> List[str]:
        """
        Select features based on variance threshold.

        Args:
            X: Features
            threshold: Variance threshold

        Returns:
            List of selected feature names
        """
        selector = VarianceThreshold(threshold=threshold)
        X_filled = X.fillna(X.mean())
        selector.fit(X_filled)

        selected_features = X.columns[selector.get_support()].tolist()

        return list(selected_features)  # type: ignore[no-any-return]

    def select_features_correlation(
        self, X: pd.DataFrame, y: pd.Series, threshold: float = 0.95
    ) -> List[str]:
        """
        Select features by removing highly correlated ones.

        Args:
            X: Features
            y: Target
            threshold: Correlation threshold

        Returns:
            List of selected feature names
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return list(X.columns.tolist())  # type: ignore[no-any-return]

        corr_matrix = X[numeric_cols].corr().abs()

        # Find highly correlated pairs
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )

        # Remove features with high correlation
        to_remove = [
            column
            for column in upper_triangle.columns
            if any(upper_triangle[column] > threshold)
        ]

        selected_features = [col for col in X.columns if col not in to_remove]

        return list(selected_features)  # type: ignore[no-any-return]

    def select_features_ensemble(
        self, X: pd.DataFrame, y: pd.Series, voting_threshold: float = 0.5
    ) -> List[str]:
        """
        Ensemble feature selection using multiple strategies.

        Args:
            X: Features
            y: Target
            voting_threshold: Minimum votes required for selection

        Returns:
            List of selected feature names
        """
        all_selections: Dict[str, int] = {}

        # Run all strategies
        if "l1" in self.strategies:
            try:
                l1_features = self.select_features_l1(X, y)
                for feat in l1_features:
                    all_selections[feat] = all_selections.get(feat, 0) + 1
            except Exception as e:
                warnings.warn(f"L1 selection failed: {e}")

        if "rfe" in self.strategies:
            try:
                rfe_features = self.select_features_rfe(X, y)
                for feat in rfe_features:
                    all_selections[feat] = all_selections.get(feat, 0) + 1
            except Exception as e:
                warnings.warn(f"RFE selection failed: {e}")

        if "variance" in self.strategies:
            try:
                var_features = self.select_features_variance(X)
                for feat in var_features:
                    all_selections[feat] = all_selections.get(feat, 0) + 1
            except Exception as e:
                warnings.warn(f"Variance selection failed: {e}")

        if "correlation" in self.strategies:
            try:
                corr_features = self.select_features_correlation(X, y)
                for feat in corr_features:
                    all_selections[feat] = all_selections.get(feat, 0) + 1
            except Exception as e:
                warnings.warn(f"Correlation selection failed: {e}")

        # Select features that meet voting threshold
        n_strategies = len(
            [
                s
                for s in self.strategies
                if s in ["l1", "rfe", "variance", "correlation"]
            ]
        )
        min_votes = max(1, int(n_strategies * voting_threshold))

        selected_features = [
            feat for feat, votes in all_selections.items() if votes >= min_votes
        ]

        # If no features selected, return all
        if not selected_features:
            selected_features = X.columns.tolist()

        return list(selected_features)  # type: ignore[no-any-return]

    def _is_classification_target(self, y: pd.Series) -> bool:
        """Determine if target is classification."""
        return y.nunique() < 20 or y.dtype in ["object", "category"]
