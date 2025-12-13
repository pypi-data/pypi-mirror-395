import h5py
from allytools.h5.aid import normalize_attr_value
def create_or_overwrite(group: h5py.Group, name: str, *, overwrite: bool) -> None:
    """
    Ensure `group[name]` is free to create. Delete if exists and overwrite=True.
    """
    if name in group:
        if overwrite:
            del group[name]
        else:
            raise KeyError(f"Dataset '{name}' already exists in group '{group.name}'")

def require_h5_version(
    node: h5py.File | h5py.Group,
    *,
    attr: str,
    expected: str | int,
) -> str:
    if attr not in node.attrs:
        raise KeyError(f"Missing HDF5 format attribute {attr!r}; "
                       f"file is invalid or uses an older format.")
    raw_version = node.attrs[attr]
    file_version = normalize_attr_value(raw_version)
    expected_str = str(expected)
    if file_version != expected_str:
        raise ValueError(f"HDF5 format version mismatch: found {file_version!r}, expected {expected_str!r}.")
    return file_version
