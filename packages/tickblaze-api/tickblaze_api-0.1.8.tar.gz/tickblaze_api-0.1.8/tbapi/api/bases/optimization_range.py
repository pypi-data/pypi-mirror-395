






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import OptimizationRange as _OptimizationRange
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_OptimizationRange)
class OptimizationRange():

    @overload
    @staticmethod
    def new(ValueStep: Any, ValueLow: Any, ValueHigh: Any) -> "OptimizationRange":
        """Constructor overload with arguments: ValueStep, ValueLow, ValueHigh"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for OptimizationRange. Use overloads for IDE type hints."""
        return OptimizationRange(*args, **kwargs)

    @property
    def value_step(self) -> Any:
        val = self._value.ValueStep
        return val
    @value_step.setter
    def value_step(self, val: Any):
        tmp = self._value
        tmp.ValueStep = val
        self._value = tmp
    @property
    def value_low(self) -> Any:
        val = self._value.ValueLow
        return val
    @value_low.setter
    def value_low(self, val: Any):
        tmp = self._value
        tmp.ValueLow = val
        self._value = tmp
    @property
    def value_high(self) -> Any:
        val = self._value.ValueHigh
        return val
    @value_high.setter
    def value_high(self, val: Any):
        tmp = self._value
        tmp.ValueHigh = val
        self._value = tmp

    def contains(self, convertible: Any) -> bool:
        result = self._value.Contains(convertible)
        return result
  


