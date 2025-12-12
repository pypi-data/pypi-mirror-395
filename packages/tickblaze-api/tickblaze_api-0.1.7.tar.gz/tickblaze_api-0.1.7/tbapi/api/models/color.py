





from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Color as _Color
from typing import Any, overload

@tb_class(_Color)
class Color():
    """Represents a color with alpha, red, green, and blue values.            The alpha value of the color.      The red value of the color.      The green value of the color.      The blue value of the color."""

    @overload
    @staticmethod
    def new(a: int, r: int, g: int, b: int) -> "Color":
        """Constructor overload with arguments: a, r, g, b"""
        ...
    @overload
    @staticmethod
    def new() -> "Color":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Color. Use overloads for IDE type hints."""
        return Color(*args, **kwargs)

    @property
    def a(self) -> int:
        """The alpha value of the color."""
        val = self._value.A
        return val
    @a.setter
    def a(self, val: int):
        tmp = self._value
        tmp.A = val
        self._value = tmp
    @property
    def r(self) -> int:
        """The red value of the color."""
        val = self._value.R
        return val
    @r.setter
    def r(self, val: int):
        tmp = self._value
        tmp.R = val
        self._value = tmp
    @property
    def g(self) -> int:
        """The green value of the color."""
        val = self._value.G
        return val
    @g.setter
    def g(self, val: int):
        tmp = self._value
        tmp.G = val
        self._value = tmp
    @property
    def b(self) -> int:
        """The blue value of the color."""
        val = self._value.B
        return val
    @b.setter
    def b(self, val: int):
        tmp = self._value
        tmp.B = val
        self._value = tmp
    @property
    def hex(self) -> str:
        """The HEX value of the color."""
        val = self._value.Hex
        return val

    def to_rgb_hex(self) -> str:
        """Converts the color to its RGB hex representation.            A string representing the RGB hex value of the color."""
        result = self._value.ToRgbHex()
        return result
  
    def to_argb_hex(self) -> str:
        """Converts the color to its ARGB hex representation.            A string representing the ARGB hex value of the color."""
        result = self._value.ToArgbHex()
        return result
  
    def to_rgba_hex(self) -> str:
        """Converts the color to its RGBA hex representation.            A string representing the RGBA hex value of the color."""
        result = self._value.ToRgbaHex()
        return result
  
    @staticmethod
    def from_rgb(r: int, g: int, b: int) -> Color:
        """Creates a color from RGB values.            Red value (0-255).      Green value (0-255).      Blue value (0-255).      A new  instance with the specified RGB values."""
        result = _Color.FromRgb(r, g, b)
        from tbapi.api.models.color import Color
        return Color(_existing=result)
  
    @staticmethod
    def from_rgba(r: int, g: int, b: int, a: int) -> Color:
        """Creates a color from RGBA values.            Red value (0-255).      Green value (0-255).      Blue value (0-255).      Alpha value (0-255).      A new  instance with the specified RGBA values."""
        result = _Color.FromRgba(r, g, b, a)
        from tbapi.api.models.color import Color
        return Color(_existing=result)
  
    @staticmethod
    def from_argb(a: int, r: int, g: int, b: int) -> Color:
        """Creates a color from ARGB values.            Alpha value (0-255).      Red value (0-255).      Green value (0-255).      Blue value (0-255).      A new  instance with the specified ARGB values."""
        result = _Color.FromArgb(a, r, g, b)
        from tbapi.api.models.color import Color
        return Color(_existing=result)
  
    @staticmethod
    def try_parse_hex(hex: str, color: Color) -> bool:
        """Attempts to parse a  from a given HEX string.            The HEX string to parse.      The parsed color if the operation is successful.      True if the parsing was successful; otherwise, false."""
        result = _Color.TryParseHex(hex, color._value)
        return result
  
    @staticmethod
    def try_parse_from_name(name: str, color: Color) -> bool:
        """Attempts to parse a  from a given name.            The name of the color to be parsed.      The parsed color if the operation is successful.      True if the parsing was successful; otherwise, false."""
        result = _Color.TryParseFromName(name, color._value)
        return result
  
    @staticmethod
    def from_name(color_name: str, fallback_color_name: str = None) -> Color:
        """Creates a color from the specified name.            The name of the color.      The fallback color name if the first is not found.      A new  instance corresponding to the name."""
        result = _Color.FromName(color_name, fallback_color_name)
        from tbapi.api.models.color import Color
        return Color(_existing=result)
  
    @staticmethod
    def try_parse(hex_or_name: str, fallback_color_name: str, color: Color) -> bool:
        """Tries to parse a color from a hex string or color name.            The hex string or color name.      The fallback color name if parsing fails.      The resulting color.      True if the parsing was successful; otherwise, false."""
        result = _Color.TryParse(hex_or_name, fallback_color_name, color._value)
        return result
  
    @staticmethod
    def from_drawing_color(color: Color) -> Color:
        """Converts a  to a .            The  instance.      A new  instance representing the system drawing color."""
        result = _Color.FromDrawingColor(color)
        from tbapi.api.models.color import Color
        return Color(_existing=result)
  

    Empty: 'Color' = None
    Transparent: 'Color' = None
    White: 'Color' = None
    LightGray: 'Color' = None
    Silver: 'Color' = None
    CoolGray: 'Color' = None
    SteelGray: 'Color' = None
    Gunmetal: 'Color' = None
    Gray: 'Color' = None
    DimGray: 'Color' = None
    DarkGray: 'Color' = None
    Black: 'Color' = None
    Red: 'Color' = None
    Orange: 'Color' = None
    Yellow: 'Color' = None
    Green: 'Color' = None
    TealGreen: 'Color' = None
    Cyan: 'Color' = None
    Blue: 'Color' = None
    DeepPurple: 'Color' = None
    Purple: 'Color' = None
    Pink: 'Color' = None

Color.Empty = Color(_existing=_Color.Empty)  # type: Color
Color.Transparent = Color(_existing=_Color.Transparent)  # type: Color
Color.White = Color(_existing=_Color.White)  # type: Color
Color.LightGray = Color(_existing=_Color.LightGray)  # type: Color
Color.Silver = Color(_existing=_Color.Silver)  # type: Color
Color.CoolGray = Color(_existing=_Color.CoolGray)  # type: Color
Color.SteelGray = Color(_existing=_Color.SteelGray)  # type: Color
Color.Gunmetal = Color(_existing=_Color.Gunmetal)  # type: Color
Color.Gray = Color(_existing=_Color.Gray)  # type: Color
Color.DimGray = Color(_existing=_Color.DimGray)  # type: Color
Color.DarkGray = Color(_existing=_Color.DarkGray)  # type: Color
Color.Black = Color(_existing=_Color.Black)  # type: Color
Color.Red = Color(_existing=_Color.Red)  # type: Color
Color.Orange = Color(_existing=_Color.Orange)  # type: Color
Color.Yellow = Color(_existing=_Color.Yellow)  # type: Color
Color.Green = Color(_existing=_Color.Green)  # type: Color
Color.TealGreen = Color(_existing=_Color.TealGreen)  # type: Color
Color.Cyan = Color(_existing=_Color.Cyan)  # type: Color
Color.Blue = Color(_existing=_Color.Blue)  # type: Color
Color.DeepPurple = Color(_existing=_Color.DeepPurple)  # type: Color
Color.Purple = Color(_existing=_Color.Purple)  # type: Color
Color.Pink = Color(_existing=_Color.Pink)  # type: Color
