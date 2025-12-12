






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import AddOn as _AddOn
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.bases.script import Script
if TYPE_CHECKING:
    from tbapi.api.interfaces.iwindow_provider import IWindowProvider

@tb_interface(_AddOn)
class AddOn(Script):
    """Represents a base class for add on scripts."""

    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for AddOn. Use overloads for IDE type hints."""
        return AddOn(*args, **kwargs)

    @property
    def window_provider(self) -> IWindowProvider:
        """Gets or sets the window provider associated with the add-on."""
        from tbapi.api.interfaces.iwindow_provider import IWindowProvider
        val = self._value.WindowProvider
        return IWindowProvider(_existing=val)
    @window_provider.setter
    def window_provider(self, val: IWindowProvider):
        tmp = self._value
        tmp.WindowProvider = val._value
        self._value = tmp

    @abstractmethod
    def create_menu_item(self) -> Any:
        """Creates a control that will be displayed in the main menu."""
        result = self._value.CreateMenuItem()
        return result
  
    def on_shutdown(self) -> None:
        """Called when the application is shutting down or when the script is reloaded.      Allows for cleanup operations or resource deallocation."""
        result = self._value.OnShutdown()
        return result
  


