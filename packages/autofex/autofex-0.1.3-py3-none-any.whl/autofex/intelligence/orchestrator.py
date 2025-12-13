"""
Intelligent Feature Engineering Orchestrator

Automatically selects and combines the best feature engineering techniques
based on data characteristics and target variable.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
import warnings

try:
    from ..mathematical.modeling import MathematicalModelingEngine
    from ..statistical.advanced_transforms import StatisticalTransforms
    from ..pandas_advanced.operations import PandasOperations
    from ..numpy_advanced.operations import NumpyOperations
    from ..scipy_advanced.operations import ScipyOperations
    from ..feature_engineering import FeatureEngineer

    _ALL_MODULES_AVAILABLE = True
except ImportError:
    _ALL_MODULES_AVAILABLE = False
    # Suppress warning during import - it's expected for optional modules
    # Warning will be shown when actually using the orchestrator if needed


class IntelligentOrchestrator:
    """
    Intelligent orchestrator that automatically selects and combines
    the best feature engineering techniques.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize intelligent orchestrator.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.auto_detect = self.config.get("auto_detect", True)
        self.max_features = self.config.get("max_features", 1000)
        self.quality_threshold = self.config.get("quality_threshold", 0.1)

    def analyze_data_characteristics(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        Analyze data characteristics to determine best feature engineering approach.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            Dictionary with data characteristics and recommendations
        """
        characteristics = {
            "n_samples": len(X),
            "n_features": X.shape[1],
            "numeric_count": len(X.select_dtypes(include=[np.number]).columns),
            "categorical_count": len(
                X.select_dtypes(include=["object", "category"]).columns
            ),
            "datetime_count": 0,
            "string_count": 0,
            "missing_percent": (X.isnull().sum().sum() / (X.shape[0] * X.shape[1]))
            * 100,
            "high_cardinality": [],
            "skewed_features": [],
            "recommendations": [],
        }

        # Detect datetime columns
        for col in X.columns:
            if pd.api.types.is_datetime64_any_dtype(X[col]):
                characteristics["datetime_count"] += 1
            elif X[col].dtype == "object":
                try:
                    pd.to_datetime(X[col], errors="raise")
                    characteristics["datetime_count"] += 1
                except Exception:
                    characteristics["string_count"] += 1

        # Detect high cardinality
        for col in X.select_dtypes(include=["object", "category"]).columns:
            if X[col].nunique() > 50:
                characteristics["high_cardinality"].append(col)

        # Detect skewed features
        for col in X.select_dtypes(include=[np.number]).columns:
            skew = X[col].skew()
            if abs(skew) > 1:
                characteristics["skewed_features"].append((col, skew))

        # Generate recommendations
        if characteristics["datetime_count"] > 0:
            characteristics["recommendations"].append("Use datetime features")
        if characteristics["string_count"] > 0:
            characteristics["recommendations"].append("Use string features")
        if len(characteristics["skewed_features"]) > 0:
            characteristics["recommendations"].append("Apply power transformations")
        if characteristics["numeric_count"] > 10:
            characteristics["recommendations"].append(
                "Use PCA for dimensionality reduction"
            )
        if len(characteristics["high_cardinality"]) > 0:
            characteristics["recommendations"].append(
                "Use target encoding for high cardinality"
            )

        return characteristics

    def intelligent_feature_engineering(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Intelligently engineer features based on data characteristics.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            DataFrame with intelligently engineered features
        """
        if not _ALL_MODULES_AVAILABLE:
            warnings.warn("Not all modules available. Using basic feature engineering.")
            return X

        # Analyze data
        characteristics = self.analyze_data_characteristics(X, y)

        all_features = [X.copy()]

        # 1. Statistical transforms for skewed data
        if len(characteristics["skewed_features"]) > 0:
            try:
                stat_transforms = StatisticalTransforms()
                transformed = stat_transforms.apply_all_transforms(X)
                if not transformed.empty:
                    all_features.append(transformed)
            except Exception as e:
                warnings.warn(f"Statistical transforms failed: {e}")

        # 2. Pandas operations for datetime and strings
        if characteristics["datetime_count"] > 0 or characteristics["string_count"] > 0:
            try:
                pandas_ops = PandasOperations(
                    {
                        "datetime_features": characteristics["datetime_count"] > 0,
                        "string_features": characteristics["string_count"] > 0,
                        "window_features": True,
                    }
                )
                pandas_features = pandas_ops.fit_transform(X)
                if not pandas_features.empty:
                    all_features.append(pandas_features)
            except Exception as e:
                warnings.warn(f"Pandas operations failed: {e}")

        # 3. Mathematical modeling for high-dimensional data
        if characteristics["numeric_count"] > 10:
            try:
                math_engine = MathematicalModelingEngine(
                    {
                        "pca_features": True,
                        "polynomial_features": True,
                        "n_components_pca": min(
                            5, characteristics["numeric_count"] // 2
                        ),
                    }
                )
                math_features = math_engine.fit_transform(X, y)
                if not math_features.empty:
                    all_features.append(math_features)
            except Exception as e:
                warnings.warn(f"Mathematical modeling failed: {e}")

        # 4. Numpy operations for array-wide features
        if characteristics["numeric_count"] >= 3:
            try:
                numpy_ops = NumpyOperations(
                    {
                        "array_features": True,
                        "aggregation_features": True,
                    }
                )
                numpy_features = numpy_ops.fit_transform(X)
                if not numpy_features.empty:
                    all_features.append(numpy_features)
            except Exception as e:
                warnings.warn(f"Numpy operations failed: {e}")

        # 5. Advanced feature engineering
        try:
            advanced_fe = FeatureEngineer(
                {
                    "statistical_aggregations": True,
                    "cross_features": True,
                }
            )
            advanced_features = advanced_fe.fit_transform(X, y)
            if not advanced_features.empty:
                all_features.append(advanced_features)
        except Exception as e:
            warnings.warn(f"Advanced feature engineering failed: {e}")

        # Combine all features
        if len(all_features) > 1:
            result = pd.concat(all_features, axis=1)
            result = result.loc[:, ~result.columns.duplicated()]
            return result

        return X

    def fit_transform(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Intelligently engineer features.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            DataFrame with engineered features
        """
        return self.intelligent_feature_engineering(X, y)
