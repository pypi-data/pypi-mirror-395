






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import SymbolInfo as _SymbolInfo
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.core.enums.instrument_type import InstrumentType
from tbapi.core.enums.exchange import Exchange
from Tickblaze.Core.Enums import InstrumentType as _InstrumentType
from Tickblaze.Core.Enums import Exchange as _Exchange
if TYPE_CHECKING:
    from tbapi.core.models.contract_settings import ContractSettings

@tb_class(_SymbolInfo)
class SymbolInfo():

    @overload
    @staticmethod
    def new() -> "SymbolInfo":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for SymbolInfo. Use overloads for IDE type hints."""
        return SymbolInfo(*args, **kwargs)

    @property
    def instrument_type(self) -> InstrumentType:
        val = int(self._value.InstrumentType)
        return InstrumentType(val)
    @instrument_type.setter
    def instrument_type(self, val: InstrumentType):
        tmp = self._value
        tmp.InstrumentType = _InstrumentType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def symbol_code(self) -> str:
        val = self._value.SymbolCode
        return val
    @symbol_code.setter
    def symbol_code(self, val: str):
        tmp = self._value
        tmp.SymbolCode = val
        self._value = tmp
    @property
    def exchange(self) -> Exchange:
        val = int(self._value.Exchange)
        return Exchange(val)
    @exchange.setter
    def exchange(self, val: Exchange):
        tmp = self._value
        tmp.Exchange = _Exchange(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def contract(self) -> ContractSettings:
        from tbapi.core.models.contract_settings import ContractSettings
        val = self._value.Contract
        return ContractSettings(_existing=val)
    @contract.setter
    def contract(self, val: ContractSettings):
        tmp = self._value
        tmp.Contract = val._value
        self._value = tmp



