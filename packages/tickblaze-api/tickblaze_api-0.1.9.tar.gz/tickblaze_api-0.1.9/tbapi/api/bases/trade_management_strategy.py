






from __future__ import annotations
from typing import TYPE_CHECKING
import clr
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import TradeManagementStrategy as _TradeManagementStrategy
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.trading_script import TradingScript
from tbapi.api.interfaces.orders.iorder import IOrder

@tb_interface(_TradeManagementStrategy)
class TradeManagementStrategy(TradingScript):
    """A base class for trade management strategies, providing methods to control the activation and deactivation of the strategy."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for TradeManagementStrategy. Use overloads for IDE type hints."""
        return TradeManagementStrategy(*args, **kwargs)

    @property
    def is_active(self) -> bool:
        """Indicates whether the trade management strategy is active."""
        val = self._value.IsActive
        return val


    @clr.clrmethod(None, [Any])
    def on_entry_order(self, order: IOrder) -> None:
        """Handles the entry order when it is placed.            The entry order for the trade."""
        ...

    @clr.clrmethod(None, [None])
    def on_shutdown(self) -> None:
        """Handles shutdown operations when the strategy is stopped or the script is terminated."""
        ...


