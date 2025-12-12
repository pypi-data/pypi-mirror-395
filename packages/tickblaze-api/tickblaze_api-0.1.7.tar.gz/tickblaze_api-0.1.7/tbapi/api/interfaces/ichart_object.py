




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IChartObject as _IChartObject
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.enums.ztype import ZType
from Tickblaze.Scripts.Api.Enums import ZType as _ZType
if TYPE_CHECKING:
    from tbapi.api.interfaces.ichart import IChart
    from tbapi.api.interfaces.ichart_scale import IChartScale
    from tbapi.api.interfaces.idrawing_context import IDrawingContext

@tb_interface(_IChartObject)
class IChartObject():
    """Represents an object displayed on a chart, including its scale, and rendering behavior."""

    @property
    def chart(self) -> IChart:
        """The chart to which this object belongs."""
        from tbapi.api.interfaces.ichart import IChart
        val = self._value.Chart
        return IChart(_existing=val)
    @property
    def chart_scale(self) -> IChartScale:
        """The scale used by this object on the chart."""
        from tbapi.api.interfaces.ichart_scale import IChartScale
        val = self._value.ChartScale
        return IChartScale(_existing=val)
    @property
    def show_on_chart(self) -> bool:
        """Indicates whether the object is visible on the chart."""
        val = self._value.ShowOnChart
        return val
    @property
    def ztype(self) -> ZType:
        val = int(self._value.ZType)
        return ZType(val)
    @ztype.setter
    def ztype(self, val: ZType):
        tmp = self._value
        tmp.ZType = _ZType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp

    @abstractmethod
    def on_render(self, context: IDrawingContext) -> None:
        """Draws the chart object using the specified drawing context.            The context used for rendering."""
        result = self._value.OnRender(context._value)
        return result
  

