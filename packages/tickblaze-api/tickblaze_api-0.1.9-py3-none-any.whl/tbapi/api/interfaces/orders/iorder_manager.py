




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IOrderManager as _IOrderManager
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.orders.iorder_accessor import IOrderAccessor
from tbapi.api.enums.order_action import OrderAction
from tbapi.api.enums.time_in_force import TimeInForce
from tbapi.api.enums.order_type import OrderType
from Tickblaze.Scripts.Api.Enums import OrderAction as _OrderAction
from Tickblaze.Scripts.Api.Enums import TimeInForce as _TimeInForce
from Tickblaze.Scripts.Api.Enums import OrderType as _OrderType
if TYPE_CHECKING:
    from tbapi.api.interfaces.orders.iorder import IOrder

@tb_interface(_IOrderManager)
class IOrderManager(IOrderAccessor):
    """Provides methods for managing orders and positions within the trading system."""


    @abstractmethod
    def execute_market_order(self, action: OrderAction, quantity: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        """Executes a market order immediately based on the given action and quantity.            The buy or sell action.      The order quantity.      Order duration setting. Defaults to Day.      Optional order comment."""
        result = self._value.ExecuteMarketOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def place_order(self, action: OrderAction, type: OrderType, quantity: float, stop_price: float | None, limit_price: float | None, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        """Places an order of specified type with defined price parameters.            The buy or sell action.      Order type (e.g., Limit, Stop).      Order quantity.      Stop price if applicable.      Limit price if applicable.      Order duration. Defaults to Day.      Optional comment for the order."""
        result = self._value.PlaceOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), _OrderType(type.value if hasattr(type, 'value') else int(type)), quantity, stop_price, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def place_limit_order(self, action: OrderAction, quantity: float, limit_price: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        """Places a limit order.            The buy or sell action.      Order quantity.      Limit price.      Order duration. Defaults to Day.      Optional comment for the order."""
        result = self._value.PlaceLimitOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def place_stop_order(self, action: OrderAction, quantity: float, stop_price: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        """Places a stop order that activates when the stop price is reached.      The buy or sell action.      Order quantity.      Stop price.      Order duration. Defaults to Day.      Optional comment for the order."""
        result = self._value.PlaceStopOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, stop_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def place_stop_limit_order(self, action: OrderAction, quantity: float, stop_price: float, limit_price: float, time_in_force: TimeInForce = TimeInForce.Day, comment: str = "") -> IOrder:
        """Places a stop-limit order.            The buy or sell action.      Order quantity.      Stop price.      Limit price.      Order duration. Defaults to Day.      Optional comment for the order."""
        result = self._value.PlaceStopLimitOrder(_OrderAction(action.value if hasattr(action, 'value') else int(action)), quantity, stop_price, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)), comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def set_stop_loss(self, order: IOrder, stop_price: float, comment: str = "") -> IOrder:
        """Sets a stop-loss order on an open position at a specified price.            The order of the open position to which the stop-loss is applied.      The price at which the stop-loss order is set.      Optional comment for the order, providing additional information or notes.      The updated order with the stop-loss applied."""
        result = self._value.SetStopLoss(order._value, stop_price, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def set_stop_loss_ticks(self, order: IOrder, ticks: int, comment: str = "") -> IOrder:
        """Sets a stop-loss order on an open position based on a specified number of ticks from the entry price.            The order of the open position to which the stop-loss is applied.      The number of ticks away from the entry price to place the stop-loss.      Optional comment for the order, providing additional information or notes.      The updated order with the stop-loss applied."""
        result = self._value.SetStopLossTicks(order._value, ticks, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def set_stop_loss_percent(self, order: IOrder, percent: float, comment: str = "") -> IOrder:
        """Sets a stop-loss order on an open position based on a specified percentage from the entry price.            The order of the open position to which the stop-loss is applied.      The percentage away from the entry price to place the stop-loss.      Optional comment for the order, providing additional information or notes.      The updated order with the stop-loss applied."""
        result = self._value.SetStopLossPercent(order._value, percent, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def set_take_profit(self, order: IOrder, limit_price: float, comment: str = "") -> IOrder:
        """Sets a take-profit order at a specified price to close a position when the price is reached.            The order of the open position to which the take-profit is applied.      The price at which the take-profit order is set.      Optional comment for the order, providing additional information or notes.      The updated order with the take-profit applied."""
        result = self._value.SetTakeProfit(order._value, limit_price, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def set_take_profit_ticks(self, order: IOrder, ticks: int, comment: str = "") -> IOrder:
        """Sets a take-profit order on an open position based on a specified number of ticks from the entry price.            The order of the open position to which the take-profit is applied.      The number of ticks away from the entry price to place the take-profit.      Optional comment for the order, providing additional information or notes.      The updated order with the take-profit applied."""
        result = self._value.SetTakeProfitTicks(order._value, ticks, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def set_take_profit_percent(self, order: IOrder, percent: float, comment: str = "") -> IOrder:
        """Sets a take-profit order on an open position based on a specified percentage from the entry price.            The order of the open position to which the take-profit is applied.      The percentage away from the entry price to place the take-profit.      Optional comment for the order, providing additional information or notes.      The updated order with the take-profit applied."""
        result = self._value.SetTakeProfitPercent(order._value, percent, comment)
        from tbapi.api.interfaces.orders.iorder import IOrder
        return IOrder(_existing=result)
  
    @abstractmethod
    def modify_order(self, order: IOrder, quantity: float, stop_price: float | None, limit_price: float | None, time_in_force: TimeInForce = TimeInForce.Day) -> None:
        """Modifies an existing order.            The order of open position.      Order quantity.      Stop price if applicable.      Limit price if applicable.      Order duration. Defaults to Day."""
        result = self._value.ModifyOrder(order._value, quantity, stop_price, limit_price, _TimeInForce(time_in_force.value if hasattr(time_in_force, 'value') else int(time_in_force)))
        return result
  
    @abstractmethod
    def cancel_order(self, order: IOrder, comment: str = "", cancel_silently: bool = False) -> None:
        """Cancels the specified order with an optional comment.      The order to cancel.      Optional comment for the order.      Indicates if the cancellation should be silent."""
        result = self._value.CancelOrder(order._value, comment, cancel_silently)
        return result
  
    @abstractmethod
    def close_position(self, comment: str = "") -> None:
        """Closes the entire position with an optional comment.            Optional comment for the order."""
        result = self._value.ClosePosition(comment)
        return result
  
    @abstractmethod
    def get_order_expected_price(self, order: IOrder) -> float:
        """Gets estimated fill price of pending order.            The pending order."""
        result = self._value.GetOrderExpectedPrice(order._value)
        return result
  

