from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from allytools.types import str_or_empty
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.tools.raytrace.enums.ray_status import  RayStatus


@dataclass(frozen=True, slots=True)
class NSCSingleRayTraceData:
    """
    Adapter for ZOSAPI.Analysis.Data.IAR_NSCSingleRayTraceData.
    Provides:
      - ReadSegmentFull(segmentNumber) -> Tuple[...], with RayStatus converted to enum
      - Properties: IsValid (bool), ZRDFile (str), NumberOfSegments (int),
                    WaveIndex (int), WavelengthUM (float)
    """
    zosapi: object
    native: object

    # --- Factory ---
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "NSCSingleRayTraceData":
        if native is None:
            raise ValueError("NSCSingleRayTraceData.from_native: native is None")
        return cls(zosapi, native)

    # --- Validation ---
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="NSCSingleRayTraceData.native", exc_type=_exc.ZemaxObjectGone)

    # --- Method ---
    def ReadSegmentFull(
        self,
        segmentNumber: int,
    ) -> Tuple[
        bool,          # success
        int,           # segmentLevel
        int,           # segmentParent
        int,           # hitObj
        int,           # hitFace
        int,           # insideOf
        RayStatus,     # status (converted)
        float, float, float,   # x, y, z
        float, float, float,   # l, m, n
        float, float,          # exr, exi
        float, float,          # eyr, eyi
        float, float,          # ezr, ezi
        float,                 # intensity
        float,                 # pathLength
        int,                   # xybin
        int,                   # lmbin
        float, float, float,   # xNorm, yNorm, zNorm
        float,                 # index
        float,                 # startingPhase
        float,                 # phaseOf
        float,                 # phaseAt
    ]:
        """
        Reads a full NSC segment record and converts status to RayStatus enum.
        """
        tup = run_native(
            "NSCSingleRayTraceData.ReadSegmentFull",
            lambda: self.native.ReadSegmentFull(int(segmentNumber)),
            ensure=self.ensure_native,
        )
        # Unpack, convert the status position to enum, and re-pack
        (
            success,
            segmentLevel, segmentParent, hitObj, hitFace, insideOf,
            status_raw,
            x, y, z, l, m, n,
            exr, exi, eyr, eyi, ezr, ezi,
            intensity, pathLength, xybin, lmbin,
            xNorm, yNorm, zNorm, index,
            startingPhase, phaseOf, phaseAt,
        ) = tup

        status = RayStatus.from_native(self.zosapi, status_raw)
        return (
            bool(success),
            int(segmentLevel), int(segmentParent), int(hitObj), int(hitFace), int(insideOf),
            status,
            float(x), float(y), float(z),
            float(l), float(m), float(n),
            float(exr), float(exi), float(eyr), float(eyi), float(ezr), float(ezi),
            float(intensity),
            float(pathLength),
            int(xybin), int(lmbin),
            float(xNorm), float(yNorm), float(zNorm),
            float(index),
            float(startingPhase), float(phaseOf), float(phaseAt),
        )

    # --- Properties (descriptors) ---
    IsValid         = PropertyScalar("IsValid",         coerce_get=bool)
    ZRDFile         = PropertyScalar("ZRDFile",         coerce_get=str_or_empty)
    NumberOfSegments= PropertyScalar("NumberOfSegments",coerce_get=int)
    WaveIndex       = PropertyScalar("WaveIndex",       coerce_get=int)
    WavelengthUM    = PropertyScalar("WavelengthUM",    coerce_get=float)

    # --- Representation ---
    def __repr__(self) -> str:
        try:
            return (
                f"NSCSingleRayTraceData("
                f"IsValid={self.IsValid}, "
                f"Segments={self.NumberOfSegments}, "
                f"λ={self.WavelengthUM:.6g} μm, "
                f"ZRD='{self.ZRDFile}')"
            )
        except Exception:
            return "NSCSingleRayTraceData(<unavailable>)"
