import numpy as np
import enum
from typing import Any, Union, get_args, get_origin
from importlib import import_module

def unwrap_optional(tp: Any) -> tuple[Any, bool]:
    """
    Return (inner_type, is_optional) for `Optional[T]` / `T | None` / `Union[T, None]`.
    """
    origin = get_origin(tp)
    if origin is Union:
        args = get_args(tp)
        if type(None) in args:
            non_none = [a for a in args if a is not type(None)]
            return (non_none[0] if non_none else Any), True
    return tp, False


def normalize_attr_value(v: Any):
    """
    Normalize an attribute read from HDF5 into Python-friendly types.
    """
    if isinstance(v, np.ndarray) and v.shape == ():
        v = v[()]
    if isinstance(v, np.generic):
        v = v.item()
    if isinstance(v, bytes):
        v = v.decode("utf-8", errors="replace")
    return v


def import_class(full_name: str):
    module_name, cls_name = full_name.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, cls_name)

def enum_class_from_type(tp: object) -> type[enum.Enum] | None:
    """
    Try to extract an Enum class from a field annotation type.
    Handles bare Enum and Optional[Enum] / Union[Enum, None].
    """
    # Simple case: direct Enum subclass
    try:
        if isinstance(tp, type) and issubclass(tp, enum.Enum):
            return tp
    except TypeError:
        pass

    # Typing constructs: Optional[...] / Union[...]
    origin = get_origin(tp)
    if origin is None:
        return None

    for arg in get_args(tp):
        try:
            if isinstance(arg, type) and issubclass(arg, enum.Enum):
                return arg
        except TypeError:
            continue

    return None

def concrete_type_from_annotation(tp: object) -> type | None:
    """
    Extract the concrete (non-None) type from an annotation.

    Examples:
      - Length                -> Length
      - Optional[Length]      -> Length
      - Union[Length, None]   -> Length
    """
    if isinstance(tp, type):
        return tp

    origin = get_origin(tp)
    if origin is None:
        return None

    for arg in get_args(tp):
        if arg is type(None):
            continue
        if isinstance(arg, type):
            return arg

    return None