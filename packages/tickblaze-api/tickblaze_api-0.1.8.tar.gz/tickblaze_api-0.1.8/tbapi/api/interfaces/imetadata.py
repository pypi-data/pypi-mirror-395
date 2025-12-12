




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IMetadata as _IMetadata
from typing import Any, overload
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from tbapi.api.models.metadata import Metadata

@tb_interface(_IMetadata)
class IMetadata():
    """Defines metadata properties for a script, including name, description, and related metadata."""

    @property
    def name(self) -> str:
        """The name of the script."""
        val = self._value.Name
        return val
    @property
    def short_name(self) -> str:
        """The short name of the script."""
        val = self._value.ShortName
        return val
    @property
    def description(self) -> str:
        """A description of the script."""
        val = self._value.Description
        return val
    @property
    def metadata(self) -> Metadata:
        """Associated metadata for the script."""
        from tbapi.api.models.metadata import Metadata
        val = self._value.Metadata
        return Metadata(_existing=val)
    @property
    def product_code_aliases(self) -> list[str]:
        val = self._value.ProductCodeAliases
        return val


