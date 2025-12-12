






from __future__ import annotations
from typing import TYPE_CHECKING
import clr
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import Strategy as _Strategy
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.trading_script import TradingScript
from tbapi.api.interfaces.ichart_object import IChartObject
from tbapi.api.interfaces.orders.istrategy_order_manager import IStrategyOrderManager
from tbapi.api.enums.ztype import ZType
from tbapi.api.enums.run_type import RunType
from Tickblaze.Scripts.Api.Enums import ZType as _ZType
from Tickblaze.Scripts.Api.Enums import RunType as _RunType
if TYPE_CHECKING:
    from tbapi.api.interfaces.ichart import IChart
    from tbapi.api.interfaces.ichart_scale import IChartScale
    from tbapi.api.interfaces.idrawing_context import IDrawingContext

@tb_interface(_Strategy)
class Strategy(TradingScript, IChartObject, IStrategyOrderManager):
    """Represents a base class for strategy scripts allowing order management."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Strategy. Use overloads for IDE type hints."""
        return Strategy(*args, **kwargs)

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
    def run_type(self) -> RunType:
        val = int(self._value.RunType)
        return RunType(val)

    def on_render(self, context: IDrawingContext) -> None:
        result = self._value.OnRender(context._value)
        return result
  
    def flatten(self, comment: str = "") -> None:
        result = self._value.Flatten(comment)
        return result
  
    def cancel_pending_orders(self, include_attached_orders: bool, comment: str = "") -> None:
        result = self._value.CancelPendingOrders(include_attached_orders, comment)
        return result
  

    @clr.clrmethod(None, [None])
    def on_tick(self) -> None:
        """Method to handle tick updates for the strategy."""
        ...

    @clr.clrmethod(None, [None])
    def on_shutdown(self) -> None:
        """Method called when the strategy is shutting down."""
        ...


