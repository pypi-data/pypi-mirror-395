






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Bar as _Bar
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_Bar)
class Bar():
    """Represents a single bar of market data, including the open, high, low, close prices, volume, and time."""

    @overload
    @staticmethod
    def new() -> "Bar":
        """Constructor overload with arguments: """
        ...
    @overload
    @staticmethod
    def new(time: datetime, open: float, high: float, low: float, close: float, volume: float) -> "Bar":
        """Constructor overload with arguments: time, open, high, low, close, volume"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Bar. Use overloads for IDE type hints."""
        return Bar(*args, **kwargs)

    @property
    def time(self) -> datetime:
        val = self._value.Time
        return to_python_datetime(val)
    @time.setter
    def time(self, val: datetime):
        tmp = self._value
        tmp.Time = to_net_datetime(val)
        self._value = tmp
    @property
    def open(self) -> float:
        val = self._value.Open
        return val
    @open.setter
    def open(self, val: float):
        tmp = self._value
        tmp.Open = val
        self._value = tmp
    @property
    def high(self) -> float:
        val = self._value.High
        return val
    @high.setter
    def high(self, val: float):
        tmp = self._value
        tmp.High = val
        self._value = tmp
    @property
    def low(self) -> float:
        val = self._value.Low
        return val
    @low.setter
    def low(self, val: float):
        tmp = self._value
        tmp.Low = val
        self._value = tmp
    @property
    def close(self) -> float:
        val = self._value.Close
        return val
    @close.setter
    def close(self, val: float):
        tmp = self._value
        tmp.Close = val
        self._value = tmp
    @property
    def volume(self) -> float:
        val = self._value.Volume
        return val
    @volume.setter
    def volume(self, val: float):
        tmp = self._value
        tmp.Volume = val
        self._value = tmp
    @property
    def is_complete(self) -> bool:
        val = self._value.IsComplete
        return val
    @is_complete.setter
    def is_complete(self, val: bool):
        tmp = self._value
        tmp.IsComplete = val
        self._value = tmp
    @property
    def is_historical(self) -> bool:
        val = self._value.IsHistorical
        return val
    @is_historical.setter
    def is_historical(self, val: bool):
        tmp = self._value
        tmp.IsHistorical = val
        self._value = tmp
    @property
    def body_ratio(self) -> float:
        """Returns the ratio of the candle body to overall bar height ratio"""
        val = self._value.BodyRatio
        return val
    @property
    def end_time(self) -> datetime:
        """The end time of the bar"""
        val = self._value.EndTime
        return to_python_datetime(val)
    @end_time.setter
    def end_time(self, val: datetime):
        tmp = self._value
        tmp.EndTime = to_net_datetime(val)
        self._value = tmp



