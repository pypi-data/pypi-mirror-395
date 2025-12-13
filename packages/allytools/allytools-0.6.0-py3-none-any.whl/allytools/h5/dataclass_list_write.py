from __future__ import annotations
import numpy as np
import h5py
from dataclasses import fields, is_dataclass
from typing import Any, Optional, Sequence
from allytools.units.quantity import Quantity
from allytools.h5.dataclass_list_cls import DATACLASS_LIST_CLS
from allytools.h5.h5aid import create_or_overwrite
from allytools.h5.basic.array_write import array_write


def dataclass_list_write(
    group: h5py.Group,
    objs: Sequence[Any],
    *,
    skip_none: bool = True,
    compression: Optional[str] = None,
    overwrite: bool = True,
) -> None:
    if len(objs) == 0:
        raise ValueError("save_dataclass_list: 'objs' is empty")

    first = objs[0]
    if not is_dataclass(first):
        raise TypeError(f"save_dataclass_list expects dataclass instances, got {type(first)!r}")
    cls = type(first)
    group.attrs[DATACLASS_LIST_CLS] = f"{cls.__module__}.{cls.__qualname__}"
    if not all(isinstance(o, cls) for o in objs):
        raise TypeError("save_dataclass_list: all objects must have the same type")

    for f in fields(cls):
        name = f.name
        vals = [getattr(o, name) for o in objs]
        if skip_none and all(v is None for v in vals):
            continue
        v0 = vals[0]

        # -------- strings: use UTF-8 vlen dtype --------
        if isinstance(v0, str):
            dt = h5py.string_dtype(encoding="utf-8")  # type: ignore[attr-defined]
            data = np.asarray([str(v) for v in vals], dtype=dt)
            create_or_overwrite(group, name, overwrite=overwrite)
            group.create_dataset(name, data=data, compression=compression)
            continue

        # -------- numpy arrays per-shot: stack to (N, ...) --------
        if isinstance(v0, np.ndarray):
            data = np.stack(vals, axis=0)
            array_write(group, name, data, compression=compression, overwrite=overwrite)
            continue

        # -------- allytools units: objects with .value and .unit --------
        if  isinstance(v0,Quantity):
            data = np.asarray([v.value for v in vals], dtype=float)
            dset = array_write(group, name, data, compression=compression, overwrite=overwrite)
            dset.attrs["quantity_cls"] = f"{type(v0).__module__}.{type(v0).__qualname__}"
            unit0 = v0.unit
            dset.attrs["unit_cls"] = f"{type(unit0).__module__}.{type(unit0).__qualname__}"
            dset.attrs["unit_name"] = unit0.name

            continue

        if isinstance(v0, (int, float, bool, np.generic)):
            data = np.asarray(vals)
            array_write(group, name, data, compression=compression, overwrite=overwrite)
            continue

        # -------- enums or objects with .value -> store underlying value --------
        if hasattr(v0, "value") and not isinstance(v0, (str, bytes)):
            base_vals = [v.value for v in vals]
            base0 = base_vals[0]
            if isinstance(base0, str):
                dt = h5py.string_dtype(encoding="utf-8")  # type: ignore[attr-defined]
                data = np.asarray([str(v) for v in base_vals], dtype=dt)
                create_or_overwrite(group, name, overwrite=overwrite)
                group.create_dataset(name, data=data, compression=compression)
            else:
                data = np.asarray(base_vals)
                array_write(group, name, data, compression=compression, overwrite=overwrite)
            continue

        # -------- fallback: store as UTF-8 strings --------
        dt = h5py.string_dtype(encoding="utf-8")  # type: ignore[attr-defined]
        data = np.asarray([str(v) for v in vals], dtype=dt)
        create_or_overwrite(group, name, overwrite=overwrite)
        group.create_dataset(name, data=data, compression=compression)
