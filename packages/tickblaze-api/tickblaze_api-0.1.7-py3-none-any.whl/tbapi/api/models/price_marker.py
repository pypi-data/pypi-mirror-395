






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import PriceMarker as _PriceMarker
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_PriceMarker)
class PriceMarker():
    """Represents settings for displaying a price marker on the Y-axis"""

    @overload
    @staticmethod
    def new(formatter: Func = None) -> "PriceMarker":
        """Constructor overload with arguments: formatter"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for PriceMarker. Use overloads for IDE type hints."""
        return PriceMarker(*args, **kwargs)

    @property
    def formatter(self) -> Func:
        """Gets a function that formats the displayed value.      The function takes a bar index as input and returns a formatted string."""
        val = self._value.Formatter
        return val
    @formatter.setter
    def formatter(self, val: Func):
        tmp = self._value
        tmp.Formatter = val
        self._value = tmp



