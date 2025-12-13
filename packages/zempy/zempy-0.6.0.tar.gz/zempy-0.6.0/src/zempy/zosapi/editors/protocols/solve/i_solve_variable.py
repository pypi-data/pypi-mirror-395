from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveVariable(ISolveData, Protocol):
    """Protocol for ISolveVariable (refactored to inherit ISolveData; unique fields only)."""
    @property
    def by(self) -> str: ...
