




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IChartPoints as _IChartPoints
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.ichart_point import IChartPoint

@tb_interface(_IChartPoints)
class IChartPoints():
    """Represents a collection of chart points that can be accessed and manipulated.      Each chart point consists of X (time) and Y (value) data values."""


    @abstractmethod
    def add(self, x_data_value: Any, y_data_value: Any) -> None:
        """Adds a new chart point to the collection with specified X and Y data values.            The X coordinate (time) of the chart point.      The Y coordinate (value) of the chart point."""
        result = self._value.Add(x_data_value, y_data_value)
        return result
  

    def __getitem__(self, index: int) -> Any:
        result = self._value[index]
        return IChartPoint(_existing=result)
