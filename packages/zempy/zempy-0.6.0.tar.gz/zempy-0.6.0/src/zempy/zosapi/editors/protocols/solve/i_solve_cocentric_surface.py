from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveCocentricSurface(ISolveData, Protocol):
    """Protocol for ISolveCocentricSurface (refactored to inherit ISolveData; unique fields only)."""
    @property
    def AboutSurface(self) -> int: ...
    @AboutSurface.setter
    def AboutSurface(self, value: int) -> None: ...
    @property
    def Documentation(self) -> str: ...
    @property
    def set(self) -> str: ...
    @property
    def by(self) -> str: ...
