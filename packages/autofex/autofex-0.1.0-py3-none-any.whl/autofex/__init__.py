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

from .core import AutoFEX
from .feature_engineering import FeatureEngineer
from .data_profiling import DataProfiler
from .leakage_detection import LeakageDetector
from .benchmarking import FeatureBenchmarker
from .lineage import FeatureLineageTracker

# NextGen improvements
try:
    from .feature_engineering.advanced import FeatureEngineer  # type: ignore[assignment]
    from .feature_selection.selector import FeatureSelector
    from .visualization import FeatureVisualizer
    from .analysis.statistical import StatisticalAnalyzer as StatisticalAnalyzer

    _NEXTGEN_AVAILABLE = True
except ImportError:
    _NEXTGEN_AVAILABLE = False

try:
    from .visualization.dashboard import InteractiveDashboard

    _DASHBOARD_AVAILABLE = True
except ImportError:
    _DASHBOARD_AVAILABLE = False
    InteractiveDashboard = None  # type: ignore

try:
    from .visualization.multidimensional import MultiDimensionalVisualizer

    _MULTIDIM_AVAILABLE = True
except ImportError:
    _MULTIDIM_AVAILABLE = False
    MultiDimensionalVisualizer = None  # type: ignore

try:
    from .analysis.ultra_stats import (
        UltraStatisticalAnalyzer as UltraStatisticalAnalyzer,
    )

    _ULTRA_STATS_AVAILABLE = True
except ImportError:
    _ULTRA_STATS_AVAILABLE = False
    UltraStatisticalAnalyzer = None  # type: ignore

try:
    from .mathematical.modeling import MathematicalModelingEngine

    _MATH_MODELING_AVAILABLE = True
except ImportError:
    _MATH_MODELING_AVAILABLE = False
    MathematicalModelingEngine = None  # type: ignore

try:
    from .statistical.stat_transforms import StatisticalTransforms

    _STAT_TRANSFORMS_AVAILABLE = True
except ImportError:
    _STAT_TRANSFORMS_AVAILABLE = False
    StatisticalTransforms = None  # type: ignore

try:
    from .pandas.operations import PandasOperations

    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False
    PandasOperations = None  # type: ignore

try:
    from .numpy.operations import NumpyOperations

    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False
    NumpyOperations = None  # type: ignore

try:
    from .scipy.operations import ScipyOperations

    _SCIPY_AVAILABLE = True
except ImportError:
    _SCIPY_AVAILABLE = False
    ScipyOperations = None  # type: ignore

try:
    from .intelligence.orchestrator import IntelligentOrchestrator
    from .intelligence.quality_scorer import FeatureQualityScorer
    from .intelligence.recommender import FeatureEngineeringRecommender

    _INTELLIGENCE_AVAILABLE = True
except ImportError:
    _INTELLIGENCE_AVAILABLE = False
    IntelligentOrchestrator = None  # type: ignore
    FeatureQualityScorer = None  # type: ignore
    FeatureEngineeringRecommender = None  # type: ignore

__version__ = "0.1.0"
__all__ = [
    "AutoFEX",
    "FeatureEngineer",
    "DataProfiler",
    "LeakageDetector",
    "FeatureBenchmarker",
    "FeatureLineageTracker",
]

if _NEXTGEN_AVAILABLE:
    __all__.extend(
        [
            "FeatureEngineer",
            "FeatureSelector",
            "FeatureVisualizer",
            "StatisticalAnalyzer",
        ]
    )

if _DASHBOARD_AVAILABLE:
    __all__.append("InteractiveDashboard")

if _MULTIDIM_AVAILABLE:
    __all__.append("MultiDimensionalVisualizer")

if _ULTRA_STATS_AVAILABLE:
    __all__.append("UltraStatisticalAnalyzer")

if _MATH_MODELING_AVAILABLE:
    __all__.append("MathematicalModelingEngine")

if _STAT_TRANSFORMS_AVAILABLE:
    __all__.append("StatisticalTransforms")

if _PANDAS_AVAILABLE:
    __all__.append("PandasOperations")

if _NUMPY_AVAILABLE:
    __all__.append("NumpyOperations")

if _SCIPY_AVAILABLE:
    __all__.append("ScipyOperations")

if _INTELLIGENCE_AVAILABLE:
    __all__.extend(
        [
            "IntelligentOrchestrator",
            "FeatureQualityScorer",
            "FeatureEngineeringRecommender",
        ]
    )
