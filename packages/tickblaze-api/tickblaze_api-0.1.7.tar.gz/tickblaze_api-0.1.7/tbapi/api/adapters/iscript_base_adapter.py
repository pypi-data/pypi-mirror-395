




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Adapters import IScriptBaseAdapter as _IScriptBaseAdapter
from typing import Any, overload
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from tbapi.api.bases.script import Script

@tb_interface(_IScriptBaseAdapter)
class IScriptBaseAdapter():
    """Interface for script base adapter."""

    @property
    def script(self) -> Script:
        """Gets the script."""
        from tbapi.api.bases.script import Script
        val = self._value.Script
        return Script(_existing=val)

    @abstractmethod
    def output_write_line(self, text: str) -> None:
        """Writes a line of text to the output.            The text to write."""
        result = self._value.OutputWriteLine(text)
        return result
  

