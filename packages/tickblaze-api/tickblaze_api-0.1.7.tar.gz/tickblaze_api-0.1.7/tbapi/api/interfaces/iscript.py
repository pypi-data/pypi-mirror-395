




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IScript as _IScript
from typing import Any, overload
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from tbapi.api.models.metadata import Metadata
    from tbapi.api.parameters import Parameters
    from tbapi.api.optimization_parameters import OptimizationParameters

@tb_interface(_IScript)
class IScript():
    """Defines properties and methods for a script, including initialization and metadata."""

    @property
    def metadata(self) -> Metadata:
        """The metadata associated with the script."""
        from tbapi.api.models.metadata import Metadata
        val = self._value.Metadata
        return Metadata(_existing=val)
    @property
    def parameters(self) -> Parameters:
        """The parameters for the script."""
        from tbapi.api.parameters import Parameters
        val = self._value.Parameters
        return Parameters(_existing=val)
    @property
    def is_initialized(self) -> bool:
        """Indicates whether the script has been initialized."""
        val = self._value.IsInitialized
        return val

    def initialize(self) -> None:
        """Initializes the script."""
        result = self._value.Initialize()
        return result
  
    @abstractmethod
    def get_parameters(self) -> Parameters:
        """Gets the parameters of the script for the UI."""
        result = self._value.GetParameters()
        from tbapi.api.parameters import Parameters
        return Parameters(_existing=result)
  
    @abstractmethod
    def get_optimization_parameters(self, parameter_values: OptimizationParameters) -> Parameters:
        """Gets the parameters of the script for the UI in an optimization context."""
        result = self._value.GetOptimizationParameters(parameter_values._value)
        from tbapi.api.parameters import Parameters
        return Parameters(_existing=result)
  

