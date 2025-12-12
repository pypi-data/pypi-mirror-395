




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import ITrade as _ITrade
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.orders.iposition_base import IPositionBase
if TYPE_CHECKING:
    from tbapi.api.interfaces.orders.iorder import IOrder

@tb_interface(_ITrade)
class ITrade(IPositionBase):

    @property
    def entry_order(self) -> IOrder:
        from tbapi.api.interfaces.orders.iorder import IOrder
        val = self._value.EntryOrder
        return IOrder(_existing=val)
    @property
    def exit_order(self) -> IOrder:
        from tbapi.api.interfaces.orders.iorder import IOrder
        val = self._value.ExitOrder
        return IOrder(_existing=val)


