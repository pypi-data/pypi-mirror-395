"""
Intelligence Module

Intelligent feature engineering orchestration, quality scoring, and recommendations.
"""

try:
    from .orchestrator import IntelligentOrchestrator
    from .quality_scorer import FeatureQualityScorer
    from .recommender import FeatureEngineeringRecommender

    _INTELLIGENCE_AVAILABLE = True
except ImportError:
    _INTELLIGENCE_AVAILABLE = False
    IntelligentOrchestrator = None  # type: ignore
    FeatureQualityScorer = None  # type: ignore
    FeatureEngineeringRecommender = None  # type: ignore

__all__ = []

if _INTELLIGENCE_AVAILABLE:
    __all__.extend(
        [
            "IntelligentOrchestrator",
            "FeatureQualityScorer",
            "FeatureEngineeringRecommender",
        ]
    )
