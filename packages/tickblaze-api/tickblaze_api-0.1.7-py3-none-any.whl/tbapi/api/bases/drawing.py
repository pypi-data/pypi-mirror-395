






from __future__ import annotations
from typing import TYPE_CHECKING
import clr
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import Drawing as _Drawing
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.symbol_script import SymbolScript
from tbapi.api.interfaces.ichart_object import IChartObject
from tbapi.api.enums.ztype import ZType
from Tickblaze.Scripts.Api.Enums import ZType as _ZType
from tbapi.api.interfaces.idrawing_context import IDrawingContext
if TYPE_CHECKING:
    from tbapi.api.interfaces.ichart import IChart
    from tbapi.api.interfaces.ichart_points import IChartPoints
    from tbapi.api.interfaces.ichart_scale import IChartScale
    from tbapi.api.interfaces.isymbol import ISymbol

@tb_interface(_Drawing)
class Drawing(SymbolScript, IChartObject):
    """Represents a base class for drawing objects that can be rendered on the chart."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Drawing. Use overloads for IDE type hints."""
        return Drawing(*args, **kwargs)

    @property
    def points_count(self) -> int:
        """Gets the number of points in the drawing."""
        val = self._value.PointsCount
        return val
    @property
    def is_created(self) -> bool:
        """Indicates whether the drawing object has been created."""
        val = self._value.IsCreated
        return val
    @is_created.setter
    def is_created(self, val: bool):
        tmp = self._value
        tmp.IsCreated = val
        self._value = tmp
    @property
    def is_selected(self) -> bool:
        """Indicates whether the drawing is selected."""
        val = self._value.IsSelected
        return val
    @is_selected.setter
    def is_selected(self, val: bool):
        tmp = self._value
        tmp.IsSelected = val
        self._value = tmp
    @property
    def is_updating(self) -> bool:
        """Indicates whether the drawing anchors are updating."""
        val = self._value.IsUpdating
        return val
    @is_updating.setter
    def is_updating(self, val: bool):
        tmp = self._value
        tmp.IsUpdating = val
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
    def points(self) -> IChartPoints:
        from tbapi.api.interfaces.ichart_points import IChartPoints
        val = self._value.Points
        return IChartPoints(_existing=val)
    @points.setter
    def points(self, val: IChartPoints):
        tmp = self._value
        tmp.Points = val._value
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
    @symbol.setter
    def symbol(self, val: ISymbol):
        tmp = self._value
        tmp.Symbol = val._value
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
    def ztype(self) -> ZType:
        val = int(self._value.ZType)
        return ZType(val)
    @ztype.setter
    def ztype(self, val: ZType):
        tmp = self._value
        tmp.ZType = _ZType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def snap_to_bar(self) -> bool:
        """Gets or sets a value indicating whether the drawing is snapped to the bar."""
        val = self._value.SnapToBar
        return val
    @snap_to_bar.setter
    def snap_to_bar(self, val: bool):
        tmp = self._value
        tmp.SnapToBar = val
        self._value = tmp
    @property
    def pending_additional_data_download(self) -> bool:
        val = self._value.PendingAdditionalDataDownload
        return val
    @pending_additional_data_download.setter
    def pending_additional_data_download(self, val: bool):
        tmp = self._value
        tmp.PendingAdditionalDataDownload = val
        self._value = tmp


    @clr.clrmethod(None, [Any, Any, int])
    def set_point(self, x_data_value: Any, y_data_value: Any, index: int) -> None:
        """Sets a point on the drawing at the specified index.            The x data value of the point.      The y data value of the point.      The index of the point to set."""
        ...

    @clr.clrmethod(None, [None])
    def on_created(self) -> None:
        """Performs actions when the drawing is created."""
        ...

    @clr.clrmethod(None, [Any])
    def on_render(self, context: IDrawingContext) -> None:
        ...


