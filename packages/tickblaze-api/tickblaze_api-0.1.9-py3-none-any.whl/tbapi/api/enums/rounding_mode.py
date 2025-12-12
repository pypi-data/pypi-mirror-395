

from enum import Enum
from Tickblaze.Scripts.Api.Enums import RoundingMode as _RoundingMode

class RoundingMode(Enum):
    """Specifies the mode of rounding."""

    ToNearest = 0
    """Rounds to the nearest value."""

    Up = 1
    """Rounds up."""

    Down = 2
    """Rounds down."""
