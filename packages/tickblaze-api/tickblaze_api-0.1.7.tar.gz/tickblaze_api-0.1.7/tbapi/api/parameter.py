






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api import Parameter as _Parameter
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_Parameter)
class Parameter():
    """Represents a parameter with associated attributes, value, and an optional numeric range and property reference."""

    @overload
    @staticmethod
    def new() -> "Parameter":
        """Constructor overload with arguments: """
        ...
    @overload
    @staticmethod
    def new(obj: Any, property: PropertyInfo, attributes: ParameterAttribute) -> "Parameter":
        """Constructor overload with arguments: obj, property, attributes"""
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Parameter. Use overloads for IDE type hints."""
        return Parameter(*args, **kwargs)

    @property
    def attributes(self) -> ParameterAttribute:
        """The attributes associated with the parameter."""
        val = self._value.Attributes
        return val
    @property
    def numeric_range(self) -> NumericRangeAttribute:
        """The optional numeric range attribute for the parameter."""
        val = self._value.NumericRange
        return val
    @property
    def __property__(self) -> PropertyInfo:
        """The property information of the parameter if available."""
        val = self._value.Property
        return val
    @property
    def is_enabled(self) -> bool:
        """Gets or sets a value indicating whether this element is enabled in the user interface (UI)."""
        val = self._value.IsEnabled
        return val
    @is_enabled.setter
    def is_enabled(self, val: bool):
        tmp = self._value
        tmp.IsEnabled = val
        self._value = tmp
    @property
    def is_visible(self) -> bool:
        """Gets or sets a value indicating whether this element is visible in the user interface (UI)."""
        val = self._value.IsVisible
        return val
    @is_visible.setter
    def is_visible(self, val: bool):
        tmp = self._value
        tmp.IsVisible = val
        self._value = tmp
    @property
    def is_optimizable(self) -> bool:
        """Gets or sets a value indicating whether this element is optimizable."""
        val = self._value.IsOptimizable
        return val
    @is_optimizable.setter
    def is_optimizable(self, val: bool):
        tmp = self._value
        tmp.IsOptimizable = val
        self._value = tmp
    @property
    def value(self) -> Any:
        """The value of the parameter."""
        val = self._value.Value
        return val
    @value.setter
    def value(self, val: Any):
        tmp = self._value
        tmp.Value = val
        self._value = tmp



