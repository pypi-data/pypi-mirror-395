import numpy as np
from typing import Any, Optional
from contextlib import suppress

#Give me a name string I can look up
def coerce_to_str(raw) -> Optional[str]:
    if isinstance(raw, str):
        return raw
    to_str = getattr(raw, "ToString", None)
    if callable(to_str):
        with suppress(Exception):
            return str(to_str())
    return None


#Give me a printable, serializable Python object
def coerce_value(v: Any) -> Any:
    """
    Convert arbitrary low-level data values into native Python types.
    This helper safely normalizes values read from h5py, NumPy, or other I/O libraries:
      - Decodes byte strings (UTF-8 by default)
      - Converts 0-D NumPy scalars to Python scalars via `.item()`
      - Leaves normal Python types and arrays untouched
      - Always returns something serializable (or at least printable)

    Examples
    --------
    >>> coerce_value(b"hello")
    'hello'
    >>> coerce_value(np.int32(42))
    42
    >>> coerce_value(np.array([1, 2, 3]))
    array([1, 2, 3])
    >>> coerce_value("ok")
    'ok'
    """
    # --- decode raw bytes to string ---
    if isinstance(v, (bytes, bytearray, memoryview)):
        try:
            return v.decode("utf-8", errors="replace")
        except Exception:
            # fallback: represent as hex or str if undecodable
            try:
                return v.hex() if isinstance(v, (bytes, bytearray)) else str(v)
            except Exception:
                return str(v)

    # --- unwrap NumPy scalar values (0-D arrays or scalars) ---
    # np.isscalar() is False for np.array(1), so check shape=() too
    if isinstance(v, np.generic):
        try:
            return v.item()
        except Exception:
            pass
    elif hasattr(v, "shape") and getattr(v, "shape", ()) == ():
        try:
            return np.asarray(v).item()
        except Exception:
            pass

    # --- handle lists or tuples recursively if desired ---
    if isinstance(v, (list, tuple)):
        return type(v)(coerce_value(x) for x in v)

    # --- leave everything else as-is ---
    return v
