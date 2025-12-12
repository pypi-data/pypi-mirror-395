






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import BarSeries as _BarSeries
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.series import Series
from tbapi.api.models.bar import Bar
if TYPE_CHECKING:
    from tbapi.api.models.symbol import Symbol
    from tbapi.core.models.contract_settings import ContractSettings
    from tbapi.api.models.bar_period import BarPeriod
    from tbapi.api.interfaces.iseries import ISeries
    from tbapi.api.bases.bar_type import BarType
    from tbapi.api.interfaces.iexchange_session import IExchangeSession

@tb_class(_BarSeries)
class BarSeries(Series):
    """Represents a series of bars, with various calculated series such as Low, High, Open, Close, and others."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for BarSeries. Use overloads for IDE type hints."""
        return BarSeries(*args, **kwargs)

    @property
    def symbol(self) -> Symbol:
        """The symbol associated with the bar series."""
        from tbapi.api.models.symbol import Symbol
        val = self._value.Symbol
        return Symbol(_existing=val)
    @symbol.setter
    def symbol(self, val: Symbol):
        tmp = self._value
        tmp.Symbol = val._value
        self._value = tmp
    @property
    def is_eth(self) -> bool:
        """True if the bar series represents ETH hours (vs RTH)"""
        val = self._value.IsETH
        return val
    @is_eth.setter
    def is_eth(self, val: bool):
        tmp = self._value
        tmp.IsETH = val
        self._value = tmp
    @property
    def contract_settings(self) -> ContractSettings:
        """For futures symbols, details which kind of contract data this series represents (which specific contract if single contract, data merge rule otherwise)"""
        from tbapi.core.models.contract_settings import ContractSettings
        val = self._value.ContractSettings
        return ContractSettings(_existing=val)
    @contract_settings.setter
    def contract_settings(self, val: ContractSettings):
        tmp = self._value
        tmp.ContractSettings = val._value
        self._value = tmp
    @property
    def period(self) -> BarPeriod:
        """The period of the bars in the series."""
        from tbapi.api.models.bar_period import BarPeriod
        val = self._value.Period
        return BarPeriod(_existing=val)
    @period.setter
    def period(self, val: BarPeriod):
        tmp = self._value
        tmp.Period = val._value
        self._value = tmp
    @property
    def low(self) -> ISeries:
        """The series of low prices for each bar."""
        val = self._value.Low
        return val
    @low.setter
    def low(self, val: ISeries):
        tmp = self._value
        tmp.Low = val
        self._value = tmp
    @property
    def time(self) -> ISeries:
        """The series of time for each bar."""
        val = self._value.Time
        return val
    @time.setter
    def time(self, val: ISeries):
        tmp = self._value
        tmp.Time = val
        self._value = tmp
    @property
    def open(self) -> ISeries:
        """The series of open prices for each bar."""
        val = self._value.Open
        return val
    @open.setter
    def open(self, val: ISeries):
        tmp = self._value
        tmp.Open = val
        self._value = tmp
    @property
    def high(self) -> ISeries:
        """The series of high prices for each bar."""
        val = self._value.High
        return val
    @high.setter
    def high(self, val: ISeries):
        tmp = self._value
        tmp.High = val
        self._value = tmp
    @property
    def close(self) -> ISeries:
        """The series of close prices for each bar."""
        val = self._value.Close
        return val
    @close.setter
    def close(self, val: ISeries):
        tmp = self._value
        tmp.Close = val
        self._value = tmp
    @property
    def volume(self) -> ISeries:
        """The series of volumes for each bar."""
        val = self._value.Volume
        return val
    @volume.setter
    def volume(self, val: ISeries):
        tmp = self._value
        tmp.Volume = val
        self._value = tmp
    @property
    def median_price(self) -> ISeries:
        """The series of median prices for each bar."""
        val = self._value.MedianPrice
        return val
    @median_price.setter
    def median_price(self, val: ISeries):
        tmp = self._value
        tmp.MedianPrice = val
        self._value = tmp
    @property
    def typical_price(self) -> ISeries:
        """The series of typical prices for each bar."""
        val = self._value.TypicalPrice
        return val
    @typical_price.setter
    def typical_price(self, val: ISeries):
        tmp = self._value
        tmp.TypicalPrice = val
        self._value = tmp
    @property
    def bar_type(self) -> BarType:
        """A shallow copy of the bar type script creating this series bars"""
        from tbapi.api.bases.bar_type import BarType
        val = self._value.BarType
        return BarType(_existing=val)
    @bar_type.setter
    def bar_type(self, val: BarType):
        tmp = self._value
        tmp.BarType = val._value
        self._value = tmp
    @property
    def start_time_utc(self) -> datetime:
        """The start of the data series"""
        val = self._value.StartTimeUtc
        return to_python_datetime(val)
    @start_time_utc.setter
    def start_time_utc(self, val: datetime):
        tmp = self._value
        tmp.StartTimeUtc = to_net_datetime(val)
        self._value = tmp
    @property
    def latest_bar_is_first_of_session(self) -> bool:
        val = self._value.LatestBarIsFirstOfSession
        return val
    @latest_bar_is_first_of_session.setter
    def latest_bar_is_first_of_session(self, val: bool):
        tmp = self._value
        tmp.LatestBarIsFirstOfSession = val
        self._value = tmp
    @property
    def session(self) -> IExchangeSession:
        from tbapi.api.interfaces.iexchange_session import IExchangeSession
        val = self._value.Session
        return IExchangeSession(_existing=val)
    @session.setter
    def session(self, val: IExchangeSession):
        tmp = self._value
        tmp.Session = val._value
        self._value = tmp

    def slice(self, date_time_utc: datetime) -> list[int]:
        """Slices the series starting from a specific UTC date/time.            The UTC date/time to slice from.      A sequence of indexes starting from the given date/time."""
        result = self._value.Slice(to_net_datetime(date_time_utc))
        return result
  


    def __getitem__(self, index: int) -> Bar:
        result = self._value[index]
        return Bar(_existing=result)

    def __setitem__(self, index: int, value: Bar):
        tmp = value
        tmp = value._value
        self._value[index] = tmp
