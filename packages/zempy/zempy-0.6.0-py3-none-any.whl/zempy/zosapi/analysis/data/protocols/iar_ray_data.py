from __future__ import annotations
from typing import Protocol, Sequence, runtime_checkable
from zempy.zosapi.analysis.data.protocols.iar_ray_info import IAR_RayInfo

@runtime_checkable
class IAR_RayData(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_RayData."""

    # ---- Methods ----
    def GetRay(self, idx: int) -> IAR_RayInfo: ...
    """Gets the specified ray by index."""

    # ---- Properties ----
    @property
    def Description(self) -> str: ...
    """Description of the ray data set."""

    @property
    def NumRays(self) -> int: ...
    """Number of rays in the data set (COM 'uint')."""

    @property
    def Rays(self) -> Sequence[IAR_RayInfo]: ...
    """Sequence of IAR_RayInfo objects representing each ray."""
