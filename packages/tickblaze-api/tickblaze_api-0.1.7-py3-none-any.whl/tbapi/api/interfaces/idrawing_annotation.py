




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IDrawingAnnotation as _IDrawingAnnotation
from typing import Any, overload
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from tbapi.api.interfaces.ichart_points import IChartPoints

@tb_interface(_IDrawingAnnotation)
class IDrawingAnnotation():
    """Represents a drawing annotation on a chart, typically used for visual elements such as lines, shapes, or markers. It contains a collection of points that define the shape or path of the annotation on the chart."""

    @property
    def points(self) -> IChartPoints:
        """Gets the collection of points associated with the drawing annotation."""
        from tbapi.api.interfaces.ichart_points import IChartPoints
        val = self._value.Points
        return IChartPoints(_existing=val)


