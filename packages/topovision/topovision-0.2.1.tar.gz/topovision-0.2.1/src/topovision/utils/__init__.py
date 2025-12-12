"""
The `utils` package provides utility functions and classes that are used
across the TopoVision application. These utilities are designed to be
reusable and to encapsulate common logic that is not specific to any
one part of the application.

Modules:
- `math`: Provides mathematical functions for calculations such as arc length.
- `units`: Provides a `UnitConverter` class for converting between different
           units of measurement.
- `perspective`: Provides a `PerspectiveCorrector` for handling perspective distortion.
"""

from . import math, perspective, units

__all__ = ["math", "units", "perspective"]
