"""
This module defines the UI themes for the TopoVision application.

It provides a structured way to define and apply visual styles,
making it easy to add new themes or customize existing ones.
"""

from tkinter import ttk
from typing import Any, Dict, Optional

# --- Theme Definitions ---

THEMES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "dark": {
        "colors": {
            "bg": "#1e1e1e",
            "fg": "#d4d4d4",
            "primary": "#007acc",
            "button_bg": "#2a2d2e",
            "button_active_bg": "#3c3f41",
            "separator": "#3c3f41",
            "button_fg": "#ffffff",
        },
        "fonts": {
            "family": "Segoe UI",
            "size": 10,
            "heading": ("Segoe UI", 12, "bold"),
        },
    },
    "light": {
        "colors": {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "primary": "#0078d7",
            "button_bg": "#e1e1e1",
            "button_active_bg": "#cccccc",
            "separator": "#cccccc",
            "button_fg": "#000000",
        },
        "fonts": {
            "family": "Segoe UI",
            "size": 10,
            "heading": ("Segoe UI", 12, "bold"),
        },
    },
}

DEFAULT_THEME = "dark"


class ThemeManager:
    """Manages the application's visual theme."""

    def __init__(self, style: ttk.Style):
        """
        Initializes the ThemeManager.

        Args:
            style (ttk.Style): The ttk.Style object to configure.
        """
        if not isinstance(style, ttk.Style):
            raise TypeError("style must be a ttk.Style object")
        self.style = style
        self.themes = THEMES
        self.current_theme: Optional[Dict[str, Dict[str, Any]]] = None

    def apply(self, theme_name: str = DEFAULT_THEME) -> None:
        """
        Applies a theme to the application.

        Args:
            theme_name (str): The name of the theme to apply (e.g., 'dark').

        Raises:
            ValueError: If the theme_name is not found in the themes dictionary.
        """
        if theme_name not in self.themes:
            raise ValueError(f"Theme '{theme_name}' not found.")

        self.current_theme = self.themes[theme_name]

        # Ensure current_theme is not None before accessing its keys
        if self.current_theme is None:
            # This case should ideally not be reached due to the check above,
            # but for MyPy's sake and robustness, we can handle it or assert.
            # For now, let's assume it's always a dict after the check.
            pass

        colors = self.current_theme["colors"]
        fonts = self.current_theme["fonts"]

        # --- Style Configuration ---
        self.style.theme_use("clam")

        self.style.configure("TFrame", background=colors["bg"])
        self.style.configure(
            "TLabel",
            background=colors["bg"],
            foreground=colors["fg"],
            font=(fonts["family"], fonts["size"]),
        )
        self.style.configure(
            "TButton",
            background=colors["button_bg"],
            foreground=colors["button_fg"],
            padding=8,
            borderwidth=1,
            relief="solid",
            bordercolor=colors["separator"],
            font=(fonts["family"], fonts["size"], "bold"),
        )
        self.style.map(
            "TButton",
            background=[("active", colors["button_active_bg"])],
            foreground=[("active", colors["button_fg"])],
            bordercolor=[("active", colors["primary"])],
        )
        self.style.configure(
            "Heading.TLabel", font=fonts["heading"], foreground=colors["primary"]
        )
        self.style.configure("TSeparator", background=colors["separator"])
