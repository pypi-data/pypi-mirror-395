




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Adapters import IAlertAdapter as _IAlertAdapter
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.adapters.alert_type import AlertType
from Tickblaze.Scripts.Api.Adapters import AlertType as _AlertType

@tb_interface(_IAlertAdapter)
class IAlertAdapter():
    """Interface for notification mechanisms such as playing sounds, sending emails, and showing dialogs."""


    @abstractmethod
    def play_sound(self, file_path: str) -> None:
        """Plays a sound from the specified file path.            The path to the sound file."""
        result = self._value.PlaySound(file_path)
        return result
  
    @abstractmethod
    def show_dialog(self, type: AlertType, message: str) -> None:
        """Shows a dialog with the specified alert type and message.            The type of the alert.      The message to display in the dialog."""
        result = self._value.ShowDialog(_AlertType(type.value if hasattr(type, 'value') else int(type)), message)
        return result
  

