"""
The visualization package for TopoVision.

This package provides tools for rendering and overlaying analysis results
onto image data, such as heatmaps.
"""

from .visualizers import HeatmapVisualizer

__all__ = [
    "HeatmapVisualizer",
]
