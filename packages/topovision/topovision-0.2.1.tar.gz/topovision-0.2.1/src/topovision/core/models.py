"""
Core data models for TopoVision.

This module defines the fundamental data structures used throughout the application,
from capturing frames to holding the results of complex analyses. These models ensure
data consistency and provide clear, self-documenting structures.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class FrameData:
    """
    Represents a single, immutable video frame with its associated metadata.

    Attributes:
        image (NDArray[np.uint8]): The image data as a NumPy array
                                   (e.g., in BGR or RGB format).
        timestamp (float): The time in seconds when the frame was captured.
        frame_number (Optional[int]): The sequential number of the frame,
                                      if available.
    """

    image: NDArray[np.uint8]
    timestamp: float
    frame_number: Optional[int] = None


@dataclass(frozen=True)
class RegionOfInterest:
    """
    Represents a rectangular region of interest (ROI) within a frame.

    The coordinates are absolute to the frame's dimensions. The top-left corner
    is (x1, y1) and the bottom-right corner is (x2, y2).

    Attributes:
        x1 (int): The starting x-coordinate.
        y1 (int): The starting y-coordinate.
        x2 (int): The ending x-coordinate.
        y2 (int): The ending y-coordinate.
    """

    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        """Returns the width of the region."""
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        """Returns the height of the region."""
        return self.y2 - self.y1

    @property
    def area(self) -> int:
        """Returns the area of the region."""
        return self.width * self.height


@dataclass(frozen=True)
class GradientResult:
    """
    Holds the calculated gradient (partial derivatives) over a region.

    Attributes:
        dz_dx (NDArray[np.float32]): The partial derivative with respect to x.
        dz_dy (NDArray[np.float32]): The partial derivative with respect to y.
        magnitude (Optional[NDArray[np.float32]]): The magnitude of the gradient.
    """

    dz_dx: NDArray[np.float32]
    dz_dy: NDArray[np.float32]
    magnitude: Optional[NDArray[np.float32]] = None


@dataclass(frozen=True)
class VolumeResult:
    """
    Holds the result of a volume calculation.

    Attributes:
        volume (float): The calculated volume under the surface defined by the ROI.
        units (str): The units of the calculated volume (e.g., "cubic_pixels").
    """

    volume: float
    units: str = "cubic_meters"


@dataclass(frozen=True)
class ArcLengthResult:
    """
    Holds the result of an arc length calculation.

    Attributes:
        length (float): The calculated arc length along a path.
        units (str): The units of the calculated length (e.g., "pixels", "meters").
        path_points (Optional[NDArray[np.int32]]): The points defining the path.
    """

    length: float
    units: str = "pixels"
    path_points: Optional[NDArray[np.int32]] = None


@dataclass(frozen=True)
class AnalysisResult:
    """
    A generic container for any type of analysis result.

    This allows for a consistent return type from different analysis strategies.

    Attributes:
        method (str): The name of the analysis method used
                      (e.g., "gradient", "volume").
        result_data (GradientResult | VolumeResult | ArcLengthResult):
            The specific result data.
        region (RegionOfInterest): The region where the analysis was performed.
    """

    method: str
    result_data: Union[GradientResult, VolumeResult, ArcLengthResult]
    region: RegionOfInterest
