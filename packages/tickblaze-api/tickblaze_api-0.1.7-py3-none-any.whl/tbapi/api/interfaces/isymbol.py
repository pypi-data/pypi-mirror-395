




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import ISymbol as _ISymbol
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.core.enums.instrument_type import InstrumentType
from tbapi.core.enums.exchange import Exchange
from tbapi.api.enums.rounding_mode import RoundingMode
from Tickblaze.Core.Enums import InstrumentType as _InstrumentType
from Tickblaze.Core.Enums import Exchange as _Exchange
from Tickblaze.Scripts.Api.Enums import RoundingMode as _RoundingMode
if TYPE_CHECKING:
    from tbapi.api.interfaces.iexchange_calendar import IExchangeCalendar

@tb_interface(_ISymbol)
class ISymbol():
    """Defines properties and methods related to a symbol, including tick size, point size, and volume normalization."""

    @property
    def code(self) -> str:
        """The code of the symbol."""
        val = self._value.Code
        return val
    @property
    def description(self) -> str:
        """The description of the symbol."""
        val = self._value.Description
        return val
    @property
    def tick_size(self) -> float:
        """The tick size of the symbol."""
        val = self._value.TickSize
        return val
    @property
    def tick_value(self) -> float:
        """The tick value of the symbol."""
        val = self._value.TickValue
        return val
    @property
    def ticks_per_point(self) -> float:
        """The number of ticks per point for the symbol."""
        val = self._value.TicksPerPoint
        return val
    @property
    def point_size(self) -> float:
        """The point size of the symbol."""
        val = self._value.PointSize
        return val
    @property
    def point_value(self) -> float:
        """The point value of the symbol."""
        val = self._value.PointValue
        return val
    @property
    def decimals(self) -> int:
        """The number of decimals for the symbol."""
        val = self._value.Decimals
        return val
    @property
    def minimum_volume(self) -> float:
        """The minimum volume for the symbol."""
        val = self._value.MinimumVolume
        return val
    @property
    def currency_code(self) -> str:
        """The currency code of the symbol."""
        val = self._value.CurrencyCode
        return val
    @property
    def type(self) -> InstrumentType:
        """The type of the instrument"""
        val = int(self._value.Type)
        return InstrumentType(val)
    @type.setter
    def type(self, val: InstrumentType):
        tmp = self._value
        tmp.Type = _InstrumentType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def exchange_calendar(self) -> IExchangeCalendar:
        """The exchange calendar for the symbol."""
        from tbapi.api.interfaces.iexchange_calendar import IExchangeCalendar
        val = self._value.ExchangeCalendar
        return IExchangeCalendar(_existing=val)
    @property
    def exchange(self) -> Exchange:
        """The exchange the symbol trades on"""
        val = int(self._value.Exchange)
        return Exchange(val)

    @abstractmethod
    def round_to_tick(self, value: float) -> float:
        """Rounds a value to the nearest tick.            The value to round.      The value rounded to the nearest tick."""
        result = self._value.RoundToTick(value)
        return result
  
    @abstractmethod
    def format_price(self, price: float) -> str:
        """Formats a price as a string for the symbol.            The price to format.      The formatted price as a string."""
        result = self._value.FormatPrice(price)
        return result
  
    @abstractmethod
    def normalize_volume(self, volume: float, rounding_mode: RoundingMode) -> float:
        """Normalizes a volume to the symbol's tradable volume, applying the specified rounding mode.            The volume to normalize.      The rounding mode to apply.      The normalized volume."""
        result = self._value.NormalizeVolume(volume, _RoundingMode(rounding_mode.value if hasattr(rounding_mode, 'value') else int(rounding_mode)))
        return result
  

