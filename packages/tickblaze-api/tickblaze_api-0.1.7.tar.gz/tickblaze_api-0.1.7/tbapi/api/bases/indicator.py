






from __future__ import annotations
from typing import TYPE_CHECKING
import clr
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import Indicator as _Indicator
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.symbol_script import SymbolScript
from tbapi.api.bases.iindicator import IIndicator
from tbapi.api.interfaces.ichart_object import IChartObject
from tbapi.api.enums.ztype import ZType
from Tickblaze.Scripts.Api.Enums import ZType as _ZType
from tbapi.api.interfaces.idrawing_context import IDrawingContext
if TYPE_CHECKING:
    from tbapi.api.interfaces.ichart import IChart
    from tbapi.api.interfaces.ichart_scale import IChartScale
    from tbapi.api.interfaces.isymbol import ISymbol
    from tbapi.api.series import Series
    from tbapi.api.plot_series import PlotSeries
    from tbapi.api.bases.watchlist_cell_value import WatchlistCellValue

@tb_interface(_Indicator)
class Indicator(SymbolScript, IIndicator, IChartObject):
    """Represents a base class for indicator scripts. Provides functionality for calculating and rendering the indicator on the chart."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Indicator. Use overloads for IDE type hints."""
        return Indicator(*args, **kwargs)

    @property
    def display_name(self) -> str:
        """Gets the display name of the indicator."""
        val = self._value.DisplayName
        return val
    @property
    def is_overlay(self) -> bool:
        val = self._value.IsOverlay
        return val
    @is_overlay.setter
    def is_overlay(self, val: bool):
        tmp = self._value
        tmp.IsOverlay = val
        self._value = tmp
    @property
    def is_percentage(self) -> bool:
        val = self._value.IsPercentage
        return val
    @is_percentage.setter
    def is_percentage(self, val: bool):
        tmp = self._value
        tmp.IsPercentage = val
        self._value = tmp
    @property
    def auto_rescale(self) -> bool:
        val = self._value.AutoRescale
        return val
    @auto_rescale.setter
    def auto_rescale(self, val: bool):
        tmp = self._value
        tmp.AutoRescale = val
        self._value = tmp
    @property
    def apply_background_color_to_all_panels(self) -> bool:
        val = self._value.ApplyBackgroundColorToAllPanels
        return val
    @apply_background_color_to_all_panels.setter
    def apply_background_color_to_all_panels(self, val: bool):
        tmp = self._value
        tmp.ApplyBackgroundColorToAllPanels = val
        self._value = tmp
    @property
    def scale_precision(self) -> int | None:
        val = self._value.ScalePrecision
        return val
    @scale_precision.setter
    def scale_precision(self, val: int | None):
        tmp = self._value
        tmp.ScalePrecision = val
        self._value = tmp
    @property
    def show_on_chart(self) -> bool:
        val = self._value.ShowOnChart
        return val
    @show_on_chart.setter
    def show_on_chart(self, val: bool):
        tmp = self._value
        tmp.ShowOnChart = val
        self._value = tmp
    @property
    def yaxis_top_margin_min(self) -> float | None:
        """Gets or sets the minimum top margin for the Y-axis as a percentage.      The value must be between 0.0 and 1.0."""
        val = self._value.YAxisTopMarginMin
        return val
    @yaxis_top_margin_min.setter
    def yaxis_top_margin_min(self, val: float | None):
        tmp = self._value
        tmp.YAxisTopMarginMin = val
        self._value = tmp
    @property
    def yaxis_bottom_margin_min(self) -> float | None:
        """Gets or sets the minimum bottom margin for the Y-axis as a percentage.      The value must be between 0.0 and 1.0."""
        val = self._value.YAxisBottomMarginMin
        return val
    @yaxis_bottom_margin_min.setter
    def yaxis_bottom_margin_min(self, val: float | None):
        tmp = self._value
        tmp.YAxisBottomMarginMin = val
        self._value = tmp
    @property
    def plots(self) -> IReadOnlyList:
        """Gets the plots of the indicator."""
        val = self._value.Plots
        return val
    @plots.setter
    def plots(self, val: IReadOnlyList):
        tmp = self._value
        tmp.Plots = val
        self._value = tmp
    @property
    def levels(self) -> IReadOnlyList:
        """Gets the levels of the indicator."""
        val = self._value.Levels
        return val
    @levels.setter
    def levels(self, val: IReadOnlyList):
        tmp = self._value
        tmp.Levels = val
        self._value = tmp
    @property
    def chart(self) -> IChart:
        from tbapi.api.interfaces.ichart import IChart
        val = self._value.Chart
        return IChart(_existing=val)
    @chart.setter
    def chart(self, val: IChart):
        tmp = self._value
        tmp.Chart = val._value
        self._value = tmp
    @property
    def chart_scale(self) -> IChartScale:
        from tbapi.api.interfaces.ichart_scale import IChartScale
        val = self._value.ChartScale
        return IChartScale(_existing=val)
    @chart_scale.setter
    def chart_scale(self, val: IChartScale):
        tmp = self._value
        tmp.ChartScale = val._value
        self._value = tmp
    @property
    def symbol(self) -> ISymbol:
        from tbapi.api.interfaces.isymbol import ISymbol
        val = self._value.Symbol
        return ISymbol(_existing=val)
    @property
    def ztype(self) -> ZType:
        val = int(self._value.ZType)
        return ZType(val)
    @ztype.setter
    def ztype(self, val: ZType):
        tmp = self._value
        tmp.ZType = _ZType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def background_color(self) -> Series:
        val = self._value.BackgroundColor
        return val

    def calculate_untill(self, last_bar_index: int) -> None:
        result = self._value.CalculateUntill(last_bar_index)
        return result
  
    def shade_between(self, series1: PlotSeries, series2: PlotSeries, fill1: Color | None, fill2: Color | None, opacity: float = 1) -> None:
        """Shades the area between two plot series.            The first plot series.      The second plot series.      The color to shade when first series is above second series.      The color to shade when first series is below second series.      The opacity of the shading, ranging from 0.0 (fully transparent) to 1.0 (fully opaque)."""
        result = self._value.ShadeBetween(series1._value, series2._value, (None if fill1 is None else fill1._value), (None if fill2 is None else fill2._value), opacity)
        return result
  
    def configure_watchlist_cell(self, cell_value: WatchlistCellValue) -> None:
        """Configures the watchlist cell representation.            The watchlist cell value to configure."""
        result = self._value.ConfigureWatchlistCell(cell_value._value)
        return result
  
    def get_yrange(self) -> tuple[float, float]:
        """Gets the visible range of the indicator values on the Y-axis.            The minimum and maximum value."""
        result = self._value.GetYRange()
        return result
  

    @clr.clrmethod(None, [int])
    def calculate(self, index: int) -> None:
        """Calculate the value(s) of the indicator for a given index.            The index of the calculated value."""
        ...

    @clr.clrmethod(None, [Any])
    def on_render(self, context: IDrawingContext) -> None:
        """Renders the indicator on the chart.            The drawing context to render the indicator."""
        ...


