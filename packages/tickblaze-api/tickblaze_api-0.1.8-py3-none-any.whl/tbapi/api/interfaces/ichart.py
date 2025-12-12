




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IChart as _IChart
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.isize import ISize
if TYPE_CHECKING:
    from tbapi.api.models.color import Color

@tb_interface(_IChart)
class IChart(ISize):
    """Represents a chart that displays financial data."""

    @property
    def bar_width(self) -> float:
        """The width of the bar as a value between 0.0 and 1.0 which defines the fraction of available space each bar should occupy."""
        val = self._value.BarWidth
        return val
    @bar_width.setter
    def bar_width(self, val: float):
        tmp = self._value
        tmp.BarWidth = val
        self._value = tmp
    @property
    def datapoint_width(self) -> float:
        """Gets the data-point width, which is the width of one data-point in pixels on the axis."""
        val = self._value.DatapointWidth
        return val
    @property
    def background_color(self) -> Color:
        """Gets the panel background color."""
        from tbapi.api.models.color import Color
        val = self._value.BackgroundColor
        return Color(_existing=val)
    @property
    def text_color(self) -> Color:
        """Gets the panel text color."""
        from tbapi.api.models.color import Color
        val = self._value.TextColor
        return Color(_existing=val)
    @property
    def first_visible_bar_index(self) -> int:
        """The index of the first visible bar on the chart."""
        val = self._value.FirstVisibleBarIndex
        return val
    @property
    def last_visible_bar_index(self) -> int:
        """The index of the last visible bar on the chart."""
        val = self._value.LastVisibleBarIndex
        return val

    @abstractmethod
    def format_time(self, time: datetime) -> str:
        """Formats the given datetime into a string representation.            The datetime value to format.      A string representing the formatted datetime."""
        result = self._value.FormatTime(to_net_datetime(time))
        return result
  
    @abstractmethod
    def get_xcoordinate_by_bar_index(self, bar_index: int) -> float:
        """Gets the X coordinate by the given bar index.            The index of the bar.      The X coordinate corresponding to the specified bar index."""
        result = self._value.GetXCoordinateByBarIndex(bar_index)
        return result
  
    @abstractmethod
    def get_xcoordinate_by_time(self, time: datetime) -> float:
        """Gets the X coordinate by the specified time.            The time to get the X coordinate for.      The X coordinate corresponding to the specified time."""
        result = self._value.GetXCoordinateByTime(to_net_datetime(time))
        return result
  
    @abstractmethod
    def get_time_by_xcoordinate(self, x: float) -> datetime:
        """Gets the time value by the specified X coordinate.            The X coordinate to get the time value for.      The time value corresponding to the specified X coordinate."""
        result = self._value.GetTimeByXCoordinate(x)
        return to_python_datetime(result)
  
    @abstractmethod
    def get_bar_index_by_xcoordinate(self, x: float) -> int:
        """Gets the bar index by the specified X coordinate.            The X coordinate to get the bar index for.      The bar index corresponding to the specified X coordinate."""
        result = self._value.GetBarIndexByXCoordinate(x)
        return result
  
    @abstractmethod
    def get_bar_index_by_time(self, time: datetime) -> int:
        """Gets the bar index by the specified time.            The time to get the bar index for.      The bar index corresponding to the specified time."""
        result = self._value.GetBarIndexByTime(to_net_datetime(time))
        return result
  

