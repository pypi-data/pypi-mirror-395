

from enum import Enum
from Tickblaze.Scripts.Api.Enums import PositionStatus as _PositionStatus

class PositionStatus(Enum):
    """Specifies the status of a position."""

    Open = 0
    """Open position."""

    Close = 1
    """Closed position."""
