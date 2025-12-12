






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import SymbolScript as _SymbolScript
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.script import Script
if TYPE_CHECKING:
    from tbapi.api.models.bar_series import BarSeries
    from tbapi.api.models.symbol import Symbol
    from tbapi.api.models.symbol_info import SymbolInfo
    from tbapi.api.models.bar_series_info import BarSeriesInfo

@tb_interface(_SymbolScript)
class SymbolScript(Script):
    """Represents a base class for scripts that can interact with chart data, parameters, and initialization processes."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for SymbolScript. Use overloads for IDE type hints."""
        return SymbolScript(*args, **kwargs)

    @property
    def portfolio_time_utc(self) -> datetime:
        val = self._value.PortfolioTimeUtc
        return to_python_datetime(val)
    @portfolio_time_utc.setter
    def portfolio_time_utc(self, val: datetime):
        tmp = self._value
        tmp.PortfolioTimeUtc = to_net_datetime(val)
        self._value = tmp
    @property
    def is_dummy(self) -> bool:
        val = self._value.IsDummy
        return val
    @property
    def bars(self) -> BarSeries:
        """The bar series associated with the script."""
        from tbapi.api.models.bar_series import BarSeries
        val = self._value.Bars
        return BarSeries(_existing=val)
    @bars.setter
    def bars(self, val: BarSeries):
        tmp = self._value
        tmp.Bars = val._value
        self._value = tmp
    @property
    def is_realtime(self) -> bool:
        val = self._value.IsRealtime
        return val
    @is_realtime.setter
    def is_realtime(self, val: bool):
        tmp = self._value
        tmp.IsRealtime = val
        self._value = tmp

    def get_bars(self, bar_series_info: BarSeriesInfo) -> BarSeries:
        """Returns a bar series which will fill automatically and can be subscribed to for data updates"""
        result = self._value.GetBars(bar_series_info._value)
        from tbapi.api.models.bar_series import BarSeries
        return BarSeries(_existing=result)
  


