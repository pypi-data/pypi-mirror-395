

from enum import Enum

class PeriodType(Enum):
    """Defines the different period types for the bar."""

    __None__ = 0
    """No period type specified."""

    Day = 1
    """The daily period."""

    Week = 2
    """The weekly period."""

    Month = 3
    """The monthly period."""

    Year = 4
    """The yearly period."""

    Second = 5
    """The period based on seconds."""

    Minute = 6
    """The period based on minutes."""

    Level2 = 7
    """The Level 2 period, typically used for market depth data."""

    Tick = 8
    """The tick-based period."""

    Range = 9
    """The range-based period."""

    Volume = 10
    """The volume-based period."""

    Momentum = 11
    """The momentum-based period."""

    HeikinAshi = 12
    """The Heikin Ashi period, a type of candlestick chart."""

    Renko = 13
    """The Renko period, another type of chart that ignores time."""

    Kagi = 14
    """The Kagi chart period."""

    LineBreak = 15
    """The Line Break chart period."""

    PointAndFigureClose = 16
    """The Point and Figure chart with close-based periods."""

    PointAndFigureHighLow = 17
    """The Point and Figure chart with high-low periods."""

    BidAsk = 18
    """The bid-ask period."""

    Custom = 19
    """The custom period type defined by the user."""
