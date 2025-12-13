from typing import Any, Optional
import re
import unicodedata

FALSEY_TOKENS = {"", "none", "null", "nan", "n/a", "-"}

def clean_str(val: Any) -> Optional[str]:
    """Normalizes a label-like value: trims, collapses whitespace, and returns None for empty/falsey tokens"""
    if val is None:
        return None
    s = unicodedata.normalize("NFC", str(val).strip())
    if not s:
        return None
    s_norm = " ".join(s.split())  # collapse multiple spaces/tabs/newlines
    return None if s_norm.lower() in FALSEY_TOKENS else s_norm

def sanitize(st: str) -> str:
    """Makes a filename-safe slug: replaces / with -, strips, removes illegal chars, and collapses repeated _."""
    st = st.replace('/', '-').strip()
    st = re.sub(r'[^\w\-.]+', '_', st)   # keep letters/digits/_-. only
    st = re.sub(r'_{2,}', '_', st)       # collapse multiple underscores
    return st

def ensure_str(val: Optional[str], fallback: str = "None") -> str:
    """Turn None into a string (or another given fallback)."""
    return fallback if val is None else str(val)

def first_token(s: Optional[str]) -> str:
    """Return substring before the first space, safely handling None and extra whitespace."""
    if not s:
        return ""
    s = s.strip()
    return s.split(maxsplit=1)[0]