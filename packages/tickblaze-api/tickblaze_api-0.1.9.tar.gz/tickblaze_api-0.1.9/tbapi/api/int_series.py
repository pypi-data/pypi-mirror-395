






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Python.Scripts.Api import IntSeries as _IntSeries
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.series import Series

@tb_class(_IntSeries)
class IntSeries(Series):
    """Represents a series of int values"""

    @overload
    @staticmethod
    def new() -> "IntSeries":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for IntSeries. Use overloads for IDE type hints."""
        return IntSeries(*args, **kwargs)




