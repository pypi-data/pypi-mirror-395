

from enum import Enum
from Tickblaze.Core.Enums import ContractType as _ContractType

class ContractType(Enum):
    """The algorithm used to adjust and serve price data between different futures expiries."""

    CashSettled = 0

    ContinuousBackAdjusted = 1
    """Data is downloaded per contract and merged by Tickblaze before being served"""

    ContinuousByDataProvider = 2
    """Data is downloaded back adjusted by the data provider served without adjustment"""

    ContinuousNonBackAdjusted = 3
    """Data is downloaded per contract and served without adjustment"""

    SingleContract = 4
    """Data is downloaded for a single contract and is served without adjustment"""
