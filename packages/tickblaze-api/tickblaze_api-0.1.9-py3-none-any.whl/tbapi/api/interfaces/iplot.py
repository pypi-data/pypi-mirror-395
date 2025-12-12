




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IPlot as _IPlot
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.core.enums.line_style import LineStyle
from Tickblaze.Core.Enums import LineStyle as _LineStyle
if TYPE_CHECKING:
    from tbapi.api.models.color import Color

@tb_interface(_IPlot)
class IPlot():
    """Defines properties for a plot including visual appearance."""

    @property
    def name(self) -> str:
        """The name of the plot."""
        val = self._value.Name
        return val
    @property
    def color(self) -> Color:
        """The color of the plot."""
        from tbapi.api.models.color import Color
        val = self._value.Color
        return Color(_existing=val)
    @property
    def line_style(self) -> LineStyle:
        """The line style of the plot."""
        val = int(self._value.LineStyle)
        return LineStyle(val)
    @property
    def thickness(self) -> int:
        """The thickness of the plot's line."""
        val = self._value.Thickness
        return val
    @property
    def is_visible(self) -> bool:
        """Indicates whether the plot is visible."""
        val = self._value.IsVisible
        return val


