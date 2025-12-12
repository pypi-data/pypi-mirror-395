"""
This module defines various analysis strategies that implement the
IAnalysisStrategy interface. Each strategy encapsulates a specific
topographic calculation method.
"""

from typing import Any, List, Tuple, Union, cast

import numpy as np
from numpy.typing import NDArray

from topovision.core.interfaces import IAnalysisStrategy
from topovision.core.models import ArcLengthResult, GradientResult, VolumeResult
from topovision.utils.math import calculate_arc_length
from topovision.utils.units import UnitConverter


class GradientStrategy(IAnalysisStrategy):
    """
    Calculates the gradient (rate of change) of the input data.
    """

    def analyze(self, data: NDArray[np.uint8], **kwargs: Any) -> GradientResult:
        """
        Computes the gradient (dz/dx, dz/dy) of the 2D data.
        """
        if data.ndim != 2:
            raise ValueError("GradientStrategy expects 2D data.")

        pixels_per_meter = kwargs.get("pixels_per_meter", 1.0)
        z_factor = kwargs.get("z_factor", 1.0)

        # The distance between pixels in meters
        dx = 1.0 / pixels_per_meter
        dy = 1.0 / pixels_per_meter

        # Scale the height data
        scaled_data = data.astype(np.float32) * z_factor

        # np.gradient computes the gradient using the provided spacing
        dz_dy, dz_dx = np.gradient(scaled_data, dy, dx)
        magnitude = np.sqrt(dz_dx**2 + dz_dy**2)

        return GradientResult(dz_dx=dz_dx, dz_dy=dz_dy, magnitude=magnitude)


class VolumeStrategy(IAnalysisStrategy):
    """
    Calculates the approximate volume under the surface defined by the input data.
    """

    def analyze(self, data: NDArray[np.uint8], **kwargs: Any) -> VolumeResult:
        """
        Computes the volume under the 2D data surface.
        """
        if data.ndim != 2:
            raise ValueError("VolumeStrategy expects 2D data.")

        z_factor = kwargs.get("z_factor", 1.0)
        pixels_per_meter = kwargs.get("pixels_per_meter", 1.0)
        unit = kwargs.get("unit", "cubic_meters")

        # The area of a single pixel in square meters
        pixel_area_sq_meters = (1.0 / pixels_per_meter) ** 2

        # Total volume is the sum of the heights of all pixels,
        # each multiplied by the area of one pixel and the z-factor.
        volume_in_cubic_meters = (
            np.sum(data.astype(np.float64)) * z_factor * pixel_area_sq_meters
        )

        # Convert to the desired output unit
        converter = UnitConverter(pixels_per_meter)
        converted_volume = converter.convert_volume(
            volume_in_cubic_meters, "cubic_meters", unit
        )

        return VolumeResult(volume=converted_volume, units=unit)


class ArcLengthStrategy(IAnalysisStrategy):
    """
    Calculates the arc length of a path defined by a series of 2D points.
    """

    def analyze(self, data: NDArray[np.uint8], **kwargs: Any) -> ArcLengthResult:
        """
        Computes the arc length of the given path.
        """
        pixels_per_meter = kwargs.get("pixels_per_meter", 1.0)
        z_factor = kwargs.get("z_factor", 1.0)
        unit = kwargs.get("unit", "meters")

        # Cast data to the expected type for path points, assuming it's provided correctly at runtime
        path_data = cast(Union[NDArray[np.float64], List[Tuple[float, float]]], data)

        # Define the scale for each axis
        scale_x = 1.0 / pixels_per_meter  # meters per pixel
        scale_z = z_factor / 255.0  # Assuming 8-bit data, normalized height

        # The y-values in `data` represent height, so we use scale_z
        length_in_meters = calculate_arc_length(
            path_data, scale_x=scale_x, scale_y=scale_z
        )

        # Convert to the desired output unit
        converter = UnitConverter(pixels_per_meter)
        converted_length = converter.convert_distance(length_in_meters, "meters", unit)

        # Ensure path_points_array is NDArray[np.float64] for calculation, then convert to np.int32 for ArcLengthResult
        path_points_array: NDArray[np.float64]
        if isinstance(path_data, list):
            path_points_array = np.asarray(path_data, dtype=np.float64)
        else:
            path_points_array = path_data

        return ArcLengthResult(
            length=converted_length,
            units=unit,
            path_points=path_points_array.astype(np.int32),  # Convert to np.int32
        )
