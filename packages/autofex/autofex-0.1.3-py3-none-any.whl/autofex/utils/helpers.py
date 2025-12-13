"""
Utility helper functions for AutoFEX.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
import warnings


def safe_divide(
    a: Union[pd.Series, np.ndarray, float],
    b: Union[pd.Series, np.ndarray, float],
    default: float = 0.0,
) -> Union[pd.Series, np.ndarray, float]:
    """
    Safely divide two values/arrays, handling division by zero.

    Args:
        a: Numerator
        b: Denominator
        default: Default value for division by zero

    Returns:
        Result of division with safe handling
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = np.divide(
            a, b, out=np.full_like(a, default, dtype=float), where=(b != 0)
        )
    return result


def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers using IQR method.

    Args:
        series: Input series
        multiplier: IQR multiplier (default 1.5)

    Returns:
        Boolean series indicating outliers
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR

    return (series < lower_bound) | (series > upper_bound)


def calculate_correlation_matrix(
    df: pd.DataFrame, method: str = "pearson"
) -> pd.DataFrame:
    """
    Calculate correlation matrix with safe handling.

    Args:
        df: Input dataframe
        method: Correlation method ('pearson', 'spearman', 'kendall')

    Returns:
        Correlation matrix
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) < 2:
        return pd.DataFrame()

    corr_matrix = df[numeric_cols].corr(method=method)

    # Fill NaN values
    corr_matrix = corr_matrix.fillna(0)

    return corr_matrix


def get_feature_stats(series: pd.Series) -> Dict[str, Any]:
    """
    Get comprehensive statistics for a feature.

    Args:
        series: Input series

    Returns:
        Dictionary with feature statistics
    """
    stats = {}

    if series.dtype in ["int64", "float64"]:
        stats.update(
            {
                "mean": series.mean(),
                "median": series.median(),
                "std": series.std(),
                "min": series.min(),
                "max": series.max(),
                "skewness": series.skew(),
                "kurtosis": series.kurtosis(),
                "zeros_count": (series == 0).sum(),
                "zeros_percentage": ((series == 0).sum() / len(series)) * 100,
                "missing_count": series.isnull().sum(),
                "missing_percentage": (series.isnull().sum() / len(series)) * 100,
            }
        )

        # Quartiles
        quartiles = series.quantile([0.25, 0.5, 0.75])
        stats["q1"] = quartiles[0.25]
        stats["q2"] = quartiles[0.5]
        stats["q3"] = quartiles[0.75]

        # Outlier detection
        outliers = detect_outliers_iqr(series)
        stats["outliers_count"] = outliers.sum()
        stats["outliers_percentage"] = (outliers.sum() / len(series)) * 100

    else:
        # Categorical statistics
        value_counts = series.value_counts()
        stats.update(
            {
                "unique_values": len(value_counts),
                "most_common": value_counts.index[0] if len(value_counts) > 0 else None,
                "most_common_count": (
                    value_counts.iloc[0] if len(value_counts) > 0 else 0
                ),
                "most_common_percentage": (
                    (value_counts.iloc[0] / len(series)) * 100
                    if len(value_counts) > 0
                    else 0
                ),
                "missing_count": series.isnull().sum(),
                "missing_percentage": (series.isnull().sum() / len(series)) * 100,
                "entropy": (
                    calculate_entropy(value_counts) if len(value_counts) > 1 else 0
                ),
            }
        )

    return stats


def calculate_entropy(value_counts: pd.Series) -> float:
    """
    Calculate Shannon entropy for categorical distribution.

    Args:
        value_counts: Value counts series

    Returns:
        Shannon entropy value
    """
    probabilities = value_counts / value_counts.sum()
    entropy: float = float(-np.sum(probabilities * np.log2(probabilities)))
    return entropy


def validate_dataframe(
    df: pd.DataFrame, checks: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Validate dataframe integrity and quality.

    Args:
        df: Input dataframe
        checks: List of validation checks to perform

    Returns:
        Validation results
    """
    if checks is None:
        checks = ["basic", "missing", "duplicates", "types"]

    results: Dict[str, Any] = {
        "valid": True,
        "issues": [],
        "warnings": [],
        "summary": {},
    }

    # Basic checks
    if "basic" in checks:
        if df.empty:
            results["issues"].append("DataFrame is empty")
            results["valid"] = False

        if len(df.columns) == 0:
            results["issues"].append("DataFrame has no columns")
            results["valid"] = False

    # Missing value checks
    if "missing" in checks:
        missing_pct = (df.isnull().sum() / len(df)) * 100
        high_missing_cols = missing_pct[missing_pct > 50]

        if len(high_missing_cols) > 0:
            results["warnings"].append(
                f"Columns with >50% missing values: {high_missing_cols.index.tolist()}"
            )

        if missing_pct.sum() > 30:
            results["warnings"].append(
                f"Overall missing data: {missing_pct.sum():.1f}%"
            )

    # Duplicate checks
    if "duplicates" in checks:
        dup_rows = df.duplicated().sum()
        dup_pct = (dup_rows / len(df)) * 100

        if dup_pct > 5:
            results["warnings"].append(
                f"High duplicate rows: {dup_pct:.1f}% ({dup_rows} rows)"
            )

    # Type consistency checks
    if "types" in checks:
        for col in df.columns:
            if df[col].dtype == "object":
                # Check if looks like numeric
                try:
                    numeric_conversion = pd.to_numeric(df[col], errors="coerce")
                    if numeric_conversion.notna().sum() > len(df[col]) * 0.8:
                        results["warnings"].append(
                            f"Column '{col}' contains mostly numeric data but is object type"
                        )
                except:
                    pass

    # Summary
    results["summary"] = {
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "n_numeric": len(df.select_dtypes(include=[np.number]).columns),
        "n_categorical": len(df.select_dtypes(include=["object", "category"]).columns),
        "total_missing": df.isnull().sum().sum(),
        "missing_percentage": (df.isnull().sum().sum() / (len(df) * len(df.columns)))
        * 100,
        "duplicate_rows": df.duplicated().sum(),
    }

    return results


def create_feature_report(
    features: List[str],
    importance_scores: Optional[pd.Series] = None,
    correlations: Optional[pd.Series] = None,
) -> pd.DataFrame:
    """
    Create a comprehensive feature report.

    Args:
        features: List of feature names
        importance_scores: Feature importance scores
        correlations: Feature-target correlations

    Returns:
        DataFrame with feature report
    """
    report_data = []

    for feature in features:
        feature_info = {
            "feature": feature,
            "importance_score": (
                importance_scores[feature]
                if importance_scores is not None and feature in importance_scores.index
                else None
            ),
            "correlation": (
                correlations[feature]
                if correlations is not None and feature in correlations.index
                else None
            ),
        }
        report_data.append(feature_info)

    return pd.DataFrame(report_data).sort_values(
        "importance_score", ascending=False, na_position="last"
    )


def split_data_stratified(
    X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Stratified train-test split that preserves class distribution.

    Args:
        X: Features
        y: Target
        test_size: Test set proportion
        random_state: Random seed

    Returns:
        X_train, X_test, y_train, y_test
    """
    from sklearn.model_selection import train_test_split

    if y.nunique() <= 10 and y.dtype in ["int64", "object", "category"]:
        # Classification with reasonable number of classes
        stratify = y
    else:
        stratify = None

    return train_test_split(  # type: ignore[no-any-return]
        X, y, test_size=test_size, random_state=random_state, stratify=stratify
    )


def handle_missing_values(
    df: pd.DataFrame, strategy: str = "median", columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Handle missing values with different strategies.

    Args:
        df: Input dataframe
        strategy: Imputation strategy ('median', 'mean', 'mode', 'drop')
        columns: Specific columns to impute (None for all)

    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()

    if columns is None:
        columns = df.columns

    for col in columns:
        if df[col].isnull().any():
            if strategy == "median":
                if df[col].dtype in ["int64", "float64"]:
                    fill_value = df[col].median()
                else:
                    fill_value = (
                        df[col].mode().iloc[0]
                        if not df[col].mode().empty
                        else "Unknown"
                    )
            elif strategy == "mean":
                if df[col].dtype in ["int64", "float64"]:
                    fill_value = df[col].mean()
                else:
                    fill_value = (
                        df[col].mode().iloc[0]
                        if not df[col].mode().empty
                        else "Unknown"
                    )
            elif strategy == "mode":
                fill_value = (
                    df[col].mode().iloc[0] if not df[col].mode().empty else "Unknown"
                )
            elif strategy == "drop":
                df_imputed = df_imputed.dropna(subset=[col])
                continue
            else:
                raise ValueError(f"Unknown imputation strategy: {strategy}")

            df_imputed[col] = df_imputed[col].fillna(fill_value)

    return df_imputed
