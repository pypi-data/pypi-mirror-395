"""
This module defines the AnalysisPanel class, which is a UI component
for displaying analysis controls in the TopoVision application.
"""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, List

from topovision.gui.i18n import Translator


class AnalysisPanel(ttk.Frame):
    """
    A panel for analysis controls, parameters, and status feedback.
    """

    def __init__(
        self,
        parent: tk.Widget,
        analysis_callback: Callable[[str, str], None],
        translator: Translator,
        available_units: List[str],
        scale_update_callback: Callable[[float], None],
        calibration_callback: Callable[[], None],
        apply_calibration_callback: Callable[[float, float], None],
        show_tutorial_callback: Callable[[str], None],
        **kwargs: Any,
    ):
        super().__init__(parent, **kwargs)
        self.analysis_callback = analysis_callback
        self._ = translator
        self.available_units = available_units
        self.selected_unit = tk.StringVar(value=self.available_units[0])
        self.scale_update_callback = scale_update_callback
        self.calibration_callback = calibration_callback
        self.apply_calibration_callback = apply_calibration_callback
        self.show_tutorial_callback = show_tutorial_callback
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        """Creates and arranges the widgets in the panel using the grid manager."""
        self.columnconfigure(0, weight=1)
        self.bind("<Enter>", lambda e: self.show_tutorial_callback("analysis_panel"))

        row = 0
        row = self._create_section(self._("calculation_parameters_title"), row)
        row = self._create_z_factor_input(row)
        row = self._create_scale_input(row)
        row = self._create_unit_selection(row)

        row = self._create_section(self._("calibration_title"), row)
        row = self._create_calibration_widgets(row)

        row = self._create_section(self._("analysis_actions_title"), row)
        row = self._create_analysis_buttons(row)

        row = self._create_section(self._("visualization_title"), row)
        row = self._create_visualization_buttons(row)

        self._create_status_label()

    def _create_section(self, text: str, row: int) -> int:
        """Creates a styled header and separator for a section."""
        ttk.Label(self, text=text, style="Heading.TLabel").grid(
            row=row, column=0, sticky="w", padx=5, pady=(15, 5)
        )
        ttk.Separator(self).grid(row=row + 1, column=0, sticky="ew", padx=5)
        return row + 2

    def _create_z_factor_input(self, row: int) -> int:
        """Creates the Z-factor input field."""
        frame = ttk.Frame(self)
        frame.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        ttk.Label(frame, text=self._("z_factor_label")).pack(side=tk.LEFT, padx=(0, 5))
        self.z_factor_entry = ttk.Entry(frame, width=10)
        self.z_factor_entry.insert(0, "1.0")
        self.z_factor_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.z_factor_entry.bind(
            "<FocusIn>", lambda e: self.show_tutorial_callback("z_factor")
        )
        return row + 1

    def _create_scale_input(self, row: int) -> int:
        """Creates the scale input field."""
        frame = ttk.Frame(self)
        frame.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        ttk.Label(frame, text=self._("scale_label")).pack(side=tk.LEFT, padx=(0, 5))
        self.scale_entry = ttk.Entry(frame, width=10)
        self.scale_entry.insert(0, "100.0")
        self.scale_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.scale_entry.bind(
            "<FocusIn>", lambda e: self.show_tutorial_callback("scale")
        )
        self.scale_entry.bind("<FocusOut>", self._on_scale_change)
        self.scale_entry.bind("<Return>", self._on_scale_change)
        return row + 1

    def _on_scale_change(self, event: Any) -> None:
        try:
            scale = self.get_scale()
            self.scale_update_callback(scale)
        except ValueError as e:
            self.set_status(str(e), is_error=True)

    def _create_unit_selection(self, row: int) -> int:
        """Creates the unit selection dropdown."""
        frame = ttk.Frame(self)
        frame.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        ttk.Label(frame, text=self._("unit_label")).pack(side=tk.LEFT, padx=(0, 5))
        self.unit_combobox = ttk.Combobox(
            frame,
            textvariable=self.selected_unit,
            values=self.available_units,
            state="readonly",
        )
        self.unit_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.unit_combobox.set(self.available_units[0])
        return row + 1

    def _create_calibration_widgets(self, row: int) -> int:
        """Creates widgets for the calibration section."""

        def on_calibrate_click() -> None:
            self.calibration_callback()
            self.show_tutorial_callback("calibrate_perspective")

        self.calibrate_btn = ttk.Button(
            self,
            text=self._("calibrate_button"),
            command=on_calibrate_click,
            style="TButton",
        )
        self.calibrate_btn.grid(row=row, column=0, sticky="ew", padx=10, pady=5)

        self.calibration_frame = ttk.Frame(self)
        self.calibration_frame.grid(row=row + 1, column=0, sticky="ew", padx=10, pady=5)
        self.calibration_frame.grid_remove()  # Hide by default

        ttk.Label(self.calibration_frame, text=self._("real_width_label")).grid(
            row=0, column=0, sticky="w"
        )
        self.real_width_entry = ttk.Entry(self.calibration_frame, width=8)
        self.real_width_entry.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(self.calibration_frame, text=self._("real_height_label")).grid(
            row=1, column=0, sticky="w", pady=(5, 0)
        )
        self.real_height_entry = ttk.Entry(self.calibration_frame, width=8)
        self.real_height_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(5, 0))

        self.apply_calibration_btn = ttk.Button(
            self.calibration_frame,
            text=self._("apply_calibration_button"),
            command=self._on_apply_calibration,
            style="TButton",
        )
        self.apply_calibration_btn.grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )

        return row + 2

    def show_calibration_inputs(self) -> None:
        """Shows the calibration input fields."""
        self.calibration_frame.grid()

    def hide_calibration_inputs(self) -> None:
        """Hides the calibration input fields."""
        self.calibration_frame.grid_remove()

    def _on_apply_calibration(self) -> None:
        try:
            width = float(self.real_width_entry.get())
            height = float(self.real_height_entry.get())
            if width <= 0 or height <= 0:
                raise ValueError(self._("calibration_invalid_dimensions"))
            self.apply_calibration_callback(width, height)
        except (ValueError, TypeError):
            self.set_status(self._("calibration_invalid_dimensions"), is_error=True)

    def _create_analysis_buttons(self, row: int) -> int:
        """Creates buttons for triggering different analyses."""
        btn_config = [
            ("gradient_button", "gradient"),
            ("volume_button", "volume"),
            ("arc_length_button", "arc_length"),
        ]
        for i, (text_key, method) in enumerate(btn_config):

            def command_factory(m: str) -> Callable[[], None]:
                return lambda: self.analysis_callback(m, self.get_selected_unit())

            btn = ttk.Button(
                self,
                text=self._(text_key),
                command=command_factory(method),
                style="TButton",
            )
            btn.grid(row=row + i, column=0, sticky="ew", padx=10, pady=2)
        return row + len(btn_config)

    def _create_visualization_buttons(self, row: int) -> int:
        """Creates buttons for view and selection control."""
        self.toggle_btn = ttk.Button(
            self,
            text=self._("toggle_view_button"),
            command=lambda: self.show_tutorial_callback("toggle_view"),
            style="TButton",
        )
        self.toggle_btn.grid(row=row, column=0, sticky="ew", padx=10, pady=5)

        self.clear_btn = ttk.Button(
            self,
            text=self._("clear_selection_button"),
            command=lambda: self.show_tutorial_callback("clear_selection"),
            style="TButton",
        )
        self.clear_btn.grid(row=row + 1, column=0, sticky="ew", padx=10, pady=5)
        return row + 2

    def _create_status_label(self) -> None:
        """Creates the label for status messages."""
        self.status_label_var = tk.StringVar(value=self._("status_ready"))
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_label_var,
            wraplength=220,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.status_label.grid(row=100, column=0, sticky="ew", padx=10, pady=(15, 5))

    def get_z_factor(self) -> float:
        try:
            z_factor = float(self.z_factor_entry.get())
            if z_factor <= 0:
                raise ValueError("Z-factor must be positive.")
            return z_factor
        except ValueError:
            raise ValueError(self._("z_factor_error"))

    def get_scale(self) -> float:
        try:
            scale = float(self.scale_entry.get())
            if scale <= 0:
                raise ValueError("Scale must be positive.")
            return scale
        except ValueError:
            raise ValueError(self._("scale_error"))

    def get_selected_unit(self) -> str:
        return self.selected_unit.get()

    def set_status(self, message: str, is_error: bool = False) -> None:
        color = "#FF6B6B" if is_error else "#E6E6E6"
        self.status_label.config(foreground=color)
        self.status_label_var.set(message)
