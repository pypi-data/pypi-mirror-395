from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence

from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar


@dataclass
class MatrixData(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Common.IMatrixData."""

    IsReadOnly   = PropertyScalar("IsReadOnly",   coerce_get=bool)
    Rows         = PropertyScalar("Rows",         coerce_get=int)
    Cols         = PropertyScalar("Cols",         coerce_get=int)
    TotalLength  = PropertyScalar("TotalLength",  coerce_get=int)

    # ---------- Data (2D) ----------
    @property
    def Data(self) -> List[List[float]]:
        """Return the full 2D data as a nested Python list (row-major)."""
        raw = run_native(
            "MatrixData.Data get",
            lambda: getattr(self.native, "Data"),
            ensure=self.ensure_native,
        )
        return [list(map(float, row)) for row in raw]

    @Data.setter
    def Data(self, values: Sequence[Sequence[float]]) -> None:
        if self.IsReadOnly:
            raise PermissionError("MatrixData is read-only; cannot set Data.")
        payload = [list(map(float, row)) for row in values]
        run_native(
            "MatrixData.Data set",
            lambda: setattr(self.native, "Data", payload),
            ensure=self.ensure_native,
        )

    # ---------- COM methods ----------
    def ReadData(self, Size: int, Data: List[float]) -> None:
        """Populate `Data` with Size = Rows * Cols elements (row-major)."""
        expected = self.TotalLength
        if int(Size) != expected:
            raise ValueError(f"Size mismatch: got {Size}, expected {expected}.")
        run_native(
            "MatrixData.ReadData",
            lambda: self.native.ReadData(int(Size), Data),
            ensure=self.ensure_native,
        )

    def WriteData(self, Size: int, Data: List[float]) -> None:
        """Write `Size` elements from `Data` into the matrix (row-major)."""
        if self.IsReadOnly:
            raise PermissionError("MatrixData is read-only; cannot write.")
        expected = self.TotalLength
        if int(Size) != expected:
            raise ValueError(f"Size mismatch: got {Size}, expected {expected}.")
        if len(Data) != expected:
            raise ValueError(f"Data length mismatch: got {len(Data)}, expected {expected}.")
        run_native(
            "MatrixData.WriteData",
            lambda: self.native.WriteData(int(Size), Data),
            ensure=self.ensure_native,
        )

    def GetValueAt(self, Row: int, Col: int) -> float:
        rows, cols = self.Rows, self.Cols
        if not (0 <= Row < rows and 0 <= Col < cols):
            raise IndexError(f"Index out of bounds: ({Row}, {Col}) not in [0..{rows-1}]x[0..{cols-1}].")
        return float(
            run_native(
                "MatrixData.GetValueAt",
                lambda: self.native.GetValueAt(int(Row), int(Col)),
                ensure=self.ensure_native,
            )
        )

    def SetValueAt(self, Row: int, Col: int, Value: float) -> None:
        if self.IsReadOnly:
            raise PermissionError("MatrixData is read-only; cannot set element.")
        rows, cols = self.Rows, self.Cols
        if not (0 <= Row < rows and 0 <= Col < cols):
            raise IndexError(f"Index out of bounds: ({Row}, {Col}) not in [0..{rows-1}]x[0..{cols-1}].")
        run_native(
            "MatrixData.SetValueAt",
            lambda: self.native.SetValueAt(int(Row), int(Col), float(Value)),
            ensure=self.ensure_native,
        )

    # ---------- Pythonic helpers ----------
    def to_list(self) -> List[List[float]]:
        """Return a nested list copy of the matrix (row-major)."""
        return self.Data

    def to_flat_list(self) -> List[float]:
        """Return all values as a single flattened list (row-major)."""
        data = self.Data
        return [x for row in data for x in row]

    def set_from(self, values: Sequence[Sequence[float]]) -> None:
        """Replace entire matrix contents from a 2D sequence with shape validation."""
        rows, cols = self.Rows, self.Cols
        if len(values) != rows or (rows and len(values[0]) != cols):
            incoming_cols = len(values[0]) if values else 0
            raise ValueError(f"Shape mismatch: incoming {len(values)}x{incoming_cols}, expected {rows}x{cols}.")
        flat: List[float] = [float(x) for row in values for x in row]
        self.WriteData(rows * cols, flat)

    def fill(self, value: float) -> None:
        """Fill all elements with the same value."""
        n = self.TotalLength
        self.WriteData(n, [float(value)] * n)

    def __len__(self) -> int:
        return self.Rows

    def __repr__(self) -> str:
        rows, cols = self.Rows, self.Cols
        readonly = "ro" if self.IsReadOnly else "rw"
        data = self.Data
        preview = [row[:3] for row in data[:3]]
        more = "…" if rows > 3 or cols > 3 else ""
        return f"MatrixData<{readonly}>[{rows}x{cols}]: {preview}{more}"
