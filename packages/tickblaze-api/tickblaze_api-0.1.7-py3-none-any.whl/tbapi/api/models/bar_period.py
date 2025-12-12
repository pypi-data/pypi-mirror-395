






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import BarPeriod as _BarPeriod
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.models.source_type import SourceType
from tbapi.api.models.period_type import PeriodType
if TYPE_CHECKING:
    from tbapi.api.models.bar_period import BarPeriod
from tbapi.api.models.source_type import SourceType
from tbapi.api.models.period_type import PeriodType
_SourceType = _BarPeriod.SourceType
_PeriodType = _BarPeriod.PeriodType

@tb_class(_BarPeriod)
class BarPeriod():
    """Represents the period of a bar, including its source type, period type, and size.            The source of the bar period (e.g., Ask, Bid, Trade).      The type of period for the bar (e.g., Day, Week, Minute).      The size of the bar period (e.g., 5 minutes, 1 day)."""

    @overload
    @staticmethod
    def new(Source: SourceType, Type: PeriodType, Size: float) -> "BarPeriod":
        """Constructor overload with arguments: Source, Type, Size"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for BarPeriod. Use overloads for IDE type hints."""
        return BarPeriod(*args, **kwargs)

    @property
    def source(self) -> SourceType:
        """The source of the bar period (e.g., Ask, Bid, Trade)."""
        val = int(self._value.Source)
        return SourceType(val)
    @source.setter
    def source(self, val: SourceType):
        tmp = self._value
        tmp.Source = _SourceType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def type(self) -> PeriodType:
        """The type of period for the bar (e.g., Day, Week, Minute)."""
        val = int(self._value.Type)
        return PeriodType(val)
    @type.setter
    def type(self, val: PeriodType):
        tmp = self._value
        tmp.Type = _PeriodType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def size(self) -> float:
        """The size of the bar period (e.g., 5 minutes, 1 day)."""
        val = self._value.Size
        return val
    @size.setter
    def size(self, val: float):
        tmp = self._value
        tmp.Size = val
        self._value = tmp



