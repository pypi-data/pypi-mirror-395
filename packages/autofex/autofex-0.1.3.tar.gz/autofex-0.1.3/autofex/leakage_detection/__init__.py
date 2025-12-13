"""
Leakage Detection Module

Detects data leakage in ML datasets:
- Target leakage
- Train-test contamination
- Feature leakage
- Time-based leakage
- Statistical leakage tests
"""

from .detector import LeakageDetector

__all__ = ["LeakageDetector"]
