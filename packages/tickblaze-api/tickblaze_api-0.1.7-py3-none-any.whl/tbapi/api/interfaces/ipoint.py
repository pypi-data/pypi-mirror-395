




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IPoint as _IPoint
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_interface(_IPoint)
class IPoint():
    """Defines properties for a point with X and Y coordinates."""

    @property
    def x(self) -> float:
        """The X coordinate of the point."""
        val = self._value.X
        return val
    @x.setter
    def x(self, val: float):
        tmp = self._value
        tmp.X = val
        self._value = tmp
    @property
    def y(self) -> float:
        """The Y coordinate of the point."""
        val = self._value.Y
        return val
    @y.setter
    def y(self, val: float):
        tmp = self._value
        tmp.Y = val
        self._value = tmp


