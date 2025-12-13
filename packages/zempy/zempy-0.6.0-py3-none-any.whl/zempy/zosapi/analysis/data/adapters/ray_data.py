from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence, TYPE_CHECKING
from allytools.types import str_or_empty
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.analysis.data.adapters.ray_info import RayInfo

if TYPE_CHECKING:
    from zempy.zosapi.analysis.data.protocols.iar_ray_data import IAR_RayData as IAR_RayDataProto
    from zempy.zosapi.analysis.data.protocols.iar_ray_info import IAR_RayInfo as IAR_RayInfoProto




@dataclass(frozen=True, slots=True)
class RayData:
    """
    Adapter for ZOSAPI.Analysis.Data.IAR_RayData.
    Exposes:
      - Methods: GetRay(idx) -> RayInfo
      - Properties: Description: str, NumRays: int, Rays: Sequence[RayInfo]
    """
    zosapi: object
    native: "IAR_RayDataProto"

    # --- Factory ---
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "RayData":
        if native is None:
            raise ValueError("RayData.from_native: native is None")
        return cls(zosapi, native)

    # --- Validation ---
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="RayData.native", exc_type=_exc.ZemaxObjectGone)

    # --- Methods ---
    def GetRay(self, idx: int) -> "IAR_RayInfoProto":
        from zempy.zosapi.analysis.data.adapters.ray_info import RayInfo
        native = run_native(
            "RayData.GetRay",
            lambda: self.native.GetRay(int(idx)),
            ensure=self.ensure_native,
        )
        return RayInfo.from_native(self.zosapi, native)

    # --- Scalar properties ---
    Description = PropertyScalar("Description", coerce_get=str_or_empty)
    NumRays     = PropertyScalar("NumRays",     coerce_get=int)

    # --- Collections ---
    @property
    def Rays(self) -> Sequence["IAR_RayInfoProto"]:
        from zempy.zosapi.analysis.data.adapters.ray_info import RayInfo
        raw = run_native(
            "RayData.Rays get",
            lambda: self.native.Rays,
            ensure=self.ensure_native,
        )
        out: List[RayInfo] = []
        if raw:
            for native_item in raw:
                out.append(RayInfo.from_native(self.zosapi, native_item))
        return out

    # --- Convenience ---
    def __len__(self) -> int:
        return self.NumRays

    def __repr__(self) -> str:
        try:
            return f"RayData(NumRays={self.NumRays}, Description='{self.Description}')"
        except Exception:
            return "RayData(<unavailable>)"
