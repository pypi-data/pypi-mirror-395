"""
AutoFE-X: Automated Feature Engineering + Data Profiling + Leakage Detection

A next-gen toolkit that becomes the brain of any ML pipeline by combining:
- Automatic feature engineering (classic + deep)
- Data quality analysis
- Leakage detection
- Auto-benchmarking of feature sets
- Graph-based feature lineage

Lightweight, fast, and interpretable. No LLMs.
"""

__version__ = "0.1.3"

# Lazy loading to avoid import errors when dependencies aren't available
__all__ = [
    "AutoFEX",
    "FeatureEngineer",
    "DataProfiler",
    "LeakageDetector",
    "FeatureBenchmarker",
    "FeatureLineageTracker",
    "FeatureSelector",
    "FeatureVisualizer",
    "StatisticalAnalyzer",
    "InteractiveDashboard",
    "MultiDimensionalVisualizer",
    "UltraStatisticalAnalyzer",
    "MathematicalModelingEngine",
    "StatisticalTransforms",
    "PandasOperations",
    "NumpyOperations",
    "ScipyOperations",
    "IntelligentOrchestrator",
    "FeatureQualityScorer",
    "FeatureEngineeringRecommender",
]


def __getattr__(name: str):
    """Lazy loading of modules to avoid import errors."""
    if name == "AutoFEX":
        from importlib import import_module

        return import_module(".core", __package__).AutoFEX

    if name == "FeatureEngineer":
        try:
            from .feature_engineering.advanced import FeatureEngineer  # type: ignore[assignment]

            return FeatureEngineer
        except ImportError:
            from .feature_engineering import FeatureEngineer  # type: ignore[assignment]

            return FeatureEngineer

    if name == "DataProfiler":
        from .data_profiling import DataProfiler

        return DataProfiler

    if name == "LeakageDetector":
        from .leakage_detection import LeakageDetector

        return LeakageDetector

    if name == "FeatureBenchmarker":
        from .benchmarking import FeatureBenchmarker

        return FeatureBenchmarker

    if name == "FeatureLineageTracker":
        from .lineage import FeatureLineageTracker

        return FeatureLineageTracker

    if name == "FeatureSelector":
        try:
            from .feature_selection.selector import FeatureSelector

            return FeatureSelector
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "FeatureVisualizer":
        try:
            from .visualization import FeatureVisualizer

            return FeatureVisualizer
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "StatisticalAnalyzer":
        try:
            from .analysis.statistical import StatisticalAnalyzer

            return StatisticalAnalyzer
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "InteractiveDashboard":
        try:
            from .visualization.dashboard import InteractiveDashboard

            return InteractiveDashboard
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "MultiDimensionalVisualizer":
        try:
            from .visualization.multidimensional import MultiDimensionalVisualizer

            return MultiDimensionalVisualizer
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "UltraStatisticalAnalyzer":
        try:
            from .analysis.ultra_stats import UltraStatisticalAnalyzer

            return UltraStatisticalAnalyzer
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "MathematicalModelingEngine":
        try:
            from .mathematical.modeling import MathematicalModelingEngine

            return MathematicalModelingEngine
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "StatisticalTransforms":
        try:
            from .statistical.stat_transforms import StatisticalTransforms

            return StatisticalTransforms
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "PandasOperations":
        try:
            from .pandas.operations import PandasOperations

            return PandasOperations
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "NumpyOperations":
        try:
            from .numpy.operations import NumpyOperations

            return NumpyOperations
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "ScipyOperations":
        try:
            from .scipy.operations import ScipyOperations

            return ScipyOperations
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "IntelligentOrchestrator":
        try:
            from .intelligence.orchestrator import IntelligentOrchestrator

            return IntelligentOrchestrator
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "FeatureQualityScorer":
        try:
            from .intelligence.quality_scorer import FeatureQualityScorer

            return FeatureQualityScorer
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name == "FeatureEngineeringRecommender":
        try:
            from .intelligence.recommender import FeatureEngineeringRecommender

            return FeatureEngineeringRecommender
        except ImportError:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
