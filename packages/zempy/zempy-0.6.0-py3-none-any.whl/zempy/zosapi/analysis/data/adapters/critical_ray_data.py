from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence
from allytools.types import str_or_empty
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar

from zempy.zosapi.analysis.data.adapters.critical_ray_info import CriticalRayInfo


@dataclass(frozen=True, slots=True)
class CriticalRayData:
    zosapi: object
    native: object

    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "CriticalRayData":
        if native is None:
            raise ValueError("CriticalRayData.from_native: native is None")
        return cls(zosapi, native)

    # public alias so descriptors/utilities can ensure native
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="CriticalRayData.native", exc_type=_exc.ZemaxObjectGone)

    # ---- Methods ----
    def GetRay(self, idx: int) -> CriticalRayInfo:
        native = run_native(
            "CriticalRayData.GetRay",
            lambda: self.native.GetRay(int(idx)),
            ensure=self.ensure_native,
        )
        return CriticalRayInfo.from_native(self.zosapi, native)

    # ---- Properties ----
    # scalar via descriptor
    NumRays = PropertyScalar("NumRays", coerce_get=int)

    # sequences kept as explicit properties
    @property
    def HeaderLabels(self) -> Sequence[str]:
        labels = run_native(
            "CriticalRayData.HeaderLabels get",
            lambda: self.native.HeaderLabels,
            ensure=self.ensure_native,
        )
        return [] if labels is None else [str_or_empty(v) for v in labels]

    @property
    def Rays(self) -> Sequence[CriticalRayInfo]:
        arr = run_native(
            "CriticalRayData.Rays get",
            lambda: self.native.Rays,
            ensure=self.ensure_native,
        )
        out: List[CriticalRayInfo] = []
        if arr is not None:
            for item in arr:
                out.append(CriticalRayInfo.from_native(self.zosapi, item))
        return out

    def __len__(self) -> int:
        return self.NumRays

    def __repr__(self) -> str:
        try:
            return f"CriticalRayData(NumRays={self.NumRays})"
        except Exception:
            return "CriticalRayData(<unavailable>)"
