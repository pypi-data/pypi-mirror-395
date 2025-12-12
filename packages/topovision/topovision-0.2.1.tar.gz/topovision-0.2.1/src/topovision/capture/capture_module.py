"""
Handles camera capture and provides different camera implementations.
"""

import logging
import threading
import time
from typing import Optional, cast

import cv2
import numpy as np
from numpy.typing import NDArray

from topovision.core.interfaces import ICamera
from topovision.core.models import FrameData

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ThreadedOpenCVCamera(ICamera):
    """
    A camera implementation using OpenCV that runs the frame-grabbing
    in a separate thread to prevent blocking the main application.
    """

    def __init__(self, camera_id: int = 0):
        """
        Initializes the threaded OpenCV camera.

        Args:
            camera_id (int): The ID of the camera to use
                             (e.g., 0 for the default camera).
        """
        self.camera_id = camera_id
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.frame_lock = threading.Lock()
        self.latest_frame: Optional[FrameData] = None
        self.capture_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def start(self) -> None:
        if self.is_running:
            logging.warning("Camera is already running.")
            return

        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            self.cap = None
            raise IOError(f"Cannot open camera {self.camera_id}")

        self.is_running = True
        self.stop_event.clear()
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        logging.info(f"Camera {self.camera_id} started.")

    def _capture_loop(self) -> None:
        """The main loop for capturing frames in the background."""
        frame_number = 0
        while not self.stop_event.is_set():
            if not self.is_running or self.cap is None:
                time.sleep(0.01)
                continue

            ret, frame = self.cap.read()
            if ret:
                timestamp = time.time()
                frame_number += 1
                with self.frame_lock:
                    # Convert color space once, right after capture
                    rgb_frame = cast(
                        NDArray[np.uint8], cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    )
                    self.latest_frame = FrameData(
                        image=rgb_frame, timestamp=timestamp, frame_number=frame_number
                    )
            else:
                logging.warning("Failed to grab frame from camera.")
                time.sleep(0.1)  # Wait a bit before retrying

    def stop(self) -> None:
        if not self.is_running and self.capture_thread is None:
            return

        self.stop_event.set()
        if self.capture_thread:
            self.capture_thread.join(timeout=2)  # Wait for the thread to finish
            if self.capture_thread.is_alive():
                logging.error("Capture thread did not terminate gracefully.")

        if self.cap:
            self.cap.release()

        self.cap = None
        self.is_running = False
        self.latest_frame = None
        logging.info(f"Camera {self.camera_id} stopped.")

    def pause(self) -> None:
        if self.is_running:
            self.is_running = False
            logging.info(f"Camera {self.camera_id} paused.")

    def resume(self) -> None:
        if not self.is_running:
            self.is_running = True
            logging.info(f"Camera {self.camera_id} resumed.")

    def get_frame(self) -> Optional[FrameData]:
        """
        Fetches the latest captured frame without blocking.

        Returns:
            The latest FrameData object, or None if no frame is available.
        """
        with self.frame_lock:
            return self.latest_frame


class MockCamera(ICamera):
    """
    A mock camera for testing and development. It generates synthetic frames
    with configurable patterns.
    """

    def __init__(
        self, width: int = 640, height: int = 480, pattern: str = "checkerboard"
    ):
        self.width = width
        self.height = height
        self.pattern = pattern
        self.is_running = False
        self._frame_counter = 0
        self._frame_rate = 30

    def start(self) -> None:
        self.is_running = True
        logging.info("Mock camera started.")

    def stop(self) -> None:
        self.is_running = False
        logging.info("Mock camera stopped.")

    def pause(self) -> None:
        self.is_running = False
        logging.info("Mock camera paused.")

    def resume(self) -> None:
        self.is_running = True
        logging.info("Mock camera resumed.")

    def get_frame(self) -> Optional[FrameData]:
        """
        Fetches the latest captured frame without blocking.

        Returns:
            The latest FrameData object, or None if no frame is available.
        """
        if not self.is_running:
            return None

        frame = self._generate_mock_frame()
        timestamp = time.time()
        self._frame_counter += 1

        time.sleep(1 / self._frame_rate)  # Simulate frame rate
        return FrameData(
            image=frame, timestamp=timestamp, frame_number=self._frame_counter
        )

    def _generate_mock_frame(self) -> NDArray[np.uint8]:
        """Generates a frame based on the selected pattern."""
        if self.pattern == "checkerboard":
            return self._create_checkerboard_frame()
        elif self.pattern == "gradient":
            return self._create_gradient_frame()
        else:  # Default to a simple color-changing frame
            return self._create_color_change_frame()

    def _create_checkerboard_frame(self) -> NDArray[np.uint8]:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        tile_size = 50
        phase = (self._frame_counter // 15) % 2  # Change pattern every 15 frames
        for y in range(0, self.height, tile_size):
            for x in range(0, self.width, tile_size):
                if (x // tile_size + y // tile_size + phase) % 2 == 0:
                    frame[y : y + tile_size, x : x + tile_size] = (255, 255, 255)
        return frame

    def _create_gradient_frame(self) -> NDArray[np.uint8]:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        ramp = np.linspace(0, 255, self.width, dtype=np.uint8)
        frame[:, :, 0] = ramp  # Blue gradient
        frame[:, :, 1] = np.roll(
            ramp, self._frame_counter * 5
        )  # Shifting green gradient
        return frame

    def _create_color_change_frame(self) -> NDArray[np.uint8]:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        color_val = (self._frame_counter * 5) % 256
        channel = self._frame_counter % 3
        frame[:, :, channel] = color_val
        return frame
