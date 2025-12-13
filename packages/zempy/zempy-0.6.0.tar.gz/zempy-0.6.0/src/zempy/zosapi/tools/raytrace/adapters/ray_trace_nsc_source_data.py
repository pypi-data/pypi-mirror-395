from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native, validate_cast,
    PropertyScalar, dataclass,
)
from zempy.zosapi.tools.raytrace.enums.nsc_trace_options import NSCTraceOptions


@dataclass()
class RayTraceNSCSourceData(BaseAdapter[Z, N]):
    """Adapter for **ZOSAPI.Tools.RayTrace.IRayTraceNSCSourceData**.

    Typical usage:
        src = tools.OpenBatchRayTrace().CreateNSCSource()
        src.UseSingleSource = True
        src.ObjectNumber = 3
        src.TraceOptions = NSCTraceOptions.Standard
        src.StartReadingResults()

        while True:
            res = src.ReadNextResult()
            if not res.ok:
                break
            for _ in range(res.numSegments):
                seg = src.ReadNextSegment()
                ...
    """

    # -------------------------- Properties --------------------------
    UseSingleSource = PropertyScalar("UseSingleSource", coerce_get=bool, coerce_set=bool)
    SurfaceNumber   = PropertyScalar("SurfaceNumber", coerce_get=int, coerce_set=int)
    ObjectNumber    = PropertyScalar("ObjectNumber", coerce_get=int, coerce_set=int)
    MaxRays         = PropertyScalar("MaxRays", coerce_get=int, coerce_set=int)
    TraceOptions    = PropertyScalar("TraceOptions", coerce_get=NSCTraceOptions, coerce_set=NSCTraceOptions)
    Wavelength      = PropertyScalar("Wavelength", coerce_get=int, coerce_set=int)
    HasResultData   = PropertyScalar("HasResultData", coerce_get=bool)

    # --------------------------- Methods ----------------------------
    def UsePrimaryWavelength(self) -> None:
        run_native(
            "IRayTraceNSCSourceData.UsePrimaryWavelength",
            lambda: self.native.UsePrimaryWavelength(),
            ensure=self.ensure_native,
        )

    def UseAnyWavelength(self) -> None:
        run_native(
            "IRayTraceNSCSourceData.UseAnyWavelength",
            lambda: self.native.UseAnyWavelength(),
            ensure=self.ensure_native,
        )

    def StartReadingResults(self) -> bool:
        return bool(
            run_native(
                "IRayTraceNSCSourceData.StartReadingResults",
                lambda: self.native.StartReadingResults(),
                ensure=self.ensure_native,
            )
        )

    def ReadNextResult(self):
        """Read the next ray header from the NSC source data.

        Layout:
            (ok, rayNumber, ErrorCode, wave, numSegments)
        """
        res = run_native(
            "IRayTraceNSCSourceData.ReadNextResult",
            lambda: self.native.ReadNextResult(),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)  # could later wrap as RayNSCResult-like dataclass

    def ReadNextSegment(self):
        """Read the next segment of a traced ray.

        Layout:
            (ok, segmentLevel, segmentParent, hitObj, InsideOf,
             x, y, z, l, m, n,
             exr, exi, eyr, eyi, ezr, ezi,
             intensity, pathLength)
        """
        res = run_native(
            "IRayTraceNSCSourceData.ReadNextSegment",
            lambda: self.native.ReadNextSegment(),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)  # could later wrap as RayNSCSegment
