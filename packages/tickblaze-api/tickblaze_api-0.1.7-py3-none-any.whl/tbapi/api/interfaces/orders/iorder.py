




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IOrder as _IOrder
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.enums.order_status import OrderStatus
from tbapi.api.enums.order_type import OrderType
from tbapi.api.enums.order_direction import OrderDirection
from tbapi.api.enums.time_in_force import TimeInForce
from Tickblaze.Scripts.Api.Enums import OrderStatus as _OrderStatus
from Tickblaze.Scripts.Api.Enums import OrderType as _OrderType
from Tickblaze.Scripts.Api.Enums import OrderDirection as _OrderDirection
from Tickblaze.Scripts.Api.Enums import TimeInForce as _TimeInForce
if TYPE_CHECKING:
    from tbapi.api.interfaces.isymbol import ISymbol

@tb_interface(_IOrder)
class IOrder():
    """Represents an order within the trading system, containing details about the order's characteristics and state."""

    @property
    def symbol(self) -> ISymbol:
        """The financial symbol associated with the order."""
        from tbapi.api.interfaces.isymbol import ISymbol
        val = self._value.Symbol
        return ISymbol(_existing=val)
    @property
    def status(self) -> OrderStatus:
        """The current status of the order (e.g., pending, executed, canceled)."""
        val = int(self._value.Status)
        return OrderStatus(val)
    @property
    def is_complete(self) -> bool:
        """Whether the order is cancelled or executed"""
        val = self._value.IsComplete
        return val
    @property
    def comment(self) -> str:
        """Comment attached to the order"""
        val = self._value.Comment
        return val
    @property
    def type(self) -> OrderType:
        """The type of the order (e.g., market, limit, stop)."""
        val = int(self._value.Type)
        return OrderType(val)
    @property
    def direction(self) -> OrderDirection:
        """The direction of the order (e.g., long, short)."""
        val = int(self._value.Direction)
        return OrderDirection(val)
    @property
    def time_in_force(self) -> TimeInForce:
        """Specifies how long the order remains active in the market (e.g., Good Till Cancelled, Immediate or Cancel)."""
        val = int(self._value.TimeInForce)
        return TimeInForce(val)
    @property
    def price(self) -> float:
        """The execution price of the order."""
        val = self._value.Price
        return val
    @property
    def stop_price(self) -> float:
        """The stop price for the order, if applicable."""
        val = self._value.StopPrice
        return val
    @property
    def limit_price(self) -> float:
        """The limit price for the order, if applicable."""
        val = self._value.LimitPrice
        return val
    @property
    def quantity(self) -> float:
        """The quantity of the order, representing the number of units to buy or sell."""
        val = self._value.Quantity
        return val
    @property
    def is_filled(self) -> bool:
        """Indicates whether the order was completely filled."""
        val = self._value.IsFilled
        return val
    @property
    def filled_quantity(self) -> float:
        """The filled quantity."""
        val = self._value.FilledQuantity
        return val
    @filled_quantity.setter
    def filled_quantity(self, val: float):
        tmp = self._value
        tmp.FilledQuantity = val
        self._value = tmp
    @property
    def price_offset(self) -> float:
        """The trailing offset, either in percent or as a fixed value."""
        val = self._value.PriceOffset
        return val
    @property
    def index(self) -> int:
        """The index of the order, providing a unique identifier within the system."""
        val = self._value.Index
        return val
    @property
    def parent_order_index(self) -> int:
        """The order index to which a StopLoss, TakeProfit or TrailingStopLoss order is attached."""
        val = self._value.ParentOrderIndex
        return val
    @property
    def is_stop_loss(self) -> bool:
        val = self._value.IsStopLoss
        return val
    @property
    def is_take_profit(self) -> bool:
        val = self._value.IsTakeProfit
        return val

    def get_order_price(self, ref_price: float | None = None) -> float:
        result = self._value.GetOrderPrice(ref_price)
        return result
  

