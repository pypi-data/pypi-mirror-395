"""
The calculus package for TopoVision.

This package provides various strategies for topographic analysis,
encapsulated within an AnalysisContext for flexible calculation.
"""

from .calculus_module import AnalysisContext
from .strategies import ArcLengthStrategy, GradientStrategy, VolumeStrategy

__all__ = [
    "AnalysisContext",
    "GradientStrategy",
    "VolumeStrategy",
    "ArcLengthStrategy",
]
