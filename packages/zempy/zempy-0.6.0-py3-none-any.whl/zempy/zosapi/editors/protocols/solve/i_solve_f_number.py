from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveFNumber(ISolveData, Protocol):
    """Protocol for ISolveFNumber (refactored to inherit ISolveData; unique fields only)."""
    @property
    def FNumber(self) -> float: ...
    @FNumber.setter
    def FNumber(self, value: float) -> None: ...
    @property
    def Documentation(self) -> str: ...
    @property
    def set(self) -> str: ...
    @property
    def by(self) -> str: ...
