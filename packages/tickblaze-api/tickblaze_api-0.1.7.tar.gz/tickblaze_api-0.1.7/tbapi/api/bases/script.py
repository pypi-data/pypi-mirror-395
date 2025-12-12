






from __future__ import annotations
from typing import TYPE_CHECKING
import clr
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import Script as _Script
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.iscript import IScript
from tbapi.api.interfaces.imetadata import IMetadata
from tbapi.api.parameters import Parameters
from tbapi.api.optimization_parameters import OptimizationParameters
if TYPE_CHECKING:
    from tbapi.api.models.metadata import Metadata
    from tbapi.api.adapters.ialert_adapter import IAlertAdapter

@tb_interface(_Script)
class Script(IScript, IMetadata):

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Script. Use overloads for IDE type hints."""
        return Script(*args, **kwargs)

    @property
    def name(self) -> str:
        val = self._value.Name
        return val
    @name.setter
    def name(self, val: str):
        tmp = self._value
        tmp.Name = val
        self._value = tmp
    @property
    def short_name(self) -> str:
        val = self._value.ShortName
        return val
    @short_name.setter
    def short_name(self, val: str):
        tmp = self._value
        tmp.ShortName = val
        self._value = tmp
    @property
    def description(self) -> str:
        val = self._value.Description
        return val
    @description.setter
    def description(self, val: str):
        tmp = self._value
        tmp.Description = val
        self._value = tmp
    @property
    def metadata(self) -> Metadata:
        from tbapi.api.models.metadata import Metadata
        val = self._value.Metadata
        return Metadata(_existing=val)
    @property
    def parameters(self) -> Parameters:
        from tbapi.api.parameters import Parameters
        val = self._value.Parameters
        return Parameters(_existing=val)
    @property
    def is_initialized(self) -> bool:
        val = self._value.IsInitialized
        return val
    @is_initialized.setter
    def is_initialized(self, val: bool):
        tmp = self._value
        tmp.IsInitialized = val
        self._value = tmp
    @property
    def product_code_aliases(self) -> list[str]:
        val = self._value.ProductCodeAliases
        return val

    def create_chart_toolbar_menu_item(self) -> Any:
        """Creates a control that will be displayed in the chart's toolbar."""
        result = self._value.CreateChartToolbarMenuItem()
        return result
  
    def register_exception(self, message: str) -> None:
        """Registers an exception            Exception message"""
        result = self._value.RegisterException(message)
        return result
  
    def dispose(self) -> None:
        result = self._value.Dispose()
        return result
  

    @clr.clrmethod(Parameters, [Parameters])
    def get_parameters(self, parameters: Parameters) -> Parameters:
        ...

    @clr.clrmethod(Parameters, [Parameters, OptimizationParameters])
    def get_optimization_parameters(self, parameters: Parameters, parameter_values: OptimizationParameters) -> Parameters:
        ...

    @clr.clrmethod(None, [None])
    def initialize(self) -> None:
        """A method call when the script is being initialized."""
        ...

    @clr.clrmethod(None, [None])
    def on_destroy(self) -> None:
        """A method call when the script is being destroyed."""
        ...


