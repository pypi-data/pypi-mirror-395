from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native,
    PropertyScalar, dataclass,
)

from zempy.zosapi.tools.raytrace.enums.opd_mode import OPDMode
from zempy.zosapi.tools.raytrace.results import RayNormUnpolarized

@dataclass()
class RayTraceNormUnpolData(BaseAdapter[Z, N]):

    NumberOfRays = PropertyScalar("NumberOfRays", coerce_get=int)
    MaxRays      = PropertyScalar("MaxRays",      coerce_get=int)
    HasResultData = PropertyScalar("HasResultData", coerce_get=bool)

    def ClearData(self) -> None:
        run_native(
            "IRayTraceNormUnpolData.ClearData",
            lambda: self.native.ClearData(),
            ensure=self.ensure_native,
        )

    def AddRay(
        self,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        calcOPD: OPDMode,
    ) -> bool:
        """Add a normalized-pupil unpolarized ray to the queue."""
        return bool(
            run_native(
                "IRayTraceNormUnpolData.AddRay",
                lambda: self.native.AddRay(waveNumber, Hx, Hy, Px, Py, OPDMode.to_native(self.zosapi, calcOPD)),
                ensure=self.ensure_native,
            )
        )

    def StartReadingResults(self) -> bool:
        return bool(
            run_native(
                "IRayTraceNormUnpolData.StartReadingResults",
                lambda: self.native.StartReadingResults(),
                ensure=self.ensure_native,
            )
        )

    def ReadNextResult(self) -> RayNormUnpolarized:
        res = run_native(
            "IRayTraceNormUnpolData.ReadNextResult(outs)",
            lambda: self.native.ReadNextResult(),
            ensure=self.ensure_native,
        )
        # ReadNextResult
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
        # out double opd,
        # out double intensity
        ray = RayNormUnpolarized(
            ok              =   bool(res[0]),
            rayNumber       =   int(res[1]),
            errorCode       =   int(res[2]),
            vignetteCode    =   int(res[3]),
            X               =   float(res[4]),
            Y               =   float(res[5]),
            Z               =   float(res[6]),
            L               =   float(res[7]),
            M               =   float(res[8]),
            N               =   float(res[9]),
            l2              =   float(res[10]),
            m2              =   float(res[11]),
            n2              =   float(res[12]),
            opd             =   float(res[13]),
            intensity       =   float(res[14]),
        )

        return ray















