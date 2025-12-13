from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveChiefRayNormal(ISolveData, Protocol):
    """Protocol for ISolveChiefRayNormal (refactored to inherit ISolveData; unique fields only)."""
    @property
    def by(self) -> str: ...
