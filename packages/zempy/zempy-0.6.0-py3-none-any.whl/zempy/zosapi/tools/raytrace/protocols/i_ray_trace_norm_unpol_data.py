from __future__ import annotations
from typing import Protocol
from zempy.zosapi.tools.raytrace.enums import OPDMode
from zempy.zosapi.tools.raytrace.ray_norm_unpolarized import RayNormUnpolarized

class IRayTraceNormUnpolData(Protocol):
    """Protocol mirroring **ZOSAPI.Tools.RayTrace.IRayTraceNormUnpolData**.

    Provides a buffered interface for *unpolarized* ray traces using normalized
    pupil coordinates. Clients typically:

    1) call :meth:`ClearData`,
    2) enqueue rays with :meth:`AddRay`,
    3) iterate results via :meth:`StartReadingResults` and :meth:`ReadNextResult`.
    """

    # --- lifecycle / buffer mgmt ---
    def ClearData(self) -> None: ...

    # --- enqueue rays ---
    def AddRay(
        self,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        calcOPD: OPDMode,
    ) -> bool: ...

    # --- results API ---
    def StartReadingResults(self) -> bool: ...

    def ReadNextResult(self) -> RayNormUnpolarized: ...

    # --- properties ---
    @property
    def NumberOfRays(self) -> int: ...

    @property
    def MaxRays(self) -> int: ...

    @property
    def HasResultData(self) -> bool: ...
