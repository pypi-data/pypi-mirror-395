




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IDrawingContext as _IDrawingContext
from typing import Any, overload
from abc import ABC, abstractmethod
from tbapi.core.enums.line_style import LineStyle
from Tickblaze.Core.Enums import LineStyle as _LineStyle
if TYPE_CHECKING:
    from tbapi.api.interfaces.isize import ISize
    from tbapi.api.models.font import Font
    from tbapi.api.interfaces.ipoint import IPoint
    from tbapi.api.models.color import Color
    from tbapi.api.models.stroke import Stroke
    from tbapi.api.models.arrow_info import ArrowInfo

@tb_interface(_IDrawingContext)
class IDrawingContext():
    """Defines a context for rendering graphical elements, including shapes, text, and lines."""

    @property
    def render_size(self) -> ISize:
        """The size of the rendering area."""
        from tbapi.api.interfaces.isize import ISize
        val = self._value.RenderSize
        return ISize(_existing=val)

    @abstractmethod
    def measure_text(self, text: str, font: Font) -> ISize:
        """Measures the dimensions of a given text string using the specified font.            The text to measure.      The font used for measurement.      The size of the rendered text."""
        result = self._value.MeasureText(text, font._value)
        from tbapi.api.interfaces.isize import ISize
        return ISize(_existing=result)
  
    @abstractmethod
    def draw_text(self, origin: IPoint, text: str, color: Color, font: Font = None) -> None:
        """Draws text at the specified origin point.            The location where the text is drawn.      The text to draw.      The color of the text.      The font used for rendering the text."""
        result = self._value.DrawText(origin._value, text, color._value, font._value)
        return result
  
    @abstractmethod
    def draw_image(self, origin: IPoint, pixels: list[Color]) -> None:
        """Draws an image at the specified origin point.            The location where the image is drawn.      The image pixels.      Optional image width.      Optional image height."""
        result = self._value.DrawImage(origin._value, pixels)
        return result
  
    @abstractmethod
    def draw_ellipse(self, center: IPoint, radius_x: float, radius_y: float, fill_color: Color | None, line_color: Color | None = None, line_thickness: int = 1, line_style: LineStyle = LineStyle.Solid) -> None:
        """Draws an ellipse with the specified dimensions and styling.            The center point of the ellipse.      The horizontal radius of the ellipse.      The vertical radius of the ellipse.      The color used to fill the ellipse.      The color of the ellipse's outline.      The thickness of the outline.      The style of the outline."""
        result = self._value.DrawEllipse(center._value, radius_x, radius_y, (None if fill_color is None else fill_color._value), (None if line_color is None else line_color._value), line_thickness, _LineStyle(line_style.value if hasattr(line_style, 'value') else int(line_style)))
        return result
  
    @abstractmethod
    def draw_ellipse_with_stroke(self, center: IPoint, radius_x: float, radius_y: float, fill_color: Color | None, stroke: Stroke) -> None:
        """Draws an ellipse with the specified dimensions and styling.            The center point of the ellipse.      The horizontal radius of the ellipse.      The vertical radius of the ellipse.      The color used to fill the ellipse.      The stroke of the outline."""
        result = self._value.DrawEllipse(center._value, radius_x, radius_y, (None if fill_color is None else fill_color._value), stroke._value)
        return result
  
    @abstractmethod
    def draw_line(self, point_a: IPoint, point_b: IPoint, color: Color, thickness: int = 1, line_style: LineStyle = LineStyle.Solid) -> None:
        """Draws a line between two points.            The first point of the line.      The second point of the line.      The color of the line.      The thickness of the line.      The style of the line."""
        result = self._value.DrawLine(point_a._value, point_b._value, color._value, thickness, _LineStyle(line_style.value if hasattr(line_style, 'value') else int(line_style)))
        return result
  
    @abstractmethod
    def draw_line_with_stroke(self, point_a: IPoint, point_b: IPoint, stroke: Stroke) -> None:
        """Draws a line between two points.            The first point of the line.      The second point of the line.      The stroke of the line."""
        result = self._value.DrawLine(point_a._value, point_b._value, stroke._value)
        return result
  
    @abstractmethod
    def draw_ray(self, point_a: IPoint, point_b: IPoint, color: Color, thickness: int = 1, line_style: LineStyle = LineStyle.Solid) -> None:
        """Draws a ray originating from a point and extending through a second point.            The starting point of the ray.      A point along the direction of the ray.      The color of the ray.      The thickness of the ray.      The style of the ray."""
        result = self._value.DrawRay(point_a._value, point_b._value, color._value, thickness, _LineStyle(line_style.value if hasattr(line_style, 'value') else int(line_style)))
        return result
  
    @abstractmethod
    def draw_ray_with_stroke(self, point_a: IPoint, point_b: IPoint, stroke: Stroke) -> None:
        """Draws a ray originating from a point and extending through a second point.            The starting point of the ray.      A point along the direction of the ray.      The stroke of the ray."""
        result = self._value.DrawRay(point_a._value, point_b._value, stroke._value)
        return result
  
    @abstractmethod
    def draw_extended_line(self, point_a: IPoint, point_b: IPoint, color: Color, thickness: int = 1, line_style: LineStyle = LineStyle.Solid) -> None:
        """Draws a line extended in both directions beyond its endpoints.            The first point on the line.      The second point on the line.      The color of the line.      The thickness of the line.      The style of the line."""
        result = self._value.DrawExtendedLine(point_a._value, point_b._value, color._value, thickness, _LineStyle(line_style.value if hasattr(line_style, 'value') else int(line_style)))
        return result
  
    @abstractmethod
    def draw_extended_line_with_stroke(self, point_a: IPoint, point_b: IPoint, stroke: Stroke) -> None:
        """Draws a line extended in both directions beyond its endpoints.            The first point on the line.      The second point on the line.      The stroke of the line."""
        result = self._value.DrawExtendedLine(point_a._value, point_b._value, stroke._value)
        return result
  
    @abstractmethod
    def draw_rectangle(self, point_a: IPoint, width: float, height: float, fill_color: Color | None, line_color: Color | None = None, line_thickness: int = 1, line_style: LineStyle = LineStyle.Solid) -> None:
        """Draws a rectangle at the specified location with the given dimensions and styling.            The top-left corner of the rectangle.      The width of the rectangle.      The height of the rectangle.      The color used to fill the rectangle.      The color of the rectangle's outline.      The thickness of the outline.      The style of the outline."""
        result = self._value.DrawRectangle(point_a._value, width, height, (None if fill_color is None else fill_color._value), (None if line_color is None else line_color._value), line_thickness, _LineStyle(line_style.value if hasattr(line_style, 'value') else int(line_style)))
        return result
  
    @abstractmethod
    def draw_rectangle_with_stroke(self, point_a: IPoint, width: float, height: float, fill_color: Color | None, stroke: Stroke) -> None:
        """Draws a rectangle at the specified location with the given dimensions and styling.            The top-left corner of the rectangle.      The width of the rectangle.      The height of the rectangle.      The color used to fill the rectangle.      The stroke of the outline."""
        result = self._value.DrawRectangle(point_a._value, width, height, (None if fill_color is None else fill_color._value), stroke._value)
        return result
  
    @abstractmethod
    def draw_rectangle_from_points(self, point_a: IPoint, point_b: IPoint, fill_color: Color | None, line_color: Color | None = None, line_thickness: int = 1, line_style: LineStyle = LineStyle.Solid) -> None:
        """Draws a rectangle defined by two points with the given styling.            The corner of the rectangle.      The opposite corner of the rectangle.      The color used to fill the rectangle.      The color of the rectangle's outline.      The thickness of the outline.      The style of the outline."""
        result = self._value.DrawRectangle(point_a._value, point_b._value, (None if fill_color is None else fill_color._value), (None if line_color is None else line_color._value), line_thickness, _LineStyle(line_style.value if hasattr(line_style, 'value') else int(line_style)))
        return result
  
    @abstractmethod
    def draw_rectangle_from_points_with_stroke(self, point_a: IPoint, point_b: IPoint, fill_color: Color | None, stroke: Stroke) -> None:
        """Draws a rectangle defined by two points with the given styling.            The corner of the rectangle.      The opposite corner of the rectangle.      The color used to fill the rectangle.      The stroke of the outline."""
        result = self._value.DrawRectangle(point_a._value, point_b._value, (None if fill_color is None else fill_color._value), stroke._value)
        return result
  
    @abstractmethod
    def draw_polygon(self, points: list[Any], fill_color: Color | None, line_color: Color | None = None, line_thickness: int = 1, line_style: LineStyle = LineStyle.Solid) -> None:
        """Draws a polygon defined by a sequence of points.            The vertices of the polygon.      The color used to fill the polygon.      The color of the polygon's outline.      The thickness of the outline.      The style of the outline."""
        result = self._value.DrawPolygon(points, (None if fill_color is None else fill_color._value), (None if line_color is None else line_color._value), line_thickness, _LineStyle(line_style.value if hasattr(line_style, 'value') else int(line_style)))
        return result
  
    @abstractmethod
    def draw_polygon_with_stroke(self, points: list[Any], fill_color: Color | None, stroke: Stroke) -> None:
        """Draws a polygon defined by a sequence of points.            The vertices of the polygon.      The color used to fill the polygon.      The stroke of the outline."""
        result = self._value.DrawPolygon(points, (None if fill_color is None else fill_color._value), stroke._value)
        return result
  
    @abstractmethod
    def draw_arrow(self, arrow_info: ArrowInfo, fill_color: Color | None, stroke: Stroke) -> None:
        """Draws an arrow            The spec of the arrow to draw.      The color used to fill the polygon.      The stroke of the outline."""
        result = self._value.DrawArrow(arrow_info._value, (None if fill_color is None else fill_color._value), stroke._value)
        return result
  

