






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api import IndexedDictionary as _IndexedDictionary
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_IndexedDictionary)
class IndexedDictionary():
    """A dictionary with an indexer that allows accessing elements by their index in addition to the key.            The type of the key in the dictionary.      The type of the value in the dictionary."""

    @overload
    @staticmethod
    def new() -> "IndexedDictionary":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for IndexedDictionary. Use overloads for IDE type hints."""
        return IndexedDictionary(*args, **kwargs)




    def __getitem__(self, index: int) -> Any:
        result = self._value[index]
        return result

    def __setitem__(self, index: int, value: Any):
        tmp = value
        self._value[index] = tmp
