from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native,
    PropertyScalar, dataclass, logging,
)
from zempy.zosapi.tools.raytrace.results import RayDirectUnpolarized

log = logging.getLogger(__name__)
@dataclass()
class RayTraceDirectUnpolData(BaseAdapter[Z, N]):

    NumberOfRays = PropertyScalar("NumberOfRays", coerce_get=int)
    MaxRays      = PropertyScalar("MaxRays",      coerce_get=int)
    HasResultData = PropertyScalar("HasResultData", coerce_get=bool)


    def ClearData(self) -> None:
        run_native(
            "IRayTraceDirectUnpolData.ClearData",
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
        """Add a direct-coordinate unpolarized ray to the queue."""
        return bool(
            run_native(
                "IRayTraceDirectUnpolData.AddRay",
                lambda: self.native.AddRay(waveNumber, X, Y, Z, L, M, N_),
                ensure=self.ensure_native,
            )
        )

    def StartReadingResults(self) -> bool:
        return bool(
            run_native(
                "IRayTraceDirectUnpolData.StartReadingResults",
                lambda: self.native.StartReadingResults(),
                ensure=self.ensure_native,
            )
        )

    def ReadNextResult(self) -> RayDirectUnpolarized:
        res = run_native(
            "IRayTraceDirectUnpolData.ReadNextResult(outs)",
            lambda: self.native.ReadNextResult(),
            ensure=self.ensure_native,
        )

        # out int rayNumber,
        # out int ErrorCode,
        # out int vignetteCode,
        # out double X,
        # out double Y,
        # out double Z,
        # out double L,
        # out double M,
        # out double N,
        # out double l2,
        # out double m2,
        # out double n2,
        # out double intensity

        ray = RayDirectUnpolarized(
            ok=bool(res[0]),
            rayNumber=int(res[1]),
            errorCode=int(res[2]),
            vignetteCode=int(res[3]),
            X=float(res[4]),
            Y=float(res[5]),
            Z=float(res[6]),
            L=float(res[7]),
            M=float(res[8]),
            N=float(res[9]),
            l2=float(res[10]),
            m2=float(res[11]),
            n2=float(res[12]),
            intensity=float(res[13]),
        )
        return ray