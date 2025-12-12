

from enum import Enum
from Tickblaze.Scripts.Api.Enums import TimeInForce as _TimeInForce

class TimeInForce(Enum):
    """Specifies the time in force for an order."""

    Day = 0
    """Order is valid for the current day only."""

    GoodTillCancel = 1
    """Order remains active until canceled."""

    FillOrKill = 2
    """Order must be filled immediately or canceled."""

    ImmediateOrCancel = 3
    """Order must be filled immediately, partially or fully, or canceled."""
