




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IExchangeSession as _IExchangeSession
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_interface(_IExchangeSession)
class IExchangeSession():
    """Defines methods and properties for handling exchange sessions, including session times and duration."""

    @property
    def end_exchange_date_time(self) -> datetime:
        """The end exchange date/time of the session."""
        val = self._value.EndExchangeDateTime
        return to_python_datetime(val)
    @property
    def end_utc_date_time(self) -> datetime:
        """The end UTC date/time of the session."""
        val = self._value.EndUtcDateTime
        return to_python_datetime(val)
    @property
    def session_minutes(self) -> int:
        """The session duration in minutes."""
        val = self._value.SessionMinutes
        return val
    @property
    def session_seconds(self) -> int:
        """The session duration in seconds."""
        val = self._value.SessionSeconds
        return val
    @property
    def start_exchange_date_time(self) -> datetime:
        """The start exchange date/time of the session."""
        val = self._value.StartExchangeDateTime
        return to_python_datetime(val)
    @property
    def start_utc_date_time(self) -> datetime:
        """The start UTC date/time of the session."""
        val = self._value.StartUtcDateTime
        return to_python_datetime(val)
    @property
    def total_minutes(self) -> int:
        """The total minute count from the first minute of the first session."""
        val = self._value.TotalMinutes
        return val

    @abstractmethod
    def contains(self, utc_date_time: datetime) -> bool:
        """Determines whether the provided UTC date/time is within the session.            The UTC date/time to check.      True if the date/time is within the session, false otherwise."""
        result = self._value.Contains(to_net_datetime(utc_date_time))
        return result
  

