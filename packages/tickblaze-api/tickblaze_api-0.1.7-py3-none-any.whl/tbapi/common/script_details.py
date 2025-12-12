



from tbapi.common.arguments import SerializableArgument
import clr
import json


class ScriptDetails(SerializableArgument):
    """Base script details class for internal use only."""

    def __init__(self):
        super().__init__()

    @clr.clrmethod(None, [str])
    def to_json(self) -> str:
        return json.dumps(
            self.encode() if isinstance(self, SerializableArgument) else str(self),
            indent=4,
            default=lambda o: (
                o.encode() if isinstance(o, SerializableArgument) else
                (o.__name__ if isinstance(o, type) else str(o))
            )
        )
        

class IndicatorDetails(ScriptDetails):
    """Indicator details class for internal use only."""

    def __init__(self, display_name: str):
        super().__init__()
        self.attribute_name = "IndicatorDetails"
        self.display_name = display_name
        

class DrawingDetails(ScriptDetails):
    """Drawing details class for internal use only."""

    def __init__(self, points_count: int):
        super().__init__()
        self.attribute_name = "DrawingDetails"
        self.points_count = points_count