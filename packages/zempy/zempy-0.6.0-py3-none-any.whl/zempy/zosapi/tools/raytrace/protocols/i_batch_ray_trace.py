from __future__ import annotations
from typing import Protocol, runtime_checkable, TYPE_CHECKING
from zempy.zosapi.tools.protocols.i_system_tool import ISystemTool
from zempy.zosapi.tools.raytrace.enums import RaysType
from zempy.zosapi.tools.raytrace.results import (RayNormPolarized, RayNormUnpolarized,
                                                 RayDirectPolarized, RayDirectUnpolarized,
                                                 RayNormPolarizedFull, RayDirectPolarizedFull,
                                                 Phase, FieldCoordinates)


if TYPE_CHECKING:
    from zempy.zosapi.tools.protocols.i_system_tool import ISystemTool
    from zempy.zosapi.tools.raytrace.protocols.i_ray_trace_norm_unpol_data import (
        IRayTraceNormUnpolData,
    )
    from zempy.zosapi.tools.raytrace.protocols.i_ray_trace_direct_unpol_data import (
        IRayTraceDirectUnpolData,
    )
    from zempy.zosapi.tools.raytrace.protocols.i_ray_trace_direct_pol_data import (
        IRayTraceDirectPolData,
    )
    from zempy.zosapi.tools.raytrace.protocols.i_ray_trace_norm_pol_data import (
        IRayTraceNormPolData,
    )

    from zempy.zosapi.tools.raytrace.protocols.i_ray_trace_nsc_data import (
        IRayTraceNSCData,
    )

    from zempy.zosapi.tools.raytrace.protocols.i_ray_trace_nsc_source_data import (
        IRayTraceNSCSourceData,
    )



@runtime_checkable
class IBatchRayTrace(ISystemTool, Protocol):
    """Protocol mirroring **ZOSAPI.Tools.RayTrace.IBatchRayTrace**.

    Interfaces and methods for running a ray trace on multiple rays at a time.
    Access via :class:`IOpticalSystemTools` (e.g., ``tools.OpenBatchRayTrace()``).
    All methods mirror ZOSAPI names (PascalCase) for 1:1 mapping.

    Notes
    -----
    - In OpticStudio, some methods use ``out`` parameters. In this Python
      protocol, the corresponding *SingleRay...* methods return typed tuples
      (see the ``...Result`` aliases above) that bundle those outputs.
    - This interface extends :class:`ISystemTool` for run/close semantics.
    """

    # -------- Unpolarized, normalized pupil --------
    def CreateNormUnpol(self, MaxRays: int, rayType: RaysType, toSurface: int) -> IRayTraceNormUnpolData: ...

    def SingleRayNormUnpol(
        self,
        rayType: RaysType,
        toSurf: int,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        calcOPD: bool,
    ) -> RayNormUnpolarized: ...

    # -------- Unpolarized, direct XYZ --------
    def CreateDirectUnpol(self, MaxRays: int, rayType: RaysType, startSurface: int, toSurface: int) -> IRayTraceDirectUnpolData: ...

    def SingleRayDirectUnpol(
        self,
        rayType: RaysType,
        startSurface: int,
        toSurface: int,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> RayDirectUnpolarized: ...

    # -------- Polarized, normalized pupil --------
    def CreateNormPol(
        self,
        MaxRays: int,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        toSurface: int,
    ) -> IRayTraceNormPolData: ...

    def SingleRayNormPol(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        toSurf: int,
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
    ) -> RayNormPolarized: ...

    def SingleRayNormPolFull(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        toSurf: int,
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
    ) -> RayNormPolarizedFull: ...

    # -------- Polarized, direct XYZ --------
    def CreateDirectPol(
        self,
        MaxRays: int,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phax: float,
        phay: float,
        startSurface: int,
        toSurface: int,
    ) -> IRayTraceDirectPolData: ...

    def SingleRayDirectPol(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        startSurface: int,
        toSurface: int,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> RayDirectPolarized: ...

    def SingleRayDirectPolFull(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        startSurface: int,
        toSurface: int,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> RayDirectPolarizedFull: ...

    # -------- NSC rays --------
    def CreateNSC(self, MaxRays: int, maxSegments: int, coherenceLength: float) -> IRayTraceNSCData: ...

    def CreateNSCSourceData(self, maxSegments: int, coherenceLength: float) -> IRayTraceNSCSourceData: ...

    # -------- Helpers --------
    def GetDirectFieldCoordinates(
        self,
        waveNumber: int,
        rayType: RaysType,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
    ) -> FieldCoordinates: ...

    def GetPhase(
        self,
        L: float,
        M: float,
        N: float,
        jx: float,
        jy: float,
        xPhaseDeg: float,
        yPhaseDeg: float,
        intensity: float,
    ) -> Phase: ...
