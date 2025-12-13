from enum import Enum
from math import pi

from enum import Enum
from math import pi


class AngleUnit(Enum):
    # factor = radians per unit
    DEG = (pi / 180.0, "°", "degrees")
    RAD = (1.0, "rad", "radians")
    MRAD = (1e-3, "mrad", "milliradians")

    def __init__(self, factor: float, symbol: str, fullname: str):
        self._factor = factor  # how many radians in 1 unit
        self._symbol = symbol
        self._fullname = fullname

    @property
    def factor(self) -> float:
        """Conversion factor to radians."""
        return self._factor

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def fullname(self) -> str:
        return self._fullname

    def __str__(self) -> str:
        return self.symbol
