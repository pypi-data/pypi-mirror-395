from __future__ import annotations
from typing import Protocol
from zempy.zosapi.tools.raytrace.results import RayDirectPolarized, RayDirectPolarizedFull

class IRayTraceDirectPolData(Protocol):
    """Protocol mirroring **ZOSAPI.Tools.RayTrace.IRayTraceDirectPolData**.

    Buffered interface for *polarized* ray traces launched with direct XYZ
    coordinates and direction cosines (L/M/N). The polarization state is taken
    from the associated batch trace context.
    """

    # --- lifecycle / buffer mgmt ---
    def ClearData(self) -> None: ...

    # --- enqueue rays ---
    def AddRay(
        self,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> bool: ...

    # --- results API ---
    def StartReadingResults(self) -> bool: ...

    def ReadNextResult(self) -> RayDirectPolarized: ...

    def ReadNextResultFull(self) -> RayDirectPolarizedFull: ...

    # --- properties ---
    @property
    def NumberOfRays(self) -> int: ...

    @property
    def MaxRays(self) -> int: ...

    @property
    def HasResultData(self) -> bool: ...
