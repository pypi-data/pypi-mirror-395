"""
Overlay utilities for TopoVision.
"""

import numpy as np
from PIL import Image


def overlay_image(
    background: Image.Image, overlay: Image.Image, position: tuple[int, int]
) -> Image.Image:
    """
    Overlays a semi-transparent image onto a background image.

    Args:
        background (Image.Image): The background image.
        overlay (Image.Image): The overlay image, which can have an alpha channel.
        position (tuple[int, int]): The (x, y) position where the overlay
                                    should be placed.

    Returns:
        Image.Image: The combined image.
    """
    # Create a copy of the background to not alter the original
    combined = background.copy()

    # Ensure overlay has an alpha channel for transparency
    overlay = overlay.convert("RGBA")

    # Paste the overlay onto the background
    combined.paste(overlay, position, overlay)

    return combined
