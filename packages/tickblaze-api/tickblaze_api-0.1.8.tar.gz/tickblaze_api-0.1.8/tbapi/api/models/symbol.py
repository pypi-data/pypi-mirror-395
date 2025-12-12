






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Symbol as _Symbol
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.isymbol import ISymbol
from tbapi.core.enums.instrument_type import InstrumentType
from tbapi.core.enums.exchange import Exchange
from tbapi.api.enums.rounding_mode import RoundingMode
from Tickblaze.Core.Enums import InstrumentType as _InstrumentType
from Tickblaze.Core.Enums import Exchange as _Exchange
from Tickblaze.Scripts.Api.Enums import RoundingMode as _RoundingMode
if TYPE_CHECKING:
    from tbapi.api.interfaces.iexchange_calendar import IExchangeCalendar

@tb_class(_Symbol)
class Symbol(ISymbol):

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Symbol. Use overloads for IDE type hints."""
        return Symbol(*args, **kwargs)

    @property
    def code(self) -> str:
        val = self._value.Code
        return val
    @property
    def description(self) -> str:
        val = self._value.Description
        return val
    @property
    def tick_size(self) -> float:
        val = self._value.TickSize
        return val
    @tick_size.setter
    def tick_size(self, val: float):
        tmp = self._value
        tmp.TickSize = val
        self._value = tmp
    @property
    def tick_value(self) -> float:
        val = self._value.TickValue
        return val
    @tick_value.setter
    def tick_value(self, val: float):
        tmp = self._value
        tmp.TickValue = val
        self._value = tmp
    @property
    def decimals(self) -> int:
        val = self._value.Decimals
        return val
    @decimals.setter
    def decimals(self, val: int):
        tmp = self._value
        tmp.Decimals = val
        self._value = tmp
    @property
    def currency_code(self) -> str:
        val = self._value.CurrencyCode
        return val
    @currency_code.setter
    def currency_code(self, val: str):
        tmp = self._value
        tmp.CurrencyCode = val
        self._value = tmp
    @property
    def exchange_calendar(self) -> IExchangeCalendar:
        from tbapi.api.interfaces.iexchange_calendar import IExchangeCalendar
        val = self._value.ExchangeCalendar
        return IExchangeCalendar(_existing=val)
    @exchange_calendar.setter
    def exchange_calendar(self, val: IExchangeCalendar):
        tmp = self._value
        tmp.ExchangeCalendar = val._value
        self._value = tmp
    @property
    def ticks_per_point(self) -> float:
        val = self._value.TicksPerPoint
        return val
    @property
    def point_size(self) -> float:
        val = self._value.PointSize
        return val
    @property
    def point_value(self) -> float:
        val = self._value.PointValue
        return val
    @property
    def minimum_volume(self) -> float:
        val = self._value.MinimumVolume
        return val
    @minimum_volume.setter
    def minimum_volume(self, val: float):
        tmp = self._value
        tmp.MinimumVolume = val
        self._value = tmp
    @property
    def type(self) -> InstrumentType:
        val = int(self._value.Type)
        return InstrumentType(val)
    @type.setter
    def type(self, val: InstrumentType):
        tmp = self._value
        tmp.Type = _InstrumentType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def exchange(self) -> Exchange:
        val = int(self._value.Exchange)
        return Exchange(val)
    @exchange.setter
    def exchange(self, val: Exchange):
        tmp = self._value
        tmp.Exchange = _Exchange(val.value if hasattr(val, "value") else int(val))
        self._value = tmp

    def round_to_tick(self, value: float) -> float:
        result = self._value.RoundToTick(value)
        return result
  
    def format_price(self, price: float) -> str:
        result = self._value.FormatPrice(price)
        return result
  
    def normalize_volume(self, volume: float, rounding_mode: RoundingMode) -> float:
        result = self._value.NormalizeVolume(volume, _RoundingMode(rounding_mode.value if hasattr(rounding_mode, 'value') else int(rounding_mode)))
        return result
  


