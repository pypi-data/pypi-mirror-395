"""
Utility Functions

Helper functions for data processing, validation, and common operations.
"""

from .helpers import (
    safe_divide,
    detect_outliers_iqr,
    calculate_correlation_matrix,
    get_feature_stats,
    validate_dataframe,
)

try:
    from .progress import ProgressTracker, RealTimeFeedback
    from .cache import OperationCache

    _UTILS_AVAILABLE = True
except ImportError:
    _UTILS_AVAILABLE = False
    ProgressTracker = None  # type: ignore
    RealTimeFeedback = None  # type: ignore
    OperationCache = None  # type: ignore

__all__ = [
    "safe_divide",
    "detect_outliers_iqr",
    "calculate_correlation_matrix",
    "get_feature_stats",
    "validate_dataframe",
]

if _UTILS_AVAILABLE:
    __all__.extend(
        [
            "ProgressTracker",
            "RealTimeFeedback",
            "OperationCache",
        ]
    )
