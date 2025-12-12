

from enum import Enum
from Tickblaze.Scripts.Api import BarSeriesEvent as _BarSeriesEvent

class BarSeriesEvent(Enum):

    BarUpdated = 0

    BarCompleted = 1
