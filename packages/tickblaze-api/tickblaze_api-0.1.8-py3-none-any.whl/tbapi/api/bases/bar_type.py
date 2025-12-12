






from __future__ import annotations
from typing import TYPE_CHECKING
import clr
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import BarType as _BarType
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.symbol_script import SymbolScript
from tbapi.api.bases.source_data_type import SourceDataType
from tbapi.api.models.bar import Bar
if TYPE_CHECKING:
    from tbapi.api.models.symbol import Symbol
    from tbapi.core.models.contract_settings import ContractSettings
    from tbapi.api.bases.bar_type import BarType
from tbapi.api.bases.source_data_type import SourceDataType
_SourceDataType = _BarType.SourceDataType

@tb_interface(_BarType)
class BarType(SymbolScript):
    """Represents a base class for defining custom bar types with metadata, bar series, and source data configuration."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for BarType. Use overloads for IDE type hints."""
        return BarType(*args, **kwargs)

    @property
    def symbol(self) -> Symbol:
        """The series underlying instrument"""
        from tbapi.api.models.symbol import Symbol
        val = self._value.Symbol
        return Symbol(_existing=val)
    @symbol.setter
    def symbol(self, val: Symbol):
        tmp = self._value
        tmp.Symbol = val._value
        self._value = tmp
    @property
    def is_eth(self) -> bool:
        """The series hours (If false, hours are RTH)"""
        val = self._value.IsETH
        return val
    @is_eth.setter
    def is_eth(self, val: bool):
        tmp = self._value
        tmp.IsETH = val
        self._value = tmp
    @property
    def contract_settings(self) -> ContractSettings:
        """For futures symbols, details which kind of contract data this series represents (which specific contract if single contract, data merge rule otherwise)"""
        from tbapi.core.models.contract_settings import ContractSettings
        val = self._value.ContractSettings
        return ContractSettings(_existing=val)
    @contract_settings.setter
    def contract_settings(self, val: ContractSettings):
        tmp = self._value
        tmp.ContractSettings = val._value
        self._value = tmp
    @property
    def source(self) -> SourceDataType:
        """The type of source data used to create the bar type."""
        val = int(self._value.Source)
        return SourceDataType(val)
    @source.setter
    def source(self, val: SourceDataType):
        tmp = self._value
        tmp.Source = _SourceDataType(val.value if hasattr(val, "value") else int(val))
        self._value = tmp
    @property
    def input_parameter_display_string(self) -> str:
        """A shorthand string to represent the input parameters, used in the data box, and anywhere else a short identifier is required"""
        val = self._value.InputParameterDisplayString
        return val

    def add_bar(self, bar: Bar) -> None:
        """Adds a new bar to the bar series.            The bar to add."""
        result = self._value.AddBar(bar._value)
        return result
  
    def update_bar(self, bar: Bar) -> None:
        """Updates the most recent bar in the bar series.            The bar data to update."""
        result = self._value.UpdateBar(bar._value)
        return result
  

    @clr.clrmethod(None, [Bar])
    def on_data_point(self, bar: Bar) -> None:
        """Processes a data point to create or update a bar.            The bar data to process."""
        ...


