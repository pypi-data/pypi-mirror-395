"""
Heatmap rendering utilities for TopoVision.

This module provides functionality to generate heatmaps from 2D numerical data
using matplotlib, optimized for a dark, minimal aesthetic.
"""

import io
from typing import Any, Optional, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.spines import Spine  # Import Spine
from numpy.typing import NDArray
from PIL import Image

from topovision.gui.i18n import get_translator  # Import the translator


def generate_heatmap(
    data: NDArray[Any],  # Changed to NDArray[Any]
    cmap: str = "plasma",
    label_key: str = "gradient_magnitude_label",  # Changed to a key for i18n
    lang: str = "en",  # Added language parameter
) -> Image.Image:
    """
    Generates a heatmap as a PIL.Image from a 2D numpy array.

    Args:
        data (NDArray[Any]): 2D matrix of numerical values.
        cmap (str): Name of the colormap to use (default: 'plasma',
                    good for dark themes).
        label_key (str): The key for the color bar label, to be translated.
        lang (str): The language code for translation.

    Returns:
        PIL.Image: RGB image containing the heatmap.

    Raises:
        ValueError: If the input data is not a valid 2D numpy array.
    """
    if data is None or not isinstance(data, np.ndarray):
        raise ValueError("Heatmap requires a valid numpy 2D array.")

    if data.ndim != 2:
        raise ValueError("Heatmap only accepts 2D matrices.")

    _ = get_translator(lang)  # Get the translator function

    # ---- Figure configuration (dark minimal) ----
    fig = plt.figure(figsize=(4, 3), dpi=120)
    ax = fig.add_subplot(111)

    # Dark theme colors
    BG_COLOR = "#111214"
    TEXT_COLOR = "white"
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)

    # 1. Draw heatmap
    img_plot = ax.imshow(data, cmap=cmap, aspect="auto")
    ax.set_axis_off()

    # 2. Add Color Bar (Legend) for visual scaling refinement
    cbar = fig.colorbar(img_plot, ax=ax, orientation="vertical", shrink=0.8, pad=0.03)

    # 3. Apply dark theme to color bar elements
    # Explicitly cast cbar.outline to Spine to help mypy
    cbar_outline: Spine = cast(Spine, cbar.outline)  # Added cast
    cbar.ax.yaxis.set_tick_params(color=TEXT_COLOR)
    cbar_outline.set_edgecolor("none")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color=TEXT_COLOR, fontsize=8)

    # 4. Set descriptive label using the translator
    translated_label = _(label_key)  # Call translator explicitly
    cbar.set_label(translated_label, color=TEXT_COLOR, fontsize=9)

    plt.tight_layout(pad=0.5)

    # Convert to image
    buffer = io.BytesIO()
    # Cast fig.canvas to Any to resolve mypy error about print_png
    cast(Any, fig.canvas).print_png(buffer)
    plt.close(fig)  # Close the figure to free up memory

    buffer.seek(0)
    img = Image.open(buffer).convert("RGB")
    return img
