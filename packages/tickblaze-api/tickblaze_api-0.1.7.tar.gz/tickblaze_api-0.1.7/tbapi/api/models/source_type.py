

from enum import Enum

class SourceType(Enum):
    """Defines the different source types for the bar."""

    Ask = 0
    """The ask price data."""

    Bid = 1
    """The bid price data."""

    Trade = 2
    """Trade data."""

    Minute = 3
    """Minute-based price data."""

    Day = 4
    """Daily price data."""

    Level2 = 5
    """Level 2 market data."""
