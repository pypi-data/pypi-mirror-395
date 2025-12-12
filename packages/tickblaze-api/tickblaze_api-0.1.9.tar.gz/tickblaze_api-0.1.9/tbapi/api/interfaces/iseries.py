




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import ISeries as _ISeries
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_interface(_ISeries)
class ISeries():
    """Defines a series of items and provides methods to retrieve specific items from the series.            The type of items in the series."""



    def __getitem__(self, index: int) -> Any:
        result = self._value[index]
        return result
