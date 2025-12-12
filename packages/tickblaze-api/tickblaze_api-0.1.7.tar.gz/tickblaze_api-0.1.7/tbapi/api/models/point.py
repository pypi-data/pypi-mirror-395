






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Point as _Point
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.ipoint import IPoint

@tb_class(_Point)
class Point(IPoint):
    """Represents a point in a 2D space with X and Y coordinates."""

    @overload
    @staticmethod
    def new() -> "Point":
        """Constructor overload with arguments: """
        ...
    @overload
    @staticmethod
    def new(point: IPoint) -> "Point":
        """Constructor overload with arguments: point"""
        ...
    @overload
    @staticmethod
    def new(x: float, y: float) -> "Point":
        """Constructor overload with arguments: x, y"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Point. Use overloads for IDE type hints."""
        return Point(*args, **kwargs)

    @property
    def x(self) -> float:
        val = self._value.X
        return val
    @x.setter
    def x(self, val: float):
        tmp = self._value
        tmp.X = val
        self._value = tmp
    @property
    def y(self) -> float:
        val = self._value.Y
        return val
    @y.setter
    def y(self, val: float):
        tmp = self._value
        tmp.Y = val
        self._value = tmp
    @property
    def magnitude(self) -> float:
        """The magnitude of the point as a vector"""
        val = self._value.Magnitude
        return val
    @property
    def angle(self) -> float:
        """The angle of the point as a vector"""
        val = self._value.Angle
        return val

    def normalize(self) -> Point:
        """Adjusts the point so that the vector it represents has a magnitude of 1"""
        result = self._value.Normalize()
        from tbapi.api.models.point import Point
        return Point(_existing=result)
  


