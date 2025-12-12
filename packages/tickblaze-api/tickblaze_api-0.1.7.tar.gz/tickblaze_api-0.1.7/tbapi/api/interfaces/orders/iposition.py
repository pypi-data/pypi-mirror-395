




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IPosition as _IPosition
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.orders.iposition_base import IPositionBase

@tb_interface(_IPosition)
class IPosition(IPositionBase):
    """Represents a trading position in the market, providing details about its state, pricing, and quantity."""

    @property
    def trades(self) -> list[Any]:
        val = self._value.Trades
        return val


