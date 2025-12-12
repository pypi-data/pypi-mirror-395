




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IWindowProvider as _IWindowProvider
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_interface(_IWindowProvider)
class IWindowProvider():
    """Provides the ability to create windows"""


    @abstractmethod
    def create_window(self, title: str) -> Any:
        """Creates a new window.            An object representing the created window, or null if the creation failed."""
        result = self._value.CreateWindow(title)
        return result
  

