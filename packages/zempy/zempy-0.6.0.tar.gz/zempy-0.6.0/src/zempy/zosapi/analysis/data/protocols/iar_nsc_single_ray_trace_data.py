from __future__ import annotations
from typing import Protocol, Tuple, runtime_checkable
from zempy.zosapi.tools.enums.ray_status import RayStatus


@runtime_checkable
class IAR_NSCSingleRayTraceData(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_NSCSingleRayTraceData."""

    # ---- Methods ----
    def ReadSegmentFull(
        self,
        segmentNumber: int,
    ) -> Tuple[
        bool,          # success
        int,           # segmentLevel
        int,           # segmentParent
        int,           # hitObj
        int,           # hitFace
        int,           # insideOf
        RayStatus,     # status
        float, float, float,   # x, y, z
        float, float, float,   # l, m, n
        float, float,          # exr, exi
        float, float,          # eyr, eyi
        float, float,          # ezr, ezi
        float,                 # intensity
        float,                 # pathLength
        int,                   # xybin
        int,                   # lmbin
        float, float, float,   # xNorm, yNorm, zNorm
        float,                 # index
        float,                 # startingPhase
        float,                 # phaseOf
        float,                 # phaseAt
    ]:
        """
        Reads a full NSC segment record.

        Returns:
            (success, segmentLevel, segmentParent, hitObj, hitFace, insideOf, status,
             x, y, z, l, m, n, exr, exi, eyr, eyi, ezr, ezi, intensity,
             pathLength, xybin, lmbin, xNorm, yNorm, zNorm, index,
             startingPhase, phaseOf, phaseAt)
        """
        ...

    # ---- Properties ----
    @property
    def IsValid(self) -> bool: ...
    @property
    def ZRDFile(self) -> str: ...
    @property
    def NumberOfSegments(self) -> int: ...
    @property
    def WaveIndex(self) -> int: ...
    @property
    def WavelengthUM(self) -> float: ...
