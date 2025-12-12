






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api import ColorSeries as _ColorSeries
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.series import Series
from tbapi.api.models.color import Color
if TYPE_CHECKING:
    from tbapi.api.plot_series import PlotSeries

@tb_class(_ColorSeries)
class ColorSeries(Series):
    """A class representing a collection of plot colors for the ."""

    @overload
    @staticmethod
    def new(plotSeries: PlotSeries) -> "ColorSeries":
        """Constructor overload with arguments: plotSeries"""
        ...
    @overload
    @staticmethod
    def new(defaultColor: Color | None = None) -> "ColorSeries":
        """Constructor overload with arguments: defaultColor"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for ColorSeries. Use overloads for IDE type hints."""
        return ColorSeries(*args, **kwargs)




    def __getitem__(self, index: int) -> Color:
        result = self._value[index]
        return Color(_existing=result)

    def __setitem__(self, index: int, value: Color):
        tmp = value
        tmp = value._value
        self._value[index] = tmp
