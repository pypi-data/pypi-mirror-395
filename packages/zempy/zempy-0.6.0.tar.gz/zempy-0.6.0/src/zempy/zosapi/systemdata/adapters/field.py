from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.editors.enums.solve_type import SolveType
from zempy.zosapi.editors.enums.solve_status import SolveStatus
from zempy.zosapi.systemdata.enums.field_column import FieldColumn

if TYPE_CHECKING:
    from zempy.zosapi.system.protocols.i_optical_system import IOpticalSystem
    from zempy.zosapi.editors.protocols.i_solve_data import ISolveData

log = logging.getLogger(__name__)
@dataclass
class Field(BaseAdapter[Z, N]):
    """Adapter over ZOSAPI.SystemData.IField using descriptor-based properties."""


    IsActive = PropertyScalar("IsActive", coerce_get=bool)  # read-only
    FieldNumber = PropertyScalar("FieldNumber", coerce_get=int)  # read-only
    X = PropertyScalar("X", coerce_get=float, coerce_set=float)
    Y = PropertyScalar("Y", coerce_get=float, coerce_set=float)
    Weight = PropertyScalar("Weight", coerce_get=float, coerce_set=float)

    VDX = PropertyScalar("VDX", coerce_get=float, coerce_set=float)
    VDY = PropertyScalar("VDY", coerce_get=float, coerce_set=float)
    VCX = PropertyScalar("VCX", coerce_get=float, coerce_set=float)
    VCY = PropertyScalar("VCY", coerce_get=float, coerce_set=float)
    VAN = PropertyScalar("VAN", coerce_get=float, coerce_set=float)
    TAN = PropertyScalar("TAN", coerce_get=float, coerce_set=float)

    Comment = PropertyScalar("Comment", coerce_get=lambda v: str(v or ""), coerce_set=str)
    Ignore = PropertyScalar("Ignore", coerce_get=bool, coerce_set=bool)

    XSolve = property_enum("XSolve", SolveType)  # read-only typed view
    YSolve = property_enum("YSolve", SolveType)  # read-only typed view




    # ---- Helper matching ZOSAPI semantics ----
    def SetXY(self, x: float, y: float) -> None:
        # Use descriptors to keep logging/guards behavior consistent
        self.X = float(x)
        self.Y = float(y)

    # ---- Methods (match ZOSAPI signatures) ----
    def GetXSolveData(self) -> ISolveData:
        return run_native(
            "Field.GetXSolveData",
            lambda: self.native.GetXSolveData(),
            ensure=self.ensure_native,
        )

    def SetXPickup(self, fromField: int, fromColumn: FieldColumn, scale: float, offset: float) -> SolveStatus:
        native = run_native(
            "Field.SetXPickup",
            lambda: self.native.SetXPickup(int(fromField), fromColumn, float(scale), float(offset)),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, native)

    def SetXFixed(self) -> SolveStatus:
        native = run_native(
            "Field.SetXFixed",
            lambda: self.native.SetXFixed(),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, native)

    def GetYSolveData(self) -> ISolveData:
        return run_native(
            "Field.GetYSolveData",
            lambda: self.native.GetYSolveData(),
            ensure=self.ensure_native,
        )

    def SetYPickup(self, fromField: int, fromColumn: FieldColumn, scale: float, offset: float) -> SolveStatus:
        native = run_native(
            "Field.SetYPickup",
            lambda: self.native.SetYPickup(int(fromField), fromColumn, float(scale), float(offset)),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, native)

    def SetYFixed(self) -> SolveStatus:
        native = run_native(
            "Field.SetYFixed",
            lambda: self.native.SetYFixed(),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, native)

    def GetSolveData(self, forColumn: FieldColumn) -> ISolveData:
        return run_native(
            "Field.GetSolveData",
            lambda: self.native.GetSolveData(forColumn),
            ensure=self.ensure_native,
        )

    def SetPickup(self, forColumn: FieldColumn, fromField: int, fromColumn: FieldColumn, scale: float, offset: float) -> SolveStatus:
        native = run_native(
            "Field.SetPickup",
            lambda: self.native.SetPickup(forColumn, int(fromField), fromColumn, float(scale), float(offset)),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, native)

    def SetFixed(self, forColumn: FieldColumn) -> SolveStatus:
        native = run_native(
            "Field.SetFixed",
            lambda: self.native.SetFixed(forColumn),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, native)

    # ---- Optional snake_case shims ----
    @property
    def is_active(self) -> bool:
        return self.IsActive

    @property
    def field_number(self) -> int:
        return self.FieldNumber

    @property
    def x(self) -> float:
        return self.X

    @x.setter
    def x(self, value: float) -> None:
        self.X = value

    @property
    def y(self) -> float:
        return self.Y

    @y.setter
    def y(self, value: float) -> None:
        self.Y = value

    def set_xy(self, x: float, y: float) -> None:
        self.SetXY(x, y)

    @property
    def weight(self) -> float:
        return self.Weight

    @weight.setter
    def weight(self, value: float) -> None:
        self.Weight = value

    @property
    def vdx(self) -> float:
        return self.VDX

    @vdx.setter
    def vdx(self, value: float) -> None:
        self.VDX = value

    @property
    def vdy(self) -> float:
        return self.VDY

    @vdy.setter
    def vdy(self, value: float) -> None:
        self.VDY = value

    @property
    def vcx(self) -> float:
        return self.VCX

    @vcx.setter
    def vcx(self, value: float) -> None:
        self.VCX = value

    @property
    def vcy(self) -> float:
        return self.VCY

    @vcy.setter
    def vcy(self, value: float) -> None:
        self.VCY = value

    @property
    def van(self) -> float:
        return self.VAN

    @van.setter
    def van(self, value: float) -> None:
        self.VAN = value

    @property
    def tan(self) -> float:
        return self.TAN

    @tan.setter
    def tan(self, value: float) -> None:
        self.TAN = value

    @property
    def comment(self) -> str:
        return self.Comment

    @comment.setter
    def comment(self, value: str) -> None:
        self.Comment = value

    @property
    def ignore(self) -> bool:
        return self.Ignore

    @ignore.setter
    def ignore(self, value: bool) -> None:
        self.Ignore = value
