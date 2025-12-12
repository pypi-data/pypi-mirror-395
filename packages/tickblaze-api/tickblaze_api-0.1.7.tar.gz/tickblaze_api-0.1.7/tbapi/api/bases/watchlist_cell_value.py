






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import WatchlistCellValue as _WatchlistCellValue
from typing import Any, overload
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from tbapi.api.models.color import Color

@tb_class(_WatchlistCellValue)
class WatchlistCellValue():
    """Represents a cell in the watchlist with value and associated colors."""

    @overload
    @staticmethod
    def new() -> "WatchlistCellValue":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for WatchlistCellValue. Use overloads for IDE type hints."""
        return WatchlistCellValue(*args, **kwargs)

    @property
    def value(self) -> float:
        """The value of the watchlist cell."""
        val = self._value.Value
        return val
    @value.setter
    def value(self, val: float):
        tmp = self._value
        tmp.Value = val
        self._value = tmp
    @property
    def display_value(self) -> str:
        """The string value of the watchlist cell."""
        val = self._value.DisplayValue
        return val
    @display_value.setter
    def display_value(self, val: str):
        tmp = self._value
        tmp.DisplayValue = val
        self._value = tmp
    @property
    def background(self) -> Color:
        """The background color of the watchlist cell."""
        from tbapi.api.models.color import Color
        val = self._value.Background
        return Color(_existing=val)
    @background.setter
    def background(self, val: Color):
        tmp = self._value
        tmp.Background = val._value
        self._value = tmp
    @property
    def foreground(self) -> Color:
        """The foreground color of the watchlist cell."""
        from tbapi.api.models.color import Color
        val = self._value.Foreground
        return Color(_existing=val)
    @foreground.setter
    def foreground(self, val: Color):
        tmp = self._value
        tmp.Foreground = val._value
        self._value = tmp



