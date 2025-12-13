"""
Feature Benchmarking Engine

Automatically benchmarks different feature sets and models to find optimal configurations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)
from sklearn.feature_selection import (
    SelectKBest,
    f_classif,
    f_regression,
    mutual_info_classif,
    mutual_info_regression,
)
import time
import warnings


class FeatureBenchmarker:
    """
    Automated benchmarking system for feature sets.

    Compares different feature engineering strategies, performs ablation studies,
    and provides performance metrics across multiple models.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize feature benchmarker.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.cv_folds = self.config.get("cv_folds", 5)
        self.scoring_metrics = self.config.get(
            "scoring_metrics", ["accuracy", "f1", "roc_auc"]
        )
        self.models = self.config.get("models", ["rf", "lr"])
        self.random_state = self.config.get("random_state", 42)
        self.n_feature_steps = self.config.get("n_feature_steps", 10)

        # Initialize models
        self.model_configs = {
            "rf": {
                "classifier": RandomForestClassifier(
                    n_estimators=100, random_state=self.random_state
                ),
                "regressor": RandomForestRegressor(
                    n_estimators=100, random_state=self.random_state
                ),
            },
            "lr": {
                "classifier": LogisticRegression(
                    random_state=self.random_state, max_iter=1000
                ),
                "regressor": LinearRegression(),
            },
        }

    def benchmark_features(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        X_test: Optional[pd.DataFrame] = None,
        feature_sets: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Benchmark different feature sets against multiple models.

        Args:
            X: Training features
            y: Training target
            X_test: Test features (optional)
            feature_sets: Custom feature sets to test (optional)

        Returns:
            Dictionary containing benchmarking results
        """
        is_classification = self._is_classification_target(y)

        # Default feature sets if none provided
        if feature_sets is None:
            feature_sets = self._get_default_feature_sets(X, y, is_classification)

        results: Dict[str, Any] = {
            "feature_sets": [],
            "model_comparison": {},
            "feature_importance": {},
            "ablation_study": {},
            "best_configurations": {},
        }

        # Benchmark each feature set
        for feature_set in feature_sets:
            set_name = feature_set["name"]
            features = feature_set["features"]

            if len(features) == 0:
                continue

            X_subset = (X[features] if isinstance(features, list) else X).copy()
            # Basic imputation handling mixed data types
            for col in X_subset.columns:
                if pd.api.types.is_numeric_dtype(X_subset[col]):
                    X_subset.loc[:, col] = X_subset[col].fillna(X_subset[col].mean())
                else:
                    mode_val = (
                        X_subset[col].mode().iloc[0]
                        if not X_subset[col].mode().empty
                        else "Unknown"
                    )
                    X_subset.loc[:, col] = X_subset[col].fillna(mode_val)

            # Encode categorical columns before passing to sklearn
            X_subset = self._encode_categorical(X_subset)

            set_results = self._benchmark_single_set(
                X_subset, y, set_name, is_classification
            )

            if X_test is not None:
                X_test_subset = (
                    X_test[features] if isinstance(features, list) else X_test
                )
                # Basic imputation handling mixed data types
                for col in X_test_subset.columns:
                    if X_test_subset[col].dtype in ["int64", "float64"]:
                        X_test_subset[col] = X_test_subset[col].fillna(
                            X_test_subset[col].mean()
                        )
                    else:
                        X_test_subset[col] = X_test_subset[col].fillna(
                            X_test_subset[col].mode().iloc[0]
                            if not X_test_subset[col].mode().empty
                            else "Unknown"
                        )
                # Test performance evaluation requires y_test which is not available
                # set_results["test_performance"] = self._evaluate_on_test(
                #     X_subset, y, X_test_subset, y_test, is_classification
                # )

            results["feature_sets"].append(set_results)

        # Overall model comparison
        results["model_comparison"] = self._compare_models_across_sets(
            results["feature_sets"], is_classification
        )

        # Feature importance analysis
        results["feature_importance"] = self.get_feature_importance(X, y)

        # Ablation study
        results["ablation_study"] = self._perform_ablation_study(
            X, y, is_classification
        )

        # Best configurations
        results["best_configurations"] = self._identify_best_configurations(results)

        return results

    def _benchmark_single_set(
        self, X: pd.DataFrame, y: pd.Series, set_name: str, is_classification: bool
    ) -> Dict[str, Any]:
        """
        Benchmark a single feature set across multiple models.
        """
        results = {
            "name": set_name,
            "n_features": X.shape[1],
            "models": {},
            "cross_validation": {},
        }

        # Cross-validation setup - adjust based on sample size
        n_samples = len(X)
        if is_classification:
            # For stratified CV, need at least n_splits samples per class
            min_class_size = (
                y.value_counts().min() if len(y.value_counts()) > 0 else n_samples
            )
            n_splits = (
                min(self.cv_folds, min_class_size, n_samples // 2)
                if n_samples >= 2
                else 1
            )
            if n_splits < 2:
                # Skip CV if not enough samples
                warnings.warn(
                    f"Insufficient samples ({n_samples}) for cross-validation. Skipping {set_name}."
                )
                results["models"] = {"error": "Insufficient samples for CV"}
                return results
            cv = StratifiedKFold(
                n_splits=n_splits, shuffle=True, random_state=self.random_state
            )
        else:
            n_splits = min(self.cv_folds, n_samples // 2) if n_samples >= 2 else 1
            if n_splits < 2:
                # Skip CV if not enough samples
                warnings.warn(
                    f"Insufficient samples ({n_samples}) for cross-validation. Skipping {set_name}."
                )
                results["models"] = {"error": "Insufficient samples for CV"}
                return results
            cv = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)

        for model_name in self.models:
            try:
                model = self.model_configs[model_name][
                    "classifier" if is_classification else "regressor"
                ]

                # Encode categorical columns before cross-validation
                X_encoded = self._encode_categorical(X)

                # Perform cross-validation
                start_time = time.time()
                cv_scores = cross_val_score(
                    model,
                    X_encoded,
                    y,
                    cv=cv,
                    scoring=self._get_sklearn_scorer(is_classification),
                )
                training_time = time.time() - start_time

                results["models"][model_name] = {
                    "cv_mean": cv_scores.mean(),
                    "cv_std": cv_scores.std(),
                    "cv_scores": cv_scores.tolist(),
                    "training_time": training_time,
                }

            except Exception as e:
                warnings.warn(f"Failed to benchmark {model_name} on {set_name}: {e}")
                results["models"][model_name] = {"error": str(e)}

        # Overall CV performance
        valid_models = [m for m in results["models"].values() if "cv_mean" in m]
        if valid_models:
            results["cross_validation"] = {
                "best_model": max(valid_models, key=lambda x: x["cv_mean"]),
                "mean_performance": np.mean([m["cv_mean"] for m in valid_models]),
                "performance_std": np.std([m["cv_mean"] for m in valid_models]),
            }

        return results

    def _evaluate_on_test(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        is_classification: bool,
    ) -> Dict[str, Any]:
        """
        Evaluate models on test set.
        """
        test_results = {}

        for model_name in self.models:
            try:
                model = self.model_configs[model_name][
                    "classifier" if is_classification else "regressor"
                ]
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                if is_classification:
                    y_proba = (
                        model.predict_proba(X_test)[:, 1]
                        if hasattr(model, "predict_proba")
                        else None
                    )

                    metrics = {
                        "accuracy": accuracy_score(y_test, y_pred),
                        "precision": precision_score(
                            y_test, y_pred, average="weighted"
                        ),
                        "recall": recall_score(y_test, y_pred, average="weighted"),
                        "f1": f1_score(y_test, y_pred, average="weighted"),
                    }

                    if y_proba is not None:
                        # Need actual test labels for AUC - this is a limitation
                        # In practice, you'd need y_test
                        pass
                else:
                    metrics = {
                        "mse": mean_squared_error(y_test, y_pred),
                        "mae": mean_absolute_error(y_test, y_pred),
                        "r2": r2_score(y_test, y_pred),
                    }

                test_results[model_name] = metrics

            except Exception as e:
                test_results[model_name] = {"error": str(e)}

        return test_results

    def get_feature_importance(
        self, X: pd.DataFrame, y: pd.Series, method: str = "mutual_info"
    ) -> pd.Series:
        """
        Calculate feature importance scores.

        Args:
            X: Features
            y: Target
            method: Importance method ("mutual_info", "f_test", "rf_importance")

        Returns:
            Series with feature importance scores
        """
        # Fill NaN values, handling mixed data types
        X_filled = X.copy()
        numeric_cols = X_filled.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            X_filled.loc[:, col] = X_filled[col].fillna(X_filled[col].mean())

        # Fill categorical columns with mode
        categorical_cols = X_filled.select_dtypes(exclude=[np.number]).columns
        for col in categorical_cols:
            mode_val = (
                X_filled[col].mode().iloc[0]
                if not X_filled[col].mode().empty
                else "Unknown"
            )
            X_filled.loc[:, col] = X_filled[col].fillna(mode_val)

        # Encode categorical columns before importance calculation
        X_filled = self._encode_categorical(X_filled)

        if method == "mutual_info":
            # Mutual info works on numeric features only
            numeric_cols = X_filled.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                # Fallback to random forest importance if no numeric features
                return self.get_feature_importance(X_filled, y, method="rf_importance")

            X_numeric = X_filled[numeric_cols]
            if self._is_classification_target(y):
                selector = SelectKBest(mutual_info_classif, k="all")
            else:
                selector = SelectKBest(mutual_info_regression, k="all")
            selector.fit(X_numeric, y)
            scores = pd.Series(selector.scores_, index=numeric_cols)

            # For non-numeric columns, assign zero importance
            all_scores = pd.Series(0.0, index=X.columns)
            all_scores.loc[numeric_cols] = scores
            return all_scores

        elif method == "f_test":
            # F-test also works on numeric features only
            numeric_cols = X_filled.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                return pd.Series(0.0, index=X.columns)

            X_numeric = X_filled[numeric_cols]
            if self._is_classification_target(y):
                selector = SelectKBest(f_classif, k="all")
            else:
                selector = SelectKBest(f_regression, k="all")
            selector.fit(X_numeric, y)
            scores = pd.Series(selector.scores_, index=numeric_cols)

            # For non-numeric columns, assign zero importance
            all_scores = pd.Series(0.0, index=X.columns)
            all_scores.loc[numeric_cols] = scores
            return all_scores

        elif method == "rf_importance":
            if self._is_classification_target(y):
                rf = RandomForestClassifier(
                    n_estimators=100, random_state=self.random_state
                )
            else:
                rf = RandomForestRegressor(
                    n_estimators=100, random_state=self.random_state
                )

            # For random forest, we can use all features (it handles mixed types better)
            rf.fit(X_filled, y)
            return pd.Series(rf.feature_importances_, index=X.columns)

        else:
            raise ValueError(f"Unknown importance method: {method}")

    def _perform_ablation_study(
        self, X: pd.DataFrame, y: pd.Series, is_classification: bool
    ) -> Dict[str, Any]:
        """
        Perform ablation study by removing features one by one.
        """
        ablation_results = []

        # Get baseline performance
        baseline_score = self._get_baseline_score(X, y, is_classification)

        # Sort features by importance
        importance_scores = self.get_feature_importance(X, y)
        sorted_features = importance_scores.sort_values(ascending=False).index.tolist()

        for i, feature in enumerate(sorted_features):
            # Remove this feature
            remaining_features = sorted_features[i + 1 :]
            if len(remaining_features) == 0:
                break

            # Handle mixed data types in ablation study
            X_ablated = X[remaining_features].copy()
            numeric_cols = X_ablated.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                X_ablated.loc[:, col] = X_ablated[col].fillna(X_ablated[col].mean())

            # Fill categorical columns with mode
            categorical_cols = X_ablated.select_dtypes(exclude=[np.number]).columns
            for col in categorical_cols:
                mode_val = (
                    X_ablated[col].mode().iloc[0]
                    if not X_ablated[col].mode().empty
                    else "Unknown"
                )
                X_ablated.loc[:, col] = X_ablated[col].fillna(mode_val)

            # Encode categorical columns
            X_ablated = self._encode_categorical(X_ablated)

            try:
                score = self._evaluate_model(X_ablated, y, is_classification)
                performance_drop = baseline_score - score

                ablation_results.append(
                    {
                        "removed_feature": feature,
                        "importance_rank": i + 1,
                        "importance_score": importance_scores[feature],
                        "remaining_features": len(remaining_features),
                        "performance": score,
                        "performance_drop": performance_drop,
                        "relative_drop": (
                            performance_drop / baseline_score
                            if baseline_score != 0
                            else 0
                        ),
                    }
                )
            except Exception as e:
                ablation_results.append({"removed_feature": feature, "error": str(e)})

        return {
            "baseline_performance": baseline_score,
            "ablation_results": ablation_results,
            "most_important_features": sorted_features[:10],
        }

    def _get_default_feature_sets(
        self, X: pd.DataFrame, y: pd.Series, is_classification: bool
    ) -> List[Dict[str, Any]]:
        """
        Generate default feature sets for benchmarking.
        """
        feature_sets = []

        # All features
        feature_sets.append(
            {
                "name": "all_features",
                "features": X.columns.tolist(),
                "description": "All available features",
            }
        )

        # Top N features by different methods
        importance_scores = self.get_feature_importance(X, y, method="mutual_info")
        top_features = importance_scores.nlargest(50).index.tolist()

        for n in [10, 25, 50]:
            if len(top_features) >= n:
                feature_sets.append(
                    {
                        "name": f"top_{n}_features",
                        "features": top_features[:n],
                        "description": f"Top {n} features by mutual information",
                    }
                )

        # Numeric only
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 0:
            feature_sets.append(
                {
                    "name": "numeric_only",
                    "features": numeric_cols,
                    "description": "Numeric features only",
                }
            )

        # Categorical only (encoded as dummies for simplicity)
        categorical_cols = X.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        if len(categorical_cols) > 0:
            feature_sets.append(
                {
                    "name": "categorical_only",
                    "features": categorical_cols,
                    "description": "Categorical features only",
                }
            )

        return feature_sets

    def _compare_models_across_sets(
        self, feature_sets: Any, is_classification: bool
    ) -> Dict[str, Any]:
        """
        Compare model performance across different feature sets.
        """
        model_comparison = {}

        for model_name in self.models:
            model_results = []

            for feature_set in feature_sets:
                if model_name in feature_set.get("models", {}):
                    model_data = feature_set["models"][model_name]
                    if "cv_mean" in model_data:
                        model_results.append(
                            {
                                "feature_set": feature_set["name"],
                                "performance": model_data["cv_mean"],
                                "std": model_data["cv_std"],
                                "n_features": feature_set["n_features"],
                            }
                        )

            if model_results:
                best_result = max(model_results, key=lambda x: x["performance"])
                model_comparison[model_name] = {
                    "results": model_results,
                    "best_feature_set": best_result["feature_set"],
                    "best_performance": best_result["performance"],
                    "avg_performance": np.mean(
                        [r["performance"] for r in model_results]
                    ),
                }

        return model_comparison

    def _identify_best_configurations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify best model and feature set combinations.
        """
        best_configs = {}

        # Best overall configuration
        all_results = []
        for feature_set in results["feature_sets"]:
            for model_name, model_data in feature_set.get("models", {}).items():
                if "cv_mean" in model_data:
                    all_results.append(
                        {
                            "feature_set": feature_set["name"],
                            "model": model_name,
                            "performance": model_data["cv_mean"],
                            "std": model_data["cv_std"],
                        }
                    )

        if all_results:
            best_overall = max(all_results, key=lambda x: x["performance"])
            best_configs["best_overall"] = best_overall

            # Best per model
            for model_name in self.models:
                model_results = [r for r in all_results if r["model"] == model_name]
                if model_results:
                    best_configs[f"best_for_{model_name}"] = max(
                        model_results, key=lambda x: x["performance"]
                    )

        return best_configs

    def _get_baseline_score(
        self, X: pd.DataFrame, y: pd.Series, is_classification: bool
    ) -> float:
        """Get baseline performance score."""
        return self._evaluate_model(X, y, is_classification)

    def _evaluate_model(
        self, X: pd.DataFrame, y: pd.Series, is_classification: bool
    ) -> float:
        """Evaluate a single model on given data."""
        model = self.model_configs["rf"][
            "classifier" if is_classification else "regressor"
        ]
        # Only fillna for numeric columns
        X_filled = X.copy()
        numeric_cols = X_filled.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            X_filled.loc[:, col] = X_filled[col].fillna(X_filled[col].mean())

        # Fill categorical columns with mode
        categorical_cols = X_filled.select_dtypes(exclude=[np.number]).columns
        for col in categorical_cols:
            mode_val = (
                X_filled[col].mode().iloc[0]
                if not X_filled[col].mode().empty
                else "Unknown"
            )
            X_filled.loc[:, col] = X_filled[col].fillna(mode_val)

        # Encode categorical columns
        X_filled = self._encode_categorical(X_filled)

        # Adjust CV splits based on sample size
        n_samples = len(X_filled)
        if is_classification:
            # For stratified CV, need at least n_splits samples per class
            min_class_size = (
                y.value_counts().min() if len(y.value_counts()) > 0 else n_samples
            )
            n_splits = min(3, min_class_size, n_samples // 2) if n_samples >= 2 else 1
            if n_splits < 2:
                # Fallback to simple train/test split if not enough samples
                from sklearn.model_selection import train_test_split

                # Check if we can use stratify (need at least 2 samples per class)
                can_stratify = (
                    is_classification and y.value_counts().min() >= 2
                    if len(y.value_counts()) > 0
                    else False
                )

                X_train, X_test, y_train, y_test = train_test_split(
                    X_filled,
                    y,
                    test_size=0.3,
                    random_state=self.random_state,
                    stratify=y if can_stratify else None,
                )
                model.fit(X_train, y_train)
                from sklearn.metrics import accuracy_score, r2_score

                if is_classification:
                    score = accuracy_score(y_test, model.predict(X_test))
                else:
                    score = r2_score(y_test, model.predict(X_test))
                return float(score)
            cv = StratifiedKFold(
                n_splits=n_splits, shuffle=True, random_state=self.random_state
            )
        else:
            n_splits = min(3, n_samples // 2) if n_samples >= 2 else 1
            if n_splits < 2:
                # Fallback to simple train/test split if not enough samples
                from sklearn.model_selection import train_test_split

                X_train, X_test, y_train, y_test = train_test_split(
                    X_filled, y, test_size=0.3, random_state=self.random_state
                )
                model.fit(X_train, y_train)
                from sklearn.metrics import r2_score

                score = r2_score(y_test, model.predict(X_test))
                return float(score)
            cv = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)

        scores = cross_val_score(
            model,
            X_filled,
            y,
            cv=cv,
            scoring=self._get_sklearn_scorer(is_classification),
        )

        return float(scores.mean())  # type: ignore[no-any-return]

    def _encode_categorical(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Encode categorical columns to numeric for sklearn compatibility.

        Args:
            X: DataFrame with potentially categorical columns

        Returns:
            DataFrame with categorical columns encoded
        """
        X_encoded = X.copy()

        # Get categorical columns
        categorical_cols = X_encoded.select_dtypes(
            include=["object", "category", "string"]
        ).columns

        # Use label encoding for categorical columns
        for col in categorical_cols:
            if (
                X_encoded[col].dtype == "object"
                or X_encoded[col].dtype.name == "category"
            ):
                # Convert to category and use codes
                X_encoded[col] = pd.Categorical(X_encoded[col]).codes
                # Handle -1 (NaN) codes by replacing with most frequent
                if (X_encoded[col] == -1).any():
                    most_frequent = (
                        X_encoded[col].mode()[0]
                        if len(X_encoded[col].mode()) > 0
                        else 0
                    )
                    X_encoded.loc[X_encoded[col] == -1, col] = most_frequent

        return X_encoded

    def _get_sklearn_scorer(self, is_classification: bool) -> str:
        """Get appropriate sklearn scorer."""
        return "accuracy" if is_classification else "neg_mean_squared_error"

    def _is_classification_target(self, y: pd.Series) -> bool:
        """Determine if target is classification."""
        return y.nunique() < 20 or y.dtype in ["object", "category"]
