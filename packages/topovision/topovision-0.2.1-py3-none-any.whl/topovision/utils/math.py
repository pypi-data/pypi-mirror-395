"""
This module provides utility functions for mathematical calculations,
optimized for performance using NumPy.
"""

from typing import List, Tuple, Union

import numpy as np
from numpy.typing import NDArray


def calculate_arc_length(
    points: Union[NDArray[np.float64], List[Tuple[float, float]]],
    scale_x: float,
    scale_y: float,
) -> float:
    """
    Calculates the arc length of a curve defined by a series of 2D points,
    where the y-values represent height.

    Args:
        points: A NumPy array of shape (N, 2) or a list of (x, y) tuples.
        scale_x (float): The conversion factor for the x-axis (e.g., meters/pixel).
        scale_y (float): The conversion factor for the y-axis (e.g., meters/pixel).

    Returns:
        The total length of the curve in real-world units.
    """
    points_arr = np.asarray(points, dtype=np.float64)

    if points_arr.ndim != 2 or points_arr.shape[1] != 2:
        raise ValueError("Input `points` must be a 2D array or a list of 2D tuples.")

    if len(points_arr) < 2:
        return 0.0

    # Apply scaling to the points
    scaled_points = np.copy(points_arr)
    scaled_points[:, 0] *= scale_x  # Scale x-coordinates
    scaled_points[:, 1] *= scale_y  # Scale y-coordinates (height)

    # Calculate the differences between consecutive points (dx, dy)
    deltas = np.diff(scaled_points, axis=0)

    # Calculate the Euclidean distance for each 3D segment
    segment_lengths = np.hypot(deltas[:, 0], deltas[:, 1])

    # Sum the lengths of all segments
    total_length = np.sum(segment_lengths)

    return float(total_length)
