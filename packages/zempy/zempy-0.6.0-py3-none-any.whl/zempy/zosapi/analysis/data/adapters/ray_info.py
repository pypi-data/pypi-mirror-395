from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.core.interop import ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar


@dataclass(frozen=True, slots=True)
class RayInfo:
    """Adapter for ZOSAPI.Analysis.Data.IAR_RayInfo."""
    zosapi: object
    native: object

    # --- Factory ---
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "RayInfo":
        if native is None:
            raise ValueError("RayInfo.from_native: native is None")
        return cls(zosapi, native)

    # --- Validation ---
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="RayInfo.native", exc_type=_exc.ZemaxObjectGone)

    # ---- Integer identifiers ----
    RayIndex   = PropertyScalar("RayIndex",   coerce_get=int)
    Segment    = PropertyScalar("Segment",    coerce_get=int)
    Parent     = PropertyScalar("Parent",     coerce_get=int)
    Level      = PropertyScalar("Level",      coerce_get=int)
    In_object  = PropertyScalar("In_object",  coerce_get=int)  # COM uses 'In_object'
    Hit_object = PropertyScalar("Hit_object", coerce_get=int)
    Hit_face   = PropertyScalar("Hit_face",   coerce_get=int)
    Vignetted  = PropertyScalar("Vignetted",  coerce_get=int)
    Error      = PropertyScalar("Error",      coerce_get=int)

    # ---- Spatial coordinates ----
    X = PropertyScalar("X", coerce_get=float)
    Y = PropertyScalar("Y", coerce_get=float)
    Z = PropertyScalar("Z", coerce_get=float)

    # ---- Direction cosines ----
    L = PropertyScalar("L", coerce_get=float)
    M = PropertyScalar("M", coerce_get=float)
    N = PropertyScalar("N", coerce_get=float)

    # ---- Surface normal vector components ----
    Nx = PropertyScalar("Nx", coerce_get=float)
    Ny = PropertyScalar("Ny", coerce_get=float)
    Nz = PropertyScalar("Nz", coerce_get=float)

    # ---- Electric field components ----
    Ex = PropertyScalar("Ex", coerce_get=float)
    Ey = PropertyScalar("Ey", coerce_get=float)
    Ez = PropertyScalar("Ez", coerce_get=float)

    # ---- Path / wavelength info ----
    PathLength        = PropertyScalar("PathLength",        coerce_get=float)
    OpticalPathLength = PropertyScalar("OpticalPathLength", coerce_get=float)
    Wavelength        = PropertyScalar("Wavelength",        coerce_get=float)

    # --- Representation ---
    def __repr__(self) -> str:
        try:
            return (
                f"RayInfo("
                f"idx={self.RayIndex}, seg={self.Segment}, "
                f"pos=({self.X:.6g},{self.Y:.6g},{self.Z:.6g}), "
                f"dir=({self.L:.6g},{self.M:.6g},{self.N:.6g}), "
                f"λ={self.Wavelength:.6g} μm)"
            )
        except Exception:
            return "RayInfo(<unavailable>)"
