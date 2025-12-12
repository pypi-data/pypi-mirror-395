"""
A thread-safe task queue for running background operations, preventing UI freezes.
"""

import logging
import queue
import threading
from typing import Any, Callable, Dict, Optional, Tuple, Union

# Configure logging for this module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TaskQueue:
    """
    Manages a queue of tasks to be executed in a background thread.
    This prevents long-running operations from freezing the main GUI thread.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskQueue, setting up the task and result queues,
        and starting the worker thread.
        """
        self._task_queue: queue.Queue[
            Tuple[Callable[..., Any], Tuple[Any, ...], Dict[str, Any]]
        ] = queue.Queue()
        self._result_queue: queue.Queue[Union[Any, Exception]] = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread: threading.Thread = threading.Thread(
            target=self._process_tasks, daemon=True
        )
        self._worker_thread.start()
        logger.info("TaskQueue worker thread started.")

    def _process_tasks(self) -> None:
        """
        The main loop for the worker thread. It continuously fetches tasks
        from the task queue and executes them. Results or exceptions are
        placed into the result queue.
        """
        while not self._stop_event.is_set():
            task_item = None  # Initialize to None
            try:
                # Use a timeout to allow the thread to check the stop event periodically
                task_item = self._task_queue.get(timeout=0.1)
                task, args, kwargs = task_item  # Unpack only if get() was successful

                logger.debug(f"Executing task: {task.__name__}")
                result = task(*args, **kwargs)
                self._result_queue.put(result)
            except queue.Empty:
                continue  # No task, check stop event again
            except Exception as e:
                # If an exception occurs during task execution,
                # put it in the result queue and log it.
                task_name = task.__name__ if "task" in locals() else "unknown"
                logger.error(f"Error executing task {task_name}: {e}", exc_info=True)
                self._result_queue.put(e)
            finally:
                # Mark the task as done ONLY if a task was successfully retrieved
                if task_item is not None:
                    self._task_queue.task_done()
        logger.info("TaskQueue worker thread stopped.")

    def submit_task(self, task: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """
        Submits a new task to be executed in the background.

        Args:
            task (Callable[..., Any]): The function to execute.
            *args: Positional arguments for the task function.
            **kwargs: Keyword arguments for the task function.
        """
        self._task_queue.put((task, args, kwargs))
        logger.debug(f"Task '{task.__name__}' submitted.")

    def get_result(self) -> Optional[Union[Any, Exception]]:
        """
        Retrieves a result from the result queue if available.
        This method is non-blocking.

        Returns:
            Optional[Union[Any, Exception]]: The result of a completed task,
            an Exception if the task failed, or None if no result is available.
        """
        try:
            return self._result_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self) -> None:
        """
        Signals the worker thread to stop and waits for it to terminate.
        This should be called when the application is shutting down.
        """
        logger.info("Stopping TaskQueue worker thread...")
        self._stop_event.set()
        # Wait for any currently processing tasks to finish and for the thread to exit
        self._worker_thread.join(timeout=5)  # Give it some time to finish
        if self._worker_thread.is_alive():
            logger.warning("TaskQueue worker thread did not terminate gracefully.")
