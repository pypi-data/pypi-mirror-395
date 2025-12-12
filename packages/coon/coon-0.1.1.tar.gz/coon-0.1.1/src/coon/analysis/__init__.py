"""
Analysis module for COON.

Provides code analysis and metrics collection for
intelligent compression strategy selection.
"""

from .analyzer import CodeAnalyzer, AnalysisResult
from .metrics import MetricsCollector, CompressionMetric


__all__ = [
    # Analyzer
    "CodeAnalyzer",
    "AnalysisResult",
    
    # Metrics
    "MetricsCollector",
    "CompressionMetric",
]
