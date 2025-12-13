"""
Leakage Detection Engine

Detects various types of data leakage in machine learning datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from scipy import stats
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import roc_auc_score, mean_squared_error
import warnings


class LeakageDetector:
    """
    Comprehensive leakage detection system that identifies:
    - Target leakage (features that directly predict target)
    - Train-test contamination
    - Time-based leakage
    - Statistical anomalies
    - Feature-target correlations that are too perfect
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize leakage detector.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.leakage_threshold = self.config.get("leakage_threshold", 0.95)
        self.perfect_prediction_threshold = self.config.get(
            "perfect_prediction_threshold", 0.99
        )
        self.cv_folds = self.config.get("cv_folds", 5)
        self.random_state = self.config.get("random_state", 42)

    def detect(
        self,
        X: pd.DataFrame,
        y: Union[pd.Series, np.ndarray],
        X_test: Optional[pd.DataFrame] = None,
        time_column: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform comprehensive leakage detection.

        Args:
            X: Training features
            y: Training target
            X_test: Test features (optional)
            time_column: Name of time column for temporal leakage detection

        Returns:
            Dictionary containing leakage analysis results
        """
        if isinstance(y, np.ndarray):
            y = pd.Series(y)

        report = {
            "target_leakage": self._detect_target_leakage(X, y),
            "statistical_anomalies": self._detect_statistical_anomalies(X, y),
            "feature_perfection": self._detect_feature_perfection(X, y),
            "duplicate_features": self._detect_duplicate_features(X),
        }

        if X_test is not None:
            report["train_test_contamination"] = self._detect_train_test_contamination(
                X, X_test
            )

        if time_column and time_column in X.columns:
            report["temporal_leakage"] = self._detect_temporal_leakage(
                X, y, time_column
            )

        # Overall assessment
        report["overall_assessment"] = self._assess_overall_leakage_risk(report)

        return report

    def _detect_target_leakage(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Detect features that might be leaking target information.
        """
        leakage_candidates = []
        is_classification = self._is_classification_target(y)

        for col in X.columns:
            try:
                feature = X[col]

                # Skip if feature has too many missing values
                if feature.isnull().mean() > 0.5:
                    continue

                # Calculate correlation/performance metrics
                if feature.dtype in ["int64", "float64"]:
                    # For numeric features, check correlation
                    if is_classification:
                        # Use point-biserial correlation for binary target
                        if y.nunique() == 2:
                            corr, p_value = stats.pointbiserialr(
                                feature.fillna(feature.mean()), y
                            )
                        else:
                            # For multiclass, use ANOVA
                            groups = [feature[y == cls].dropna() for cls in y.unique()]
                            if len(groups) > 1 and all(len(g) > 0 for g in groups):
                                f_stat, p_value = stats.f_oneway(*groups)
                                corr = (
                                    np.sqrt(f_stat / (f_stat + len(y) - len(groups)))
                                    if f_stat > 0
                                    else 0
                                )
                            else:
                                continue
                    else:
                        # Regression: Pearson correlation
                        corr, p_value = stats.pearsonr(
                            feature.fillna(feature.mean()), y
                        )
                else:
                    # For categorical features, check if they perfectly predict target
                    contingency = pd.crosstab(feature, y)
                    chi2, p_value, _, _ = stats.chi2_contingency(contingency)
                    corr = np.sqrt(chi2 / (chi2 + len(feature))) if chi2 > 0 else 0

                # Check for suspiciously high correlations
                abs_corr = abs(corr)
                if abs_corr > self.leakage_threshold:
                    leakage_candidates.append(
                        {
                            "feature": col,
                            "correlation": corr,
                            "abs_correlation": abs_corr,
                            "p_value": p_value,
                            "risk_level": "high" if abs_corr > 0.99 else "medium",
                        }
                    )

            except Exception as e:
                warnings.warn(f"Could not analyze leakage for column {col}: {e}")

        return {
            "leakage_candidates": sorted(
                leakage_candidates, key=lambda x: x["abs_correlation"], reverse=True
            ),
            "threshold": self.leakage_threshold,
            "total_candidates": len(leakage_candidates),
        }

    def _detect_statistical_anomalies(
        self, X: pd.DataFrame, y: pd.Series
    ) -> Dict[str, Any]:
        """
        Detect statistical anomalies that might indicate leakage.
        """
        anomalies = []

        # Check for features with unusual distributions in target groups
        is_classification = self._is_classification_target(y)

        if (
            is_classification and y.nunique() <= 10
        ):  # Only for reasonable number of classes
            for col in X.select_dtypes(include=[np.number]).columns:
                try:
                    feature = X[col].dropna()

                    # Compare distributions across target classes
                    class_stats = []
                    for cls in y.unique():
                        class_data = feature[y == cls]
                        if len(class_data) > 10:
                            class_stats.append(
                                {
                                    "class": cls,
                                    "mean": class_data.mean(),
                                    "std": class_data.std(),
                                    "n": len(class_data),
                                }
                            )

                    if len(class_stats) >= 2:
                        means = [stat["mean"] for stat in class_stats]
                        mean_range = max(means) - min(means)

                        # Check if means are suspiciously different
                        if mean_range > 0:
                            # Cohen's d effect size
                            pooled_std = np.sqrt(
                                sum(
                                    stat["std"] ** 2 * stat["n"] for stat in class_stats
                                )
                                / sum(stat["n"] for stat in class_stats)
                            )
                            effect_size = (
                                mean_range / pooled_std if pooled_std > 0 else 0
                            )

                            if effect_size > 3.0:  # Very large effect size
                                anomalies.append(
                                    {
                                        "feature": col,
                                        "anomaly_type": "large_class_difference",
                                        "effect_size": effect_size,
                                        "class_means": {
                                            stat["class"]: stat["mean"]
                                            for stat in class_stats
                                        },
                                    }
                                )

                except Exception as e:
                    continue

        return {"statistical_anomalies": anomalies, "total_anomalies": len(anomalies)}

    def _detect_feature_perfection(
        self, X: pd.DataFrame, y: pd.Series
    ) -> Dict[str, Any]:
        """
        Detect features that might perfectly predict the target.
        """
        perfect_features = []
        is_classification = self._is_classification_target(y)

        for col in X.columns:
            try:
                feature = X[col]

                if is_classification:
                    # For classification, check if feature perfectly separates classes
                    if feature.dtype in ["int64", "float64"]:
                        # Check if different feature values always map to same target
                        unique_combinations = (
                            X[[col]].assign(target=y).drop_duplicates()
                        )
                        if len(unique_combinations) == len(feature.unique()):
                            # Each feature value maps to exactly one target value
                            perfect_features.append(
                                {
                                    "feature": col,
                                    "perfection_type": "perfect_separation",
                                    "unique_combinations": len(unique_combinations),
                                }
                            )
                else:
                    # For regression, check for exact matches
                    correlation = abs(feature.corr(y))
                    if correlation > self.perfect_prediction_threshold:
                        perfect_features.append(
                            {
                                "feature": col,
                                "correlation": correlation,
                                "perfection_type": "high_correlation",
                            }
                        )

            except Exception as e:
                continue

        return {
            "perfect_features": perfect_features,
            "threshold": self.perfect_prediction_threshold,
            "total_perfect_features": len(perfect_features),
        }

    def _detect_duplicate_features(self, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect duplicate or nearly duplicate features.
        """
        duplicates = []
        cols = X.columns

        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                try:
                    col1, col2 = cols[i], cols[j]

                    # Check for exact duplicates
                    if X[col1].equals(X[col2]):
                        duplicates.append(
                            {
                                "feature1": col1,
                                "feature2": col2,
                                "similarity": 1.0,
                                "duplicate_type": "exact",
                            }
                        )
                        continue

                    # Check for high correlation (numeric features)
                    if X[col1].dtype in ["int64", "float64"] and X[col2].dtype in [
                        "int64",
                        "float64",
                    ]:
                        corr = abs(X[col1].corr(X[col2]))
                        if corr > self.leakage_threshold:
                            duplicates.append(
                                {
                                    "feature1": col1,
                                    "feature2": col2,
                                    "similarity": corr,
                                    "duplicate_type": "high_correlation",
                                }
                            )

                except Exception as e:
                    continue

        return {"duplicate_features": duplicates, "total_duplicates": len(duplicates)}

    def _detect_train_test_contamination(
        self, X_train: pd.DataFrame, X_test: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Detect if test data has leaked into training data.
        """
        contamination_indicators = []

        # Check for overlapping IDs or indices
        if hasattr(X_train.index, "name") and hasattr(X_test.index, "name"):
            if X_train.index.name == X_test.index.name:
                overlapping_indices = set(X_train.index) & set(X_test.index)
                if len(overlapping_indices) > 0:
                    contamination_indicators.append(
                        {
                            "contamination_type": "overlapping_indices",
                            "overlapping_count": len(overlapping_indices),
                            "overlap_percentage": len(overlapping_indices)
                            / len(X_test)
                            * 100,
                        }
                    )

        # Check for identical rows
        train_hashes = set(X_train.apply(lambda x: hash(tuple(x)), axis=1))
        test_hashes = set(X_test.apply(lambda x: hash(tuple(x)), axis=1))
        overlapping_rows = len(train_hashes & test_hashes)

        if overlapping_rows > 0:
            contamination_indicators.append(
                {
                    "contamination_type": "identical_rows",
                    "overlapping_rows": overlapping_rows,
                    "overlap_percentage": overlapping_rows / len(X_test) * 100,
                }
            )

        # Statistical comparison
        for col in X_train.select_dtypes(include=[np.number]).columns:
            if col in X_test.columns:
                try:
                    train_stats = X_train[col].describe()
                    test_stats = X_test[col].describe()

                    # Check if distributions are suspiciously similar
                    stat_diff = (
                        abs(train_stats["mean"] - test_stats["mean"])
                        / train_stats["std"]
                    )
                    if stat_diff < 0.1:  # Very similar means
                        contamination_indicators.append(
                            {
                                "contamination_type": "similar_distributions",
                                "feature": col,
                                "statistical_difference": stat_diff,
                            }
                        )
                except:
                    continue

        return {
            "contamination_indicators": contamination_indicators,
            "risk_level": "high" if len(contamination_indicators) > 2 else "low",
        }

    def _detect_temporal_leakage(
        self, X: pd.DataFrame, y: pd.Series, time_column: str
    ) -> Dict[str, Any]:
        """
        Detect temporal leakage patterns.
        """
        temporal_issues = []

        try:
            # Sort by time
            df_sorted = X.assign(target=y).sort_values(time_column)

            # Check for features that correlate too strongly with future target values
            for col in X.select_dtypes(include=[np.number]).columns:
                if col != time_column:
                    # Rolling correlation with future values
                    series = df_sorted[col]
                    target = df_sorted["target"]

                    # Check correlation between current feature and future target
                    future_corr = series.corr(
                        target.shift(-1)
                    )  # Feature at t vs target at t+1

                    if abs(future_corr) > self.leakage_threshold:
                        temporal_issues.append(
                            {
                                "feature": col,
                                "future_correlation": future_corr,
                                "issue_type": "predicts_future_target",
                            }
                        )

        except Exception as e:
            warnings.warn(f"Temporal leakage detection failed: {e}")

        return {
            "temporal_issues": temporal_issues,
            "total_temporal_issues": len(temporal_issues),
        }

    def _assess_overall_leakage_risk(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide overall assessment of leakage risk.
        """
        risk_score = 0
        risk_factors = []

        # Target leakage risk
        target_candidates = len(
            report.get("target_leakage", {}).get("leakage_candidates", [])
        )
        if target_candidates > 0:
            risk_score += min(target_candidates * 2, 10)
            risk_factors.append(
                f"{target_candidates} potential target leakage features"
            )

        # Perfect features
        perfect_count = len(
            report.get("feature_perfection", {}).get("perfect_features", [])
        )
        if perfect_count > 0:
            risk_score += perfect_count * 5
            risk_factors.append(
                f"{perfect_count} features with perfect target prediction"
            )

        # Statistical anomalies
        anomaly_count = report.get("statistical_anomalies", {}).get(
            "total_anomalies", 0
        )
        if anomaly_count > 0:
            risk_score += anomaly_count
            risk_factors.append(f"{anomaly_count} statistical anomalies")

        # Train-test contamination
        contamination = report.get("train_test_contamination", {})
        if contamination.get("risk_level") == "high":
            risk_score += 5
            risk_factors.append("High risk of train-test contamination")

        # Determine risk level
        if risk_score >= 10:
            risk_level = "high"
        elif risk_score >= 5:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "recommendations": self._get_leakage_recommendations(risk_level),
        }

    def _get_leakage_recommendations(self, risk_level: str) -> List[str]:
        """Get recommendations based on risk level."""
        base_recs = [
            "Review feature engineering process for potential target leakage",
            "Ensure proper temporal ordering in time-series data",
            "Validate train/test split integrity",
        ]

        if risk_level == "high":
            base_recs.extend(
                [
                    "URGENT: Remove or investigate perfect prediction features",
                    "Check for data collection timing issues",
                    "Consider using cross-validation with time-aware splits",
                ]
            )
        elif risk_level == "medium":
            base_recs.extend(
                [
                    "Investigate highly correlated features",
                    "Review feature creation pipeline",
                    "Monitor model performance on held-out data",
                ]
            )

        return base_recs

    def _is_classification_target(self, y: pd.Series) -> bool:
        """Determine if target is classification."""
        return y.nunique() < 20 or y.dtype in ["object", "category"]
