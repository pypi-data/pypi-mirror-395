

from enum import Enum
from Tickblaze.Scripts.Api.Enums import OrderAction as _OrderAction

class OrderAction(Enum):
    """Specifies the action of an order."""

    Buy = 0
    """Buy order action."""

    Sell = 1
    """Sell order action."""

    SellShort = 2
    """Sell short order action."""

    BuyToCover = 3
    """Buy to cover order action."""
