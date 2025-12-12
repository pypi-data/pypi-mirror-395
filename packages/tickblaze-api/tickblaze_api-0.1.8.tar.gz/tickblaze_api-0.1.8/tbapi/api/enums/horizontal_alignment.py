

from enum import Enum
from Tickblaze.Scripts.Api.Enums import HorizontalAlignment as _HorizontalAlignment

class HorizontalAlignment(Enum):
    """Specifies the horizontal aligment."""

    Left = 0
    """Aligns content to the left."""

    Center = 1
    """Aligns content to the center."""

    Right = 2
    """Aligns content to the right."""
