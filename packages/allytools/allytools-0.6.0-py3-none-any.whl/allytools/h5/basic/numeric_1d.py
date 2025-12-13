import numpy as np
import h5py
from allytools.h5.basic.array_write import array_write

def numeric_1d_write(
    group: h5py.Group,
    name: str,
    values,
    *,
    compression=None,
    overwrite: bool = True,
) -> None:
    """
    Save a 1D numeric array using save_array.
    """
    data = np.asarray(values)
    array_write(group, name, data, compression=compression, overwrite=overwrite)


