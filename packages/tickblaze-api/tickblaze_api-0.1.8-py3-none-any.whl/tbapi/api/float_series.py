






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Python.Scripts.Api import FloatSeries as _FloatSeries
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.series import Series

@tb_class(_FloatSeries)
class FloatSeries(Series):
    """Represents a series of float values"""

    @overload
    @staticmethod
    def new() -> "FloatSeries":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for FloatSeries. Use overloads for IDE type hints."""
        return FloatSeries(*args, **kwargs)




