

from enum import Enum
from Tickblaze.Scripts.Api.Enums import OrderType as _OrderType

class OrderType(Enum):
    """Specifies the type of an order."""

    Market = 0
    """Market order type."""

    Limit = 1
    """Limit order type."""

    Stop = 2
    """Stop order type."""

    StopLimit = 3
    """Stop limit order type."""
