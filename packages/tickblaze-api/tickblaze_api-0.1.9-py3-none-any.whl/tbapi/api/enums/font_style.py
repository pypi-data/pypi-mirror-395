

from enum import Enum
from Tickblaze.Scripts.Api.Enums import FontStyle as _FontStyle

class FontStyle(Enum):
    """Specifies the style of a font."""

    Italic = 0
    """Italic text style."""

    Normal = 1
    """Normal text style."""

    Oblique = 2
    """Oblique text style."""
