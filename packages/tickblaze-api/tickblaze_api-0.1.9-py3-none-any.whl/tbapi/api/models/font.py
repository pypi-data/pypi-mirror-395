






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Font as _Font
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.enums.font_style import FontStyle
from tbapi.api.enums.font_weight import FontWeight
from Tickblaze.Scripts.Api.Enums import FontStyle as _FontStyle
from Tickblaze.Scripts.Api.Enums import FontWeight as _FontWeight

@tb_class(_Font)
class Font():
    """Represents a font with a family name, size, style, and weight."""

    @overload
    @staticmethod
    def new(familyName: str = "Segoe UI", size: int = 12, style: FontStyle = FontStyle.Normal, weight: FontWeight = FontWeight.Regular) -> "Font":
        """Constructor overload with arguments: familyName, size, style, weight"""
        ...
    @overload
    @staticmethod
    def new() -> "Font":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Font. Use overloads for IDE type hints."""
        return Font(*args, **kwargs)

    @property
    def family_name(self) -> str:
        """Gets or sets the font family name."""
        val = self._value.FamilyName
        return val
    @family_name.setter
    def family_name(self, val: str):
        tmp = self._value
        tmp.FamilyName = val
        self._value = tmp
    @property
    def size(self) -> int:
        """Gets or sets the font size."""
        val = self._value.Size
        return val
    @size.setter
    def size(self, val: int):
        tmp = self._value
        tmp.Size = val
        self._value = tmp
    @property
    def style(self) -> FontStyle:
        """Gets or sets the font style."""
        val = int(self._value.Style)
        return FontStyle(val)
    @style.setter
    def style(self, val: FontStyle):
        tmp = self._value
        tmp.Style = _FontStyle(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def weight(self) -> FontWeight:
        """Gets or sets the font weight."""
        val = int(self._value.Weight)
        return FontWeight(val)
    @weight.setter
    def weight(self, val: FontWeight):
        tmp = self._value
        tmp.Weight = _FontWeight(val.value if hasattr(val, "value") else int(val))
        self._value = tmp



