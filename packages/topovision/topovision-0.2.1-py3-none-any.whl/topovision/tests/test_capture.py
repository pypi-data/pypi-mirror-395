"""
Unit tests for camera capture and control.
"""

import time
import unittest
from typing import Optional
from unittest.mock import MagicMock, patch

import numpy as np

from topovision.core.interfaces import ICamera
from topovision.core.models import FrameData
from topovision.gui.camera_controller import CameraController


class MockCamera(ICamera):
    """A mock camera implementation for testing purposes."""

    def __init__(self, frame_rate: int = 30) -> None:
        self._is_running = False
        self._frame_rate = frame_rate
        self._frame_count = 0
        self._start_time = 0.0

    def start(self) -> None:
        self._is_running = True
        self._start_time = time.time()

    def stop(self) -> None:
        self._is_running = False

    def pause(self) -> None:
        self._is_running = False

    def resume(self) -> None:
        # In the refactored CameraController, start() handles resume logic
        # For the mock, we'll just set is_running to True
        self._is_running = True

    def get_frame(self) -> Optional[FrameData]:
        if not self._is_running:
            return None

        elapsed_time = time.time() - self._start_time
        # Ensure we don't generate frames too quickly for the mock's internal state
        # This is a simplification; a real mock might use a queue or more complex timing
        if self._frame_count < (elapsed_time * self._frame_rate):
            self._frame_count += 1
            image = np.zeros((100, 100, 3), dtype=np.uint8)
            return FrameData(
                image=image, timestamp=time.time(), frame_number=self._frame_count
            )
        return None


class TestCameraController(unittest.TestCase):
    """Tests the CameraController's logic and state management."""

    def setUp(self) -> None:
        """Set up a mock camera and controller for each test."""
        self.mock_camera = MockCamera()
        self.update_callback = MagicMock()
        self.controller = CameraController(self.mock_camera, self.update_callback)

    def test_initial_state(self) -> None:
        """Test that the controller starts in a non-running state."""
        self.assertFalse(self.controller.is_running)
        self.assertFalse(self.controller.started_once)

    def test_start_and_stop(self) -> None:
        """Test the full start-stop lifecycle."""
        self.controller.start()
        self.assertTrue(self.controller.is_running)
        self.assertTrue(self.controller.started_once)

        self.controller.stop()
        self.assertFalse(self.controller.is_running)
        self.assertFalse(self.controller.started_once)

    def test_pause_and_resume(self) -> None:
        """Test the pause and resume functionality."""
        self.controller.start()
        self.assertTrue(self.controller.is_running)

        self.controller.pause()
        self.assertFalse(self.controller.is_running)
        self.assertTrue(self.controller.started_once)  # Should still be true

        # In the refactored CameraController, start() now handles resuming
        self.controller.start()  # Changed from self.controller.resume()
        self.assertTrue(self.controller.is_running)

    def test_toggle(self) -> None:
        """Test the toggle functionality."""
        self.assertFalse(self.controller.is_running)

        self.controller.toggle()
        self.assertTrue(self.controller.is_running)

        self.controller.toggle()
        self.assertFalse(self.controller.is_running)

    def test_get_frame(self) -> None:
        """Test that get_frame retrieves a frame when running."""
        self.controller.start()
        time.sleep(0.1)  # Allow time for a frame to be "generated"
        frame = self.controller.get_frame()
        self.assertIsNotNone(frame)
        self.assertIsInstance(frame, np.ndarray)  # Changed from FrameData to np.ndarray

    def test_get_frame_when_paused(self) -> None:
        """Test that get_frame returns None when paused."""
        self.controller.start()
        self.controller.pause()
        frame = self.controller.get_frame()
        self.assertIsNone(frame)

    def test_invalid_camera_interface(self) -> None:
        """Test that the controller raises an error with an invalid camera object."""

        # Create a dummy object that doesn't conform to ICamera
        class BadCamera:
            pass

        with self.assertRaises(TypeError):
            CameraController(
                camera=BadCamera(),  # type: ignore[arg-type] # Re-added type ignore for mypy
                update_callback=self.update_callback,
            )


if __name__ == "__main__":
    unittest.main()
