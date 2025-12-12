

from enum import Enum

class SourceDataType(Enum):
    """Enumerates the possible types of source data used to create bars."""

    Tick = 0
    """Source data is based on tick data."""

    Minute = 1
    """Source data is based on minute data."""

    Daily = 2
    """Source data is based on daily data."""
