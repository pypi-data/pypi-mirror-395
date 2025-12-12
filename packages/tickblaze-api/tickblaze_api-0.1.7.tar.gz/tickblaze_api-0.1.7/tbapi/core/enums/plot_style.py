

from enum import Enum
from Tickblaze.Core.Enums import PlotStyle as _PlotStyle

class PlotStyle(Enum):
    """Specifies the style of a plot."""

    Histogram = 105
    """Histogram plot style."""

    Cross = 106
    """Cross plot style."""

    Dot = 107
    """Dot plot style."""

    Hash = 108
    """Hash plot style."""

    Line = 109
    """Line plot style."""

    Square = 110
    """Square plot style."""

    Stair = 111
    """Stair plot style."""

    TriangleDown = 112
    """Triangle down plot style."""

    TriangleLeft = 113
    """Triangle left plot style."""

    TriangleRight = 114
    """Triangle right plot style."""

    TriangleUp = 115
    """Triangle up plot style."""
