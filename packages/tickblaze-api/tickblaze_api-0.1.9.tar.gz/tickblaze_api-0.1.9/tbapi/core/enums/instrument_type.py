

from enum import Enum
from Tickblaze.Core.Enums import InstrumentType as _InstrumentType

class InstrumentType(Enum):
    """Represents the instrument types."""

    Bond = 100

    CFD = 101

    ETF = 102

    Forex = 103

    Future = 104

    Index = 105

    MutualFund = 106

    Option = 107

    Stock = 108

    CryptoCurrency = 109

    Unknown = 110
