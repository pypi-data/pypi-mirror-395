

from enum import Enum
from Tickblaze.Scripts.Api.Adapters import AlertType as _AlertType

class AlertType(Enum):
    """Enum representing different types of alerts."""

    Good = 0
    """Represents a good alert."""

    Bad = 1
    """Represents a bad alert."""

    Neutral = 2
    """Represents a neutral alert."""

    Important = 3
    """Represents an important alert."""
