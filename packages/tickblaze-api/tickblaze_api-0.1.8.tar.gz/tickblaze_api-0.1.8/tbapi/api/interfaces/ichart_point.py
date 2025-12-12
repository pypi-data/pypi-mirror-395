




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IChartPoint as _IChartPoint
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.ipoint import IPoint

@tb_interface(_IChartPoint)
class IChartPoint(IPoint):
    """Represents a point on a chart with a specific index, time, and value.      Used to store data points on the chart, where each point has a unique index and associated time and value."""

    @property
    def index(self) -> int:
        """The index of the chart point, which serves as the position identifier of the point in the chart's data series."""
        val = self._value.Index
        return val
    @property
    def time(self) -> Any:
        """The time associated with the chart point. It represents the time at which the data point occurred."""
        val = self._value.Time
        return val
    @time.setter
    def time(self, val: Any):
        tmp = self._value
        tmp.Time = val
        self._value = tmp
    @property
    def value(self) -> Any:
        """The value associated with the chart point, representing the data value at the given time."""
        val = self._value.Value
        return val
    @value.setter
    def value(self, val: Any):
        tmp = self._value
        tmp.Value = val
        self._value = tmp


