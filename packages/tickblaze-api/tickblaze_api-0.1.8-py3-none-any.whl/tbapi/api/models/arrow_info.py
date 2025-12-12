





from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import ArrowInfo as _ArrowInfo
from typing import Any, overload
if TYPE_CHECKING:
    from tbapi.api.models.point import Point
    from tbapi.api.interfaces.ipoint import IPoint

@tb_class(_ArrowInfo)
class ArrowInfo():
    """Struct used to define an arrow"""

    @overload
    @staticmethod
    def new(start: IPoint, end: IPoint, width: float) -> "ArrowInfo":
        """Constructor overload with arguments: start, end, width"""
        ...
    @overload
    @staticmethod
    def new(length: float, angle: float, end: IPoint, width: float) -> "ArrowInfo":
        """Constructor overload with arguments: length, angle, end, width"""
        ...
    @overload
    @staticmethod
    def new() -> "ArrowInfo":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for ArrowInfo. Use overloads for IDE type hints."""
        return ArrowInfo(*args, **kwargs)

    @property
    def width(self) -> float:
        """The width of the arrow in pixels"""
        val = self._value.Width
        return val
    @property
    def length(self) -> float:
        """The length in pixels"""
        val = self._value.Length
        return val
    @property
    def angle(self) -> float:
        """The angle in radians"""
        val = self._value.Angle
        return val
    @property
    def head_length_ratio(self) -> float:
        """The fraction of the overall arrow length that the arrow head takes up"""
        val = self._value.HeadLengthRatio
        return val
    @head_length_ratio.setter
    def head_length_ratio(self, val: float):
        tmp = self._value
        tmp.HeadLengthRatio = val
        self._value = tmp
    @property
    def tail_width_ratio(self) -> float:
        """The ratio of the arrow head width taken up by the tail"""
        val = self._value.TailWidthRatio
        return val
    @tail_width_ratio.setter
    def tail_width_ratio(self, val: float):
        tmp = self._value
        tmp.TailWidthRatio = val
        self._value = tmp
    @property
    def start(self) -> Point:
        """The start point of the arrow"""
        from tbapi.api.models.point import Point
        val = self._value.Start
        return Point(_existing=val)
    @property
    def end(self) -> Point:
        """The end point of the arrow"""
        from tbapi.api.models.point import Point
        val = self._value.End
        return Point(_existing=val)
    @property
    def drawing_points(self) -> list[Point]:
        """The points that make up the arrow polygon"""
        val = self._value.DrawingPoints
        return val


