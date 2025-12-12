"""
Camera Controller for TopoVision.

This module provides a controller to manage the camera's lifecycle,
including starting, pausing, and stopping the video feed.
"""

import logging
from typing import Any, Callable, Optional

import numpy as np
from numpy.typing import NDArray

from topovision.core.interfaces import ICamera as ConcreteICamera
from topovision.core.models import FrameData


class CameraController:
    """
    Manages camera operations and state.

    This class acts as a high-level interface to the camera, abstracting
    the underlying state management for starting, pausing, and stopping.
    """

    def __init__(
        self,
        camera: ConcreteICamera,
        update_callback: Callable[[NDArray[Any]], None],  # Changed to NDArray[Any]
    ):
        """
        Initializes the CameraController.

        Args:
            camera (ConcreteICamera): The camera instance to control.
            update_callback (Callable[[NDArray[Any]], None]): A callback to be invoked
                with the latest frame for UI updates.
        """
        if not isinstance(camera, ConcreteICamera):
            raise TypeError(
                "The provided camera object does not implement the ICamera interface."
            )
        self.camera = camera
        self._update_callback = update_callback
        self._is_running = False
        self._started_once = False

    @property
    def is_running(self) -> bool:
        """Returns True if the camera is currently capturing frames."""
        return self._is_running

    @property
    def started_once(self) -> bool:
        """Returns True if the camera has been started at least once."""
        return self._started_once

    def start(self) -> None:
        """Starts or resumes the camera feed."""
        if self._is_running:
            return

        try:
            if not self._started_once:
                self.camera.start()
                self._started_once = True
                logging.info("Camera started for the first time.")
            else:
                self.camera.resume()
                logging.info("Camera resumed.")
            self._is_running = True
        except Exception as e:
            logging.error(f"Failed to start or resume camera: {e}")
            self._is_running = False
            raise

    def pause(self) -> None:
        if not self._is_running:
            return

        try:
            self.camera.pause()
            self._is_running = False
            logging.info("Camera paused.")
        except Exception as e:
            logging.error(f"Failed to pause camera: {e}")
            raise

    def stop(self) -> None:
        if not self._started_once:
            return

        try:
            self.camera.stop()
            self._is_running = False
            self._started_once = False
            logging.info("Camera stopped.")
        except Exception as e:
            logging.error(f"Failed to stop camera: {e}")
            # Still update state, as the camera might be unusable
            self._is_running = False
            self._started_once = False
            raise

    def toggle(self) -> None:
        """Toggles the camera state between running and paused."""
        if self._is_running:
            self.pause()
        else:
            self.start()

    def get_frame(self) -> Optional[NDArray[Any]]:  # Changed to NDArray[Any]
        """
        Retrieves the latest frame from the camera.

        Returns:
            Optional[NDArray[Any]]: The frame as a NumPy array, or None if no
            frame is available or the camera is not running.
        """
        if not self._is_running:
            return None
        frame_data: Optional[FrameData] = self.camera.get_frame()
        if frame_data:
            return frame_data.image
        return None
