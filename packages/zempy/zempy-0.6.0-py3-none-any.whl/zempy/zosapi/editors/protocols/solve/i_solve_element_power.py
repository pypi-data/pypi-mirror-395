from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveElementPower(ISolveData, Protocol):
    """Protocol for ISolveElementPower (refactored to inherit ISolveData; unique fields only)."""
    @property
    def Power(self) -> float: ...
    @Power.setter
    def Power(self, value: float) -> None: ...
    @property
    def Documentation(self) -> str: ...
    @property
    def set(self) -> str: ...
    @property
    def by(self) -> str: ...
