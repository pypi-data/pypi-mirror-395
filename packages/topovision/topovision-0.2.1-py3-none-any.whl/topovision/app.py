"""
TopoVision main application entry point.

This module initializes the application, sets up dependency injection
using the ServiceProvider, and starts the main GUI loop.
"""

import logging
import sys

from topovision.services.service_provider import ServiceProvider

# Configure basic logging for the application
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Entry point for the TopoVision system.
    Initializes services and starts the main application window.
    """
    logger.info("🚀 TopoVision application starting...")

    # Determine if a mock camera should be used (e.g., for development/testing)
    # This could be made configurable via command-line arguments or a config file.
    use_mock_camera = False

    # Default language for the UI
    app_language = "en"  # Could also be made configurable

    service_provider = None  # Initialize to None for finally block

    try:
        # --- Dependency Injection ---
        # The ServiceProvider orchestrates the creation and linking of all components.
        service_provider = ServiceProvider(
            use_mock_camera=use_mock_camera, lang=app_language
        )

        # Get the main window from the service provider, which has all its
        # dependencies (camera, calculus module, task queue, preprocessor) injected.
        app = service_provider.main_window

        # Run the main application loop. This call is blocking until the GUI is closed.
        app.run()

    except Exception as e:
        logger.critical(
            f"Unhandled error during application startup: {e}", exc_info=True
        )
        sys.exit(1)  # Exit with an error code

    finally:
        # Ensure resources are properly cleaned up, especially the TaskQueue's thread.
        if service_provider and service_provider.task_queue:
            service_provider.task_queue.stop()
            logger.info("TaskQueue stopped during application shutdown.")
        logger.info("TopoVision application finished.")


if __name__ == "__main__":
    main()
