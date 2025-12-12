

from enum import Enum
from Tickblaze.Scripts.Api.Enums import OrderDirection as _OrderDirection

class OrderDirection(Enum):
    """Specifies the direction of an order."""

    Long = 0
    """Long position direction."""

    Short = 1
    """Short position direction."""
