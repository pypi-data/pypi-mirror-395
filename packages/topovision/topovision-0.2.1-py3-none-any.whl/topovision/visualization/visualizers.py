"""
This module defines visualizers for analysis results.
"""

from typing import Optional, cast

import cv2
import numpy as np
from numpy.typing import NDArray
from PIL import Image

from topovision.core.models import AnalysisResult, GradientResult


class HeatmapVisualizer:
    """
    A visualizer for creating heatmaps from analysis results.
    """

    def visualize(
        self,
        analysis_result: AnalysisResult,
        original_image: Image.Image,
        inverse_matrix: Optional[NDArray[np.float64]] = None,
        src_quad: Optional[NDArray[np.float32]] = None,
    ) -> Image.Image:
        """
        Generates a heatmap visualization for the given analysis result.
        """
        if isinstance(analysis_result.result_data, GradientResult):
            return self._create_gradient_heatmap(
                analysis_result, original_image, inverse_matrix, src_quad
            )
        return original_image

    def _create_gradient_heatmap(
        self,
        analysis_result: AnalysisResult,
        original_image: Image.Image,
        inverse_matrix: Optional[NDArray[np.float64]],
        src_quad: Optional[NDArray[np.float32]],
    ) -> Image.Image:
        """
        Creates a heatmap for a GradientResult, handling perspective correction.
        """
        if not isinstance(analysis_result.result_data, GradientResult):
            return original_image

        gradient_result = analysis_result.result_data
        magnitude = gradient_result.magnitude
        if magnitude is None:
            return original_image

        # Normalize the magnitude to the 0-255 range
        if np.max(magnitude) > 0:
            norm_magnitude = (
                (magnitude - np.min(magnitude))
                / (np.max(magnitude) - np.min(magnitude))
                * 255
            ).astype(np.uint8)
        else:
            norm_magnitude = np.zeros_like(magnitude, dtype=np.uint8)

        heatmap_color = cv2.applyColorMap(norm_magnitude, cv2.COLORMAP_JET)

        if inverse_matrix is not None and src_quad is not None:
            # Warp the heatmap back to the original image's perspective
            warped_heatmap = cv2.warpPerspective(
                heatmap_color,
                inverse_matrix,
                (original_image.width, original_image.height),
            )
            # Create a single-channel mask to blend only within the selected quad
            mask = np.zeros(
                (original_image.height, original_image.width), dtype=np.uint8
            )
            # Ensure src_quad is int32 for fillConvexPoly and color is a sequence
            cv2.fillConvexPoly(
                mask, src_quad.astype(np.int32), (255,)
            )  # Changed 255 to (255,)

            # Blend using the mask
            original_np = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
            blended_np = np.where(
                mask[:, :, None] > 0,  # Expand mask to 3 channels for comparison
                cv2.addWeighted(original_np, 0.4, warped_heatmap, 0.6, 0),
                original_np,
            )
            return cast(
                Image.Image,
                Image.fromarray(cv2.cvtColor(blended_np, cv2.COLOR_BGR2RGB)),
            )
        else:
            # Original logic for rectangular selection without perspective
            heatmap_pil = cast(
                Image.Image,
                Image.fromarray(cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)),
            )
            region = analysis_result.region
            if heatmap_pil.size != (region.width, region.height):
                heatmap_pil = heatmap_pil.resize((region.width, region.height))

            original_crop = original_image.crop(
                (region.x1, region.y1, region.x2, region.y2)
            )
            blended_image = Image.blend(original_crop, heatmap_pil, alpha=0.6)
            final_image = original_image.copy()
            final_image.paste(blended_image, (region.x1, region.y1))
            return final_image
