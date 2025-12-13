from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native, validate_cast,
    PropertyScalar, dataclass,
)

from zempy.zosapi.tools.raytrace.enums.nsc_trace_options import NSCTraceOptions
from zempy.zosapi.tools.raytrace.results import RayNSCResult, RayNSCSegment

@dataclass()
class RayTraceNSCData(BaseAdapter[Z, N]):
    """Adapter for **ZOSAPI.Tools.RayTrace.IRayTraceNSCData**.

    Typical usage:
        buf = tools.OpenBatchRayTrace().CreateNSC(MaxRays, maxSegments, coherenceLength)
        buf.ClearData()
        buf.AddRay(wave, surf, NSCTraceOptions.Standard, X, Y, Z, L, M, N, InsideOf, exr, exi, eyr, eyi, ezr, ezi)
        buf.StartReadingResults()
        ok, *res = buf.ReadNextResult()
        ok, *seg = buf.ReadNextSegment()
    """

    # -------------------------- Properties --------------------------
    NumberOfRays = PropertyScalar("NumberOfRays", coerce_get=int)
    MaxRays      = PropertyScalar("MaxRays",      coerce_get=int)
    HasResultData = PropertyScalar("HasResultData", coerce_get=bool)

    # --------------------------- Methods ----------------------------
    def ClearData(self) -> None:
        run_native(
            "IRayTraceNSCData.ClearData",
            lambda: self.native.ClearData(),
            ensure=self.ensure_native,
        )

    def AddRay(
        self,
        waveNumber: int,
        surf: int,
        mode: NSCTraceOptions,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N_: float,
        InsideOf: int,
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> bool:
        """Add a non-sequential ray to the queue with position, direction, and polarization."""
        return bool(
            run_native(
                "IRayTraceNSCData.AddRay",
                lambda: self.native.AddRay(
                    waveNumber, surf, mode, X, Y, Z, L, M, N_, InsideOf, exr, exi, eyr, eyi, ezr, ezi
                ),
                ensure=self.ensure_native,
            )
        )

    def StartReadingResults(self) -> bool:
        return bool(
            run_native(
                "IRayTraceNSCData.StartReadingResults",
                lambda: self.native.StartReadingResults(),
                ensure=self.ensure_native,
            )
        )

    def ReadNextResult(self) -> RayNSCResult:
        """Read the next NSC result header record.

        Layout:
            (ok, rayNumber, ErrorCode, wave, numSegments)
        """
        res = run_native(
            "IRayTraceNSCData.ReadNextResult",
            lambda: self.native.ReadNextResult(),
            ensure=self.ensure_native,
        )
        return validate_cast(res, RayNSCResult)

    def ReadNextSegment(self) -> RayNSCSegment:
        """Read the next NSC segment record.

        Layout:
            (ok, segmentLevel, segmentParent, hitObj, InsideOf, X, Y, Z, L, M, N, exr, exi, eyr, eyi, ezr, ezi, intensity, pathLength)
        """
        res = run_native(
            "IRayTraceNSCData.ReadNextSegment",
            lambda: self.native.ReadNextSegment(),
            ensure=self.ensure_native,
        )
        return validate_cast(res, RayNSCSegment)
