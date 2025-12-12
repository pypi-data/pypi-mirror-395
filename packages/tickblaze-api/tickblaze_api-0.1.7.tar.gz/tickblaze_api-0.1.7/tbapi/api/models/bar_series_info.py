






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import BarSeriesInfo as _BarSeriesInfo
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bar_series_event import BarSeriesEvent
from Tickblaze.Scripts.Api import BarSeriesEvent as _BarSeriesEvent
if TYPE_CHECKING:
    from tbapi.api.models.bar_period import BarPeriod
    from tbapi.api.models.symbol_info import SymbolInfo
    from tbapi.api.bases.bar_type import BarType

@tb_class(_BarSeriesInfo)
class BarSeriesInfo():

    @overload
    @staticmethod
    def new() -> "BarSeriesInfo":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for BarSeriesInfo. Use overloads for IDE type hints."""
        return BarSeriesInfo(*args, **kwargs)

    @property
    def is_eth(self) -> bool | None:
        val = self._value.IsETH
        return val
    @is_eth.setter
    def is_eth(self, val: bool | None):
        tmp = self._value
        tmp.IsETH = val
        self._value = tmp
    @property
    def period(self) -> BarPeriod:
        from tbapi.api.models.bar_period import BarPeriod
        val = self._value.Period
        return BarPeriod(_existing=val)
    @period.setter
    def period(self, val: BarPeriod):
        tmp = self._value
        tmp.Period = val._value
        self._value = tmp
    @property
    def start_time_utc(self) -> datetime | None:
        val = self._value.StartTimeUtc
        return to_python_datetime(val)
    @start_time_utc.setter
    def start_time_utc(self, val: datetime | None):
        tmp = self._value
        tmp.StartTimeUtc = to_net_datetime(val)
        self._value = tmp
    @property
    def end_time_utc(self) -> datetime:
        val = self._value.EndTimeUtc
        return to_python_datetime(val)
    @end_time_utc.setter
    def end_time_utc(self, val: datetime):
        tmp = self._value
        tmp.EndTimeUtc = to_net_datetime(val)
        self._value = tmp
    @property
    def update_event(self) -> BarSeriesEvent:
        val = int(self._value.UpdateEvent)
        return BarSeriesEvent(val)
    @update_event.setter
    def update_event(self, val: BarSeriesEvent):
        tmp = self._value
        tmp.UpdateEvent = _BarSeriesEvent(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def symbol_info(self) -> SymbolInfo:
        """The symbol to find. If left null, the script's symbol will be used."""
        from tbapi.api.models.symbol_info import SymbolInfo
        val = self._value.SymbolInfo
        return SymbolInfo(_existing=val)
    @symbol_info.setter
    def symbol_info(self, val: SymbolInfo):
        tmp = self._value
        tmp.SymbolInfo = val._value
        self._value = tmp
    @property
    def bar_type(self) -> BarType:
        from tbapi.api.bases.bar_type import BarType
        val = self._value.BarType
        return BarType(_existing=val)
    @bar_type.setter
    def bar_type(self, val: BarType):
        tmp = self._value
        tmp.BarType = val._value
        self._value = tmp



