

from enum import Enum
from Tickblaze.Scripts.Api.Enums import OrderStatus as _OrderStatus

class OrderStatus(Enum):
    """Specifies the status of an order."""

    Unknown = 0
    """Status is unknown."""

    Pending = 1
    """Order is pending."""

    Executed = 2
    """Order has been executed."""

    Cancelled = 3
    """Order has been cancelled."""
