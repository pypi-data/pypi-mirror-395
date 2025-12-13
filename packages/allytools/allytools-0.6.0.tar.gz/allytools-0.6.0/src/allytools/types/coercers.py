def str_or_empty(v): return "" if v is None else str(v)
def bool_from_int(v): return bool(int(v)) if v is not None else False
def float_or_none(v): return float(v) if v is not None else None
