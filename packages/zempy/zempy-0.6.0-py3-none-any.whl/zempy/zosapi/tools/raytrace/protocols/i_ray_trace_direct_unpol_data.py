from __future__ import annotations
from typing import Protocol
from zempy.zosapi.tools.raytrace.ray_direct_unpolarized import RayDirectUnpolarized



class IRayTraceDirectUnpolData(Protocol):
    """Protocol mirroring **ZOSAPI.Tools.RayTrace.IRayTraceDirectUnpolData**.

    Provides a buffered interface for *unpolarized* ray traces using direct
    XYZ launch coordinates plus direction cosines L/M/N.

    Typical usage:
        1) :meth:`ClearData`
        2) enqueue with :meth:`AddRay`
        3) :meth:`StartReadingResults` then iterate :meth:`ReadNextResult`
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

    def ReadNextResult(self) -> RayDirectUnpolarized: ...

    # --- properties ---
    @property
    def NumberOfRays(self) -> int: ...

    @property
    def MaxRays(self) -> int: ...

    @property
    def HasResultData(self) -> bool: ...
