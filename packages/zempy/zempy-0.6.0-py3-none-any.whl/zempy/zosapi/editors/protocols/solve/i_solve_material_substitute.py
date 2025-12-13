from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveMaterialSubstitute(ISolveData, Protocol):
    """Protocol for ISolveMaterialSubstitute (refactored to inherit ISolveData; unique fields only)."""
    @property
    def Catalog(self) -> str: ...
    @Catalog.setter
    def Catalog(self, value: str) -> None: ...
    @property
    def Documentation(self) -> str: ...
    @property
    def set(self) -> str: ...
    @property
    def by(self) -> str: ...
