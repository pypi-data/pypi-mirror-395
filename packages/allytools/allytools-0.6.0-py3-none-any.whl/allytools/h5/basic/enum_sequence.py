import h5py
from typing import Type, TypeVar
from allytools.h5.basic.string_1d import string_1d_write
from allytools.h5.basic.numeric_1d import numeric_1d_write

E = TypeVar("E")


def enum_sequence_read(
    group: h5py.Group,
    name: str,
    enum_cls: Type[E],
) -> list[E]:
    """
    Read a sequence of enum-like values stored by save_enum_sequence.

    Assumes that enum_cls can be constructed from the stored base type
    (str or int/other numeric).
    """
    ds = group[name]
    raw = ds.asstr()[...] if h5py.check_string_dtype(ds.dtype) else ds[...]
    return [enum_cls(v) for v in raw]

def enum_sequence_write(
    group: h5py.Group,
    name: str,
    vals,
    *,
    compression=None,
    overwrite: bool = True,
) -> None:
    """
    Save a sequence of enum-like objects with .value.

    - if .value is string → 1D UTF-8 dataset
    - else → 1D numeric dataset
    """
    base_vals = [v.value for v in vals]
    base0 = base_vals[0]
    if isinstance(base0, str):
        string_1d_write(
            group,
            name,
            [str(v) for v in base_vals],
            compression=compression,
            overwrite=overwrite,
        )
    else:
        numeric_1d_write(
            group,
            name,
            base_vals,
            compression=compression,
            overwrite=overwrite,
        )
