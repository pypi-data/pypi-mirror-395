






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import PositionSizer as _PositionSizer
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.symbol_script import SymbolScript
from tbapi.api.interfaces.orders.iorder_accessor import IOrderAccessor
from tbapi.api.enums.run_type import RunType
from Tickblaze.Scripts.Api.Enums import RunType as _RunType
if TYPE_CHECKING:
    from tbapi.api.interfaces.isymbol import ISymbol
    from tbapi.api.interfaces.iaccount import IAccount
    from tbapi.api.interfaces.orders.iposition import IPosition

@tb_interface(_PositionSizer)
class PositionSizer(SymbolScript, IOrderAccessor):
    """A base class for position sizing scripts."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for PositionSizer. Use overloads for IDE type hints."""
        return PositionSizer(*args, **kwargs)

    @property
    def symbol(self) -> ISymbol:
        from tbapi.api.interfaces.isymbol import ISymbol
        val = self._value.Symbol
        return ISymbol(_existing=val)
    @property
    def account(self) -> IAccount:
        from tbapi.api.interfaces.iaccount import IAccount
        val = self._value.Account
        return IAccount(_existing=val)
    @property
    def pending_orders(self) -> IReadOnlyList:
        val = self._value.PendingOrders
        return val
    @property
    def position(self) -> IPosition:
        from tbapi.api.interfaces.orders.iposition import IPosition
        val = self._value.Position
        return IPosition(_existing=val)
    @property
    def run_type(self) -> RunType:
        val = int(self._value.RunType)
        return RunType(val)

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        result = self._value.GetExchangeRate(from_currency, to_currency)
        return result
  


