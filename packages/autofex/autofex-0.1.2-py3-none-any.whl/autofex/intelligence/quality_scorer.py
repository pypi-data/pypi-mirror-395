"""
Feature Quality Scoring System

Automatically scores and ranks features based on multiple quality dimensions.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from scipy import stats
import warnings

try:
    from sklearn.feature_selection import (
        mutual_info_classif,
        mutual_info_regression,
        f_classif,
        f_regression,
    )
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("scikit-learn not available. Some quality metrics will be limited.")


class FeatureQualityScorer:
    """
    Comprehensive feature quality scoring system.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize feature quality scorer.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.importance_methods = self.config.get(
            "importance_methods", ["mutual_info", "f_test", "rf"]
        )

    def score_feature_quality(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        feature_name: str,
    ) -> Dict[str, Any]:
        """
        Score quality of a single feature.

        Args:
            X: Feature DataFrame
            y: Target variable
            feature_name: Name of feature to score

        Returns:
            Dictionary with quality scores
        """
        if feature_name not in X.columns:
            return {"error": f"Feature {feature_name} not found"}

        feature = X[feature_name].dropna()

        if len(feature) < 3:
            return {"error": "Insufficient data"}

        scores: Dict[str, Any] = {
            "feature": feature_name,
            "predictive_power": 0.0,
            "stability": 1.0,
            "uniqueness": 1.0,
            "efficiency": 1.0,
            "overall_score": 0.0,
        }

        # Predictive power
        try:
            if y.dtype in ["object", "category"] or y.nunique() < 20:
                # Classification
                if SKLEARN_AVAILABLE:
                    mi = mutual_info_classif(
                        feature.values.reshape(-1, 1),
                        y,
                        random_state=42,
                    )[0]
                    f_stat, _ = f_classif(feature.values.reshape(-1, 1), y)
                    f_stat = f_stat[0] if len(f_stat) > 0 else 0
                else:
                    mi = 0
                    f_stat = 0
            else:
                # Regression
                if SKLEARN_AVAILABLE:
                    mi = mutual_info_regression(
                        feature.values.reshape(-1, 1),
                        y,
                        random_state=42,
                    )[0]
                    f_stat, _ = f_regression(feature.values.reshape(-1, 1), y)
                    f_stat = f_stat[0] if len(f_stat) > 0 else 0
                else:
                    mi = 0
                    f_stat = 0

            # Normalize to 0-1
            scores["predictive_power"] = min(1.0, (mi + f_stat / 100) / 2)
        except Exception:
            pass

        # Stability (variance-based)
        try:
            cv = feature.std() / (feature.mean() + 1e-8)  # Coefficient of variation
            scores["stability"] = 1.0 / (1.0 + cv)  # Lower CV = higher stability
        except Exception:
            pass

        # Uniqueness (non-redundancy)
        try:
            numeric_cols = X.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                correlations = X[numeric_cols].corrwith(feature).abs()
                max_corr = (
                    correlations.drop(feature_name).max()
                    if len(correlations) > 1
                    else 0
                )
                scores["uniqueness"] = (
                    1.0 - max_corr
                )  # Lower correlation = higher uniqueness
        except Exception:
            pass

        # Efficiency (inverse of missing data and outliers)
        try:
            missing_pct = feature.isnull().sum() / len(feature)
            # Outlier detection (IQR)
            q1, q3 = feature.quantile(0.25), feature.quantile(0.75)
            iqr = q3 - q1
            outliers = (
                (feature < (q1 - 1.5 * iqr)) | (feature > (q3 + 1.5 * iqr))
            ).sum()
            outlier_pct = outliers / len(feature)
            scores["efficiency"] = 1.0 - (missing_pct + outlier_pct) / 2
        except Exception:
            pass

        # Overall score (weighted average)
        weights = {
            "predictive_power": 0.4,
            "stability": 0.2,
            "uniqueness": 0.2,
            "efficiency": 0.2,
        }

        overall_score: float = 0.0
        for key in weights.keys():
            score_val: Any = scores.get(key, 0.0)
            weight_val: float = float(weights.get(key, 0.0))
            overall_score += float(score_val) * weight_val
        scores["overall_score"] = overall_score

        return scores

    def score_all_features(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        top_n: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Score quality of all features.

        Args:
            X: Feature DataFrame
            y: Target variable
            top_n: Return only top N features (None = all)

        Returns:
            DataFrame with quality scores for all features
        """
        scores_list = []

        for col in X.columns:
            try:
                score = self.score_feature_quality(X, y, col)
                if "error" not in score:
                    scores_list.append(score)
            except Exception as e:
                warnings.warn(f"Failed to score {col}: {e}")

        if not scores_list:
            return pd.DataFrame()

        scores_df = pd.DataFrame(scores_list)

        # Sort by overall score
        scores_df = scores_df.sort_values("overall_score", ascending=False)

        if top_n:
            scores_df = scores_df.head(top_n)

        return scores_df

    def get_top_features(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        n_features: int = 50,
        min_score: float = 0.1,
    ) -> List[str]:
        """
        Get top quality features.

        Args:
            X: Feature DataFrame
            y: Target variable
            n_features: Maximum number of features
            min_score: Minimum quality score

        Returns:
            List of top feature names
        """
        scores_df = self.score_all_features(X, y)

        if scores_df.empty:
            return []

        # Filter by minimum score
        top_features = (
            scores_df[scores_df["overall_score"] >= min_score]["feature"]
            .head(n_features)
            .tolist()
        )

        return list(top_features)  # type: ignore[no-any-return]

    def get_feature_rankings(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> Dict[str, Any]:
        """
        Get comprehensive feature rankings.

        Args:
            X: Feature DataFrame
            y: Target variable

        Returns:
            Dictionary with feature rankings
        """
        scores_df = self.score_all_features(X, y)

        if scores_df.empty:
            return {}

        return {
            "top_predictive": scores_df.nlargest(10, "predictive_power")[
                "feature"
            ].tolist(),
            "top_stable": scores_df.nlargest(10, "stability")["feature"].tolist(),
            "top_unique": scores_df.nlargest(10, "uniqueness")["feature"].tolist(),
            "top_efficient": scores_df.nlargest(10, "efficiency")["feature"].tolist(),
            "top_overall": scores_df.nlargest(10, "overall_score")["feature"].tolist(),
            "all_scores": scores_df.to_dict("records"),
        }
