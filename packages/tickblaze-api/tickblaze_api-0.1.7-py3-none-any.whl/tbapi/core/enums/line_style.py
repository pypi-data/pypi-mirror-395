

from enum import Enum
from Tickblaze.Core.Enums import LineStyle as _LineStyle

class LineStyle(Enum):
    """Specifies the style of a line."""

    Solid = 100
    """Solid line."""

    Dash = 101
    """Dashed line."""

    Dot = 102
    """Dotted line."""

    DashDot = 103
    """Dash-dot line."""

    DashDotDot = 104
    """Dash-dot-dot line."""
