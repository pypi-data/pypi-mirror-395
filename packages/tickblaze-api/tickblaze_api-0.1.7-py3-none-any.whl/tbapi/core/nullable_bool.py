

from enum import Enum
from Tickblaze.Core import NullableBool as _NullableBool

class NullableBool(Enum):

    Null = 0

    __True__ = 1

    __False__ = 2
