from functools import wraps
from tbapi.common.converters import *
from enum import Enum, IntFlag
from tbapi.imports import _python_interop_service
from tbapi.common.script_details import *
import os, sys


def with_wrapper_factory(decorator):
    """
    Decorator for internal use only.
    """
    def wrapped(cls):
        cls = decorator(cls)

        if os.environ.get("INSTANTIATION_ENABLED") != "1":
            return cls

        module = sys.modules[cls.__module__]
        current_file = os.path.abspath(module.__file__)
        orig_init = getattr(cls, "__init__", lambda self, *a, **kw: None)

        @wraps(orig_init)
        def __init__(self, *args, **kwargs):
            if "_existing" not in kwargs or kwargs["_existing"] is None:
                wrapper_value = _python_interop_service.CreateWrapperInstance(
                    current_file, cls.__name__, self
                )
                kwargs["_existing"] = wrapper_value
                self._value = wrapper_value
            orig_init(self, *args, **kwargs)

            if hasattr(self, "_value") and self._value is not None:
                _python_interop_service.TryInvokePostInit(self._value)

        cls.__init__ = __init__
        return cls

    return wrapped


def tb_indicator(arg=None, *, display_name: str = ""):
    """
    Todo: description (indicator)
    """
    if callable(arg):
        cls = arg
        cls.__is_indicator__ = True
        cls.__script_details__ = IndicatorDetails(display_name)
        return with_wrapper_factory(lambda c: c)(cls)

    @with_wrapper_factory
    def decorator(cls):
        cls.__is_indicator__ = True
        cls.__script_details__ = IndicatorDetails(display_name)
        return cls
    return decorator


def tb_drawing(arg=None, *, points_count: int = 1):
    """
    Todo: description (drawing)
    """
    if callable(arg):
        cls = arg
        cls.__is_drawing__ = True
        cls.__script_details__ = DrawingDetails(points_count)
        return with_wrapper_factory(lambda c: c)(cls)

    @with_wrapper_factory
    def decorator(cls):
        cls.__is_drawing__ = True
        cls.__script_details__ = DrawingDetails(points_count)
        return cls
    return decorator


def tb_strategy(arg=None):
    """
    Todo: description (strategy)
    """
    if callable(arg):
        cls = arg
        cls.__is_strategy__ = True
        return with_wrapper_factory(lambda c: c)(cls)

    @with_wrapper_factory
    def decorator(cls):
        cls.__is_strategy__ = True
        return cls
    return decorator


def tb_bar_type(arg=None):
    """
    Todo: description (bar_type)
    """
    if callable(arg):
        cls = arg
        cls.__is_bar_type__ = True
        return with_wrapper_factory(lambda c: c)(cls)

    @with_wrapper_factory
    def decorator(cls):
        cls.__is_bar_type__ = True
        return cls
    return decorator


def tb_tms(arg=None):
    """
    Todo: description (tms)
    """
    if callable(arg):
        cls = arg
        cls.__is_tms__ = True
        return with_wrapper_factory(lambda c: c)(cls)

    @with_wrapper_factory
    def decorator(cls):
        cls.__is_tms__ = True
        return cls
    return decorator


def tb_class(origin_type):
    """
    Decorator for internal use only.
    """
    def decorator(cls):
        cls._value = None
        cls.__tb_decorated__ = True
        orig_new = getattr(cls, "__new__", object.__new__)

        def __new__(subcls, *args, **kwargs):
            _existing = kwargs.pop("_existing", None)

            obj = orig_new(subcls)

            if cls is not subcls:
                return obj

            if hasattr(obj, "_value") and obj._value is not None:
                return obj

            if _existing is not None:
                obj._value = _existing
            else:
                processed_args = []
                for arg in args:
                    if isinstance(arg, (Enum, IntFlag)):
                        processed_args.append(get_origin_enum(cls, arg))
                    elif hasattr(arg, "_value"):
                        processed_args.append(arg._value)
                    else:
                        processed_args.append(arg)
                obj._value = origin_type(*processed_args)

            return obj

        def __init__(self, *args, **kwargs):
            pass

        def __repr__(self):
            return f"{cls.__name__}({self._value.ToString()})"

        cls.__new__ = staticmethod(__new__)
        cls.__init__ = __init__
        cls.__repr__ = __repr__
        return cls

    return decorator


def tb_interface(origin_type):
    """
    Decorator for internal use only.
    """
    def decorator(cls):
        cls._value = None
        cls.__tb_decorated__ = True
        orig_new = getattr(cls, "__new__", object.__new__)

        def __new__(subcls, *args, **kwargs):
            _existing = kwargs.pop("_existing", None)

            if _existing is not None:
                obj = orig_new(subcls)
                obj._value = _existing
                return obj

            if cls is subcls:
                raise TypeError(f"Cannot instantiate class {cls.__name__} directly")

            obj = orig_new(subcls)
            return obj

        def __init__(self, *args, **kwargs):
            pass

        def __repr__(self):
            return f"{cls.__name__}({self._value.ToString()})"

        cls.__new__ = staticmethod(__new__)
        cls.__init__ = __init__
        cls.__repr__ = __repr__
        return cls

    return decorator
