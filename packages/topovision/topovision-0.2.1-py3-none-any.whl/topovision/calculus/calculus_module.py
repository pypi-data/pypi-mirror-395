"""
Analysis Context for TopoVision.

This module defines the AnalysisContext class, which acts as a context
for executing different topographic analysis strategies.
"""

from typing import Any, Dict, Optional, Union

import numpy as np
from numpy.typing import NDArray

from topovision.core.interfaces import IAnalysisStrategy
from topovision.core.models import (
    AnalysisResult,
    ArcLengthResult,
    GradientResult,
    VolumeResult,
)

from .strategies import ArcLengthStrategy, GradientStrategy, VolumeStrategy


class AnalysisContext:
    """
    A context for performing various topographic calculations
    using different strategies.

    This class allows for dynamic switching of analysis algorithms (strategies)
    at runtime, adhering to the Strategy design pattern.
    """

    def __init__(self) -> None:
        """
        Initializes the AnalysisContext with available strategies.
        """
        self._strategies: Dict[str, IAnalysisStrategy] = {
            "gradient": GradientStrategy(),
            "volume": VolumeStrategy(),
            "arc_length": ArcLengthStrategy(),
        }
        self._current_strategy_name: Optional[str] = None

    @property
    def strategy(self) -> Optional[IAnalysisStrategy]:
        """Returns the currently active analysis strategy."""
        if self._current_strategy_name in self._strategies:
            return self._strategies[self._current_strategy_name]
        return None

    def set_strategy(self, strategy_name: str) -> None:
        """
        Sets the calculation strategy to be used.

        Args:
            strategy_name (str): The name of the strategy to set
                                 (e.g., "gradient", "volume").

        Raises:
            ValueError: If the specified strategy name is not found.
        """
        valid_strategies = list(self._strategies.keys())
        if strategy_name not in valid_strategies:
            raise ValueError(
                f"Strategy '{strategy_name}' not found. "
                f"Available strategies: {valid_strategies}"
            )
        self._current_strategy_name = strategy_name

    def calculate(
        self,
        data: NDArray[Any],
        **kwargs: Any,  # Changed from NDArray[Any, Any] to NDArray[Any]
    ) -> Union[GradientResult, VolumeResult, ArcLengthResult]:
        """
        Performs a calculation on the given data using the current strategy.

        Args:
            data (NDArray[Any]): The input data for the calculation.
            **kwargs: Additional parameters for the calculation,
                      passed directly to the strategy.

        Returns:
            Union[GradientResult, VolumeResult, ArcLengthResult]: The result of
            the calculation, typed according to the specific strategy used.

        Raises:
            RuntimeError: If no strategy has been set before calling calculate.
        """
        if self._current_strategy_name is None:
            raise RuntimeError(
                "No analysis strategy has been set. Call set_strategy() first."
            )

        # Existing strategies
        if self._current_strategy_name not in self._strategies:
            raise ValueError(f"Strategy '{self._current_strategy_name}' not found.")
        return self._strategies[self._current_strategy_name].analyze(data, **kwargs)
