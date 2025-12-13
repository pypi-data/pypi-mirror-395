from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List

from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc


@dataclass(frozen=True, slots=True)
class VectorData:
    zosapi: object
    native: object

    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "VectorData":
        if native is None:
            raise ValueError("VectorData.from_native: native is None")
        return cls(zosapi, native)

    # ensure= callback for run_native
    def _ensure_native(self) -> None:
        ensure_not_none(
            self.native,
            what="VectorData.native",
            exc_type=_exc.ZemaxObjectGone,   # <-- pass the required exception type
        )

    # -------- properties --------
    @property
    def IsReadOnly(self) -> bool:
        return bool(run_native(
            "VectorData.IsReadOnly get",
            lambda: getattr(self.native, "IsReadOnly"),
            ensure=self._ensure_native,
        ))

    @property
    def Length(self) -> int:
        return int(run_native(
            "VectorData.Length get",
            lambda: getattr(self.native, "Length"),
            ensure=self._ensure_native,
        ))

    @property
    def Data(self) -> List[float]:
        data = run_native(
            "VectorData.Data get",
            lambda: getattr(self.native, "Data"),
            ensure=self._ensure_native,
        )
        return [float(x) for x in data] if data is not None else []

    @Data.setter
    def Data(self, values: List[float]) -> None:
        if self.IsReadOnly:
            raise PermissionError("VectorData is read-only; cannot set Data.")
        run_native(
            "VectorData.Data set",
            lambda: setattr(self.native, "Data", list(values)),
            ensure=self._ensure_native,
        )

    # -------- original COM methods --------
    def ReadData(self, Size: int, Data: List[float]) -> None:
        run_native(
            "VectorData.ReadData",
            lambda: self.native.ReadData(int(Size), Data),
            ensure=self._ensure_native,
        )

    def WriteData(self, Size: int, Data: List[float]) -> None:
        if self.IsReadOnly:
            raise PermissionError("VectorData is read-only; cannot write.")
        run_native(
            "VectorData.WriteData",
            lambda: self.native.WriteData(int(Size), Data),
            ensure=self._ensure_native,
        )

    def GetValueAt(self, position: int) -> float:
        return float(run_native(
            "VectorData.GetValueAt",
            lambda: self.native.GetValueAt(int(position)),
            ensure=self._ensure_native,
        ))

    def SetValueAt(self, position: int, Value: float) -> None:
        if self.IsReadOnly:
            raise PermissionError("VectorData is read-only; cannot set element.")
        run_native(
            "VectorData.SetValueAt",
            lambda: self.native.SetValueAt(int(position), float(Value)),
            ensure=self._ensure_native,
        )

    # -------- helpers --------
    def to_list(self) -> List[float]:
        return self.Data

    def set_from(self, values: Iterable[float]) -> None:
        vals = list(values)
        self.WriteData(len(vals), vals)

    def fill(self, value: float) -> None:
        n = self.Length
        self.WriteData(n, [float(value)] * n)

    def __len__(self) -> int:
        return self.Length

    def __repr__(self) -> str:
        n = self.Length
        readonly = "ro" if self.IsReadOnly else "rw"
        preview = self.Data[:5]
        more = "…" if n > 5 else ""
        return f"VectorData<{readonly}>[{n}]: {preview}{more}"
