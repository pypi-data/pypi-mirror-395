from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar, Protocol, runtime_checkable

U = TypeVar("U", bound=Enum)

@runtime_checkable
class SupportsQuantity(Protocol[U]):
    """
    Structural protocol for any scalar with a numeric value and a unit.
    Angle, Length, Percentage, etc. can all match this.
    """

    @property
    def value(self) -> float:
        ...

    @property
    def unit(self) -> U:
        ...

class Quantity(ABC, Generic[U]):
    """
    Nominal base class for your own quantities (Angle, Length, ...).
    This is *not* a Protocol, just a regular ABC.
    """

    @property
    @abstractmethod
    def value(self) -> float:
        ...

    @property
    @abstractmethod
    def unit(self) -> U:
        ...

    def as_tuple(self) -> tuple[float, U]:
        return self.value, self.unit