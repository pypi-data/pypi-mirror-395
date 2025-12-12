




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Bases import IIndicator as _IIndicator
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.api.interfaces.iscript import IScript
if TYPE_CHECKING:
    from tbapi.api.series import Series

@tb_interface(_IIndicator)
class IIndicator(IScript):
    """Represents an indicator script that can be overlaid on a chart or displayed on a separate indicator panel."""

    @property
    def is_overlay(self) -> bool:
        """Indicates whether this instance is overlayed on the chart or plotted on a separate indicator panel."""
        val = self._value.IsOverlay
        return val
    @property
    def is_percentage(self) -> bool:
        """Indicates whether the indicator is a percentage indicator. The default value is false."""
        val = self._value.IsPercentage
        return val
    @property
    def auto_rescale(self) -> bool:
        """Indicates whether this instance automatically rescales the chart or not."""
        val = self._value.AutoRescale
        return val
    @auto_rescale.setter
    def auto_rescale(self, val: bool):
        tmp = self._value
        tmp.AutoRescale = val
        self._value = tmp
    @property
    def apply_background_color_to_all_panels(self) -> bool:
        """Indicates whether a background color should be applied to all panels."""
        val = self._value.ApplyBackgroundColorToAllPanels
        return val
    @apply_background_color_to_all_panels.setter
    def apply_background_color_to_all_panels(self, val: bool):
        tmp = self._value
        tmp.ApplyBackgroundColorToAllPanels = val
        self._value = tmp
    @property
    def scale_precision(self) -> int | None:
        """The number of decimals displayed on the price scale of the indicator panel."""
        val = self._value.ScalePrecision
        return val
    @property
    def background_color(self) -> Series:
        """Sets the background color of the chart panel."""
        val = self._value.BackgroundColor
        return val


