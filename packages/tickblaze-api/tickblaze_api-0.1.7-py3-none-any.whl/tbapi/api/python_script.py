






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Python.Scripts.Api import PythonScript as _PythonScript
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_PythonScript)
class PythonScript():

    @overload
    @staticmethod
    def new() -> "PythonScript":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for PythonScript. Use overloads for IDE type hints."""
        return PythonScript(*args, **kwargs)




