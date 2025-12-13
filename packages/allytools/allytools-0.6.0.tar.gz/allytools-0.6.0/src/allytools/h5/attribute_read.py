from dataclasses import fields, is_dataclass, MISSING
from typing import Any, Type
from allytools.h5.aid import normalize_attr_value

def get_attrs_as_dict(h5obj) -> dict[str, Any]:
    """
    Read all attributes from an HDF5 object into a plain dict (normalized).
    """
    out: dict[str, Any] = {}
    for k, v in h5obj.attrs.items():
        out[k] = normalize_attr_value(v)
    return out

def attribute_read(h5obj, cls: Type):
    """
    Construct a dataclass instance from an HDF5 object's attributes.
    Missing attributes fall back to dataclass defaults.
    """
    if not is_dataclass(cls):
        raise TypeError(f"Expected dataclass type, got {cls}")

    attrs = get_attrs_as_dict(h5obj)
    kwargs: dict[str, Any] = {}
    for f in fields(cls):
        if f.name in attrs:
            kwargs[f.name] = attrs[f.name]
        elif f.default is not MISSING or f.default_factory is not MISSING:  # type: ignore[attr-defined]
            pass
        else:
            pass
    return cls(**kwargs)
