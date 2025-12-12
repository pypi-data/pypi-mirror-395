






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import DataSeries as _DataSeries
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.series import Series

@tb_class(_DataSeries)
class DataSeries(Series):
    """Represents a series of double values for data points, with a default value of ."""

    @overload
    @staticmethod
    def new() -> "DataSeries":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for DataSeries. Use overloads for IDE type hints."""
        return DataSeries(*args, **kwargs)




