from __future__ import annotations
from typing import Sequence, Protocol, runtime_checkable
from zempy.zosapi.analysis.data.protocols.iar_critical_ray_info import IAR_CriticalRayInfo


@runtime_checkable
class IAR_CriticalRayData(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_CriticalRayData."""

    # ---- Methods ----
    def GetRay(self, idx: int) -> IAR_CriticalRayInfo: ...
    """Gets the specified critical ray (COM 'uint' → int)."""

    # ---- Properties ----
    @property
    def NumRays(self) -> int: ...
    """Number of critical rays available in the analysis (COM 'uint')."""

    @property
    def HeaderLabels(self) -> Sequence[str]: ...
    """Header labels describing each column of the critical ray data (COM 'string[]')."""

    @property
    def Rays(self) -> Sequence[IAR_CriticalRayInfo]: ...
    """Sequence of IAR_CriticalRayInfo objects, one per critical ray."""
