






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import CommissionSimulator as _CommissionSimulator
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.script import Script
if TYPE_CHECKING:
    from tbapi.api.models.symbol import Symbol

@tb_interface(_CommissionSimulator)
class CommissionSimulator(Script):

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for CommissionSimulator. Use overloads for IDE type hints."""
        return CommissionSimulator(*args, **kwargs)


    @abstractmethod
    def calculate(self, symbol_info: Symbol, fill_quantity: float, fill_price: float, is_first_fill: bool) -> float:
        result = self._value.Calculate(symbol_info._value, fill_quantity, fill_price, is_first_fill)
        return result
  


