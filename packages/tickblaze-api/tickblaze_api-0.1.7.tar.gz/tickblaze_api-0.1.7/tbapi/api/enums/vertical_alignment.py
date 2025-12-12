

from enum import Enum
from Tickblaze.Scripts.Api.Enums import VerticalAlignment as _VerticalAlignment

class VerticalAlignment(Enum):
    """Specifies the vertical alignment."""

    Top = 0
    """Aligns the content to the top."""

    Center = 1
    """Aligns the content to the center."""

    Bottom = 2
    """Aligns the content to the bottom."""
