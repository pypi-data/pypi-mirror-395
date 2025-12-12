




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IChartScale as _IChartScale
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_interface(_IChartScale)
class IChartScale():
    """Represents the scale for the price axis in a chart, including the maximum and minimum price.      It provides methods to format prices and convert between price values and their corresponding Y coordinates."""

    @property
    def max_price(self) -> float:
        """The maximum price value on the scale."""
        val = self._value.MaxPrice
        return val
    @property
    def min_price(self) -> float:
        """The minimum price value on the scale."""
        val = self._value.MinPrice
        return val

    @abstractmethod
    def format_price(self, value: float) -> str:
        """Formats the given price value into a string representation.            The price value to format.      A string representing the formatted price."""
        result = self._value.FormatPrice(value)
        return result
  
    @abstractmethod
    def get_ycoordinate_by_value(self, value: float) -> float:
        """Gets the Y coordinate in pixels for the specified axis value.            The axis value to convert.      The Y coordinate in pixels corresponding to the specified axis value."""
        result = self._value.GetYCoordinateByValue(value)
        return result
  
    @abstractmethod
    def get_value_by_ycoordinate(self, y: float) -> float:
        """Gets the axis value for the specified Y coordinate in pixels.            The Y coordinate in pixels to convert.      The axis value corresponding to the specified Y coordinate in pixels."""
        result = self._value.GetValueByYCoordinate(y)
        return result
  

