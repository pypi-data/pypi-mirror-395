




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces.Orders import IPositions as _IPositions
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.orders.iposition import IPosition

@tb_interface(_IPositions)
class IPositions():
    """Represents a collection of positions."""

    @property
    def count(self) -> int:
        """Gets the number of positions in the collection."""
        val = self._value.Count
        return val


    def __getitem__(self, index: int) -> Any:
        result = self._value[index]
        return IPosition(_existing=result)
