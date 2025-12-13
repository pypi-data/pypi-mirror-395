"""
Numpy Operations

Leverages numpy for array operations and mathematical features.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
import warnings


class NumpyOperations:
    """
    Numpy-based feature engineering operations.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize numpy operations.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

    def create_array_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using numpy array operations.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with array-based features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())
        X_array = X_numeric.values

        features = pd.DataFrame(index=X.index)

        # Array-wide statistics
        features["array_mean"] = np.mean(X_array, axis=1)
        features["array_std"] = np.std(X_array, axis=1)
        features["array_min"] = np.min(X_array, axis=1)
        features["array_max"] = np.max(X_array, axis=1)
        features["array_median"] = np.median(X_array, axis=1)
        features["array_range"] = features["array_max"] - features["array_min"]

        # Percentiles
        for p in [25, 50, 75, 90, 95]:
            features[f"array_p{p}"] = np.percentile(X_array, p, axis=1)

        # Norms
        features["array_l2_norm"] = np.linalg.norm(X_array, axis=1, ord=2)
        features["array_l1_norm"] = np.linalg.norm(X_array, axis=1, ord=1)

        # Array operations
        features["array_sum"] = np.sum(X_array, axis=1)
        features["array_prod"] = np.prod(np.abs(X_array) + 1e-8, axis=1)  # Avoid zero
        features["array_mean_abs"] = np.mean(np.abs(X_array), axis=1)

        # Non-zero counts
        features["array_nonzero_count"] = np.count_nonzero(X_array, axis=1)
        features["array_positive_count"] = np.sum(X_array > 0, axis=1)
        features["array_negative_count"] = np.sum(X_array < 0, axis=1)

        return features

    def create_broadcasting_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using numpy broadcasting.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with broadcasting features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())
        X_array = X_numeric.values

        features = pd.DataFrame(index=X.index)

        # Column means for broadcasting
        col_means = np.mean(X_array, axis=0, keepdims=True)
        col_stds = np.std(X_array, axis=0, keepdims=True) + 1e-8

        # Distance from mean (broadcasted)
        features["mean_distance"] = np.mean(np.abs(X_array - col_means), axis=1)
        features["std_distance"] = np.mean(
            np.abs((X_array - col_means) / col_stds), axis=1
        )

        # Pairwise operations (sample of pairs)
        if X_array.shape[1] >= 2:
            # First two columns
            col1 = X_array[:, 0]
            col2 = X_array[:, 1]

            features["pairwise_ratio"] = col1 / (col2 + 1e-8)
            features["pairwise_diff"] = col1 - col2
            features["pairwise_sum"] = col1 + col2
            features["pairwise_prod"] = col1 * col2

        return features

    def create_matrix_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using numpy matrix operations.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with matrix-based features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())
        X_array = X_numeric.values

        features = pd.DataFrame(index=X.index)

        # Covariance matrix features (for each row's relationship to others)
        try:
            # Sample-based covariance
            if len(X_array) > 10:
                cov_matrix = np.cov(X_array.T)
                # Eigenvalues
                eigenvals = np.linalg.eigvals(cov_matrix)
                features["cov_eigenval_max"] = np.max(eigenvals)
                features["cov_eigenval_min"] = np.min(eigenvals)
                features["cov_eigenval_mean"] = np.mean(eigenvals)
        except Exception:
            pass

        # Row-wise dot products with mean vector
        mean_vector = np.mean(X_array, axis=0)
        features["dot_product_with_mean"] = np.dot(X_array, mean_vector)

        # Row-wise variance
        features["row_variance"] = np.var(X_array, axis=1)

        return features

    def create_math_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using numpy mathematical functions.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with math features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col].fillna(X[col].mean())
            col_features = pd.DataFrame(index=X.index)

            # Trigonometric functions
            col_features[f"{col}_sin"] = np.sin(series)
            col_features[f"{col}_cos"] = np.cos(series)
            col_features[f"{col}_tan"] = np.tan(series)

            # Hyperbolic functions
            col_features[f"{col}_sinh"] = np.sinh(series)
            col_features[f"{col}_cosh"] = np.cosh(series)
            col_features[f"{col}_tanh"] = np.tanh(series)

            # Exponential and logarithmic
            col_features[f"{col}_exp"] = np.exp(
                np.clip(series, -10, 10)
            )  # Clip to avoid overflow
            col_features[f"{col}_expm1"] = np.expm1(np.clip(series, -10, 10))
            col_features[f"{col}_log1p"] = np.log1p(series.clip(lower=0))

            # Special functions
            col_features[f"{col}_abs"] = np.abs(series)
            col_features[f"{col}_sign"] = np.sign(series)
            col_features[f"{col}_floor"] = np.floor(series)
            col_features[f"{col}_ceil"] = np.ceil(series)
            col_features[f"{col}_round"] = np.round(series)

            # Power functions
            col_features[f"{col}_power_2"] = np.power(series, 2)
            col_features[f"{col}_power_3"] = np.power(series, 3)
            col_features[f"{col}_power_0_5"] = np.power(series.clip(lower=0), 0.5)

            features.append(col_features)

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_aggregation_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using numpy aggregation functions.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with aggregation features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())
        X_array = X_numeric.values

        features = pd.DataFrame(index=X.index)

        # Various aggregations
        features["agg_mean"] = np.mean(X_array, axis=1)
        features["agg_median"] = np.median(X_array, axis=1)
        features["agg_std"] = np.std(X_array, axis=1)
        features["agg_var"] = np.var(X_array, axis=1)
        features["agg_min"] = np.min(X_array, axis=1)
        features["agg_max"] = np.max(X_array, axis=1)
        features["agg_sum"] = np.sum(X_array, axis=1)
        features["agg_prod"] = np.prod(np.abs(X_array) + 1e-8, axis=1)

        # Percentiles
        for p in [10, 25, 50, 75, 90]:
            features[f"agg_p{p}"] = np.percentile(X_array, p, axis=1)

        # Skewness and kurtosis (row-wise approximation)
        mean = np.mean(X_array, axis=1, keepdims=True)
        std = np.std(X_array, axis=1, keepdims=True) + 1e-8
        normalized = (X_array - mean) / std
        features["agg_skew"] = np.mean(normalized**3, axis=1)
        features["agg_kurtosis"] = np.mean(normalized**4, axis=1) - 3

        return features

    def fit_transform(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Apply all numpy operations.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            DataFrame with all numpy-based features
        """
        all_features = []

        # Array features
        if self.config.get("array_features", True):
            array_features = self.create_array_features(X)
            if not array_features.empty:
                all_features.append(array_features)

        # Broadcasting features
        if self.config.get("broadcasting_features", True):
            broadcast_features = self.create_broadcasting_features(X)
            if not broadcast_features.empty:
                all_features.append(broadcast_features)

        # Matrix features
        if self.config.get("matrix_features", True):
            matrix_features = self.create_matrix_features(X)
            if not matrix_features.empty:
                all_features.append(matrix_features)

        # Math features
        if self.config.get("math_features", True):
            math_features = self.create_math_features(X)
            if not math_features.empty:
                all_features.append(math_features)

        # Aggregation features
        if self.config.get("aggregation_features", True):
            agg_features = self.create_aggregation_features(X)
            if not agg_features.empty:
                all_features.append(agg_features)

        if all_features:
            result = pd.concat(all_features, axis=1)
            result = result.loc[:, ~result.columns.duplicated()]
            return result

        return pd.DataFrame(index=X.index)
