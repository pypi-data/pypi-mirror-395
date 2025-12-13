import numpy as np
import h5py
from allytools.h5.h5aid import create_or_overwrite


def string_1d_write(
    group: h5py.Group,
    name: str,
    strings,
    *,
    compression=None,
    overwrite: bool = True,
) -> None:
    """
    Save a 1D array of strings (UTF-8 vlen) to <name>.
    """
    dt = h5py.string_dtype(encoding="utf-8")  # type: ignore[attr-defined]
    data = np.asarray(strings, dtype=dt)
    create_or_overwrite(group, name, overwrite=overwrite)
    group.create_dataset(name, data=data, compression=compression)

def string_1d_read(group: h5py.Group, name: str) -> np.ndarray:
    """
    Read a 1D UTF-8 string dataset written by save_string_1d.
    Returns np.ndarray of dtype '<U...' or 'object' with Python str.
    """
    ds = group[name]
    return ds.asstr()[...]  # h5py converts to str