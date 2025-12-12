






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Stroke as _Stroke
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.core.enums.line_style import LineStyle
from tbapi.api.models.stroke_editable_fields import StrokeEditableFields
from Tickblaze.Core.Enums import LineStyle as _LineStyle
from Tickblaze.Scripts.Api.Models import StrokeEditableFields as _StrokeEditableFields
if TYPE_CHECKING:
    from tbapi.api.models.color import Color

@tb_class(_Stroke)
class Stroke():
    """Represents a line style with color, dash style, and thickness."""

    @overload
    @staticmethod
    def new() -> "Stroke":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Stroke. Use overloads for IDE type hints."""
        return Stroke(*args, **kwargs)

    @property
    def color(self) -> Color:
        """The color of the stroke."""
        from tbapi.api.models.color import Color
        val = self._value.Color
        return Color(_existing=val)
    @color.setter
    def color(self, val: Color):
        tmp = self._value
        tmp.Color = val._value
        self._value = tmp
    @property
    def line_style(self) -> LineStyle:
        """The line style for the stroke."""
        val = int(self._value.LineStyle)
        return LineStyle(val)
    @line_style.setter
    def line_style(self, val: LineStyle):
        tmp = self._value
        tmp.LineStyle = _LineStyle(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def thickness(self) -> int:
        """The thickness of the stroke."""
        val = self._value.Thickness
        return val
    @thickness.setter
    def thickness(self, val: int):
        tmp = self._value
        tmp.Thickness = val
        self._value = tmp
    @property
    def is_visible(self) -> bool:
        """Indicates whether the stroke is visible"""
        val = self._value.IsVisible
        return val
    @is_visible.setter
    def is_visible(self, val: bool):
        tmp = self._value
        tmp.IsVisible = val
        self._value = tmp
    @property
    def editable_fields(self) -> StrokeEditableFields:
        val = int(self._value.EditableFields)
        return StrokeEditableFields(val)
    @editable_fields.setter
    def editable_fields(self, val: StrokeEditableFields):
        tmp = self._value
        tmp.EditableFields = _StrokeEditableFields(val.value if hasattr(val, "value") else int(val))
        self._value = tmp



