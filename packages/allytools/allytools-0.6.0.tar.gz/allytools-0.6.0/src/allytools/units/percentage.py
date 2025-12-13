from enum import Enum
from dataclasses import dataclass

from allytools.units.quantity import Quantity

class PercentageUnit(Enum):
    PERCENT = "%"

@dataclass(frozen=True)
class Percentage(Quantity[PercentageUnit]):
    _value: float  # numeric percent, e.g., 37.5 → 37.5%

    @property
    def value(self) -> float:
        return self._value

    @property
    def unit(self) -> PercentageUnit:
        return PercentageUnit.PERCENT

    def as_fraction(self) -> float:
        return self.value / 100.0

    def __str__(self):
        return f"{self.value:.2f}%"
