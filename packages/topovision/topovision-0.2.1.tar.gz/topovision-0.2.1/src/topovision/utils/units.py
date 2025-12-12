"""
A module for handling unit conversions in TopoVision.

This module provides a `UnitConverter` class that facilitates the conversion
of measurements between different units, such as pixels, meters, and feet.
The converter is designed to be extensible, allowing for the addition of
new units and conversion factors.
"""

from typing import Dict, Union


class UnitConverter:
    """
    A class for converting values between different units of measurement.
    """

    def __init__(self, pixels_per_meter: Union[int, float]):
        """
        Initializes the UnitConverter with an initial scale factor.

        Args:
            pixels_per_meter (Union[int, float]): The number of pixels that
                                                  represent one meter.
        """
        self.to_meters: Dict[str, float] = {}
        self.update_scale(pixels_per_meter)

    def update_scale(self, pixels_per_meter: Union[int, float]) -> None:
        """
        Updates the pixels-per-meter scale and recalculates conversion factors.

        Args:
            pixels_per_meter (Union[int, float]): The new number of pixels
                                                  representing one meter.
        """
        if not isinstance(pixels_per_meter, (int, float)) or pixels_per_meter <= 0:
            raise ValueError("pixels_per_meter must be a positive number.")

        self.pixels_per_meter = float(pixels_per_meter)

        # Conversion factors to meters
        self.to_meters = {
            "pixels": 1.0 / self.pixels_per_meter,
            "meters": 1.0,
            "kilometers": 1000.0,
            "centimeters": 0.01,
            "miles": 1609.34,
            "feet": 0.3048,
        }

    def convert_distance(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Converts a distance value from one unit to another.

        Args:
            value (float): The distance value to convert.
            from_unit (str): The starting unit (e.g., "pixels", "meters").
            to_unit (str): The target unit (e.g., "kilometers", "feet").

        Returns:
            float: The converted distance value.
        """
        if from_unit not in self.to_meters or to_unit not in self.to_meters:
            raise ValueError("Invalid unit specified for distance conversion.")

        # Convert the value to meters first
        value_in_meters = value * self.to_meters[from_unit]

        # Then convert from meters to the target unit
        return value_in_meters / self.to_meters[to_unit]

    def convert_volume(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Converts a volume value from one unit to another.

        Args:
            value (float): The volume value to convert.
            from_unit (str): The starting unit (e.g., "cubic_pixels", "cubic_meters").
            to_unit (str): The target unit (e.g., "cubic_kilometers", "cubic_feet").

        Returns:
            float: The converted volume value.
        """
        from_unit_base = from_unit.replace("cubic_", "")
        to_unit_base = to_unit.replace("cubic_", "")

        if from_unit_base not in self.to_meters or to_unit_base not in self.to_meters:
            raise ValueError("Invalid unit specified for volume conversion.")

        # Get the linear conversion factor
        linear_factor = self.to_meters[from_unit_base]

        # For volume, the conversion factor is cubed
        value_in_cubic_meters = value * (linear_factor**3)

        # Convert from cubic meters to the target unit
        return value_in_cubic_meters / (self.to_meters[to_unit_base] ** 3)
