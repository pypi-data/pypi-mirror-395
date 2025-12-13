import h5py
import numpy as np
from dataclasses import fields, is_dataclass
from typing import TypeVar, List
from allytools.h5.aid import import_class, concrete_type_from_annotation, enum_class_from_type
from allytools.h5.dataclass_list_cls import DATACLASS_LIST_CLS

T = TypeVar("T")


def dataclass_list_read(group: h5py.Group) -> List[T]:
    """
    Read a list of dataclass instances written by `dataclass_list_save`.
    """
    cls_name = group.attrs[DATACLASS_LIST_CLS]
    cls = import_class(cls_name)

    if not is_dataclass(cls):
        raise TypeError(f"dataclass_list_read expects a dataclass type, got {cls!r}")

    # Keep actual datasets so we can inspect attributes (unit_cls, etc.)
    datasets: dict[str, h5py.Dataset] = {
        name: dset
        for name, dset in group.items()
        if isinstance(dset, h5py.Dataset)
    }

    if not datasets:
        raise ValueError("dataclass_list_read: group has no datasets")

    # Determine N from the first dataset
    first_dset = next(iter(datasets.values()))
    if first_dset.ndim == 0:
        n_items = 1
    else:
        n_items = first_dset.shape[0]

    result: List[T] = []

    for i in range(n_items):
        kwargs: dict[str, object] = {}
        for f in fields(cls):
            name = f.name

            # If the field wasn't written (skip_none=True and all values were None)
            if name not in datasets:
                kwargs[name] = None
                continue

            dset = datasets[name]
            data = np.asarray(dset[...])

            # Per-shot slice: scalar, string, or array
            if data.ndim == 0:
                v = data[()]  # scalar
            else:
                v = data[i]

            # Convert numpy scalar to native Python scalar
            if isinstance(v, np.generic):
                v = v.item()

            # Decode bytes -> str (for vlen string datasets)
            if isinstance(v, (bytes, bytearray)):
                v = v.decode("utf-8")

            # -------- allytools units reconstruction (Length, Angle, etc.) --------
            if "unit_cls" in dset.attrs:

                # Prefer quantity_cls from attrs if present
                quantity_cls_name = dset.attrs.get("quantity_cls", None)

                if quantity_cls_name is not None:
                    quantity_cls = import_class(quantity_cls_name)
                else:
                    # Fallback: infer from the field annotation
                    quantity_cls = concrete_type_from_annotation(f.type)

                if quantity_cls is not None and v is not None:
                    unit_cls_name = dset.attrs["unit_cls"]
                    unit_cls = import_class(unit_cls_name)

                    # Restore unit either from 'unit_value' or 'unit_name'
                    unit_name = dset.attrs["unit_name"]
                    unit = getattr(unit_cls, unit_name)
                    v = quantity_cls(v, unit)
                kwargs[name] = v
                continue

            # -------- Enums reconstruction --------
            enum_cls = enum_class_from_type(f.type)
            if enum_cls is not None and v is not None:
                v = enum_cls(v)

            kwargs[name] = v

        result.append(cls(**kwargs))

    return result
