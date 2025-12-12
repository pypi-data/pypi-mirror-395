



from typing import TypeVar, Generic, Optional, Callable, Any, Dict, Final
from dataclasses import dataclass
from enum import Enum, IntFlag
from tbapi.common.converters import *
from tbapi.common.arguments import SerializableArgument
from typing import get_args, get_origin
import clr
import json


class NumericRange(SerializableArgument):
    """
    Specifies the numeric range constraints for a parameter.

    Attributes:
        min_value: The minimum value of the numeric range. Default is 0.
        max_value: The maximum value of the numeric range. Default is inf.
        step: The step value for incrementing within the range. Default is 1.
    """

    def __init__(self, min_value: float = 0, max_value: float = 999999, step: float = 1):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.attribute_name = "NumericRange"
        super().__init__()

    @classmethod
    def new(cls, min_value: float = 0, max_value: float = 999999, step: float = 1):
        return cls(min_value, max_value, step)


T = TypeVar("T")


class TbDescriptorBase(Generic[T], SerializableArgument):
    """Base descriptor for internal use only."""

    def __init__(self, name: str) -> None:
        self.property_name: str = name
        self._clr_name: Optional[str] = None
        self.py_type: Optional[type] = None
        super().__init__()

    def __set_name__(self, owner: type, name: str) -> None:
        self._clr_name = "".join(part.capitalize() for part in name.split("_"))
        annots = getattr(owner, "__annotations__", {})

        if name in annots:
            self.py_type = annots[name]

        if self.py_type is None:
            if hasattr(self, "__orig_class__"):
                args = get_args(self.__orig_class__)
                if args:
                    self.py_type = args[0]

        self.property_type = self.get_full_type_name()

    def __get__(self, obj: Any, objtype: Optional[type] = None) -> Optional[T]:
        if obj is None:
            return self

        value_obj = getattr(obj, "_value", None)
        if value_obj is None:
            return None

        raw_value = getattr(value_obj, self._clr_name)

        if issubclass(self.py_type, Enum) or issubclass(self.py_type, IntFlag):
            return self.py_type(int(raw_value))

        if self.py_type is not None and hasattr(self.py_type, "_value") and hasattr(self.py_type, "__tb_decorated__"):
            return self.py_type(_existing=raw_value)

        return raw_value

    def __set__(self, obj: Any, val: T) -> None:
        value_obj: Any = getattr(obj, "_value", None)
        if value_obj is None:
            raise AttributeError("_value not initialized on the wrapper instance")

        if self.py_type is not None and hasattr(val, "_value") and hasattr(val, "__tb_decorated__"):
            setattr(value_obj, self._clr_name, val._value)
        else:
            if isinstance(val, (Enum, IntFlag)):
                setattr(value_obj, self._clr_name, get_origin_enum(val, val))
            else:
                setattr(value_obj, self._clr_name, val)

    def get_full_type_name(self) -> str:
        """
        Returns the full type name of the parameter (module + class).
        For internal use only
        """
        if hasattr(self, "py_type") and self.py_type is not None:
            py_type = self.py_type
            module = getattr(py_type, "__module__", "UnknownModule")
            name = getattr(py_type, "__name__", "UnknownType")
            if module == "builtins":
                return name
            return f"{module}.{name}"

        if hasattr(self, "__orig_class__") and self.__orig_class__ is not None:
            s = str(self.__orig_class__)
            start = s.find("[")
            end = s.find("]")
            if start >= 0 and end > start:
                return s[start + 1:end]

        return "Unknown"

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


class ScriptParameter(TbDescriptorBase[T]):
    """
    Specifies metadata for a parameter property.

    Attributes:
        name: The display name of the parameter.
        group_name: Group name of the parameter (optional).
        description: Description of the parameter (optional).
        order: Order of the parameter (optional).
        show_in_signature: Indicates whether the parameter is shown in the script signature.
        numeric_range: The numeric range constraints for a parameter.
    """

    def __init__(
            self,
            name: str,
            group_name: Optional[str] = None,
            description: Optional[str] = None,
            order: Optional[int] = None,
            show_in_signature: Optional[bool] = None,
            numeric_range : Optional[NumericRange] = None,
    ) -> None:
        super().__init__(name)
        self.group_name = group_name
        self.description = description
        self.order = order
        self.show_in_signature = show_in_signature
        self.numeric_range = numeric_range
        self.attribute_name = "ScriptParameter"
        self.parameter_name = name


class Plot(TbDescriptorBase[T]):
    """
    Specifies metadata for a Plot property.

    Attributes:
        name: The display name of the plot.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.attribute_name  = "Plot"
        self.plot_name = name

class Source(TbDescriptorBase[T]):
    """
    Specifies metadata for a Source property.
    """

    def __init__(self, name: str = "Source") -> None:
        super().__init__(name)
        self.attribute_name  = "Source"
        self.source_name = name