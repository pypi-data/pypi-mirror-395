




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import ISize as _ISize
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_interface(_ISize)
class ISize():
    """Defines properties for the size, including height and width."""

    @property
    def height(self) -> float:
        """The height of the size."""
        val = self._value.Height
        return val
    @property
    def width(self) -> float:
        """The width of the size."""
        val = self._value.Width
        return val


