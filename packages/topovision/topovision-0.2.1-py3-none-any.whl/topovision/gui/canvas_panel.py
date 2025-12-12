"""
Canvas Panel for TopoVision.

This module defines a custom Tkinter Canvas that allows users to select
a rectangular region or four points for calibration.
"""

import tkinter as tk
from typing import Any, Callable, List, Optional, Tuple


class CanvasPanel(tk.Canvas):
    """
    A custom canvas for displaying video and handling user selections.
    """

    MIN_SELECTION_SIZE = 10  # Minimum size for a valid selection

    def __init__(
        self,
        parent: tk.Widget,
        **kwargs: Any,
    ):
        """
        Initializes the CanvasPanel.
        """
        super().__init__(parent, **kwargs)

        self._selection_start: Optional[Tuple[int, int]] = None
        self._selection_rect_id: Optional[int] = None
        self.selected_region: Optional[Tuple[int, int, int, int]] = None

        self.on_selection_made: Optional[Callable[..., None]] = None
        self.on_calibration_point_added: Optional[
            Callable[[List[Tuple[int, int]]], None]
        ] = None

        self.is_calibration_mode = False
        self.calibration_points: List[Tuple[int, int]] = []

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

    def start_calibration(self) -> None:
        """Activates calibration mode, clearing only previous calibration points."""
        self.is_calibration_mode = True
        self.calibration_points = []
        self.clear_selection()
        self.delete("calibration_point")

    def stop_calibration(self) -> None:
        """Deactivates calibration mode."""
        self.is_calibration_mode = False
        self.delete("calibration_point")

    def _on_press(self, event: tk.Event) -> None:  # Removed [Any]
        """Handles the initial click."""
        if self.is_calibration_mode:
            if len(self.calibration_points) < 4:
                self.calibration_points.append((event.x, event.y))
                self._draw_calibration_point(event.x, event.y)
                if self.on_calibration_point_added:
                    self.on_calibration_point_added(self.calibration_points)
        else:
            self._selection_start = (event.x, event.y)
            self.delete("selection")

    def _draw_calibration_point(self, x: int, y: int) -> None:
        """Draws a visual marker for a calibration point."""
        self.create_oval(
            x - 3,
            y - 3,
            x + 3,
            y + 3,
            fill="#FFD34D",
            outline="white",
            tags="calibration_point",
        )

    def _on_drag(self, event: tk.Event) -> None:  # Removed [Any]
        """Handles dragging to draw a selection rectangle."""
        if self.is_calibration_mode or not self._selection_start:
            return

        x1, y1 = self._selection_start
        x2, y2 = event.x, event.y

        self.delete("selection")
        self._selection_rect_id = self.create_rectangle(
            x1, y1, x2, y2, outline="#FFD34D", width=2, dash=(3, 2), tags="selection"
        )

    def _on_release(self, event: tk.Event) -> None:  # Removed [Any]
        """Finalizes the selection."""
        if self.is_calibration_mode or not self._selection_start:
            return

        x1, y1 = self._selection_start
        x2, y2 = event.x, event.y
        self._selection_start = None

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        if (x2 - x1) < self.MIN_SELECTION_SIZE or (y2 - y1) < self.MIN_SELECTION_SIZE:
            self.delete("selection")
            if self.on_selection_made:
                self.on_selection_made(
                    None, "selection_too_small", min_size=self.MIN_SELECTION_SIZE
                )
            return

        self.selected_region = (x1, y1, x2, y2)

        if self.on_selection_made:
            self.on_selection_made(self.selected_region, "selection_made")

    def clear_selection(self) -> None:
        """Clears the current selection rectangle and region data."""
        self.selected_region = None
        self.delete("selection")
        if self.on_selection_made:
            self.on_selection_made(None, "selection_cleared")
