"""
Custom exceptions used across the TopoVision system.

Defining custom exceptions helps in creating a more robust and readable
error-handling mechanism, allowing specific errors to be caught and
handled appropriately.
"""


class TopoVisionError(Exception):
    """Base class for all custom exceptions in TopoVision."""

    pass


class CameraError(TopoVisionError):
    """Exception raised for errors related to camera operations."""

    def __init__(self, message: str = "A camera-related error occurred."):
        self.message = message
        super().__init__(self.message)


class AnalysisError(TopoVisionError):
    """Exception raised for errors during topographic analysis calculations."""

    def __init__(self, message: str = "An error occurred during analysis calculation."):
        self.message = message
        super().__init__(self.message)


class VisualizationError(TopoVisionError):
    """Exception raised for errors during visualization processes."""

    def __init__(self, message: str = "An error occurred during visualization."):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(TopoVisionError):
    """Exception raised for invalid or missing configuration settings."""

    def __init__(self, message: str = "An application configuration error occurred."):
        self.message = message
        super().__init__(self.message)


class InvalidInputError(TopoVisionError):
    """Exception raised for invalid input data or parameters."""

    def __init__(self, message: str = "Invalid input data or parameters provided."):
        self.message = message
        super().__init__(self.message)
