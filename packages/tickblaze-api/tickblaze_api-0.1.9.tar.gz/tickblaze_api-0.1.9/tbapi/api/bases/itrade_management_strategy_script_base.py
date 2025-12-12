




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import ITradeManagementStrategyScriptBase as _ITradeManagementStrategyScriptBase
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.orders.iorder_manager import IOrderManager

@tb_interface(_ITradeManagementStrategyScriptBase)
class ITradeManagementStrategyScriptBase(IOrderManager):
    """Interface for a trade management strategy script base, providing methods to start and stop the strategy."""

    @property
    def is_active(self) -> bool:
        """Indicates whether the strategy is currently active."""
        val = self._value.IsActive
        return val

    @abstractmethod
    def start(self) -> None:
        """Starts the strategy."""
        result = self._value.Start()
        return result
  
    @abstractmethod
    def stop(self) -> None:
        """Stops the strategy."""
        result = self._value.Stop()
        return result
  

