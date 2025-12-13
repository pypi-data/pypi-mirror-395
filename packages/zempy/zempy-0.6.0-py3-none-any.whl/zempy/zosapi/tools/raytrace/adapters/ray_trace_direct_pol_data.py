from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native, validate_cast,
    PropertyScalar, dataclass,
)

from zempy.zosapi.tools.raytrace.results import RayDirectPolarized, RayDirectPolarizedFull

@dataclass()
class RayTraceDirectPolData(BaseAdapter[Z, N]):
    """Adapter for **ZOSAPI.Tools.RayTrace.IRayTraceDirectPolData**.

    Typical usage:
        buf = tools.OpenBatchRayTrace().CreateDirectPol(MaxRays, rayType, Ex, Ey, phaX, phaY, startSurface, toSurface)
        buf.ClearData()
        buf.AddRay(wave, X, Y, Z, L, M, N)
        buf.StartReadingResults()
        ok, *rec = buf.ReadNextResult()
        ok, *rec_full = buf.ReadNextResultFull()
    """

    # -------------------------- Properties --------------------------
    NumberOfRays = PropertyScalar("NumberOfRays", coerce_get=int)
    MaxRays      = PropertyScalar("MaxRays",      coerce_get=int)
    HasResultData = PropertyScalar("HasResultData", coerce_get=bool)

    # --------------------------- Methods ----------------------------
    def ClearData(self) -> None:
        run_native(
            "IRayTraceDirectPolData.ClearData",
            lambda: self.native.ClearData(),
            ensure=self.ensure_native,
        )

    def AddRay(
        self,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N_: float,
    ) -> bool:
        """Add a direct-coordinate *polarized* ray to the queue."""
        return bool(
            run_native(
                "IRayTraceDirectPolData.AddRay",
                lambda: self.native.AddRay(waveNumber, X, Y, Z, L, M, N_),
                ensure=self.ensure_native,
            )
        )

    def StartReadingResults(self) -> bool:
        return bool(
            run_native(
                "IRayTraceDirectPolData.StartReadingResults",
                lambda: self.native.StartReadingResults(),
                ensure=self.ensure_native,
            )
        )

    def ReadNextResult(self) -> RayDirectPolarized:
        res = run_native(
            "IRayTraceDirectPolData.ReadNextResult",
            lambda: self.native.ReadNextResult(),
            ensure=self.ensure_native,
        )
        # out int rayNumber,
        # out int ErrorCode,
        # out double exr,
        # out double exi,
        # out double eyr,
        # out double eyi,
        # out double ezr,
        # out double ezi,
        # out double intensity
        ray = RayDirectPolarized(
            ok=bool(res[0]),
            rayNumber=int(res[1]),
            errorCode=int(res[2]),
            vignetteCode=int(res[3]),
            exr=float(res[4]),
            exi=float(res[5]),
            eyr=float(res[6]),
            eyi=float(res[7]),
            ezr=float(res[8]),
            ezi=float(res[9]),
            intensity=float(res[10]),
        )

        return ray

    def ReadNextResultFull(self) -> RayDirectPolarizedFull:
        res = run_native(
            "IRayTraceDirectPolData.ReadNextResultFull",
            lambda: self.native.ReadNextResultFull(),
            ensure=self.ensure_native,
        )
        # Optional: sanity check to catch API/interop drift early
        if len(res) != 17:
            raise RuntimeError(
                f"Unexpected result length {len(res)} for ReadNextResultFull: {res!r}"
            )

        ray = RayDirectPolarizedFull(
            ok=bool(res[0]),
            rayNumber=int(res[1]),
            errorCode=int(res[2]),
            vignetteCode=int(res[3]),
            xo=float(res[4]),
            yo=float(res[5]),
            zo=float(res[6]),
            lo=float(res[7]),
            mo=float(res[8]),
            no=float(res[9]),
            exr=float(res[10]),
            exi=float(res[11]),
            eyr=float(res[12]),
            eyi=float(res[13]),
            ezr=float(res[14]),
            ezi=float(res[15]),
            intensity=float(res[16]),
        )
        return ray
