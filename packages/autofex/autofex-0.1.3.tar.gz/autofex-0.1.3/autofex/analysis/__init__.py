"""
Statistical Analysis Module

Goes beyond basic scipy to provide integrated statistical insights.
"""

from .statistical import StatisticalAnalyzer

try:
    from .ultra_stats import UltraStatisticalAnalyzer

    _ULTRA_AVAILABLE = True
except ImportError:
    _ULTRA_AVAILABLE = False
    UltraStatisticalAnalyzer = None  # type: ignore

__all__ = ["StatisticalAnalyzer"]

if _ULTRA_AVAILABLE:
    __all__.append("UltraStatisticalAnalyzer")
