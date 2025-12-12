"""
A module for handling perspective correction in TopoVision.
"""

from typing import List, Tuple, cast

import cv2
import numpy as np
from numpy.typing import NDArray


class PerspectiveCorrector:
    """
    A class to handle perspective transformation based on a four-point homography.
    """

    def __init__(
        self,
        src_points: List[Tuple[int, int]],
        real_width: float,
        real_height: float,
    ):
        """
        Initializes the PerspectiveCorrector.

        Args:
            src_points (List[Tuple[int, int]]): A list of four (x, y) tuples
                                                from the image.
            real_width (float): The actual width of the reference object in meters.
            real_height (float): The actual height of the reference object in meters.
        """
        if len(src_points) != 4:
            raise ValueError("Source must contain exactly four points.")
        if real_width <= 0 or real_height <= 0:
            raise ValueError("Real-world dimensions must be positive.")

        self.src_points: NDArray[np.float32] = np.array(src_points, dtype=np.float32)
        self.real_width = real_width
        self.real_height = real_height

        # Define a target rectangle for a "top-down" view.
        # We maintain a consistent pixel density for the corrected view.
        # Let's use a reference of 1000 pixels for the longest dimension.
        if real_width >= real_height:
            self.dst_width_px = 1000
            self.dst_height_px = int(1000 * real_height / real_width)
        else:
            self.dst_height_px = 1000
            self.dst_width_px = int(1000 * real_width / real_height)

        self.dst_points: NDArray[np.float32] = np.array(
            [
                [0, 0],
                [self.dst_width_px - 1, 0],
                [self.dst_width_px - 1, self.dst_height_px - 1],
                [0, self.dst_height_px - 1],
            ],
            dtype=np.float32,
        )

        # The scale of the orthographic (top-down) view
        self.pixels_per_meter = self.dst_width_px / self.real_width

        # Compute the perspective transformation matrix
        self.matrix: NDArray[np.float32] = cast(
            NDArray[np.float32],
            cv2.getPerspectiveTransform(self.src_points, self.dst_points),
        )
        self.inverse_matrix: NDArray[np.float32] = cast(
            NDArray[np.float32],
            cv2.getPerspectiveTransform(self.dst_points, self.src_points),
        )

    def transform_point(self, point: Tuple[float, float]) -> Tuple[float, float]:
        """
        Transforms a single point from image perspective to top-down view.

        Args:
            point (Tuple[float, float]): The (x, y) coordinate in the image.

        Returns:
            Tuple[float, float]: The corrected (x, y) coordinate in the top-down view.
        """
        point_np: NDArray[np.float32] = np.array([[point]], dtype=np.float32)
        transformed_point = cv2.perspectiveTransform(point_np, self.matrix)
        # The output of perspectiveTransform is an array of shape (1, 1, 2)
        return (float(transformed_point[0][0][0]), float(transformed_point[0][0][1]))

    def warp_image(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Applies the perspective warp to an entire image.

        Args:
            image (NDArray[np.uint8]): The source image.

        Returns:
            NDArray[np.uint8]: The resulting top-down image.
        """
        # cv2.warpPerspective should return the same dtype as the input image
        return cast(
            NDArray[np.uint8],
            cv2.warpPerspective(
                image, self.matrix, (self.dst_width_px, self.dst_height_px)
            ),
        )
