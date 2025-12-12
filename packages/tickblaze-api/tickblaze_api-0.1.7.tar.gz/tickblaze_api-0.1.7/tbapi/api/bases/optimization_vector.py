






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import OptimizationVector as _OptimizationVector
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_OptimizationVector)
class OptimizationVector():

    @overload
    @staticmethod
    def new() -> "OptimizationVector":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for OptimizationVector. Use overloads for IDE type hints."""
        return OptimizationVector(*args, **kwargs)

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
    def values(self) -> IReadOnlyList:
        val = self._value.Values
        return val
    @values.setter
    def values(self, val: IReadOnlyList):
        tmp = self._value
        tmp.Values = val
        self._value = tmp
    @property
    def score(self) -> float:
        val = self._value.Score
        return val
    @score.setter
    def score(self, val: float):
        tmp = self._value
        tmp.Score = val
        self._value = tmp
    @property
    def is_processed(self) -> bool:
        val = self._value.IsProcessed
        return val
    @is_processed.setter
    def is_processed(self, val: bool):
        tmp = self._value
        tmp.IsProcessed = val
        self._value = tmp



