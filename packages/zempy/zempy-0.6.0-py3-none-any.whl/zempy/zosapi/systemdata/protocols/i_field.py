from __future__ import annotations
from typing import Any, Protocol, runtime_checkable
from zempy.zosapi.editors.solve.enums.solve_type import SolveType
from zempy.zosapi.editors.solve.enums.solve_status import SolveStatus
from zempy.zosapi.system.protocols.i_optical_system import IOpticalSystem


@runtime_checkable
class IField(Protocol):
    """Protocol for a Python adapter over ZOSAPI.SystemData.IField."""
    system: IOpticalSystem
    native: Any


    # ---- Optional guard hooks (recommended) ----
    def ensure_native(self) -> None: ...

    @property
    def IsActive(self) -> bool: ... # read-only

    @property
    def FieldNumber(self) -> int: ... # read-only

    @property
    def X(self) -> float: ...
    @X.setter
    def X(self, value: float) -> None: ...


    @property
    def Y(self) -> float: ...
    @Y.setter
    def Y(self, value: float) -> None: ...


    def SetXY(self, x: float, y: float) -> None: ...


    @property
    def Weight(self) -> float: ...
    @Weight.setter
    def Weight(self, value: float) -> None: ...


    @property
    def VDX(self) -> float: ...
    @VDX.setter
    def VDX(self, value: float) -> None: ...


    @property
    def VDY(self) -> float: ...
    @VDY.setter
    def VDY(self, value: float) -> None: ...


    @property
    def VCX(self) -> float: ...
    @VCX.setter
    def VCX(self, value: float) -> None: ...


    @property
    def VCY(self) -> float: ...
    @VCY.setter
    def VCY(self, value: float) -> None: ...


    @property
    def VAN(self) -> float: ...
    @VAN.setter
    def VAN(self, value: float) -> None: ...


    @property
    def TAN(self) -> float: ...
    @TAN.setter
    def TAN(self, value: float) -> None: ...


    @property
    def Comment(self) -> str: ...
    @Comment.setter
    def Comment(self, value: str) -> None: ...


    @property
    def Ignore(self) -> bool: ...
    @Ignore.setter
    def Ignore(self, value: bool) -> None: ...


    # ---- Enum-typed properties ----
    @property
    def XSolve(self) -> SolveType: ... # read-only typed view


    @property
    def YSolve(self) -> SolveType: ... # read-only typed view


    def GetXSolveData(self) -> Any: ...
    def GetYSolveData(self) -> Any: ...
    def GetSolveData(self, column: Any) -> Any: ...


    def SetXPickup(self, from_field: int, from_column: Any, scale: float = 1.0, offset: float = 0.0) -> SolveStatus: ...
    def SetXFixed(self) -> SolveStatus: ...


    def SetYPickup(self, from_field: int, from_column: Any, scale: float = 1.0, offset: float = 0.0) -> SolveStatus: ...
    def SetYFixed(self) -> SolveStatus: ...


    def SetPickup(self, column: Any, from_field: int, from_column: Any, scale: float = 1.0, offset: float = 0.0) -> SolveStatus: ...
    def SetFixed(self, column: Any) -> SolveStatus: ...