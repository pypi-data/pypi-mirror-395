




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IPositionBase as _IPositionBase
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.enums.position_status import PositionStatus
from tbapi.api.enums.order_direction import OrderDirection
from Tickblaze.Scripts.Api.Enums import PositionStatus as _PositionStatus
from Tickblaze.Scripts.Api.Enums import OrderDirection as _OrderDirection
if TYPE_CHECKING:
    from tbapi.api.interfaces.isymbol import ISymbol

@tb_interface(_IPositionBase)
class IPositionBase():

    @property
    def status(self) -> PositionStatus:
        """Gets the current status of the position."""
        val = int(self._value.Status)
        return PositionStatus(val)
    @property
    def entry_price(self) -> float:
        """Gets the price at which the position was entered."""
        val = self._value.EntryPrice
        return val
    @property
    def exit_price(self) -> float:
        """Gets the price at which the position was exited. This is zero for an open position."""
        val = self._value.ExitPrice
        return val
    @property
    def quantity(self) -> float:
        """Gets the quantity of the position."""
        val = self._value.Quantity
        return val
    @property
    def commission(self) -> float:
        """Gets the total commission incurred for the position."""
        val = self._value.Commission
        return val
    @property
    def direction(self) -> OrderDirection:
        """Gets the direction of the position, indicating whether it is long or short."""
        val = int(self._value.Direction)
        return OrderDirection(val)
    @property
    def unrealized_profit_loss(self) -> float:
        """The unrealized profit/loss of the position"""
        val = self._value.UnrealizedProfitLoss
        return val
    @property
    def realized_profit_loss(self) -> float:
        """The realized profit/loss of the position"""
        val = self._value.RealizedProfitLoss
        return val
    @property
    def current_price(self) -> float:
        """The positions current price"""
        val = self._value.CurrentPrice
        return val
    @property
    def symbol(self) -> ISymbol:
        """Gets the trading symbol associated with the position."""
        from tbapi.api.interfaces.isymbol import ISymbol
        val = self._value.Symbol
        return ISymbol(_existing=val)
    @symbol.setter
    def symbol(self, val: ISymbol):
        tmp = self._value
        tmp.Symbol = val._value
        self._value = tmp


