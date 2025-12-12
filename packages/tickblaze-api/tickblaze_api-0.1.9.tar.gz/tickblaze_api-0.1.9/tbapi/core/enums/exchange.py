

from enum import Enum
from Tickblaze.Core.Enums import Exchange as _Exchange

class Exchange(Enum):

    Unknown = 0

    AMEX = 1

    ARCA = 2

    BATS = 3

    CBOE = 4

    CBOT = 5

    CME = 6

    COMEX = 7

    EUREX = 8

    NYSE = 9

    NYMEX = 10

    NASDAQ = 11

    PINK = 12
    """A catchall for all pink sheet stock exchanges"""
