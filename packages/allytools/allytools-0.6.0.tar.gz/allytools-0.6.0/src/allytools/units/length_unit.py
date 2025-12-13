from enum import Enum
from allytools.logger import get_logger

class LengthUnit(Enum):
    PM = (1e-9, "pm", "picometers")
    NM = (1e-6, "nm", "nanometers")
    UM = (1e-3, "µm", "micrometers")
    MM = (1.0, "mm", "millimeters")
    CM = (10.0, "cm", "centimeters")
    M = (1e3, "m", "meters")
    KM = (1e6, "km", "kilometers")
    INCH = (25.4, "in", "inches")

    def __init__(self, factor: float, symbol: str, fullname: str):
        self._factor = factor
        self._symbol = symbol
        self._fullname = fullname

    @property
    def factor(self) -> float:
        return self._factor

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def fullname(self) -> str:
        return self._fullname

    def __str__(self) -> str:
        return f"{self.symbol}"

log = get_logger(__name__)

def length_unit_from_token(token: str) -> LengthUnit | None:
    """
    Convert a raw unit token like 'µm', 'um', 'mm', 'nm', etc.
    into a LengthUnit enum.

    Order of resolution:
        1) direct match against LengthUnit.symbol
        2) normalized/prefix match
        3) return None if no match
    """

    if not token:
        log.warning("Empty length unit token")
        return None
    raw = token.strip()

    for unit in LengthUnit:
        if raw == unit.symbol:
            return unit

    if raw in ['"', "″"]:
        return LengthUnit.INCH

    t = raw.lower().replace("µ", "u")

    if t.startswith("pm"):
        return LengthUnit.PM
    if t.startswith("nm"):
        return LengthUnit.NM
    if t.startswith("um"):
        return LengthUnit.UM
    if t.startswith("mm"):
        return LengthUnit.MM
    if t.startswith("cm"):
        return LengthUnit.CM
    if t.startswith("m") and not t.startswith(("mm", "cm", "km")):
        return LengthUnit.M
    if t.startswith("km"):
        return LengthUnit.KM
    if t.startswith(("in", "inch",)):
        return LengthUnit.INCH

    log.warning("Unknown length unit token: %r", token)
    return None
