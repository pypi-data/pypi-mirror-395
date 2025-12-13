from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Any
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.editors.enums.cell_data_type import CellDataType
from zempy.zosapi.editors.enums.solve_type import SolveType
from zempy.zosapi.editors.enums.solve_status import SolveStatus
from zempy.zosapi.editors.adapters.editor_row import EditorRow

if TYPE_CHECKING:
    from zempy.zosapi.editors.protocols.i_solve_data import ISolveData



@dataclass
class EditorCell(BaseAdapter[Z, N]):

    Row = property_adapter(        "Row", adapter=EditorRow)
    Col = PropertyScalar("Col", coerce_get=int)
    IsActive = PropertyScalar("IsActive", coerce_get=bool)
    IsReadOnly = PropertyScalar("IsReadOnly", coerce_get=bool)
    Header = PropertyScalar("Header", coerce_get=str)
    IntegerValue = PropertyScalar("IntegerValue", coerce_get=int, coerce_set=int)
    DoubleValue = PropertyScalar("DoubleValue", coerce_get=float, coerce_set=float)
    Value = PropertyScalar("Value", coerce_get=str, coerce_set=str)
    DataType = property_enum("DataType", CellDataType)
    Solve = property_enum("Solve", SolveType)


    def Clear(self) -> None:
        run_native("EditorCell.Clear", lambda: self.native.Clear(), ensure=self.ensure_native)

    def ClearSolve(self) -> SolveStatus:
        raw = run_native(
            "EditorCell.ClearSolve",
            lambda: self.native.ClearSolve(),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, raw)

    def SetSolve(self, solve: ISolveData | Any) -> SolveStatus:
        native_solve = getattr(solve, "native", solve)
        raw = run_native(
            "EditorCell.SetSolve",
            lambda: self.native.SetSolve(native_solve),
            ensure=self.ensure_native,
        )
        return SolveStatus.from_native(self.zosapi, raw)

    def SetPickup(
        self,
        source_row: int,
        source_col: int,
        scale: float = 1.0,
        offset: float = 0.0,
        invert: bool = False,
        operand: Optional[str] = None,
    ) -> None:
        def _call():
            if operand is None:
                return self.native.SetPickup(
                    source_row, source_col, float(scale), float(offset), bool(invert)
                )
            return self.native.SetPickup(
                source_row,
                source_col,
                float(scale),
                float(offset),
                bool(invert),
                operand,
            )
        run_native("EditorCell.SetPickup", _call, ensure=self.ensure_native)
