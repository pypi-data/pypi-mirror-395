





from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Core.Models import ContractSettings as _ContractSettings
from typing import Any, overload
from tbapi.core.enums.contract_type import ContractType
from Tickblaze.Core.Enums import ContractType as _ContractType

@tb_class(_ContractSettings)
class ContractSettings():
    """Describes how futures data should be back adjusted and served"""

    @overload
    @staticmethod
    def new() -> "ContractSettings":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for ContractSettings. Use overloads for IDE type hints."""
        return ContractSettings(*args, **kwargs)

    @property
    def type(self) -> ContractType:
        """The specific merge rule used to backfill data"""
        val = int(self._value.Type)
        return ContractType(val)
    @type.setter
    def type(self, val: ContractType):
        tmp = self._value
        tmp.Type = _ContractType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def year(self) -> int:
        """The individual contracts year (Ignored unless  is set to )"""
        val = self._value.Year
        return val
    @year.setter
    def year(self, val: int):
        tmp = self._value
        tmp.Year = val
        self._value = tmp
    @property
    def month(self) -> int:
        """The individual contracts month (Ignored unless  is set to )"""
        val = self._value.Month
        return val
    @month.setter
    def month(self, val: int):
        tmp = self._value
        tmp.Month = val
        self._value = tmp


