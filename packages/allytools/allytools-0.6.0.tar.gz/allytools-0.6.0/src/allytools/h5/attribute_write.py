from __future__ import annotations
from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any
import numpy as np
import h5py

def _to_hdf5_attr_value(v: Any):
    """
    Normalize Python/NumPy value into an HDF5-attribute-safe value.
    - Scalars: Python scalars
    - Strings: variable-length UTF-8
    - Small numeric arrays: NumPy arrays
    """
    if v is None:
        return None

    if isinstance(v, np.generic):
        v = v.item()

    if isinstance(v, Enum):
        v = v.value

    if isinstance(v, bytes):
        v = v.decode("utf-8", errors="replace")

    if isinstance(v, (list, tuple)):
        v = np.asarray(v)

    if isinstance(v, np.ndarray):
        if v.dtype.kind in {"U", "S", "O"}:
            raise TypeError("Arrays of strings are not supported as HDF5 attributes; use a dataset.")
        return v

    if isinstance(v, str):
        return np.array(v, dtype=h5py.string_dtype(encoding="utf-8"))  # type: ignore[attr-defined]

    if isinstance(v, np.datetime64):
        return np.array(str(v.astype("datetime64[ns]")), dtype=h5py.string_dtype("utf-8"))  # type: ignore[attr-defined]

    return v


def attribute_write(h5obj, obj, *, skip_none: bool = True) -> None:
    """
    Copy fields from a dataclass (or items from a dict) into HDF5 attributes.
    Overwrites existing attributes.
    """
    if is_dataclass(obj):
        items = ((f.name, getattr(obj, f.name)) for f in fields(obj))
    elif isinstance(obj, dict):
        items = obj.items()
    else:
        raise TypeError(f"Expected dataclass or dict, got {type(obj)}")

    for k, v in items:
        if skip_none and v is None:
            continue
        norm = _to_hdf5_attr_value(v)
        if norm is None and skip_none:
            continue
        h5obj.attrs[k] = norm

