"""
This module defines the service provider for the TopoVision application,
which handles the creation and provision of all major components.
It acts as a central registry for dependencies, promoting a clean
architecture and easier testing.
"""

from typing import Optional

from topovision.calculus.calculus_module import AnalysisContext
from topovision.capture.capture_module import MockCamera, ThreadedOpenCVCamera
from topovision.capture.preprocessing import GaussianBlurStrategy, ImagePreprocessor
from topovision.core.interfaces import ICamera
from topovision.gui.gui_module import MainWindow
from topovision.services.task_queue import TaskQueue


class ServiceProvider:
    """
    A central service provider for managing and injecting dependencies
    across the TopoVision application.
    """

    def __init__(self, use_mock_camera: bool = False, lang: str = "en"):
        """
        Initializes the service provider.

        Args:
            use_mock_camera (bool): If True, a mock camera will be used.
            lang (str): The default language for the application UI.
        """
        self._use_mock_camera = use_mock_camera
        self._lang = lang

        # Lazily loaded services
        self._camera: Optional[ICamera] = None
        self._main_window: Optional[MainWindow] = None
        self._analysis_context: Optional[AnalysisContext] = None
        self._task_queue: Optional[TaskQueue] = None
        self._image_preprocessor: Optional[ImagePreprocessor] = (
            None  # Updated type hint
        )

    @property
    def camera(self) -> ICamera:
        """Provides a camera instance (either real or mock)."""
        if self._camera is None:
            if self._use_mock_camera:
                self._camera = MockCamera()
            else:
                self._camera = ThreadedOpenCVCamera(camera_id=0)
        return self._camera

    @property
    def image_preprocessor(self) -> ImagePreprocessor:  # Updated return type hint
        """
        Provides an ImagePreprocessor instance with a default Gaussian blur strategy.
        """
        if self._image_preprocessor is None:
            # Default to GaussianBlurStrategy, can be made configurable
            self._image_preprocessor = ImagePreprocessor(
                strategy=GaussianBlurStrategy(kernel_size=(5, 5))
            )
        return self._image_preprocessor

    @property
    def analysis_context(self) -> AnalysisContext:
        """Provides an AnalysisContext instance."""
        if self._analysis_context is None:
            self._analysis_context = AnalysisContext()
        return self._analysis_context

    @property
    def task_queue(self) -> TaskQueue:
        """Provides a TaskQueue instance for background processing."""
        if self._task_queue is None:
            self._task_queue = TaskQueue()
        return self._task_queue

    @property
    def main_window(self) -> MainWindow:
        """
        Provides a MainWindow instance, injecting all required services.
        This ensures the MainWindow is properly initialized with its dependencies.
        """
        if self._main_window is None:
            self._main_window = MainWindow(
                camera=self.camera,
                calculus_module=self.analysis_context,  # Renamed to analysis_context
                task_queue=self.task_queue,
                preprocessor=self.image_preprocessor,
                lang=self._lang,
            )
        return self._main_window
