import h5py
import numpy as np

def array_read(group: h5py.Group, name: str) -> np.ndarray:
    """
    Read an HDF5 dataset as a NumPy array.
    """
    if name not in group:
        raise KeyError(f"Dataset '{name}' not found in group '{group.name}'")
    return np.asarray(group[name][()])
