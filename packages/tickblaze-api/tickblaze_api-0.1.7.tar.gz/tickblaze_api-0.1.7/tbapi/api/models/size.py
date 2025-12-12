





from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Size as _Size
from typing import Any, overload
from tbapi.api.interfaces.isize import ISize

@tb_class(_Size)
class Size():
    """Represents the size of an object with width and height."""

    @overload
    @staticmethod
    def new() -> "Size":
        """Constructor overload with arguments: """
        ...
    @overload
    @staticmethod
    def new(width: float, height: float) -> "Size":
        """Constructor overload with arguments: width, height"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Size. Use overloads for IDE type hints."""
        return Size(*args, **kwargs)

    @property
    def height(self) -> float:
        """The height of the size."""
        val = self._value.Height
        return val
    @height.setter
    def height(self, val: float):
        tmp = self._value
        tmp.Height = val
        self._value = tmp
    @property
    def width(self) -> float:
        """The width of the size."""
        val = self._value.Width
        return val
    @width.setter
    def width(self, val: float):
        tmp = self._value
        tmp.Width = val
        self._value = tmp


