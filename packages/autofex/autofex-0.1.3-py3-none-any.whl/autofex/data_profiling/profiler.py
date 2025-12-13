"""
Data Profiling Engine

Analyzes data quality, distributions, outliers, and statistical properties..
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from scipy import stats
from collections import defaultdict
import warnings


class DataProfiler:
    """
    Comprehensive data profiling engine that analyzes data quality,
    distributions, correlations, and potential issues.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize data profiler.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.missing_threshold = self.config.get("missing_threshold", 0.5)
        self.outlier_method = self.config.get("outlier_method", "iqr")
        self.correlation_threshold = self.config.get("correlation_threshold", 0.95)
        self.sample_size = self.config.get("sample_size", 10000)

    def analyze(
        self, X: pd.DataFrame, y: Optional[Union[pd.Series, np.ndarray]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive data profiling.

        Args:
            X: Feature DataFrame
            y: Target variable (optional)

        Returns:
            Dictionary containing profiling results
        """
        report = {
            "overview": self._get_overview_stats(X, y),
            "missing_values": self._analyze_missing_values(X),
            "data_types": self._analyze_data_types(X),
            "distributions": self._analyze_distributions(X),
            "outliers": self._detect_outliers(X),
            "correlations": self._analyze_correlations(X),
            "duplicates": self._analyze_duplicates(X),
            "cardinality": self._analyze_cardinality(X),
        }

        if y is not None:
            report["target_analysis"] = self._analyze_target_relationships(X, y)

        return report

    def _get_overview_stats(
        self, X: pd.DataFrame, y: Optional[Union[pd.Series, np.ndarray]] = None
    ) -> Dict[str, Any]:
        """Get basic overview statistics."""
        return {
            "n_rows": len(X),
            "n_features": len(X.columns),
            "n_numeric": len(X.select_dtypes(include=[np.number]).columns),
            "n_categorical": len(
                X.select_dtypes(include=["object", "category"]).columns
            ),
            "memory_usage": X.memory_usage(deep=True).sum(),
            "target_type": (
                "classification"
                if y is not None and self._is_classification_target(y)
                else "regression"
            ),
        }

    def _analyze_missing_values(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing value patterns."""
        missing_stats = X.isnull().sum()
        missing_pct = (missing_stats / len(X)) * 100

        # Columns with high missing rates
        high_missing_cols = missing_pct[missing_pct > (self.missing_threshold * 100)]

        # Missing value patterns
        missing_matrix = X.isnull().astype(int)
        missing_corr = missing_matrix.corr()

        return {
            "missing_counts": missing_stats.to_dict(),
            "missing_percentages": missing_pct.to_dict(),
            "high_missing_columns": high_missing_cols.index.tolist(),
            "total_missing_cells": X.isnull().sum().sum(),
            "missing_patterns_correlation": (
                missing_corr.to_dict() if len(missing_corr) > 0 else {}
            ),
        }

    def _analyze_data_types(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data types and potential type issues."""
        dtypes = X.dtypes
        inferred_types = {}

        for col in X.columns:
            series = X[col]
            if series.dtype == "object":
                # Try to infer if numeric
                try:
                    pd.to_numeric(series, errors="coerce")
                    inferred_types[col] = "numeric_string"
                except:
                    inferred_types[col] = "categorical"
            elif series.dtype in ["int64", "float64"]:
                # Check if integer values in float column
                if series.dtype == "float64":
                    non_null_series = series.dropna()
                    if (
                        len(non_null_series) > 0
                        and (non_null_series == non_null_series.astype(int)).all()
                    ):
                        inferred_types[col] = "integer_as_float"
                    else:
                        inferred_types[col] = "numeric"
                else:
                    inferred_types[col] = "numeric"
            else:
                inferred_types[col] = str(series.dtype)

        return {
            "dtypes": dtypes.to_dict(),
            "inferred_types": inferred_types,
            "type_consistency": self._check_type_consistency(X),
        }

    def _analyze_distributions(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Analyze feature distributions."""
        distributions = {}

        for col in X.columns:
            series = X[col].dropna()

            if len(series) == 0:
                distributions[col] = {"empty": True}
                continue

            col_dist = {}

            if series.dtype in ["int64", "float64"]:
                col_dist.update(
                    {
                        "mean": series.mean(),
                        "median": series.median(),
                        "std": series.std(),
                        "skewness": series.skew(),
                        "kurtosis": series.kurtosis(),
                        "min": series.min(),
                        "max": series.max(),
                        "quartiles": series.quantile([0.25, 0.75]).to_dict(),
                        "zeros_count": (series == 0).sum(),
                        "zeros_percentage": ((series == 0).sum() / len(series)) * 100,
                        "negative_count": (series < 0).sum(),
                        "negative_percentage": ((series < 0).sum() / len(series)) * 100,
                    }
                )

                # Normality test (requires at least 8 samples)
                try:
                    sample_series = series.sample(min(self.sample_size, len(series)))
                    if len(sample_series) >= 8:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", category=RuntimeWarning)
                            _, p_value = stats.normaltest(sample_series)
                        col_dist["normality_p_value"] = p_value
                        col_dist["is_normal"] = p_value > 0.05
                    else:
                        col_dist["normality_test_skipped"] = (
                            "Insufficient samples (< 8)"
                        )
                except Exception:
                    col_dist["normality_test_failed"] = True

            else:
                # Categorical distribution
                value_counts = series.value_counts()
                col_dist.update(
                    {
                        "unique_values": len(value_counts),
                        "most_common": (
                            value_counts.index[0] if len(value_counts) > 0 else None
                        ),
                        "most_common_count": (
                            value_counts.iloc[0] if len(value_counts) > 0 else 0
                        ),
                        "entropy": (
                            stats.entropy(value_counts) if len(value_counts) > 1 else 0
                        ),
                    }
                )

            distributions[col] = col_dist

        return distributions

    def _detect_outliers(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers in numeric columns."""
        outlier_report: Dict[str, Any] = {}

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            series = X[col].dropna()

            if len(series) < 10:  # Need minimum data for outlier detection
                outlier_report[col] = {"insufficient_data": True}
                continue

            if self.outlier_method == "iqr":
                outliers = self._detect_outliers_iqr(series)
            elif self.outlier_method == "zscore":
                outliers = self._detect_outliers_zscore(series)
            else:
                outliers = self._detect_outliers_iqr(series)

            outlier_report[col] = {
                "outlier_count": len(outliers),
                "outlier_percentage": (len(outliers) / len(series)) * 100,
                "outlier_indices": (
                    outliers.index.tolist() if len(outliers) < 100 else []
                ),  # Limit output
                "method": self.outlier_method,
            }

        return outlier_report

    def _detect_outliers_iqr(self, series: pd.Series) -> pd.Series:
        """Detect outliers using IQR method."""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        return series[(series < lower_bound) | (series > upper_bound)]

    def _detect_outliers_zscore(
        self, series: pd.Series, threshold: float = 3.0
    ) -> pd.Series:
        """Detect outliers using Z-score method."""
        z_scores = np.abs(stats.zscore(series))
        return series[z_scores > threshold]

    def _analyze_correlations(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Analyze feature correlations."""
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return {"insufficient_numeric_features": True}

        # Pearson correlation
        pearson_corr = X[numeric_cols].corr()

        # Spearman correlation (rank-based)
        spearman_corr = X[numeric_cols].corr(method="spearman")

        # Highly correlated pairs
        high_corr_pairs = []
        for i in range(len(pearson_corr.columns)):
            for j in range(i + 1, len(pearson_corr.columns)):
                corr_val = abs(pearson_corr.iloc[i, j])
                if corr_val > self.correlation_threshold:
                    high_corr_pairs.append(
                        {
                            "feature1": pearson_corr.columns[i],
                            "feature2": pearson_corr.columns[j],
                            "correlation": pearson_corr.iloc[i, j],
                            "abs_correlation": corr_val,
                        }
                    )

        return {
            "pearson_correlation": pearson_corr.to_dict(),
            "spearman_correlation": spearman_corr.to_dict(),
            "highly_correlated_pairs": high_corr_pairs,
            "correlation_threshold": self.correlation_threshold,
        }

    def _analyze_duplicates(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Analyze duplicate rows and values."""
        duplicate_rows = X.duplicated().sum()
        duplicate_pct = (duplicate_rows / len(X)) * 100

        # Check for duplicate columns
        duplicate_cols = []
        for i in range(len(X.columns)):
            for j in range(i + 1, len(X.columns)):
                if X.iloc[:, i].equals(X.iloc[:, j]):
                    duplicate_cols.append((X.columns[i], X.columns[j]))

        return {
            "duplicate_rows": duplicate_rows,
            "duplicate_percentage": duplicate_pct,
            "duplicate_columns": duplicate_cols,
        }

    def _analyze_cardinality(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Analyze feature cardinality."""
        cardinality = {}

        for col in X.columns:
            unique_vals = X[col].nunique()
            total_vals = len(X[col])

            cardinality[col] = {
                "unique_values": unique_vals,
                "total_values": total_vals,
                "uniqueness_ratio": unique_vals / total_vals,
                "is_high_cardinality": unique_vals > min(100, total_vals * 0.1),
                "is_low_cardinality": unique_vals <= 2,
            }

        return cardinality

    def _analyze_target_relationships(
        self, X: pd.DataFrame, y: Union[pd.Series, np.ndarray]
    ) -> Dict[str, Any]:
        """Analyze relationships between features and target."""
        if isinstance(y, np.ndarray):
            y = pd.Series(y)

        is_classification = self._is_classification_target(y)

        relationships = {}

        for col in X.columns:
            series = X[col].dropna()

            if series.dtype in ["int64", "float64"]:
                # Numeric feature analysis
                if is_classification:
                    # ANOVA or Kruskal-Wallis test
                    try:
                        groups = [series[y == cls] for cls in y.unique()]
                        if len(groups) > 1:
                            h_stat, p_value = stats.kruskal(*groups)
                            relationships[col] = {
                                "test_type": "kruskal_wallis",
                                "statistic": h_stat,
                                "p_value": p_value,
                                "significant": p_value < 0.05,
                            }
                    except:
                        relationships[col] = {"test_failed": True}
                else:
                    # Correlation with target
                    corr = series.corr(y)
                    relationships[col] = {
                        "correlation_with_target": corr,
                        "abs_correlation": abs(corr),
                    }

        return {
            "target_type": "classification" if is_classification else "regression",
            "feature_target_relationships": relationships,
        }

    def _check_type_consistency(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Check for type consistency issues."""
        issues = []

        for col in X.columns:
            series = X[col]
            if series.dtype == "object":
                # Check if column looks like it should be numeric
                numeric_series = pd.to_numeric(series, errors="coerce")
                if numeric_series.notna().sum() > len(series) * 0.8:
                    issues.append(
                        {
                            "column": col,
                            "issue": "numeric_strings",
                            "conversion_rate": numeric_series.notna().sum()
                            / len(series),
                        }
                    )

        return {"type_consistency_issues": issues}

    def _is_classification_target(self, y: pd.Series) -> bool:
        """Determine if target is classification or regression."""
        unique_vals = y.nunique()
        return unique_vals < 20 or y.dtype in ["object", "category"]
