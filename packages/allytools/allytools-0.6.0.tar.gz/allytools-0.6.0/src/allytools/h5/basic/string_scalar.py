import numpy as np
import h5py
from allytools.h5.h5aid import create_or_overwrite

def string_scalar_write(
    group: h5py.Group,
    name: str,
    value: str,
    *,
    overwrite: bool = True,
) -> None:
    """
    Save a single scalar string (UTF-8) to <name>.
    """
    dt = h5py.string_dtype(encoding="utf-8")  # type: ignore[attr-defined]
    create_or_overwrite(group, name, overwrite=overwrite)
    group.create_dataset(name, data=np.array(value, dtype=dt))

def string_scalar_read(group: h5py.Group, name: str) -> str:
    """
    Read a scalar UTF-8 string dataset written by save_string_scalar.
    """
    ds = group[name]
    return ds.asstr()[()]