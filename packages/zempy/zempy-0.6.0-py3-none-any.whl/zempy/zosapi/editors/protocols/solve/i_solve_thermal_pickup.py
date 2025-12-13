from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveThermalPickup(ISolveData, Protocol):
    """Protocol for ISolveThermalPickup (refactored to inherit ISolveData; unique fields only)."""
    @property
    def Configuration(self) -> int: ...
    @Configuration.setter
    def Configuration(self, value: int) -> None: ...
    @property
    def Documentation(self) -> str: ...
    @property
    def set(self) -> str: ...
    @property
    def by(self) -> str: ...
