




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IExchangeCalendar as _IExchangeCalendar
from typing import Any, overload
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from tbapi.api.interfaces.iexchange_session import IExchangeSession

@tb_interface(_IExchangeCalendar)
class IExchangeCalendar():
    """Defines methods for handling exchange calendars, including date/time conversion and session status."""


    @abstractmethod
    def exchange_date_time_to_utc_date_time(self, exchange_date_time: datetime) -> datetime:
        """Converts a specified exchange date/time to a UTC date/time.            The exchange date/time to convert.      The specified exchange date/time converted to UTC date/time."""
        result = self._value.ExchangeDateTimeToUtcDateTime(to_net_datetime(exchange_date_time))
        return to_python_datetime(result)
  
    @abstractmethod
    def is_session_open(self, utc_date_time: datetime, is_intraday: bool) -> bool:
        """Determines whether there is an open session at a specified date/time.            The UTC date/time.      Indicates whether the test is for intraday data.      True if there is an open session, false otherwise."""
        result = self._value.IsSessionOpen(to_net_datetime(utc_date_time), is_intraday)
        return result
  
    @abstractmethod
    def utc_date_time_to_exchange_date_time(self, utc_date_time: datetime) -> datetime:
        """Converts a specified UTC date/time to an exchange date/time.            The UTC date/time to convert.      The specified UTC date/time converted to exchange date/time."""
        result = self._value.UtcDateTimeToExchangeDateTime(to_net_datetime(utc_date_time))
        return to_python_datetime(result)
  
    @abstractmethod
    def get_session(self, utc_date_time: datetime) -> IExchangeSession:
        """Retrieves a session at a specific UTC date/time.            The UTC date/time to convert.      The session at the specified UTC date/time, or null if none exists."""
        result = self._value.GetSession(to_net_datetime(utc_date_time))
        from tbapi.api.interfaces.iexchange_session import IExchangeSession
        return IExchangeSession(_existing=result)
  

