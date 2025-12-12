import unittest
from unittest.mock import MagicMock

import numpy as np

from topovision.calculus.calculus_module import AnalysisContext
from topovision.calculus.strategies import (
    ArcLengthStrategy,
    GradientStrategy,
    VolumeStrategy,
)
from topovision.core.models import ArcLengthResult, GradientResult, VolumeResult


class TestAnalysisContext(unittest.TestCase):
    """Test suite for the AnalysisContext."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.context = AnalysisContext()
        self.data = np.array([[1, 2], [3, 4]], dtype=np.uint8)

    def test_set_valid_strategy(self) -> None:
        """Test setting a valid analysis strategy."""
        self.context.set_strategy("gradient")
        self.assertIsInstance(self.context.strategy, GradientStrategy)

    def test_set_invalid_strategy(self) -> None:
        """Test setting an invalid analysis strategy."""
        with self.assertRaises(ValueError):
            self.context.set_strategy("invalid_strategy")

    def test_calculate_without_strategy(self) -> None:
        """Test calculating without a strategy set."""
        with self.assertRaises(RuntimeError):
            self.context.calculate(self.data)

    def test_calculate_with_gradient_strategy(self) -> None:
        """Test calculation with the gradient strategy."""
        self.context.set_strategy("gradient")
        result = self.context.calculate(self.data)
        self.assertIsInstance(result, GradientResult)

    def test_calculate_with_volume_strategy(self) -> None:
        """Test calculation with the volume strategy."""
        self.context.set_strategy("volume")
        result = self.context.calculate(self.data, z_factor=2.0)
        self.assertIsInstance(result, VolumeResult)


class TestAnalysisStrategies(unittest.TestCase):
    """Test suite for the individual analysis strategies."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.gradient_strategy = GradientStrategy()
        self.volume_strategy = VolumeStrategy()
        self.arc_length_strategy = ArcLengthStrategy()
        self.data_2d = np.array([[1, 2], [3, 4]], dtype=np.uint8)

    def test_gradient_strategy(self) -> None:
        """Test the gradient calculation."""
        result = self.gradient_strategy.analyze(self.data_2d)
        self.assertIsInstance(result, GradientResult)
        self.assertEqual(result.dz_dx.shape, self.data_2d.shape)
        self.assertEqual(result.dz_dy.shape, self.data_2d.shape)

    def test_gradient_strategy_with_invalid_data(self) -> None:
        """Test gradient strategy with invalid (non-2D) data."""
        with self.assertRaises(ValueError):
            self.gradient_strategy.analyze(np.array([1, 2, 3]))

    def test_volume_strategy(self) -> None:
        """Test the volume calculation."""
        result = self.volume_strategy.analyze(
            self.data_2d, z_factor=1.0, pixels_per_meter=1.0
        )
        self.assertIsInstance(result, VolumeResult)
        # Sum of pixels * z_factor * pixel_area
        expected_volume = (1 + 2 + 3 + 4) * 1.0 * (1.0**2)
        self.assertAlmostEqual(result.volume, expected_volume)

    def test_volume_strategy_with_scaling(self) -> None:
        """Test volume strategy with a z-factor."""
        result = self.volume_strategy.analyze(
            self.data_2d, z_factor=2.5, pixels_per_meter=10.0
        )
        self.assertIsInstance(result, VolumeResult)
        pixel_area = (1.0 / 10.0) ** 2
        expected_volume = (1 + 2 + 3 + 4) * 2.5 * pixel_area
        self.assertAlmostEqual(result.volume, expected_volume)

    def test_volume_strategy_with_invalid_data(self) -> None:
        """Test volume strategy with invalid (non-2D) data."""
        with self.assertRaises(ValueError):
            self.volume_strategy.analyze(np.array([1, 2, 3]))

    def test_arc_length_strategy(self) -> None:
        """Test the arc length calculation."""
        strategy = ArcLengthStrategy()
        points = np.array([[i, i] for i in range(10)])

        pixels_per_meter = 1.0
        z_factor = 1.0

        result = strategy.analyze(
            points, pixels_per_meter=pixels_per_meter, z_factor=z_factor, unit="meters"
        )

        self.assertIsInstance(result, ArcLengthResult)

        scale_x = 1.0 / pixels_per_meter
        scale_z = z_factor / 255.0

        scaled_points = np.zeros((10, 2))
        scaled_points[:, 0] = np.arange(10) * scale_x
        scaled_points[:, 1] = np.arange(10) * scale_z

        diffs = np.diff(scaled_points, axis=0)
        expected_length = np.sum(np.sqrt(np.sum(diffs**2, axis=1)))

        self.assertAlmostEqual(result.length, expected_length)

    def test_arc_length_with_empty_data(self) -> None:
        """Test arc length with empty or single-point data."""
        with self.assertRaises(ValueError):
            self.arc_length_strategy.analyze([])
        self.assertEqual(
            self.arc_length_strategy.analyze(np.array([[1, 1]])).length, 0.0
        )
