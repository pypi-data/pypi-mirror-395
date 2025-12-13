from __future__ import annotations
from zempy.zosapi.core.im_adapter import (
    BaseAdapter, Z, N, run_native, validate_cast,
    PropertyScalar, dataclass,
)

from zempy.zosapi.tools.raytrace.results import RayNormPolarized, RayNormPolarizedFull

@dataclass()
class RayTraceNormPolData(BaseAdapter[Z, N]):

    NumberOfRays = PropertyScalar("NumberOfRays", coerce_get=int)
    MaxRays      = PropertyScalar("MaxRays",      coerce_get=int)
    HasResultData = PropertyScalar("HasResultData", coerce_get=bool)
    def ClearData(self) -> None:
        run_native(
            "IRayTraceNormPolData.ClearData",
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
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> bool:
        """Add a normalized-pupil *polarized* ray to the queue (with E-field components)."""
        return bool(
            run_native(
                "IRayTraceNormPolData.AddRay",
                lambda: self.native.AddRay(
                    waveNumber, Hx, Hy, Px, Py, exr, exi, eyr, eyi, ezr, ezi
                ),
                ensure=self.ensure_native,
            )
        )

    def StartReadingResults(self) -> bool:
        return bool(
            run_native(
                "IRayTraceNormPolData.StartReadingResults",
                lambda: self.native.StartReadingResults(),
                ensure=self.ensure_native,
            )
        )

    def ReadNextResult(self) -> RayNormPolarized:
        res = run_native(
            "IRayTraceNormPolData.ReadNextResult",
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
        ray = RayNormPolarized(
            ok=bool(res[0]),
            rayNumber=int(res[1]),
            errorCode=int(res[2]),
            exr=float(res[3]),
            exi=float(res[4]),
            eyr=float(res[5]),
            eyi=float(res[6]),
            ezr=float(res[7]),
            ezi=float(res[8]),
            intensity=float(res[9]),
        )
        return ray

    def ReadNextResultFull(self) -> RayNormPolarizedFull:
        res = run_native(
            "IRayTraceNormPolData.ReadNextResultFull",
            lambda: self.native.ReadNextResultFull(),
            ensure=self.ensure_native,
        )
        # out int rayNumber
        # out int ErrorCode
        # out double xo
        # out double yo
        # out double zo
        # out double lo
        # out double mo
        # out double no
        # out double exr
        # out double exi
        # out double eyr
        # out double eyi
        # out double ezr
        # out double ezi
        # out double intensity
        ray = RayNormPolarizedFull(
            ok=bool(res[0]),
            rayNumber=int(res[1]),
            errorCode=int(res[2]),
            xo=float(res[3]),
            yo=float(res[4]),
            zo=float(res[5]),
            lo=float(res[6]),
            mo=float(res[7]),
            no=float(res[8]),
            exr=float(res[9]),
            exi=float(res[10]),
            eyr=float(res[11]),
            eyi=float(res[12]),
            ezr=float(res[13]),
            ezi=float(res[14]),
            intensity=float(res[15]),
        )
        return ray
