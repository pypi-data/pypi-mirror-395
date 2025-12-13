from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveChiefRayHeight(ISolveData, Protocol):
    """Protocol for ISolveChiefRayHeight (refactored to inherit ISolveData; unique fields only)."""
    @property
    def Height(self) -> float: ...
    @Height.setter
    def Height(self, value: float) -> None: ...
    @property
    def Documentation(self) -> str: ...
    @property
    def set(self) -> str: ...
    @property
    def by(self) -> str: ...
