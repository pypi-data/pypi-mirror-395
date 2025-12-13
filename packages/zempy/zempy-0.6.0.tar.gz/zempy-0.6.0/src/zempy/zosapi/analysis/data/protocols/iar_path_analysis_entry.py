from __future__ import annotations
from typing import Sequence, Protocol, runtime_checkable

@runtime_checkable
class IAR_PathAnalysisEntry(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_PathAnalysisEntry."""

    # ---- Methods ----
    def GetPathObjectNumber(self, objectNumber: int) -> int: ...
    """Returns the object number corresponding to the specified path index."""

    # ---- Properties ----
    @property
    def PathNumber(self) -> int: ...
    """Path index (COM 'uint')."""

    @property
    def RaysInPath(self) -> int: ...
    """Total number of rays in this path (COM 'UInt64' → int)."""

    @property
    def HitsInPath(self) -> int: ...
    """Number of hits in the path (COM 'uint')."""

    @property
    def GhostsInPath(self) -> int: ...
    """Number of ghost reflections in the path (COM 'uint')."""

    @property
    def UniqueObjectsInPath(self) -> int: ...
    """Number of unique objects in the path (COM 'uint')."""

    @property
    def TotalPathFlux(self) -> float: ...
    """Total flux associated with this path (COM 'double')."""

    @property
    def NumberOfObjectsInPath(self) -> int: ...
    """Number of objects that compose this path (COM 'uint')."""

    @property
    def PathObjectList(self) -> Sequence[int]: ...
    """List of object numbers in the path (COM 'int[]')."""

    @property
    def PathObjectAndFaceList(self) -> Sequence[Sequence[int]]: ...
    """2D list of [object, face] pairs (COM 'int[,]')."""

    @property
    def PathSource(self) -> int: ...
    """Index of the source object for this path (COM 'int')."""
