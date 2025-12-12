






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api import PlotSeries as _PlotSeries
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.models.data_series import DataSeries
from tbapi.api.interfaces.iplot import IPlot
from tbapi.core.enums.plot_style import PlotStyle
from tbapi.core.enums.line_style import LineStyle
from Tickblaze.Core.Enums import PlotStyle as _PlotStyle
from Tickblaze.Core.Enums import LineStyle as _LineStyle
if TYPE_CHECKING:
    from tbapi.api.models.color import Color
    from tbapi.api.models.stroke import Stroke
    from tbapi.api.color_series import ColorSeries
    from tbapi.api.series import Series
    from tbapi.api.models.price_marker import PriceMarker

@tb_class(_PlotSeries)
class PlotSeries(DataSeries, IPlot):
    """Represents a series of plot data, including properties for color, line style, thickness, and visibility."""

    @overload
    @staticmethod
    def new() -> "PlotSeries":
        """Constructor overload with arguments: """
        ...
    @overload
    @staticmethod
    def new(color: Color) -> "PlotSeries":
        """Constructor overload with arguments: color"""
        ...
    @overload
    @staticmethod
    def new(color: Color, lineStyle: LineStyle = LineStyle.Solid, thickness: int = 1) -> "PlotSeries":
        """Constructor overload with arguments: color, lineStyle, thickness"""
        ...
    @overload
    @staticmethod
    def new(stroke: Stroke, plotStyle: PlotStyle = PlotStyle.Line) -> "PlotSeries":
        """Constructor overload with arguments: stroke, plotStyle"""
        ...
    @overload
    @staticmethod
    def new(color: Color, plotStyle: PlotStyle = PlotStyle.Line, thickness: int = 1) -> "PlotSeries":
        """Constructor overload with arguments: color, plotStyle, thickness"""
        ...
    @overload
    @staticmethod
    def new(name: str, color: Color, plotStyle: PlotStyle = PlotStyle.Line, lineStyle: LineStyle = LineStyle.Solid, thickness: int = 1, isVisible: bool = True) -> "PlotSeries":
        """Constructor overload with arguments: name, color, plotStyle, lineStyle, thickness, isVisible"""
        ...
    @overload
    @staticmethod
    def new(name: str, stroke: Stroke, plotStyle: PlotStyle = PlotStyle.Line) -> "PlotSeries":
        """Constructor overload with arguments: name, stroke, plotStyle"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for PlotSeries. Use overloads for IDE type hints."""
        return PlotSeries(*args, **kwargs)

    @property
    def name(self) -> str:
        """The name of the plot series."""
        val = self._value.Name
        return val
    @name.setter
    def name(self, val: str):
        tmp = self._value
        tmp.Name = val
        self._value = tmp
    @property
    def color(self) -> Color:
        """The color of the plot series."""
        from tbapi.api.models.color import Color
        val = self._value.Color
        return Color(_existing=val)
    @color.setter
    def color(self, val: Color):
        tmp = self._value
        tmp.Color = val._value
        self._value = tmp
    @property
    def plot_style(self) -> PlotStyle:
        """The style of the plot (line, bars, etc.)."""
        val = int(self._value.PlotStyle)
        return PlotStyle(val)
    @plot_style.setter
    def plot_style(self, val: PlotStyle):
        tmp = self._value
        tmp.PlotStyle = _PlotStyle(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def line_style(self) -> LineStyle:
        """The line style for the plot series."""
        val = int(self._value.LineStyle)
        return LineStyle(val)
    @line_style.setter
    def line_style(self, val: LineStyle):
        tmp = self._value
        tmp.LineStyle = _LineStyle(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def thickness(self) -> int:
        """The thickness of the plot series line."""
        val = self._value.Thickness
        return val
    @thickness.setter
    def thickness(self, val: int):
        tmp = self._value
        tmp.Thickness = val
        self._value = tmp
    @property
    def stroke(self) -> Stroke:
        """The stroke for the plot series"""
        from tbapi.api.models.stroke import Stroke
        val = self._value.Stroke
        return Stroke(_existing=val)
    @stroke.setter
    def stroke(self, val: Stroke):
        tmp = self._value
        tmp.Stroke = val._value
        self._value = tmp
    @property
    def is_visible(self) -> bool:
        """Indicates whether the plot series is visible."""
        val = self._value.IsVisible
        return val
    @is_visible.setter
    def is_visible(self, val: bool):
        tmp = self._value
        tmp.IsVisible = val
        self._value = tmp
    @property
    def colors(self) -> ColorSeries:
        """The collection of plot colors."""
        from tbapi.api.color_series import ColorSeries
        val = self._value.Colors
        return ColorSeries(_existing=val)
    @property
    def is_line_break(self) -> Series:
        """A series representing line break points in the plot series."""
        val = self._value.IsLineBreak
        return val
    @property
    def price_marker(self) -> PriceMarker:
        """The price marker of the plot series."""
        from tbapi.api.models.price_marker import PriceMarker
        val = self._value.PriceMarker
        return PriceMarker(_existing=val)
    @price_marker.setter
    def price_marker(self, val: PriceMarker):
        tmp = self._value
        tmp.PriceMarker = val._value
        self._value = tmp
    @property
    def is_editor_browsable(self) -> bool:
        """Indicates whether the plot series should be visible in the indicator editor."""
        val = self._value.IsEditorBrowsable
        return val
    @is_editor_browsable.setter
    def is_editor_browsable(self, val: bool):
        tmp = self._value
        tmp.IsEditorBrowsable = val
        self._value = tmp
    @property
    def is_color_editor_browsable(self) -> bool:
        """Indicates whether the color of the plot series should be visible in the indicator editor."""
        val = self._value.IsColorEditorBrowsable
        return val
    @is_color_editor_browsable.setter
    def is_color_editor_browsable(self, val: bool):
        tmp = self._value
        tmp.IsColorEditorBrowsable = val
        self._value = tmp

    def clone(self) -> PlotSeries:
        """Creates a copy of the current  instance.            A new instance of  with the same values."""
        result = self._value.Clone()
        from tbapi.api.plot_series import PlotSeries
        return PlotSeries(_existing=result)
  


    def __getitem__(self, index: int) -> float:
        result = self._value[index]
        return result

    def __setitem__(self, index: int, value: float):
        tmp = value
        self._value[index] = tmp
