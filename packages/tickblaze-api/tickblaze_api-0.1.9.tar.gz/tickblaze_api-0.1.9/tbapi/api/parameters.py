






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api import Parameters as _Parameters
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.indexed_dictionary import IndexedDictionary

@tb_class(_Parameters)
class Parameters(IndexedDictionary):
    """Represents a collection of parameters, either from an object or a dictionary of key-value pairs."""

    @overload
    @staticmethod
    def new(obj: Any) -> "Parameters":
        """Constructor overload with arguments: obj"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Parameters. Use overloads for IDE type hints."""
        return Parameters(*args, **kwargs)




