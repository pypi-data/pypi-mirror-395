from __future__ import annotations
from typing import Protocol

from zempy.zosapi.tools.raytrace.ray_norm_polarized import RayNormPolarized, RayNormPolarizedFull



class IRayTraceNormPolData(Protocol):
    """Protocol mirroring **ZOSAPI.Tools.RayTrace.IRayTraceNormPolData**.

    Buffered interface for *polarized* ray traces in normalized pupil coords.
    Each added ray carries full E-field components (real & imaginary parts).
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
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> bool: ...

    # --- results API ---
    def StartReadingResults(self) -> bool: ...

    def ReadNextResult(self) -> RayNormPolarized: ...

    def ReadNextResultFull(self) -> RayNormPolarizedFull: ...

    # --- properties ---
    @property
    def NumberOfRays(self) -> int: ...

    @property
    def MaxRays(self) -> int: ...

    @property
    def HasResultData(self) -> bool: ...
