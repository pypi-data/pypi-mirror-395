






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api import OptimizationParameters as _OptimizationParameters
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.indexed_dictionary import IndexedDictionary
if TYPE_CHECKING:
    from tbapi.api.bases.script import Script

@tb_class(_OptimizationParameters)
class OptimizationParameters(IndexedDictionary):
    """Represents a collection of parameters, either from an object or a dictionary of key-value pairs."""

    @overload
    @staticmethod
    def new(script: Script, optimizedParameters: list[OptimizationParameter]) -> "OptimizationParameters":
        """Constructor overload with arguments: script, optimizedParameters"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for OptimizationParameters. Use overloads for IDE type hints."""
        return OptimizationParameters(*args, **kwargs)


    def contains_true(self, parameter_name: str) -> bool:
        result = self._value.ContainsTrue(parameter_name)
        return result
  
    def contains_false(self, parameter_name: str) -> bool:
        result = self._value.ContainsFalse(parameter_name)
        return result
  


