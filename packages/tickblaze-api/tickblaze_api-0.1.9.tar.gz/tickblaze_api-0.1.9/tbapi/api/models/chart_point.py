






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import ChartPoint as _ChartPoint
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.models.point import Point
from tbapi.api.interfaces.ichart_point import IChartPoint

@tb_class(_ChartPoint)
class ChartPoint(Point, IChartPoint):

    @overload
    @staticmethod
    def new() -> "ChartPoint":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for ChartPoint. Use overloads for IDE type hints."""
        return ChartPoint(*args, **kwargs)

    @property
    def index(self) -> int:
        val = self._value.Index
        return val
    @property
    def time(self) -> Any:
        val = self._value.Time
        return val
    @time.setter
    def time(self, val: Any):
        tmp = self._value
        tmp.Time = val
        self._value = tmp
    @property
    def value(self) -> Any:
        val = self._value.Value
        return val
    @value.setter
    def value(self, val: Any):
        tmp = self._value
        tmp.Value = val
        self._value = tmp



