def obj_to_str(v: object, *, digits: int = 4) -> object:
    """
    Returns a readable name or formatted value for logging.
    - Enums: use .name
    - Floats: round/format with given precision
    - Tuples/lists of floats: same per element
    - Others: str() fallback
    """
    # Enum or object with 'name'
    if hasattr(v, "name"):
        return getattr(v, "name")

    # Single float/int
    if isinstance(v, (float, int)):
        return f"{v:.{digits}f}"

    # Tuple or list of numeric values
    if isinstance(v, (tuple, list)) and all(isinstance(x, (float, int)) for x in v):
        return "(" + ", ".join(f"{x:.{digits}f}" for x in v) + ")"

    # Length-like objects (with .value)
    if hasattr(v, "value") and isinstance(getattr(v, "value"), (float, int)):
        val = getattr(v, "value")
        return f"{val:.{digits}f}"

    # Fallback: raw string or repr
    return str(v)