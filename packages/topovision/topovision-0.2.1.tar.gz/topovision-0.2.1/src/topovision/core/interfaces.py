"""
Core interfaces for TopoVision.

This module defines the abstract base classes (interfaces) that form the
contracts for the main components of the application. Adhering to these
interfaces allows for modularity and interchangeability of components.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Union  # Import Any

import numpy as np
from numpy.typing import NDArray
from PIL import Image

from .models import (
    AnalysisResult,
    ArcLengthResult,
    FrameData,
    GradientResult,
    RegionOfInterest,
    VolumeResult,
)


class ICamera(ABC):
    """Abstract interface for a camera device."""

    @abstractmethod
    def start(self) -> None:
        """Starts the camera capture stream."""
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Stops the camera and releases all associated resources."""
        raise NotImplementedError

    @abstractmethod
    def pause(self) -> None:
        """Pauses the camera capture stream without releasing resources."""
        raise NotImplementedError

    @abstractmethod
    def resume(self) -> None:
        """Resumes a paused camera stream."""
        raise NotImplementedError

    @abstractmethod
    def get_frame(self) -> Optional[FrameData]:
        """
        Fetches the latest frame from the camera.

        Returns:
            Optional[FrameData]: A FrameData object containing the image and
            metadata, or None if a frame is not available.
        """
        raise NotImplementedError


class IAnalysisStrategy(ABC):
    """Abstract interface for a single analysis method (e.g., gradient, volume)."""

    @abstractmethod
    def analyze(
        self, data: NDArray[np.uint8], **kwargs: Any
    ) -> Union[GradientResult, VolumeResult, ArcLengthResult]:
        """
        Performs a specific analysis on the given data.

        Args:
            data (NDArray[np.uint8]): The input data for analysis, typically a
                                     grayscale image region.
            **kwargs: Additional parameters required for the analysis (e.g., z_factor).

        Returns:
            A specific result object (e.g., GradientResult, VolumeResult).
        """
        raise NotImplementedError


class IVisualizer(ABC):
    """Abstract interface for visualizing analysis results."""

    @abstractmethod
    def visualize(
        self, analysis_result: AnalysisResult, original_image: Image.Image
    ) -> Image.Image:
        """
        Creates a visualization of the analysis result.

        Args:
            analysis_result (AnalysisResult): The result of the analysis.
            original_image (Image.Image): The original image on which to
                                                 overlay the visualization.

        Returns:
            Image.Image: The image with the visualization overlaid.
        """
        raise NotImplementedError


class IPreprocessor(ABC):
    """Abstract interface for an image pre-processing filter."""

    @abstractmethod
    def process(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Applies a pre-processing step to an image.

        Args:
            image (NDArray[np.uint8]): The input image.

        Returns:
            NDArray[np.uint8]: The processed image.
        """
        raise NotImplementedError
