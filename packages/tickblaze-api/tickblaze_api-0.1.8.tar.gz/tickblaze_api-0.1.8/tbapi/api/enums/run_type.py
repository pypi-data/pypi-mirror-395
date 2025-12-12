

from enum import Enum
from Tickblaze.Scripts.Api.Enums import RunType as _RunType

class RunType(Enum):

    Backtest = 0

    Optimization = 1

    Live = 2
