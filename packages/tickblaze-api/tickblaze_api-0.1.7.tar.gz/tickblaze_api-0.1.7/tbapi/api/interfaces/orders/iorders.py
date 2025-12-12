




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IOrders as _IOrders
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.orders.iorder import IOrder

@tb_interface(_IOrders)
class IOrders():
    """Represents a collection of orders."""

    @property
    def count(self) -> int:
        """Gets the total number of orders in the collection."""
        val = self._value.Count
        return val


    def __getitem__(self, index: int) -> Any:
        result = self._value[index]
        return IOrder(_existing=result)
