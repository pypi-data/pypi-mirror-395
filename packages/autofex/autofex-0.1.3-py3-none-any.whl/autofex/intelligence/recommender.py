"""
Intelligent Feature Engineering Recommender

Automatically recommends feature engineering strategies based on data analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
import warnings


class FeatureEngineeringRecommender:
    """
    Intelligent recommender for feature engineering strategies.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize feature engineering recommender.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

    def recommend_transformations(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> List[Dict[str, Any]]:
        """
        Recommend feature transformations based on data characteristics.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            List of transformation recommendations
        """
        recommendations = []

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            series = X[col].dropna()

            if len(series) < 3:
                continue

            col_recommendations = []

            # Skewness-based recommendations
            skew = series.skew()
            if abs(skew) > 2:
                col_recommendations.append(
                    {
                        "column": col,
                        "transformation": (
                            "boxcox" if series.min() > 0 else "yeojohnson"
                        ),
                        "reason": f"Highly skewed (skew={skew:.2f})",
                        "priority": "high",
                        "expected_impact": "Normalize distribution, improve model performance",
                    }
                )
            elif abs(skew) > 1:
                col_recommendations.append(
                    {
                        "column": col,
                        "transformation": "log" if series.min() > 0 else "sqrt",
                        "reason": f"Moderately skewed (skew={skew:.2f})",
                        "priority": "medium",
                        "expected_impact": "Reduce skewness",
                    }
                )

            # Outlier-based recommendations
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            outliers = ((series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))).sum()
            outlier_pct = outliers / len(series)

            if outlier_pct > 0.1:
                col_recommendations.append(
                    {
                        "column": col,
                        "transformation": "robust_scale",
                        "reason": f"High outlier percentage ({outlier_pct*100:.1f}%)",
                        "priority": "high",
                        "expected_impact": "Reduce outlier impact",
                    }
                )

            # Scale-based recommendations
            if series.std() / (series.mean() + 1e-8) > 1:
                col_recommendations.append(
                    {
                        "column": col,
                        "transformation": "standardize",
                        "reason": "High coefficient of variation",
                        "priority": "medium",
                        "expected_impact": "Normalize scale",
                    }
                )

            recommendations.extend(col_recommendations)

        return recommendations

    def recommend_feature_engineering(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        Recommend overall feature engineering strategy.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            Dictionary with feature engineering recommendations
        """
        recommendations: Dict[str, Any] = {
            "transformations": self.recommend_transformations(X, y),
            "strategies": [],
            "warnings": [],
            "opportunities": [],
        }
        # Type annotations for nested lists
        recommendations_warnings: List[str] = recommendations["warnings"]  # type: ignore
        recommendations_opportunities: List[str] = recommendations["opportunities"]  # type: ignore

        numeric_count = len(X.select_dtypes(include=[np.number]).columns)
        categorical_count = len(X.select_dtypes(include=["object", "category"]).columns)
        datetime_count = sum(
            1
            for col in X.columns
            if pd.api.types.is_datetime64_any_dtype(X[col])
            or (X[col].dtype == "object" and self._is_datetime_string(X[col]))
        )

        # Dimensionality recommendations
        if numeric_count > 20:
            recommendations["strategies"].append(
                {
                    "strategy": "pca",
                    "reason": f"High dimensionality ({numeric_count} numeric features)",
                    "priority": "high",
                    "config": {"n_components": min(10, numeric_count // 2)},
                }
            )

        # Categorical recommendations
        if categorical_count > 0:
            high_cardinality = [
                col
                for col in X.select_dtypes(include=["object", "category"]).columns
                if X[col].nunique() > 20
            ]
            if high_cardinality:
                recommendations["strategies"].append(
                    {
                        "strategy": "target_encoding",
                        "reason": f"High cardinality features: {len(high_cardinality)}",
                        "priority": "high",
                        "features": high_cardinality,
                    }
                )

        # Time-series recommendations
        if datetime_count > 0:
            recommendations["strategies"].append(
                {
                    "strategy": "datetime_features",
                    "reason": f"Datetime columns detected: {datetime_count}",
                    "priority": "high",
                    "config": {"extract_components": True, "cyclical_encoding": True},
                }
            )

        # Interaction recommendations
        if numeric_count >= 2:
            recommendations["strategies"].append(
                {
                    "strategy": "polynomial_interactions",
                    "reason": "Multiple numeric features available",
                    "priority": "medium",
                    "config": {"degree": 2},
                }
            )

        # Window features for time-series
        if datetime_count > 0 or len(X) > 100:
            recommendations["strategies"].append(
                {
                    "strategy": "rolling_windows",
                    "reason": "Time-series or large dataset",
                    "priority": "medium",
                    "config": {"window_sizes": [3, 7, 14, 30]},
                }
            )

        # Warnings
        missing_pct = (X.isnull().sum().sum() / (X.shape[0] * X.shape[1])) * 100
        if missing_pct > 10:
            recommendations_warnings.append(
                f"High missing data: {missing_pct:.1f}%. Consider imputation."
            )

        # Opportunities
        if numeric_count < 5:
            recommendations_opportunities.append(
                "Low feature count. Consider feature engineering to expand features."
            )

        return recommendations

    def _is_datetime_string(self, series: pd.Series) -> bool:
        """Check if string series can be parsed as datetime."""
        try:
            sample = series.dropna().head(10)
            if len(sample) == 0:
                return False
            pd.to_datetime(sample, errors="raise")
            return True
        except Exception:
            return False

    def get_auto_config(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        Generate automatic configuration based on recommendations.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            Dictionary with auto-generated configuration
        """
        recommendations = self.recommend_feature_engineering(X, y)

        config: Dict[str, Any] = {
            "feature_engineering": {},
            "mathematical_modeling": {},
            "statistical_transforms": {},
            "pandas_operations": {},
        }

        # Apply transformation recommendations
        high_priority_transforms = [
            rec["transformation"]
            for rec in recommendations["transformations"]
            if rec.get("priority") == "high"
        ]

        if (
            "boxcox" in high_priority_transforms
            or "yeojohnson" in high_priority_transforms
        ):
            config["statistical_transforms"]["power_transforms"] = True

        # Apply strategy recommendations
        for strategy in recommendations["strategies"]:
            if strategy["strategy"] == "pca":
                config["mathematical_modeling"]["pca_features"] = True
                config["mathematical_modeling"]["n_components_pca"] = strategy[
                    "config"
                ]["n_components"]
            elif strategy["strategy"] == "datetime_features":
                config["pandas_operations"]["datetime_features"] = True
            elif strategy["strategy"] == "rolling_windows":
                config["pandas_operations"]["window_features"] = True

        return config
