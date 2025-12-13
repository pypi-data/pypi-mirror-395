"""
Pandas Operations

Leverages pandas for data manipulation and feature engineering.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
import warnings


class PandasOperations:
    """
    Pandas-based feature engineering operations.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize pandas operations.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

    def create_window_features(
        self,
        X: pd.DataFrame,
        window_sizes: List[int] = [3, 7, 14, 30],
        functions: List[str] = ["mean", "std", "min", "max", "median"],
    ) -> pd.DataFrame:
        """
        Create rolling window features using pandas.

        Args:
            X: Input DataFrame
            window_sizes: List of window sizes
            functions: List of aggregation functions

        Returns:
            DataFrame with window features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col]

            for window in window_sizes:
                if len(series) < window:
                    continue

                rolling = series.rolling(window=window, min_periods=1)

                for func in functions:
                    if hasattr(rolling, func):
                        try:
                            result = getattr(rolling, func)()
                            features.append(
                                pd.DataFrame(
                                    {f"{col}_rolling_{window}_{func}": result},
                                    index=X.index,
                                )
                            )
                        except Exception:
                            pass

                # Expanding window
                expanding = series.expanding(min_periods=1)
                for func in functions:
                    if hasattr(expanding, func):
                        try:
                            result = getattr(expanding, func)()
                            features.append(
                                pd.DataFrame(
                                    {f"{col}_expanding_{func}": result},
                                    index=X.index,
                                )
                            )
                        except Exception:
                            pass

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_groupby_features(
        self,
        X: pd.DataFrame,
        group_cols: List[str],
        agg_functions: List[str] = ["mean", "std", "count", "min", "max"],
    ) -> pd.DataFrame:
        """
        Create groupby aggregation features.

        Args:
            X: Input DataFrame
            group_cols: Columns to group by
            agg_functions: Aggregation functions

        Returns:
            DataFrame with groupby features
        """
        if not group_cols or not all(col in X.columns for col in group_cols):
            return pd.DataFrame(index=X.index)

        numeric_cols = X.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col not in group_cols]

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        try:
            grouped = X.groupby(group_cols)[numeric_cols]

            for func in agg_functions:
                if hasattr(grouped, func):
                    try:
                        agg_result = getattr(grouped, func)()
                        # Merge back to original index
                        agg_result = agg_result.reset_index()
                        merged = X[group_cols].merge(
                            agg_result,
                            on=group_cols,
                            how="left",
                            suffixes=("", f"_{func}"),
                        )
                        # Select only new columns
                        new_cols = [col for col in merged.columns if f"_{func}" in col]
                        if new_cols:
                            features.append(merged[new_cols].set_index(X.index))
                    except Exception:
                        pass

            # Count per group
            try:
                count_result = (
                    X.groupby(group_cols).size().reset_index(name="group_count")
                )
                merged = X[group_cols].merge(count_result, on=group_cols, how="left")
                features.append(
                    pd.DataFrame({"group_count": merged["group_count"]}, index=X.index)
                )
            except Exception:
                pass

        except Exception as e:
            warnings.warn(f"Groupby features failed: {e}")

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_pivot_features(
        self,
        X: pd.DataFrame,
        index_col: str,
        columns_col: str,
        values_col: str,
    ) -> pd.DataFrame:
        """
        Create pivot table features.

        Args:
            X: Input DataFrame
            index_col: Column for index
            columns_col: Column for columns
            values_col: Column for values

        Returns:
            DataFrame with pivot features
        """
        if not all(col in X.columns for col in [index_col, columns_col, values_col]):
            return pd.DataFrame(index=X.index)

        try:
            pivot = X.pivot_table(
                index=index_col,
                columns=columns_col,
                values=values_col,
                aggfunc=["mean", "sum", "count"],
                fill_value=0,
            )

            # Flatten column names
            pivot.columns = [f"{col[0]}_{col[1]}" for col in pivot.columns]

            # Merge back to original index
            if index_col in X.columns:
                merged = X[[index_col]].merge(
                    pivot.reset_index(), on=index_col, how="left"
                )
                pivot_features = merged.drop(columns=[index_col]).set_index(X.index)
                return pivot_features

        except Exception as e:
            warnings.warn(f"Pivot features failed: {e}")

        return pd.DataFrame(index=X.index)

    def create_cross_tab_features(
        self,
        X: pd.DataFrame,
        col1: str,
        col2: str,
    ) -> pd.DataFrame:
        """
        Create crosstab features.

        Args:
            X: Input DataFrame
            col1: First categorical column
            col2: Second categorical column

        Returns:
            DataFrame with crosstab features
        """
        if col1 not in X.columns or col2 not in X.columns:
            return pd.DataFrame(index=X.index)

        try:
            crosstab = pd.crosstab(X[col1], X[col2], normalize="index")
            crosstab = crosstab.reset_index()

            # Merge back
            merged = X[[col1]].merge(crosstab, on=col1, how="left")
            crosstab_features = merged.drop(columns=[col1]).set_index(X.index)
            return crosstab_features

        except Exception as e:
            warnings.warn(f"Crosstab features failed: {e}")

        return pd.DataFrame(index=X.index)

    def create_datetime_features(
        self,
        X: pd.DataFrame,
        date_cols: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Create datetime features from date columns.

        Args:
            X: Input DataFrame
            date_cols: List of date column names (None = auto-detect)

        Returns:
            DataFrame with datetime features
        """
        if date_cols is None:
            # Auto-detect datetime columns
            date_cols = []
            for col in X.columns:
                if pd.api.types.is_datetime64_any_dtype(X[col]):
                    date_cols.append(col)
                else:
                    # Try to parse as datetime
                    try:
                        pd.to_datetime(X[col], errors="raise")
                        date_cols.append(col)
                    except Exception:
                        pass

        if not date_cols:
            return pd.DataFrame(index=X.index)

        features = []

        for col in date_cols:
            try:
                if not pd.api.types.is_datetime64_any_dtype(X[col]):
                    dt_series = pd.to_datetime(X[col], errors="coerce")
                else:
                    dt_series = X[col]

                dt_features = pd.DataFrame(index=X.index)

                # Extract components
                dt_features[f"{col}_year"] = dt_series.dt.year
                dt_features[f"{col}_month"] = dt_series.dt.month
                dt_features[f"{col}_day"] = dt_series.dt.day
                dt_features[f"{col}_dayofweek"] = dt_series.dt.dayofweek
                dt_features[f"{col}_dayofyear"] = dt_series.dt.dayofyear
                dt_features[f"{col}_week"] = dt_series.dt.isocalendar().week
                dt_features[f"{col}_quarter"] = dt_series.dt.quarter
                dt_features[f"{col}_is_weekend"] = (dt_series.dt.dayofweek >= 5).astype(
                    int
                )

                # Cyclical encoding
                dt_features[f"{col}_month_sin"] = np.sin(
                    2 * np.pi * dt_series.dt.month / 12
                )
                dt_features[f"{col}_month_cos"] = np.cos(
                    2 * np.pi * dt_series.dt.month / 12
                )
                dt_features[f"{col}_dayofweek_sin"] = np.sin(
                    2 * np.pi * dt_series.dt.dayofweek / 7
                )
                dt_features[f"{col}_dayofweek_cos"] = np.cos(
                    2 * np.pi * dt_series.dt.dayofweek / 7
                )

                # Time since reference
                if len(dt_series.dropna()) > 0:
                    reference_date = dt_series.min()
                    dt_features[f"{col}_days_since_ref"] = (
                        dt_series - reference_date
                    ).dt.days

                features.append(dt_features)

            except Exception as e:
                warnings.warn(f"Datetime features failed for {col}: {e}")

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_string_features(
        self,
        X: pd.DataFrame,
        string_cols: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Create features from string columns.

        Args:
            X: Input DataFrame
            string_cols: List of string column names (None = auto-detect)

        Returns:
            DataFrame with string features
        """
        if string_cols is None:
            string_cols = X.select_dtypes(include=["object"]).columns.tolist()

        if not string_cols:
            return pd.DataFrame(index=X.index)

        features = []

        for col in string_cols:
            if not X[col].dtype == "object":
                continue

            series = X[col].astype(str)
            col_features = pd.DataFrame(index=X.index)

            # Basic string features
            col_features[f"{col}_length"] = series.str.len()
            col_features[f"{col}_word_count"] = series.str.split().str.len()
            col_features[f"{col}_char_count"] = series.str.replace(" ", "").str.len()
            col_features[f"{col}_uppercase_count"] = series.str.findall(
                r"[A-Z]"
            ).str.len()
            col_features[f"{col}_lowercase_count"] = series.str.findall(
                r"[a-z]"
            ).str.len()
            col_features[f"{col}_digit_count"] = series.str.findall(r"\d").str.len()
            col_features[f"{col}_special_count"] = series.str.findall(
                r"[^a-zA-Z0-9\s]"
            ).str.len()

            # Pattern features
            col_features[f"{col}_has_email"] = series.str.contains(
                r"@", na=False
            ).astype(int)
            col_features[f"{col}_has_url"] = series.str.contains(
                r"http", na=False
            ).astype(int)
            col_features[f"{col}_has_phone"] = series.str.contains(
                r"\d{3}-\d{3}-\d{4}", na=False
            ).astype(int)

            # N-grams (simple version)
            try:
                words = series.str.split()
                col_features[f"{col}_avg_word_length"] = words.apply(
                    lambda x: np.mean([len(w) for w in x]) if x else 0
                )
            except Exception:
                pass

            features.append(col_features)

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_cumulative_features(
        self,
        X: pd.DataFrame,
        sort_col: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Create cumulative features.

        Args:
            X: Input DataFrame
            sort_col: Column to sort by (None = use index)

        Returns:
            DataFrame with cumulative features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        if sort_col and sort_col in X.columns:
            X_sorted = X.sort_values(sort_col)
        else:
            X_sorted = X

        features = []

        for col in numeric_cols:
            series = X_sorted[col]

            # Cumulative sum
            features.append(
                pd.DataFrame(
                    {f"{col}_cumsum": series.cumsum()},
                    index=X_sorted.index,
                )
            )

            # Cumulative product
            try:
                features.append(
                    pd.DataFrame(
                        {f"{col}_cumprod": series.cumprod()},
                        index=X_sorted.index,
                    )
                )
            except Exception:
                pass

            # Cumulative max/min
            features.append(
                pd.DataFrame(
                    {f"{col}_cummax": series.cummax()},
                    index=X_sorted.index,
                )
            )
            features.append(
                pd.DataFrame(
                    {f"{col}_cummin": series.cummin()},
                    index=X_sorted.index,
                )
            )

        if features:
            result = pd.concat(features, axis=1)
            # Reorder to match original index
            result = result.reindex(X.index)
            return result
        return pd.DataFrame(index=X.index)

    def create_diff_features(
        self,
        X: pd.DataFrame,
        periods: List[int] = [1, 2, 3, 7],
    ) -> pd.DataFrame:
        """
        Create difference features.

        Args:
            X: Input DataFrame
            periods: List of periods for differencing

        Returns:
            DataFrame with difference features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col]

            for period in periods:
                if len(series) > period:
                    # Forward difference
                    diff = series.diff(periods=period)
                    features.append(
                        pd.DataFrame(
                            {f"{col}_diff_{period}": diff},
                            index=X.index,
                        )
                    )

                    # Percentage change
                    pct_change = series.pct_change(periods=period)
                    features.append(
                        pd.DataFrame(
                            {f"{col}_pct_change_{period}": pct_change},
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
        Apply all pandas operations.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            DataFrame with all pandas-based features
        """
        all_features = []

        # Window features
        if self.config.get("window_features", True):
            window_features = self.create_window_features(X)
            if not window_features.empty:
                all_features.append(window_features)

        # Datetime features
        if self.config.get("datetime_features", True):
            datetime_features = self.create_datetime_features(X)
            if not datetime_features.empty:
                all_features.append(datetime_features)

        # String features
        if self.config.get("string_features", True):
            string_features = self.create_string_features(X)
            if not string_features.empty:
                all_features.append(string_features)

        # Cumulative features
        if self.config.get("cumulative_features", True):
            cumulative_features = self.create_cumulative_features(X)
            if not cumulative_features.empty:
                all_features.append(cumulative_features)

        # Difference features
        if self.config.get("diff_features", True):
            diff_features = self.create_diff_features(X)
            if not diff_features.empty:
                all_features.append(diff_features)

        if all_features:
            result = pd.concat(all_features, axis=1)
            result = result.loc[:, ~result.columns.duplicated()]
            return result

        return pd.DataFrame(index=X.index)
