






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api import Series as _Series
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.iseries import ISeries

@tb_class(_Series)
class Series(ISeries):
    """Represents a series of values of type .      Provides methods to append, access, and enumerate over the values in the series.            The type of the values in the series."""

    @overload
    @staticmethod
    def new() -> "Series":
        """Constructor overload with arguments: """
        ...
    @overload
    @staticmethod
    def new(defaultValue: Any) -> "Series":
        """Constructor overload with arguments: defaultValue"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Series. Use overloads for IDE type hints."""
        return Series(*args, **kwargs)

    @property
    def count(self) -> int:
        """Gets the count of values in the series."""
        val = self._value.Count
        return val

    def get_enumerator(self) -> IEnumerator:
        """Gets an enumerator for the series values.            An enumerator for the series values."""
        result = self._value.GetEnumerator()
        return result
  


    def __getitem__(self, index: int) -> Any:
        result = self._value[index]
        return result

    def __setitem__(self, index: int, value: Any):
        tmp = value
        self._value[index] = tmp
