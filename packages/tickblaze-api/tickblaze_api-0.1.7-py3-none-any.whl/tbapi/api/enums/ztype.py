

from enum import Enum
from Tickblaze.Scripts.Api.Enums import ZType as _ZType

class ZType(Enum):

    AboveChart = 0

    BelowChart = 1

    AboveAndBelowChart = 2
