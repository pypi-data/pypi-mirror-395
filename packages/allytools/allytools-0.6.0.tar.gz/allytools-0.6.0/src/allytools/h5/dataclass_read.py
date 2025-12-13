import h5py
import numpy as np
from dataclasses import fields, is_dataclass
from typing import Any
from allytools.h5.aid import unwrap_optional


def dataclass_read(group: h5py.Group, cls: Any):
    """
    Construct dataclass `cls` from datasets/subgroups within `group`.
    - Missing fields fall back to dataclass defaults.
    - Strings/bytes normalized to str.
    - 0-d arrays / numpy scalars normalized to Python scalars.
    - ndarrays returned as numpy arrays.
    - Nested dataclasses supported if a subgroup exists under field name.
    """
    if not is_dataclass(cls):
        raise TypeError(f"Expected dataclass type, got {cls}")

    kwargs: dict[str, Any] = {}
    for f in fields(cls):
        name = f.name
        inner_t, _ = unwrap_optional(f.type)

        if name not in group:
            continue
        node = group[name]
        # subgroup → nested dataclass
        if isinstance(node, h5py.Group) and is_dataclass(inner_t):
            kwargs[name] = dataclass_read(node, inner_t)
            continue

        if not isinstance(node, h5py.Dataset):
            raise TypeError(f"Field '{name}' is not a dataset/group in '{group.name}'")

        raw = node[()]
        # arrays (ndim >= 1) → ndarray
        if isinstance(raw, np.ndarray) and raw.ndim >= 1:
            kwargs[name] = np.asarray(raw)
            continue
        # scalars → normalize
        kwargs[name] = as_python_scalar(raw)
    return cls(**kwargs)
