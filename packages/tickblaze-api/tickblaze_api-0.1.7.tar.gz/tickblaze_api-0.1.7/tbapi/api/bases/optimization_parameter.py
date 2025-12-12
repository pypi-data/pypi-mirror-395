






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import OptimizationParameter as _OptimizationParameter
from typing import Any, overload
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from tbapi.api.bases.optimization_range import OptimizationRange

@tb_class(_OptimizationParameter)
class OptimizationParameter():

    @overload
    @staticmethod
    def new(Index: int, PropertyName: str, Type: Type, Range: OptimizationRange = None, AllowedValues: list[Any] = None) -> "OptimizationParameter":
        """Constructor overload with arguments: Index, PropertyName, Type, Range, AllowedValues"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for OptimizationParameter. Use overloads for IDE type hints."""
        return OptimizationParameter(*args, **kwargs)

    @property
    def index(self) -> int:
        val = self._value.Index
        return val
    @index.setter
    def index(self, val: int):
        tmp = self._value
        tmp.Index = val
        self._value = tmp
    @property
    def property_name(self) -> str:
        val = self._value.PropertyName
        return val
    @property_name.setter
    def property_name(self, val: str):
        tmp = self._value
        tmp.PropertyName = val
        self._value = tmp
    @property
    def type(self) -> Type:
        val = self._value.Type
        return val
    @type.setter
    def type(self, val: Type):
        tmp = self._value
        tmp.Type = val
        self._value = tmp
    @property
    def range(self) -> OptimizationRange:
        from tbapi.api.bases.optimization_range import OptimizationRange
        val = self._value.Range
        return OptimizationRange(_existing=val)
    @range.setter
    def range(self, val: OptimizationRange):
        tmp = self._value
        tmp.Range = val._value
        self._value = tmp
    @property
    def allowed_values(self) -> list[Any]:
        val = self._value.AllowedValues
        return val
    @allowed_values.setter
    def allowed_values(self, val: list[Any]):
        tmp = self._value
        tmp.AllowedValues = val
        self._value = tmp



