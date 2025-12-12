




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IOrderAccessor as _IOrderAccessor
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.enums.run_type import RunType
from Tickblaze.Scripts.Api.Enums import RunType as _RunType
if TYPE_CHECKING:
    from tbapi.api.interfaces.isymbol import ISymbol
    from tbapi.api.interfaces.iaccount import IAccount
    from tbapi.api.interfaces.orders.iposition import IPosition

@tb_interface(_IOrderAccessor)
class IOrderAccessor():
    """Provides access to order-related information and functionality within the trading system."""

    @property
    def symbol(self) -> ISymbol:
        """The financial symbol associated with the orders and position."""
        from tbapi.api.interfaces.isymbol import ISymbol
        val = self._value.Symbol
        return ISymbol(_existing=val)
    @property
    def account(self) -> IAccount:
        """The account associated with the orders and position."""
        from tbapi.api.interfaces.iaccount import IAccount
        val = self._value.Account
        return IAccount(_existing=val)
    @property
    def pending_orders(self) -> IReadOnlyList:
        """A collection of orders that are currently pending execution."""
        val = self._value.PendingOrders
        return val
    @property
    def position(self) -> IPosition:
        """The position associated with the current symbol and account."""
        from tbapi.api.interfaces.orders.iposition import IPosition
        val = self._value.Position
        return IPosition(_existing=val)
    @property
    def run_type(self) -> RunType:
        val = int(self._value.RunType)
        return RunType(val)

    @abstractmethod
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Retrieves the exchange rate for converting one currency to another.            The currency to convert from (e.g., "USD").      The currency to convert to (e.g., "EUR").      The exchange rate between the specified currencies."""
        result = self._value.GetExchangeRate(from_currency, to_currency)
        return result
  

