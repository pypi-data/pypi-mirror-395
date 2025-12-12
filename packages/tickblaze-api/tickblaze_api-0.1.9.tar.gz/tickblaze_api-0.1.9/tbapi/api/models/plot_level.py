






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import PlotLevel as _PlotLevel
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.iplot import IPlot
from tbapi.core.enums.line_style import LineStyle
from Tickblaze.Core.Enums import LineStyle as _LineStyle
if TYPE_CHECKING:
    from tbapi.api.models.stroke import Stroke
    from tbapi.api.models.color import Color

@tb_class(_PlotLevel)
class PlotLevel(IPlot):
    """Represents a level on a plot with configurable value, color, line style, thickness, and visibility."""

    @overload
    @staticmethod
    def new(value: float, color: Color, lineStyle: LineStyle = LineStyle.Dash, thickness: int = 1) -> "PlotLevel":
        """Constructor overload with arguments: value, color, lineStyle, thickness"""
        ...
    @overload
    @staticmethod
    def new(name: str, value: float, color: Color, lineStyle: LineStyle = LineStyle.Dash, thickness: int = 1, isVisible: bool = True) -> "PlotLevel":
        """Constructor overload with arguments: name, value, color, lineStyle, thickness, isVisible"""
        ...
    @overload
    @staticmethod
    def new(name: str, value: float, stroke: Stroke) -> "PlotLevel":
        """Constructor overload with arguments: name, value, stroke"""
        ...
    @overload
    @staticmethod
    def new(value: float, color: str, lineStyle: LineStyle = LineStyle.Dash, thickness: int = 1) -> "PlotLevel":
        """Constructor overload with arguments: value, color, lineStyle, thickness"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for PlotLevel. Use overloads for IDE type hints."""
        return PlotLevel(*args, **kwargs)

    @property
    def name(self) -> str:
        """The name of the plot level."""
        val = self._value.Name
        return val
    @name.setter
    def name(self, val: str):
        tmp = self._value
        tmp.Name = val
        self._value = tmp
    @property
    def value(self) -> float:
        """The value of the plot level."""
        val = self._value.Value
        return val
    @value.setter
    def value(self, val: float):
        tmp = self._value
        tmp.Value = val
        self._value = tmp
    @property
    def stroke(self) -> Stroke:
        from tbapi.api.models.stroke import Stroke
        val = self._value.Stroke
        return Stroke(_existing=val)
    @stroke.setter
    def stroke(self, val: Stroke):
        tmp = self._value
        tmp.Stroke = val._value
        self._value = tmp
    @property
    def color(self) -> Color:
        """The color of the plot level."""
        from tbapi.api.models.color import Color
        val = self._value.Color
        return Color(_existing=val)
    @color.setter
    def color(self, val: Color):
        tmp = self._value
        tmp.Color = val._value
        self._value = tmp
    @property
    def line_style(self) -> LineStyle:
        """The line style for the plot level."""
        val = int(self._value.LineStyle)
        return LineStyle(val)
    @line_style.setter
    def line_style(self, val: LineStyle):
        tmp = self._value
        tmp.LineStyle = _LineStyle(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def thickness(self) -> int:
        """The thickness of the plot level line."""
        val = self._value.Thickness
        return val
    @thickness.setter
    def thickness(self, val: int):
        tmp = self._value
        tmp.Thickness = val
        self._value = tmp
    @property
    def is_visible(self) -> bool:
        """Indicates whether the plot level is visible."""
        val = self._value.IsVisible
        return val
    @is_visible.setter
    def is_visible(self, val: bool):
        tmp = self._value
        tmp.IsVisible = val
        self._value = tmp

    def clone(self) -> PlotLevel:
        """Creates a copy of the current  instance.            A new instance of  with the same values."""
        result = self._value.Clone()
        from tbapi.api.models.plot_level import PlotLevel
        return PlotLevel(_existing=result)
  


