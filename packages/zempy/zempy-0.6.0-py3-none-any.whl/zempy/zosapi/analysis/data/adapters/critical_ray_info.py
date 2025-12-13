from __future__ import annotations
from dataclasses import dataclass

from zempy.zosapi.core.interop import ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.tools.enums.critical_ray_type import CriticalRayType


@dataclass(frozen=True, slots=True)
class CriticalRayInfo:
    """Adapter for ZOSAPI.Analysis.Data.IAR_CriticalRayInfo."""
    zosapi: object
    native: object

    # --- Factory ---
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "CriticalRayInfo":
        if native is None:
            raise ValueError("CriticalRayInfo.from_native: native is None")
        return cls(zosapi, native)

    # --- Validation ---
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="CriticalRayInfo.native", exc_type=_exc.ZemaxObjectGone)

    # ---- Identifiers / classification ----
    FieldPoint        = PropertyScalar("FieldPoint",        coerce_get=int)
    RayType           = property_enum("RayType", CriticalRayType)
    Pass_             = PropertyScalar("Pass",              coerce_get=bool)   # COM name 'Pass'
    TerminationObject = PropertyScalar("TerminationObject", coerce_get=int)

    # ---- Physical parameters ----
    Wavelength = PropertyScalar("Wavelength", coerce_get=float)

    # ---- Input vector ----
    XIn = PropertyScalar("XIn", coerce_get=float)
    YIn = PropertyScalar("YIn", coerce_get=float)
    ZIn = PropertyScalar("ZIn", coerce_get=float)
    LIn = PropertyScalar("LIn", coerce_get=float)
    MIn = PropertyScalar("MIn", coerce_get=float)
    NIn = PropertyScalar("NIn", coerce_get=float)

    # ---- Target vector ----
    XTarget = PropertyScalar("XTarget", coerce_get=float)
    YTarget = PropertyScalar("YTarget", coerce_get=float)
    ZTarget = PropertyScalar("ZTarget", coerce_get=float)
    LTarget = PropertyScalar("LTarget", coerce_get=float)
    MTarget = PropertyScalar("MTarget", coerce_get=float)
    NTarget = PropertyScalar("NTarget", coerce_get=float)

    # ---- Actual vector ----
    XActual = PropertyScalar("XActual", coerce_get=float)
    YActual = PropertyScalar("YActual", coerce_get=float)
    ZActual = PropertyScalar("ZActual", coerce_get=float)
    LActual = PropertyScalar("LActual", coerce_get=float)
    MActual = PropertyScalar("MActual", coerce_get=float)
    NActual = PropertyScalar("NActual", coerce_get=float)

    # ---- Representation ----
    def __repr__(self) -> str:
        try:
            return (
                f"CriticalRayInfo("
                f"FP={self.FieldPoint}, "
                f"RayType={self.RayType.name}, "
                f"λ={self.Wavelength:.6g} μm)"
            )
        except Exception:
            return "CriticalRayInfo(<unavailable>)"
