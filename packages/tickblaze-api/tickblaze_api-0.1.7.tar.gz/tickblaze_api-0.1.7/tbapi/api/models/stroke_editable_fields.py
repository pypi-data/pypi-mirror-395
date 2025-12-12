

from enum import IntFlag
from Tickblaze.Scripts.Api.Models import StrokeEditableFields as _StrokeEditableFields

class StrokeEditableFields(IntFlag):

    Color = 1

    IsVisible = 2

    Thickness = 4

    LineStyle = 8

    All = 15
