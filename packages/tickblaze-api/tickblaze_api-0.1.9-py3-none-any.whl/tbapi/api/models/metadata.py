






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Models import Metadata as _Metadata
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_Metadata)
class Metadata():
    """Represents metadata about a given object, including its name, type, assembly, and version."""

    @overload
    @staticmethod
    def new() -> "Metadata":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for Metadata. Use overloads for IDE type hints."""
        return Metadata(*args, **kwargs)

    @property
    def name(self) -> str:
        """The name of the metadata."""
        val = self._value.Name
        return val
    @name.setter
    def name(self, val: str):
        tmp = self._value
        tmp.Name = val
        self._value = tmp
    @property
    def short_name(self) -> str:
        """The short name of the metadata, typically consisting of uppercase characters from the name."""
        val = self._value.ShortName
        return val
    @short_name.setter
    def short_name(self, val: str):
        tmp = self._value
        tmp.ShortName = val
        self._value = tmp
    @property
    def description(self) -> str:
        """A description of the metadata."""
        val = self._value.Description
        return val
    @description.setter
    def description(self, val: str):
        tmp = self._value
        tmp.Description = val
        self._value = tmp
    @property
    def type(self) -> str:
        """The full type name of the metadata."""
        val = self._value.Type
        return val
    @property
    def assembly(self) -> str:
        """The assembly name containing the metadata."""
        val = self._value.Assembly
        return val
    @property
    def version(self) -> str:
        """The version of the metadata."""
        val = self._value.Version
        return val
    @property
    def resource_id(self) -> int:
        """The resource ID associated with the metadata."""
        val = self._value.ResourceId
        return val
    @property
    def script_version(self) -> Version:
        """The version of the script."""
        val = self._value.ScriptVersion
        return val



