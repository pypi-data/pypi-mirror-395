"""
Feature Engineering Techniques

This module introduces a collection of higher-level feature engineering methods, including:

- Statistical aggregations and summary metrics
- Time-series–oriented feature generation
- Binning and discretization strategies
- Cross-feature interaction construction
- Domain-specific transformation routines

These tools expand the core feature engineering pipeline with richer and more adaptable transformations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from scipy import stats
from sklearn.preprocessing import KBinsDiscretizer
import warnings


class FeatureEngineer:
    """
    Feature engineering with statistical aggregations,
    time-series features, and domain-specific transformations.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize feature engineer.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.enable_statistical_agg = self.config.get("statistical_aggregations", True)
        self.enable_time_series = self.config.get("time_series_features", True)
        self.enable_binning = self.config.get("advanced_binning", True)
        self.enable_cross_features = self.config.get("cross_features", True)
        self.n_bins = self.config.get("n_bins", 5)

    def create_statistical_aggregations(
        self, X: pd.DataFrame, group_by: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Create statistical aggregation features.

        Args:
            X: Input features
            group_by: Columns to group by (if None, creates global aggregations)

        Returns:
            DataFrame with aggregation features
        """
        features = []

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if group_by and all(col in X.columns for col in group_by):
            # Group-based aggregations
            for col in numeric_cols:
                if col not in group_by:
                    grouped = X.groupby(group_by)[col]
                    features.append(
                        pd.DataFrame(
                            {
                                f"{col}_group_mean": grouped.transform("mean"),
                                f"{col}_group_std": grouped.transform("std"),
                                f"{col}_group_min": grouped.transform("min"),
                                f"{col}_group_max": grouped.transform("max"),
                                f"{col}_group_median": grouped.transform("median"),
                            }
                        )
                    )
        else:
            # Global aggregations across rows
            for col in numeric_cols:
                col_data = X[col].dropna()
                if len(col_data) > 0:
                    features.append(
                        pd.DataFrame(
                            {
                                f"{col}_global_mean": [col_data.mean()] * len(X),
                                f"{col}_global_std": [col_data.std()] * len(X),
                                f"{col}_global_min": [col_data.min()] * len(X),
                                f"{col}_global_max": [col_data.max()] * len(X),
                            },
                            index=X.index,
                        )
                    )

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_time_series_features(
        self, X: pd.DataFrame, time_column: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Create time-series features (lags, rolling stats, differences).

        Args:
            X: Input features
            time_column: Name of time column (if None, uses index)

        Returns:
            DataFrame with time-series features
        """
        features = []

        if time_column and time_column in X.columns:
            X_sorted = X.sort_values(time_column)
        else:
            X_sorted = X.copy()

        numeric_cols = X_sorted.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if col == time_column:
                continue

            series = X_sorted[col]

            # Lag features
            for lag in [1, 2, 3, 7]:
                if len(series) > lag:
                    lag_feature = series.shift(lag)
                    features.append(
                        pd.DataFrame(
                            {f"{col}_lag_{lag}": lag_feature}, index=X_sorted.index
                        )
                    )

            # Rolling statistics
            for window in [3, 7, 14]:
                if len(series) >= window:
                    rolling = series.rolling(window=window, min_periods=1)
                    features.append(
                        pd.DataFrame(
                            {
                                f"{col}_rolling_mean_{window}": rolling.mean(),
                                f"{col}_rolling_std_{window}": rolling.std(),
                            },
                            index=X_sorted.index,
                        )
                    )

            # Differences
            if len(series) > 1:
                diff1 = series.diff(1)
                diff7 = (
                    series.diff(7) if len(series) > 7 else pd.Series(index=series.index)
                )
                features.append(
                    pd.DataFrame(
                        {
                            f"{col}_diff_1": diff1,
                            f"{col}_diff_7": diff7,
                        },
                        index=X_sorted.index,
                    )
                )

        if features:
            result = pd.concat(features, axis=1)
            # Reorder to match original index
            if time_column:
                result = result.reindex(X.index)
            return result

        return pd.DataFrame(index=X.index)

    def create_advanced_binning(
        self, X: pd.DataFrame, strategy: str = "quantile"
    ) -> pd.DataFrame:
        """
        Create advanced binning features.

        Args:
            X: Input features
            strategy: Binning strategy ('quantile', 'uniform', 'kmeans')

        Returns:
            DataFrame with binned features
        """
        features = []

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            try:
                discretizer_params = {
                    "n_bins": self.n_bins,
                    "encode": "ordinal",
                    "strategy": strategy,
                }
                # Suppress FutureWarning for quantile_method in sklearn >= 1.3
                if strategy == "quantile":
                    discretizer_params["quantile_method"] = "averaged_inverted_cdf"
                discretizer = KBinsDiscretizer(**discretizer_params)
                binned = discretizer.fit_transform(X[[col]])
                features.append(
                    pd.DataFrame(
                        {f"{col}_binned_{strategy}": binned.flatten()}, index=X.index
                    )
                )

                # Also create one-hot encoded bins
                binned_onehot = pd.get_dummies(
                    pd.Series(binned.flatten(), index=X.index, name=f"{col}_binned")
                )
                features.append(binned_onehot)

            except Exception as e:
                warnings.warn(f"Binning failed for {col}: {e}")
                continue

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_cross_features(
        self, X: pd.DataFrame, max_interactions: int = 10
    ) -> pd.DataFrame:
        """
        Create intelligent cross-feature interactions.

        Args:
            X: Input features
            max_interactions: Maximum number of interactions to create

        Returns:
            DataFrame with cross-feature interactions
        """
        features = []

        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) < 2:
            return pd.DataFrame(index=X.index)

        # Create ratio features (division)
        for i, col1 in enumerate(numeric_cols[:max_interactions]):
            for col2 in numeric_cols[i + 1 : i + max_interactions]:
                if col1 != col2:
                    # Ratio
                    ratio = X[col1] / (X[col2] + 1e-8)
                    features.append(
                        pd.DataFrame({f"{col1}_div_{col2}": ratio}, index=X.index)
                    )

                    # Product
                    product = X[col1] * X[col2]
                    features.append(
                        pd.DataFrame({f"{col1}_mul_{col2}": product}, index=X.index)
                    )

                    # Sum
                    sum_feat = X[col1] + X[col2]
                    features.append(
                        pd.DataFrame({f"{col1}_add_{col2}": sum_feat}, index=X.index)
                    )

                    # Difference
                    diff = X[col1] - X[col2]
                    features.append(
                        pd.DataFrame({f"{col1}_sub_{col2}": diff}, index=X.index)
                    )

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_rank_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create rank-based features.

        Args:
            X: Input features

        Returns:
            DataFrame with rank features
        """
        features = []

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            # Percentile rank
            rank_pct = X[col].rank(pct=True)
            features.append(pd.DataFrame({f"{col}_rank_pct": rank_pct}, index=X.index))

            # Standard rank
            rank = X[col].rank()
            features.append(pd.DataFrame({f"{col}_rank": rank}, index=X.index))

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_polynomial_features_advanced(
        self, X: pd.DataFrame, degree: int = 3, interaction_only: bool = False
    ) -> pd.DataFrame:
        """
        Create advanced polynomial features with better selection.

        Args:
            X: Input features
            degree: Polynomial degree
            interaction_only: Only interaction terms

        Returns:
            DataFrame with polynomial features
        """
        from sklearn.preprocessing import PolynomialFeatures

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return pd.DataFrame(index=X.index)

        # Limit to top correlated features to avoid explosion
        if len(numeric_cols) > 10:
            # Select top 10 features by variance
            variances = X[numeric_cols].var()
            top_cols = variances.nlargest(10).index.tolist()
            numeric_cols = top_cols

        try:
            poly = PolynomialFeatures(
                degree=degree, interaction_only=interaction_only, include_bias=False
            )

            X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())
            poly_features = poly.fit_transform(X_numeric)
            feature_names = poly.get_feature_names_out(numeric_cols)

            # Create DataFrame
            poly_df = pd.DataFrame(poly_features, columns=feature_names, index=X.index)

            # Remove original features (keep only new ones)
            new_features = [col for col in poly_df.columns if col not in numeric_cols]

            return poly_df[new_features]

        except Exception as e:
            warnings.warn(f"Polynomial features failed: {e}")
            return pd.DataFrame(index=X.index)

    def create_domain_features(
        self, X: pd.DataFrame, domain: str = "general"
    ) -> pd.DataFrame:
        """
        Create domain-specific features.

        Args:
            X: Input features
            domain: Domain type ('general', 'financial', 'temporal', 'spatial')

        Returns:
            DataFrame with domain-specific features
        """
        features = []

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if domain == "financial":
            # Financial domain features
            for col in numeric_cols:
                # Returns
                returns = X[col].pct_change()
                features.append(
                    pd.DataFrame({f"{col}_returns": returns}, index=X.index)
                )

                # Volatility (rolling std of returns)
                if len(returns) > 7:
                    volatility = returns.rolling(7).std()
                    features.append(
                        pd.DataFrame({f"{col}_volatility": volatility}, index=X.index)
                    )

        elif domain == "spatial":
            # Spatial features (if lat/lon present)
            lat_cols = [col for col in X.columns if "lat" in col.lower()]
            lon_cols = [col for col in X.columns if "lon" in col.lower()]

            if lat_cols and lon_cols:
                lat = X[lat_cols[0]]
                lon = X[lon_cols[0]]

                # Distance from origin
                distance = np.sqrt(lat**2 + lon**2)
                features.append(
                    pd.DataFrame({"distance_from_origin": distance}, index=X.index)
                )

        elif domain == "temporal":
            # Temporal features
            for col in numeric_cols:
                # Cyclical encoding (if values are cyclical)
                if X[col].min() >= 0 and X[col].max() <= 365:
                    # Day of year encoding
                    sin_val = np.sin(2 * np.pi * X[col] / 365)
                    cos_val = np.cos(2 * np.pi * X[col] / 365)
                    features.append(
                        pd.DataFrame(
                            {
                                f"{col}_sin": sin_val,
                                f"{col}_cos": cos_val,
                            },
                            index=X.index,
                        )
                    )

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def fit_transform(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Apply all feature engineering techniques.

        Args:
            X: Input features
            y: Target variable (optional)

        Returns:
            DataFrame with all features
        """
        all_features = [X.copy()]

        if self.enable_statistical_agg:
            agg_features = self.create_statistical_aggregations(X)
            if not agg_features.empty:
                all_features.append(agg_features)

        if self.enable_time_series:
            ts_features = self.create_time_series_features(X)
            if not ts_features.empty:
                all_features.append(ts_features)

        if self.enable_binning:
            bin_features = self.create_advanced_binning(X)
            if not bin_features.empty:
                all_features.append(bin_features)

        if self.enable_cross_features:
            cross_features = self.create_cross_features(X)
            if not cross_features.empty:
                all_features.append(cross_features)

        # Always add rank features
        rank_features = self.create_rank_features(X)
        if not rank_features.empty:
            all_features.append(rank_features)

        # Combine all features
        result = pd.concat(all_features, axis=1)

        # Remove duplicate columns
        result = result.loc[:, ~result.columns.duplicated()]

        return result
