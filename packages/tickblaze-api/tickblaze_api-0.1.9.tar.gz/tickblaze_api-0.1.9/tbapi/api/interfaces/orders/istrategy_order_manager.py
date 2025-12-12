




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IStrategyOrderManager as _IStrategyOrderManager
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.orders.iorder_manager import IOrderManager

@tb_interface(_IStrategyOrderManager)
class IStrategyOrderManager(IOrderManager):


    @abstractmethod
    def flatten(self, comment: str = "") -> None:
        """Closes positions and cancel pending orders.            Optional comment for the orders and cancellations.            Will also automatically flatten incoming fills appearing after the call      is made. This behavior is automatically disabled when a new entry is made."""
        result = self._value.Flatten(comment)
        return result
  
    @abstractmethod
    def cancel_pending_orders(self, include_attached_orders: bool, comment: str = "") -> None:
        """Cancels all pending orders            True if attached orders should be included      Comment to place on order"""
        result = self._value.CancelPendingOrders(include_attached_orders, comment)
        return result
  

