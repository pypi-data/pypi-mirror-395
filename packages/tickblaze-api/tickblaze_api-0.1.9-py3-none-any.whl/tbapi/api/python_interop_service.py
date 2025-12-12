






from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_class, tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Python.Scripts.Api import PythonInteropService as _PythonInteropService
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_class(_PythonInteropService)
class PythonInteropService():
    """This class is invoked directly from Python via PythonNet.      Do not remove or modify its constructors or method signatures,      as this will break interop with the Python side."""

    @overload
    @staticmethod
    def new() -> "PythonInteropService":
        """Constructor overload with arguments: """
        ...
    @staticmethod
    def new(*args, **kwargs):
        """Generic factory method for PythonInteropService. Use overloads for IDE type hints."""
        return PythonInteropService(*args, **kwargs)


    @staticmethod
    def create_wrapper_instance(module_file_path: str, class_name: str, script: Any = None) -> Any:
        result = _PythonInteropService.CreateWrapperInstance(module_file_path, class_name, script)
        return result
  
    @staticmethod
    def try_invoke_post_init(target: Any) -> None:
        result = _PythonInteropService.TryInvokePostInit(target)
        return result
  


