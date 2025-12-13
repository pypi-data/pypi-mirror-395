"""
Statistical Transformations

Leverages scipy.stats and numpy for statistical feature engineering.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from scipy import stats
from scipy.special import boxcox, logit, expit
from scipy.stats import yeojohnson
import warnings


class StatisticalTransforms:
    """
    Statistical transformations using scipy and numpy.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize statistical transforms.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

    def boxcox_transform(
        self, series: pd.Series, lmbda: Optional[float] = None
    ) -> pd.Series:
        """
        Apply Box-Cox transformation for normality.

        Args:
            series: Input series
            lmbda: Lambda parameter (None = optimize)

        Returns:
            Transformed series
        """
        series_clean = series.dropna()

        if len(series_clean) < 3:
            return pd.Series(index=series.index)

        # Box-Cox requires positive values
        if (series_clean <= 0).any():
            # Shift to make positive
            series_positive = series_clean - series_clean.min() + 1
        else:
            series_positive = series_clean

        try:
            if lmbda is None:
                transformed, lmbda_opt = stats.boxcox(series_positive)
            else:
                transformed = boxcox(series_positive, lmbda)
                lmbda_opt = lmbda

            result = pd.Series(index=series.index, dtype=float)
            result.loc[series_clean.index] = transformed
            return result
        except Exception as e:
            warnings.warn(f"Box-Cox transformation failed: {e}")
            return pd.Series(index=series.index)

    def yeojohnson_transform(
        self, series: pd.Series, lmbda: Optional[float] = None
    ) -> pd.Series:
        """
        Apply Yeo-Johnson transformation (works with negative values).

        Args:
            series: Input series
            lmbda: Lambda parameter (None = optimize)

        Returns:
            Transformed series
        """
        series_clean = series.dropna()

        if len(series_clean) < 3:
            return pd.Series(index=series.index)

        try:
            if lmbda is None:
                transformed, lmbda_opt = yeojohnson(series_clean)
            else:
                transformed, lmbda_opt = yeojohnson(series_clean, lmbda=lmbda)

            result = pd.Series(index=series.index, dtype=float)
            result.loc[series_clean.index] = transformed
            return result
        except Exception as e:
            warnings.warn(f"Yeo-Johnson transformation failed: {e}")
            return pd.Series(index=series.index)

    def quantile_transform(
        self, series: pd.Series, output_distribution: str = "uniform"
    ) -> pd.Series:
        """
        Apply quantile transformation to uniform or normal distribution.

        Args:
            series: Input series
            output_distribution: 'uniform' or 'normal'

        Returns:
            Transformed series
        """
        from sklearn.preprocessing import QuantileTransformer

        series_clean = series.dropna()

        if len(series_clean) < 3:
            return pd.Series(index=series.index)

        try:
            qt = QuantileTransformer(
                output_distribution=output_distribution,
                random_state=42,
            )
            transformed = qt.fit_transform(series_clean.values.reshape(-1, 1)).flatten()

            result = pd.Series(index=series.index, dtype=float)
            result.loc[series_clean.index] = transformed
            return result
        except Exception as e:
            warnings.warn(f"Quantile transformation failed: {e}")
            return pd.Series(index=series.index)

    def power_transform(
        self, series: pd.Series, method: str = "yeo-johnson"
    ) -> pd.Series:
        """
        Apply power transformation.

        Args:
            series: Input series
            method: 'yeo-johnson' or 'box-cox'

        Returns:
            Transformed series
        """
        from sklearn.preprocessing import PowerTransformer

        series_clean = series.dropna()

        if len(series_clean) < 3:
            return pd.Series(index=series.index)

        try:
            pt = PowerTransformer(method=method, standardize=False)
            transformed = pt.fit_transform(series_clean.values.reshape(-1, 1)).flatten()

            result = pd.Series(index=series.index, dtype=float)
            result.loc[series_clean.index] = transformed
            return result
        except Exception as e:
            warnings.warn(f"Power transformation failed: {e}")
            return pd.Series(index=series.index)

    def rank_transform(self, series: pd.Series, method: str = "average") -> pd.Series:
        """
        Apply rank transformation.

        Args:
            series: Input series
            method: Ranking method ('average', 'min', 'max', 'dense', 'ordinal')

        Returns:
            Ranked series
        """
        return series.rank(method=method, pct=True)

    def zscore_transform(self, series: pd.Series) -> pd.Series:
        """
        Apply z-score transformation.

        Args:
            series: Input series

        Returns:
            Z-score transformed series
        """
        return (series - series.mean()) / (series.std() + 1e-8)

    def robust_scale_transform(self, series: pd.Series) -> pd.Series:
        """
        Apply robust scaling (using median and IQR).

        Args:
            series: Input series

        Returns:
            Robust scaled series
        """
        median = series.median()
        iqr = series.quantile(0.75) - series.quantile(0.25)
        return (series - median) / (iqr + 1e-8)

    def create_statistical_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create comprehensive statistical features.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with statistical features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        features = []

        for col in numeric_cols:
            series = X[col]
            col_features = {}

            # Basic statistics
            col_features[f"{col}_mean"] = series.mean()
            col_features[f"{col}_std"] = series.std()
            col_features[f"{col}_median"] = series.median()
            col_features[f"{col}_mad"] = (
                (series - series.median()).abs().median()
            )  # MAD
            col_features[f"{col}_iqr"] = series.quantile(0.75) - series.quantile(0.25)

            # Percentiles
            for p in [10, 25, 50, 75, 90, 95, 99]:
                col_features[f"{col}_p{p}"] = series.quantile(p / 100)

            # Higher moments
            col_features[f"{col}_skew"] = series.skew()
            col_features[f"{col}_kurtosis"] = series.kurtosis()

            # Range statistics
            col_features[f"{col}_range"] = series.max() - series.min()
            col_features[f"{col}_coef_var"] = series.std() / (series.mean() + 1e-8)

            # Distribution tests
            try:
                _, p_value = stats.normaltest(series.dropna())
                col_features[f"{col}_normality_p"] = p_value
            except Exception:
                pass

            # Outlier counts (IQR method)
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            outliers = ((series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))).sum()
            col_features[f"{col}_outlier_count"] = outliers

            features.append(pd.DataFrame(col_features, index=[X.index[0]]))

        if features:
            result = pd.concat(features, axis=1)
            if len(result) == 1:
                result = result.reindex(X.index, method="ffill")
            return result
        return pd.DataFrame(index=X.index)

    def create_correlation_features(
        self, X: pd.DataFrame, method: str = "pearson"
    ) -> pd.DataFrame:
        """
        Create correlation-based features.

        Args:
            X: Input DataFrame
            method: Correlation method ('pearson', 'spearman', 'kendall')

        Returns:
            DataFrame with correlation features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return pd.DataFrame(index=X.index)

        corr_matrix = X[numeric_cols].corr(method=method)

        features = []

        for col in numeric_cols:
            col_corrs = corr_matrix[col].drop(col)
            if len(col_corrs) > 0:
                features.append(
                    pd.DataFrame(
                        {
                            f"{col}_max_corr": [col_corrs.abs().max()],
                            f"{col}_mean_corr": [col_corrs.abs().mean()],
                            f"{col}_min_corr": [col_corrs.abs().min()],
                        },
                        index=[X.index[0]],
                    )
                )

        if features:
            result = pd.concat(features, axis=1)
            if len(result) == 1:
                result = result.reindex(X.index, method="ffill")
            return result
        return pd.DataFrame(index=X.index)

    def apply_all_transforms(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all statistical transformations.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with all transformed features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        all_features = []

        for col in numeric_cols:
            series = X[col]
            col_transforms = {}

            # Box-Cox
            try:
                boxcox_transformed = self.boxcox_transform(series)
                if not boxcox_transformed.empty:
                    col_transforms[f"{col}_boxcox"] = boxcox_transformed
            except Exception:
                pass

            # Yeo-Johnson
            try:
                yj_transformed = self.yeojohnson_transform(series)
                if not yj_transformed.empty:
                    col_transforms[f"{col}_yeojohnson"] = yj_transformed
            except Exception:
                pass

            # Quantile transform
            try:
                qt_uniform = self.quantile_transform(series, "uniform")
                if not qt_uniform.empty:
                    col_transforms[f"{col}_quantile_uniform"] = qt_uniform

                qt_normal = self.quantile_transform(series, "normal")
                if not qt_normal.empty:
                    col_transforms[f"{col}_quantile_normal"] = qt_normal
            except Exception:
                pass

            # Rank transform
            col_transforms[f"{col}_rank"] = self.rank_transform(series)

            # Z-score
            col_transforms[f"{col}_zscore"] = self.zscore_transform(series)

            # Robust scale
            col_transforms[f"{col}_robust_scale"] = self.robust_scale_transform(series)

            if col_transforms:
                all_features.append(pd.DataFrame(col_transforms, index=X.index))

        if all_features:
            return pd.concat(all_features, axis=1)
        return pd.DataFrame(index=X.index)
