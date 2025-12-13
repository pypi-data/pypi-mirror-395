import numpy as np
import h5py
from dataclasses import fields, is_dataclass
from typing import Any, Optional
from allytools.h5.h5aid import create_or_overwrite
from allytools.h5.basic.array_write import array_write

def dataclass_write(
    group: h5py.Group,
    obj: Any,
    *,
    skip_none: bool = True,
    compression: Optional[str] = None,
    overwrite: bool = True,
) -> None:
    """
    Write each dataclass field to an HDF5 dataset.
    - lists/tuples → ndarray
    - strings → UTF-8 scalar dataset
    - ndarrays → via save_array (compression/overwrite honored)
    - numpy scalars → Python scalars
    """
    if not is_dataclass(obj):
        raise TypeError(f"Expected dataclass instance, got {type(obj)}")

    for f in fields(obj):
        name = f.name
        value = getattr(obj, name)

        if skip_none and value is None:
            continue

        # lists/tuples → ndarray
        if isinstance(value, (list, tuple)):
            value = np.asarray(value)

        # strings → UTF-8 scalar dataset
        if isinstance(value, str):
            dt = h5py.string_dtype(encoding="utf-8")  # type: ignore[attr-defined]
            create_or_overwrite(group, name, overwrite=overwrite)
            group.create_dataset(name, data=np.array(value, dtype=dt))
            continue

        # ndarray → use save_array
        if isinstance(value, np.ndarray):
            array_write(group, name, value, compression=compression, overwrite=overwrite)
            continue

        # numpy scalar → Python
        if isinstance(value, np.generic):
            value = value.item()

        # everything else (ints/floats/bools)
        create_or_overwrite(group, name, overwrite=overwrite)
        group.create_dataset(name, data=value)