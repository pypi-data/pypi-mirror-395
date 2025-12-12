import unittest
from unittest.mock import MagicMock

import cv2
import numpy as np
from PIL import Image

from topovision.core.models import AnalysisResult, GradientResult, RegionOfInterest
from topovision.visualization.visualizers import HeatmapVisualizer


class TestHeatmapVisualizer(unittest.TestCase):
    """Test suite for the HeatmapVisualizer."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.visualizer = HeatmapVisualizer()
        self.original_image = Image.new("RGB", (100, 100), "blue")
        self.region = RegionOfInterest(x1=10, y1=10, x2=90, y2=90)

        # Create a mock gradient result
        gradient_data = np.random.rand(80, 80).astype(np.float32)
        gradient_result = GradientResult(
            dz_dx=gradient_data, dz_dy=gradient_data, magnitude=gradient_data
        )
        self.analysis_result = AnalysisResult(
            method="gradient", result_data=gradient_result, region=self.region
        )

    def test_visualize_returns_image(self) -> None:
        """Test that visualize returns a PIL Image."""
        visualization = self.visualizer.visualize(
            self.analysis_result, self.original_image
        )
        self.assertIsInstance(visualization, Image.Image)

    def test_visualize_with_no_magnitude(self) -> None:
        """Test that the original image is returned if there's no magnitude."""
        gradient_result = GradientResult(
            dz_dx=np.zeros((80, 80)), dz_dy=np.zeros((80, 80)), magnitude=None
        )
        analysis_result = AnalysisResult(
            method="gradient", result_data=gradient_result, region=self.region
        )
        visualization = self.visualizer.visualize(analysis_result, self.original_image)
        self.assertIs(visualization, self.original_image)

    def test_visualize_with_zero_magnitude(self) -> None:
        """Test visualization with a zero-magnitude gradient."""
        gradient_result = GradientResult(
            dz_dx=np.zeros((80, 80)),
            dz_dy=np.zeros((80, 80)),
            magnitude=np.zeros((80, 80)),
        )
        analysis_result = AnalysisResult(
            method="gradient", result_data=gradient_result, region=self.region
        )
        visualization = self.visualizer.visualize(analysis_result, self.original_image)
        self.assertIsInstance(visualization, Image.Image)

    def test_visualize_blending(self) -> None:
        """
        Test that the heatmap is blended onto the original image.
        """
        # Define a simple perspective transform for the test
        src_quad = np.float32([[10, 10], [90, 10], [90, 90], [10, 90]])
        dst_rect = np.float32([[0, 0], [80, 0], [80, 80], [0, 80]])
        inverse_matrix = cv2.getPerspectiveTransform(dst_rect, src_quad)

        visualization = self.visualizer.visualize(
            self.analysis_result,
            self.original_image,
            inverse_matrix=inverse_matrix,
            src_quad=src_quad,
        )

        vis_array = np.array(visualization)
        orig_array = np.array(self.original_image)

        self.assertFalse(np.array_equal(vis_array, orig_array))

    def test_visualize_without_perspective(self) -> None:
        """Test blending without perspective correction."""
        visualization = self.visualizer.visualize(
            self.analysis_result, self.original_image
        )
        vis_array = np.array(visualization)
        orig_array = np.array(self.original_image)
        self.assertFalse(np.array_equal(vis_array, orig_array))
