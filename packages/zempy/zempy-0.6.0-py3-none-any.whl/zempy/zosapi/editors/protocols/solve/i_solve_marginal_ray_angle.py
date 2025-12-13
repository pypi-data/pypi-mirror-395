from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

@runtime_checkable
class ISolveMarginalRayAngle(ISolveData, Protocol):
    """Protocol for ISolveMarginalRayAngle (refactored to inherit ISolveData; unique fields only)."""
    @property
    def Angle(self) -> float: ...
    @Angle.setter
    def Angle(self, value: float) -> None: ...
    @property
    def Documentation(self) -> str: ...
    @property
    def set(self) -> str: ...
    @property
    def by(self) -> str: ...
