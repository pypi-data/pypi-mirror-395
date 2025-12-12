






from __future__ import annotations
from typing import TYPE_CHECKING
import clr
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import TradingScript as _TradingScript
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.symbol_script import SymbolScript
from tbapi.api.interfaces.orders.iorder_manager import IOrderManager
from tbapi.api.enums.run_type import RunType
from tbapi.api.enums.order_action import OrderAction
from tbapi.api.enums.time_in_force import TimeInForce
from tbapi.api.enums.order_type import OrderType
from Tickblaze.Scripts.Api.Enums import RunType as _RunType
from Tickblaze.Scripts.Api.Enums import OrderAction as _OrderAction
from Tickblaze.Scripts.Api.Enums import TimeInForce as _TimeInForce
from Tickblaze.Scripts.Api.Enums import OrderType as _OrderType
from tbapi.api.interfaces.orders.iorder import IOrder
if TYPE_CHECKING:
    from tbapi.api.interfaces.isymbol import ISymbol
    from tbapi.api.interfaces.iaccount import IAccount
    from tbapi.api.interfaces.orders.iposition import IPosition

@tb_interface(_TradingScript)
class TradingScript(SymbolScript, IOrderManager):
    """Represents a trading script that allows the execution and management of orders and positions in a trading system."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for TradingScript. Use overloads for IDE type hints."""
        return TradingScript(*args, **kwargs)

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

    def execute_market_order(self, action: OrderAction, quantity: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        result = self._value.ExecuteMarketOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def place_order(self, action: OrderAction, type: OrderType, quantity: float, stop_price: float | None, limit_price: float | None, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        result = self._value.PlaceOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), _OrderType(type.value if hasattr(type, 'value') else int(type)), quantity, stop_price, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def place_limit_order(self, action: OrderAction, quantity: float, limit_price: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        result = self._value.PlaceLimitOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def place_stop_limit_order(self, action: OrderAction, quantity: float, stop_price: float, limit_price: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        result = self._value.PlaceStopLimitOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, stop_price, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def place_stop_order(self, action: OrderAction, quantity: float, stop_price: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        result = self._value.PlaceStopOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, stop_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def set_stop_loss(self, order: IOrder, stop_price: float, comment: str = "") -> IOrder:
        result = self._value.SetStopLoss(order._value, stop_price, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def set_stop_loss_ticks(self, order: IOrder, ticks: int, comment: str = "") -> IOrder:
        result = self._value.SetStopLossTicks(order._value, ticks, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def set_stop_loss_percent(self, order: IOrder, percent: float, comment: str = "") -> IOrder:
        result = self._value.SetStopLossPercent(order._value, percent, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def set_take_profit(self, order: IOrder, limit_price: float, comment: str = "") -> IOrder:
        result = self._value.SetTakeProfit(order._value, limit_price, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def set_take_profit_ticks(self, order: IOrder, ticks: int, comment: str = "") -> IOrder:
        result = self._value.SetTakeProfitTicks(order._value, ticks, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def set_take_profit_percent(self, order: IOrder, percent: float, comment: str = "") -> IOrder:
        result = self._value.SetTakeProfitPercent(order._value, percent, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    def modify_order(self, order: IOrder, quantity: float, stop_price: float | None, limit_price: float | None, time_in_force: TimeInForce = TimeInForce.Day) -> None:
        result = self._value.ModifyOrder(order._value, quantity, stop_price, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)))
        return result
  
    def cancel_order(self, order: IOrder, comment: str = "", cancel_silently: bool = False) -> None:
        result = self._value.CancelOrder(order._value, comment, cancel_silently)
        return result
  
    def close_position(self, comment: str = "") -> None:
        result = self._value.ClosePosition(comment)
        return result
  
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        result = self._value.GetExchangeRate(from_currency, to_currency)
        return result
  
    def get_order_expected_price(self, order: IOrder) -> float:
        result = self._value.GetOrderExpectedPrice(order._value)
        return result
  

    @clr.clrmethod(None, [Any])
    def on_order_update(self, order: IOrder) -> None:
        """Called when an order's status is updated.            The updated order."""
        ...

    @clr.clrmethod(None, [Any])
    def on_order_fill_update(self, order: IOrder) -> None:
        """Called when an order's fill status is updated (after positions, trades, and dependant orders are updated).            The updated order."""
        ...

    @clr.clrmethod(None, [None])
    def on_position_update(self) -> None:
        """Called when the position's status is updated."""
        ...

    @clr.clrmethod(None, [None])
    def on_bar_update(self) -> None:
        """Called when the bar data is updated."""
        ...

    @clr.clrmethod(None, [int])
    def on_bar(self, index: int) -> None:
        """Called when bar is updated.            The index of the updated bar."""
        ...


