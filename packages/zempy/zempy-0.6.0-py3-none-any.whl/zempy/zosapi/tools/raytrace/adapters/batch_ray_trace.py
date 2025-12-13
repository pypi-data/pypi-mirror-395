from __future__ import annotations
from typing import Tuple
from zempy.zosapi.core.im_adapter import (
    Z, N, run_native, validate_cast, dataclass
)
from zempy.zosapi.tools.adapters.system_tool import SystemTool
from zempy.zosapi.tools.raytrace.enums.rays_type import RaysType
from zempy.zosapi.tools.raytrace.adapters.ray_trace_norm_unpol_data import RayTraceNormUnpolData
from zempy.zosapi.tools.raytrace.adapters.ray_trace_direct_unpol_data import RayTraceDirectUnpolData
from zempy.zosapi.tools.raytrace.adapters.ray_trace_norm_pol_data import RayTraceNormPolData
from zempy.zosapi.tools.raytrace.adapters.ray_trace_direct_pol_data import RayTraceDirectPolData
from zempy.zosapi.tools.raytrace.adapters.ray_trace_nsc_data import RayTraceNSCData
from zempy.zosapi.tools.raytrace.adapters.ray_trace_nsc_source_data import RayTraceNSCSourceData


@dataclass()
class BatchRayTrace(SystemTool[Z, N]):
    """Adapter for **ZOSAPI.Tools.RayTrace.IBatchRayTrace**.
    - Create* methods return your typed adapters (from_native).
    - SingleRay* and utilities return tuples (swap `tuple` -> your typed tuples if desired).
    """

    def CreateNormUnpol(self, MaxRays: int, rayType: RaysType, toSurface: int) -> RayTraceNormUnpolData:
        native = run_native(
            "IBatchRayTrace.CreateNormUnpol",
            lambda: self.native.CreateNormUnpol(MaxRays, RaysType.to_native(self.zosapi, rayType), toSurface),
            ensure=self.ensure_native,
        )
        return RayTraceNormUnpolData.from_native(self.zosapi, native)

    def CreateDirectUnpol(self, MaxRays: int, rayType: RaysType, startSurface: int, toSurface: int) -> RayTraceDirectUnpolData:
        native = run_native(
            "IBatchRayTrace.CreateDirectUnpol",
            lambda: self.native.CreateDirectUnpol(MaxRays,  RaysType.to_native(self.zosapi, rayType), startSurface, toSurface),
            ensure=self.ensure_native,
        )
        return RayTraceDirectUnpolData.from_native(self.zosapi, native)

    def CreateNormPol(self, MaxRays: int, rayType: RaysType, Ex: float, Ey: float, phaX: float, phaY: float, toSurface: int) -> RayTraceNormPolData:
        native = run_native(
            "IBatchRayTrace.CreateNormPol",
            lambda: self.native.CreateNormPol(MaxRays,  RaysType.to_native(self.zosapi, rayType), Ex, Ey, phaX, phaY, toSurface),
            ensure=self.ensure_native,
        )
        return RayTraceNormPolData.from_native(self.zosapi, native)

    def CreateDirectPol(self, MaxRays: int, rayType: RaysType, Ex: float, Ey: float, phaX: float, phaY: float, startSurface: int, toSurface: int) -> RayTraceDirectPolData:
        native = run_native(
            "IBatchRayTrace.CreateDirectPol",
            lambda: self.native.CreateDirectPol(MaxRays, RaysType.to_native(self.zosapi, rayType), Ex, Ey, phaX, phaY, startSurface, toSurface),
            ensure=self.ensure_native,
        )
        return RayTraceDirectPolData.from_native(self.zosapi, native)

    def CreateNSC(self, MaxRays: int, maxSegments: int, coherenceLength: float) -> RayTraceNSCData:
        native = run_native(
            "IBatchRayTrace.CreateNSC",
            lambda: self.native.CreateNSC(MaxRays, maxSegments, coherenceLength),
            ensure=self.ensure_native,
        )
        return RayTraceNSCData.from_native(self.zosapi, native)

    def CreateNSCSourceData(self, maxSegments: int, coherenceLength: float) -> RayTraceNSCSourceData:
        native = run_native(
            "IBatchRayTrace.CreateNSCSourceData",
            lambda: self.native.CreateNSCSourceData(maxSegments, coherenceLength),
            ensure=self.ensure_native,
        )
        return RayTraceNSCSourceData.from_native(self.zosapi, native)

    def SingleRayNormUnpol(
        self, rayType: RaysType, toSurf: int, waveNumber: int,
        Hx: float, Hy: float, Px: float, Py: float, calcOPD: bool
    ) -> Tuple:
        """Returns:
        (ok, ErrorCode, vignetteCode, xo, yo, zo, lo, mo, no, l2o, m2o, n2o, opd, intensity)
        """
        res = run_native(
            "IBatchRayTrace.SingleRayNormUnpol",
            lambda: self.native.SingleRayNormUnpol(
                RaysType.to_native(self.zosapi, rayType), toSurf, waveNumber, Hx, Hy, Px, Py, calcOPD
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)

    def SingleRayDirectUnpol(
        self, rayType: RaysType, startSurface: int, toSurface: int, waveNumber: int,
        X: float, Y: float, Z: float, L: float, M: float, N_: float
    ) -> Tuple:
        """Returns:
        (ok, ErrorCode, vignetteCode, xo, yo, zo, lo, mo, no, l2o, m2o, n2o, intensity)
        """
        res = run_native(
            "IBatchRayTrace.SingleRayDirectUnpol",
            lambda: self.native.SingleRayDirectUnpol(
                RaysType.to_native(self.zosapi, rayType), startSurface, toSurface, waveNumber, X, Y, Z, L, M, N_
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)

    def SingleRayNormPol(
        self, rayType: RaysType, Ex: float, Ey: float, phaX: float, phaY: float,
        toSurf: int, waveNumber: int, Hx: float, Hy: float, Px: float, Py: float,
        exr: float, exi: float, eyr: float, eyi: float, ezr: float, ezi: float
    ) -> Tuple:
        """Returns:
        (ok, ErrorCode, exro, exio, eyro, eyio, ezro, ezio, intensity)
        """
        res = run_native(
            "IBatchRayTrace.SingleRayNormPol",
            lambda: self.native.SingleRayNormPol(
                RaysType.to_native(self.zosapi, rayType), Ex, Ey, phaX, phaY, toSurf, waveNumber, Hx, Hy, Px, Py,
                exr, exi, eyr, eyi, ezr, ezi
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)

    def SingleRayNormPolFull(
        self, rayType: RaysType, Ex: float, Ey: float, phaX: float, phaY: float,
        toSurf: int, waveNumber: int, Hx: float, Hy: float, Px: float, Py: float,
        exr: float, exi: float, eyr: float, eyi: float, ezr: float, ezi: float
    ) -> Tuple:
        """Returns:
        (ok, ErrorCode, xo, yo, zo, lo, mo, no, exro, exio, eyro, eyio, ezro, ezio, intensity)
        """
        res = run_native(
            "IBatchRayTrace.SingleRayNormPolFull",
            lambda: self.native.SingleRayNormPolFull(
                RaysType.to_native(self.zosapi, rayType), Ex, Ey, phaX, phaY, toSurf, waveNumber, Hx, Hy, Px, Py,
                exr, exi, eyr, eyi, ezr, ezi
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)

    def SingleRayDirectPol(
        self, rayType: RaysType, Ex: float, Ey: float, phaX: float, phaY: float,
        startSurface: int, toSurface: int, waveNumber: int,
        X: float, Y: float, Z: float, L: float, M: float, N_: float
    ) -> Tuple:
        """Returns:
        (ok, ErrorCode, vignetteCode, exro, exio, eyro, eyio, ezro, ezio, intensity)
        """
        res = run_native(
            "IBatchRayTrace.SingleRayDirectPol",
            lambda: self.native.SingleRayDirectPol(
                RaysType.to_native(self.zosapi, rayType), Ex, Ey, phaX, phaY, startSurface, toSurface, waveNumber,
                X, Y, Z, L, M, N_
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)

    def SingleRayDirectPolFull(
        self, rayType: RaysType, Ex: float, Ey: float, phaX: float, phaY: float,
        startSurface: int, toSurface: int, waveNumber: int,
        X: float, Y: float, Z: float, L: float, M: float, N_: float
    ) -> Tuple:
        """Returns:
        (ok, ErrorCode, vignetteCode, xo, yo, zo, lo, mo, no, exro, exio, eyro, eyio, ezro, ezio, intensity)
        """
        res = run_native(
            "IBatchRayTrace.SingleRayDirectPolFull",
            lambda: self.native.SingleRayDirectPolFull(
                RaysType.to_native(self.zosapi, rayType), Ex, Ey, phaX, phaY, startSurface, toSurface, waveNumber,
                X, Y, Z, L, M, N_
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)

    # ------------------------------ Utilities (tuples) ------------------------------
    def GetDirectFieldCoordinates(
        self, waveNumber: int, rayType: RaysType, Hx: float, Hy: float, Px: float, Py: float
    ) -> Tuple:
        """Convert from normalized pupil to direct XYZ/LMN.
        Returns: (ok, X, Y, Z, L, M, N)
        """
        res = run_native(
            "IBatchRayTrace.GetDirectFieldCoordinates",
            lambda: self.native.GetDirectFieldCoordinates(
                waveNumber, RaysType.to_native(self.zosapi, rayType), Hx, Hy, Px, Py
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)

    def GetPhase(
        self, L: float, M: float, N_: float,
        jx: float, jy: float, xPhaseDeg: float, yPhaseDeg: float, intensity: float
    ) -> Tuple:
        """Returns: (ok, exr, exi, eyr, eyi, ezr, ezi)"""
        res = run_native(
            "IBatchRayTrace.GetPhase",
            lambda: self.native.GetPhase(
                L, M, N_, jx, jy, xPhaseDeg, yPhaseDeg, intensity
            ),
            ensure=self.ensure_native,
        )
        return validate_cast(res, tuple)
