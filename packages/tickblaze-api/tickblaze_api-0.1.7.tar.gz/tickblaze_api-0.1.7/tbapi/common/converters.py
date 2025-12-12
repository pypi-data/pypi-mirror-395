



import sys
from datetime import datetime
from System import DateTime


def to_python_datetime(net_dt: DateTime) -> datetime:
    """
    Convert .NET DateTime -> Python datetime.datetime
    """
    if net_dt is None:
        return None

    return datetime(
        net_dt.Year,
        net_dt.Month,
        net_dt.Day,
        net_dt.Hour,
        net_dt.Minute,
        net_dt.Second,
        net_dt.Millisecond * 1000,  # milliseconds -> microseconds
    )


def to_net_datetime(py_dt: datetime) -> DateTime:
    """
    Convert Python datetime.datetime -> .NET DateTime
    """
    if py_dt is None:
        return None

    return DateTime(
        py_dt.year,
        py_dt.month,
        py_dt.day,
        py_dt.hour,
        py_dt.minute,
        py_dt.second,
        int(py_dt.microsecond / 1000),  # microseconds -> milliseconds
    )

def get_origin_enum(cls, arg):
    enum_name = f"_{type(arg).__name__}"
    module = sys.modules[cls.__module__]
    clr_enum = getattr(module, enum_name, None)
    if clr_enum is None:
        raise TypeError(f"No CLR enum found for {type(arg).__name__}")
    return clr_enum(int(arg.value))