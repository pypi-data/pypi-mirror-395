"""
Core AutoFE-X class that orchestrates all feature engineering and analysis components.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from .data_profiling import DataProfiler
from .leakage_detection import LeakageDetector
from .benchmarking import FeatureBenchmarker
from .lineage import FeatureLineageTracker
from .utils.progress import ProgressTracker, RealTimeFeedback
from .utils.cache import OperationCache

# Import FeatureEngineer - try advanced first, fallback to base
try:
    from .feature_engineering.advanced import FeatureEngineer  # type: ignore[assignment]
    from .feature_selection.selector import FeatureSelector
    from .visualization import FeatureVisualizer

    _NEXTGEN_AVAILABLE = True
except ImportError:
    _NEXTGEN_AVAILABLE = False
    from .feature_engineering import FeatureEngineer  # type: ignore[assignment]

    FeatureSelector = None  # type: ignore
    FeatureVisualizer = None  # type: ignore


@dataclass
class AutoFEXResult:
    """Container for AutoFEX pipeline results."""

    original_data: pd.DataFrame
    engineered_features: pd.DataFrame
    data_quality_report: Dict[str, Any]
    leakage_report: Dict[str, Any]
    benchmark_results: Dict[str, Any]
    feature_lineage: Dict[str, Any]
    processing_time: float


class AutoFEX:
    """
    Main AutoFEX class that orchestrates automated feature engineering,
    data profiling, leakage detection, and benchmarking.

    Example:
        >>> afx = AutoFEX()
        >>> result = afx.process(X_train, y_train, X_test)
        >>> print(result.data_quality_report)
        >>> engineered_train = result.engineered_features
    """

    def __init__(
        self,
        feature_engineering_config: Optional[Dict[str, Any]] = None,
        profiling_config: Optional[Dict[str, Any]] = None,
        leakage_config: Optional[Dict[str, Any]] = None,
        benchmarking_config: Optional[Dict[str, Any]] = None,
        lineage_config: Optional[Dict[str, Any]] = None,
        random_state: int = 42,
        enable_progress: bool = True,
        enable_cache: bool = True,
        cache_dir: Optional[str] = None,
        cache_ttl: Optional[float] = None,
        n_jobs: Optional[int] = None,
        parallel_backend: str = "threading",
    ):
        """
        Initialize AutoFEX pipeline.

        Args:
            feature_engineering_config: Configuration for feature engineering
            profiling_config: Configuration for data profiling
            leakage_config: Configuration for leakage detection
            benchmarking_config: Configuration for benchmarking
            lineage_config: Configuration for lineage tracking
            random_state: Random seed for reproducibility
            enable_progress: Whether to show progress tracking
            enable_cache: Whether to enable caching
            cache_dir: Directory for cache files
            cache_ttl: Time-to-live for cache entries in seconds
            n_jobs: Number of parallel jobs (-1 for all CPUs, None for sequential)
            parallel_backend: Backend for parallel processing ('threading', 'multiprocessing', 'loky')
        """
        self.random_state = random_state
        np.random.seed(random_state)

        # Set up parallel processing in feature engineering config
        if feature_engineering_config is None:
            feature_engineering_config = {}
        feature_engineering_config["n_jobs"] = n_jobs
        feature_engineering_config["parallel_backend"] = parallel_backend

        # Initialize components
        self.feature_engineer = FeatureEngineer(config=feature_engineering_config)
        self.data_profiler = DataProfiler(config=profiling_config or {})
        self.leakage_detector = LeakageDetector(config=leakage_config or {})
        self.benchmarker = FeatureBenchmarker(config=benchmarking_config or {})

        # Initialize progress tracking and caching
        self.enable_progress = enable_progress
        self.progress_tracker = (
            ProgressTracker(show_progress=enable_progress) if enable_progress else None
        )
        self.real_time_feedback = RealTimeFeedback() if enable_progress else None

        self.cache = (
            OperationCache(
                cache_dir=cache_dir,
                ttl_seconds=cache_ttl,
                enabled=enable_cache,
            )
            if enable_cache
            else None
        )
        self.lineage_tracker = FeatureLineageTracker(config=lineage_config or {})

        # Components (if available)
        self.use_features = (
            feature_engineering_config.get("use_adv", False)
            if feature_engineering_config
            else False
        )
        if _NEXTGEN_AVAILABLE and self.use_features:
            self.feature_engineer = FeatureEngineer(
                config=feature_engineering_config or {}
            )
            self.feature_selector = FeatureSelector(
                config=feature_engineering_config.get("selection_config", {}) or {}
            )
            self.visualizer = FeatureVisualizer()

    def process(
        self,
        X: pd.DataFrame,
        y: Optional[Union[pd.Series, np.ndarray]] = None,
        X_test: Optional[pd.DataFrame] = None,
        target_name: str = "target",
    ) -> AutoFEXResult:
        """
        Run the complete AutoFEX pipeline with progress tracking and caching.

        Args:
            X: Training features
            y: Training target (optional, required for supervised operations)
            X_test: Test features (optional)
            target_name: Name for target variable in lineage tracking

        Returns:
            AutoFEXResult containing all pipeline outputs
        """
        import time

        start_time = time.time()
        total_steps = (
            5 if y is not None else 3
        )  # Adjust based on whether target is available

        # Initialize progress tracking
        if self.progress_tracker:
            self.progress_tracker.start(
                f"AutoFE-X Pipeline Processing ({X.shape[0]} rows, {X.shape[1]} features)"
            )
            self.progress_tracker.total_steps = total_steps

        # Initialize lineage tracking
        step = 1
        if self.progress_tracker:
            self.progress_tracker.update(
                step, "Initializing lineage tracking", "lineage_init"
            )
        self.lineage_tracker.start_session(X.columns.tolist())

        # Step 1: Data profiling (with caching)
        step = 2
        if self.progress_tracker:
            self.progress_tracker.update(
                step, "Analyzing data quality", "data_profiling"
            )

        if self.cache:

            def _profile_data():
                return self.data_profiler.analyze(X, y)

            quality_report = self.cache.cache_function("data_profiling", _profile_data)
        else:
            quality_report = self.data_profiler.analyze(X, y)

        if self.real_time_feedback:
            missing_pct = (
                quality_report.get("missing_values", {}).get("total_missing_cells", 0)
                / (X.shape[0] * X.shape[1])
                * 100
                if X.shape[0] * X.shape[1] > 0
                else 0
            )
            self.real_time_feedback.update_metric("missing_data_percent", missing_pct)
            self.real_time_feedback.update_metric("n_features", X.shape[1])
            self.real_time_feedback.update_metric("n_samples", X.shape[0])

        # Step 2: Leakage detection (if target available, with caching)
        leakage_report = {}
        if y is not None:
            step = 3
            if self.progress_tracker:
                self.progress_tracker.update(
                    step, "Detecting data leakage", "leakage_detection"
                )

            if self.cache:

                def _detect_leakage():
                    return self.leakage_detector.detect(X, y)

                leakage_report = self.cache.cache_function(
                    "leakage_detection", _detect_leakage
                )
            else:
                leakage_report = self.leakage_detector.detect(X, y)

            if self.real_time_feedback and leakage_report:
                risk_level = leakage_report.get("overall_assessment", {}).get(
                    "risk_level", "unknown"
                )
                risk_score = leakage_report.get("overall_assessment", {}).get(
                    "risk_score", 0
                )
                self.real_time_feedback.update_metric("leakage_risk_level", risk_level)
                self.real_time_feedback.update_metric("leakage_risk_score", risk_score)

        # Step 3: Feature engineering (with caching and parallel processing)
        step = 4 if y is not None else 3
        if self.progress_tracker:
            self.progress_tracker.update(
                step, "Engineering features", "feature_engineering"
            )

        # Set up progress callback for feature engineering
        if self.progress_tracker and hasattr(
            self.feature_engineer, "set_progress_callback"
        ):

            def _progress_callback(completed: int, total: int):
                if self.progress_tracker:
                    self.progress_tracker.update(
                        step,
                        f"Engineering features: {completed}/{total} columns",
                        "feature_engineering",
                    )

            self.feature_engineer.set_progress_callback(_progress_callback)

        if self.cache:

            def _engineer_features():
                return self.feature_engineer.fit_transform(X, y)

            engineered_features = self.cache.cache_function(
                "feature_engineering", _engineer_features
            )
        else:
            engineered_features = self.feature_engineer.fit_transform(X, y)

        if self.real_time_feedback:
            expansion_ratio = (
                engineered_features.shape[1] / X.shape[1] if X.shape[1] > 0 else 0
            )
            self.real_time_feedback.update_metric(
                "feature_expansion_ratio", expansion_ratio
            )
            self.real_time_feedback.update_metric(
                "n_engineered_features", engineered_features.shape[1]
            )

        # Step 4: Update lineage with engineered features
        self.lineage_tracker.add_transformation(
            "feature_engineering",
            X.columns.tolist(),
            engineered_features.columns.tolist(),
        )

        # Step 5: Benchmarking (if target available, with caching)
        benchmark_results = {}
        if y is not None:
            step = 5
            if self.progress_tracker:
                self.progress_tracker.update(
                    step, "Benchmarking feature sets", "benchmarking"
                )

            if self.cache:

                def _benchmark_features():
                    return self.benchmarker.benchmark_features(X, y, X_test)

                benchmark_results = self.cache.cache_function(
                    "benchmarking", _benchmark_features
                )
            else:
                benchmark_results = self.benchmarker.benchmark_features(X, y, X_test)

            if self.real_time_feedback and benchmark_results:
                best_config = benchmark_results.get("best_configurations", {}).get(
                    "best_overall", {}
                )
                if best_config:
                    self.real_time_feedback.update_metric(
                        "best_model", best_config.get("model", "N/A")
                    )
                    self.real_time_feedback.update_metric(
                        "best_performance", best_config.get("performance", 0)
                    )

        processing_time = time.time() - start_time

        # Finish progress tracking
        if self.progress_tracker:
            self.progress_tracker.finish(f"Pipeline completed successfully")
            if self.real_time_feedback:
                self.real_time_feedback.print_summary()

        return AutoFEXResult(
            original_data=X,
            engineered_features=engineered_features,
            data_quality_report=quality_report,
            leakage_report=leakage_report,
            benchmark_results=benchmark_results,
            feature_lineage=self.lineage_tracker.get_lineage_graph(),
            processing_time=processing_time,
        )

    def get_feature_importance(
        self, X: pd.DataFrame, y: pd.Series, method: str = "mutual_info"
    ) -> pd.Series:
        """
        Get feature importance scores.

        Args:
            X: Features
            y: Target
            method: Importance method ("mutual_info", "f_test", "chi2")

        Returns:
            Series with feature importance scores
        """
        return self.benchmarker.get_feature_importance(X, y, method)

    def suggest_feature_transformations(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest feature transformations based on data analysis.

        Args:
            X: Input features
            y: Target variable (optional)

        Returns:
            List of suggested transformations
        """
        suggestions = []

        # Analyze data types and suggest transformations
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        categorical_cols = X.select_dtypes(include=["object", "category"]).columns

        # Numeric feature suggestions
        for col in numeric_cols:
            if X[col].skew() > 1:
                suggestions.append(
                    {
                        "column": col,
                        "transformation": "log_transform",
                        "reason": f"High skewness ({X[col].skew():.2f})",
                        "expected_impact": "Normalize distribution",
                    }
                )

        # Categorical feature suggestions
        for col in categorical_cols:
            if X[col].nunique() > 10:
                suggestions.append(
                    {
                        "column": col,
                        "transformation": "target_encoding",
                        "reason": f"High cardinality ({X[col].nunique()} unique values)",
                        "expected_impact": "Reduce dimensionality",
                    }
                )

        return suggestions
