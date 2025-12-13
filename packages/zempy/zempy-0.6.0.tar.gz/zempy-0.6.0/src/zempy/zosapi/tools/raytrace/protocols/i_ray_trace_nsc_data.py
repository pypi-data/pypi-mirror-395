from __future__ import annotations
from typing import Protocol
from zempy.zosapi.tools.raytrace.enums.nsc_trace_options import NSCTraceOptions
from zempy.zosapi.tools.raytrace.ray_nsc import RayNSCResult, RayNSCSegment


class IRayTraceNSCData(Protocol):
    """Protocol mirroring **ZOSAPI.Tools.RayTrace.IRayTraceNSCData**.

    Interface for creating and reading non-sequential ray traces. Each added ray
    defines its wave, surface, trace mode, launch point (X/Y/Z), direction (L/M/N),
    polarization (exr/exi, eyr/eyi, ezr/ezi), and InsideOf context.
    """

    # --- lifecycle / buffer mgmt ---
    def ClearData(self) -> None: ...

    # --- enqueue rays ---
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
        N: float,
        InsideOf: int,
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> bool: ...

    # --- results API ---
    def StartReadingResults(self) -> bool: ...

    def ReadNextResult(self) -> RayNSCResult: ...

    def ReadNextSegment(self) -> RayNSCSegment: ...

    # --- properties ---
    @property
    def NumberOfRays(self) -> int: ...

    @property
    def MaxRays(self) -> int: ...

    @property
    def HasResultData(self) -> bool: ...
