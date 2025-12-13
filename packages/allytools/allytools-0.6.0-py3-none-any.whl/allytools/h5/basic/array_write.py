import h5py
import numpy as np
from typing import Optional
from allytools.h5.h5aid import create_or_overwrite

def array_write(
    group: h5py.Group,
    name: str,
    array: np.ndarray,
    *,
    compression: Optional[str] = "gzip",
    overwrite: bool = True,
) -> h5py.Dataset:
    """
    Save a NumPy array to an HDF5 dataset (optionally compressed).

    Returns
    -------
    h5py.Dataset
        The created dataset object (allows chaining).
    """
    if not isinstance(array, np.ndarray):
        raise TypeError(f"Expected np.ndarray, got {type(array)}")

    create_or_overwrite(group, name, overwrite=overwrite)
    dset = group.create_dataset(name, data=array, compression=compression)
    return dset
