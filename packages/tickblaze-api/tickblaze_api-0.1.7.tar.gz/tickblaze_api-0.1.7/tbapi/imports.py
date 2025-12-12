import os
from abc import ABC, abstractmethod

import pythonnet
import clr_loader

coreclr = clr_loader.get_coreclr()

pythonnet.set_runtime(coreclr)

import clr

_directory_path = os.path.abspath(os.path.dirname(__file__))

_assembly_names = [
    "Tickblaze.Core.dll",
    "Tickblaze.Core.Data.dll",
    "Tickblaze.Scripts.Api.dll",
    "Tickblaze.Model.Shared.dll",
    "Tickblaze.Python.Scripts.Api.dll",
]

for assembly_name in _assembly_names:
    _assembly_path = os.path.join(_directory_path, "references", assembly_name)
    clr.AddReference(_assembly_path)


from Tickblaze.Python.Scripts.Api import (
    PythonInteropService as _python_interop_service,
)