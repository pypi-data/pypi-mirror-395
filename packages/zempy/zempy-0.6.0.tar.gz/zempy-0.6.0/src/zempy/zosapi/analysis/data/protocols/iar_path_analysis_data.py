from __future__ import annotations
from typing import Protocol, Sequence, runtime_checkable
from zempy.zosapi.analysis.data.protocols.iar_path_analysis_entry import IAR_PathAnalysisEntry


@runtime_checkable
class IAR_PathAnalysisData(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_PathAnalysisData."""

    # ---- Methods ----
    def GetPathNumber(self, idx: int) -> IAR_PathAnalysisEntry: ...
    """Gets data for the specified path (COM 'uint' → int)."""

    def GetPathUncategorized(self) -> IAR_PathAnalysisEntry: ...
    """Gets the uncategorized path data entry."""

    # ---- Properties ----
    @property
    def TotalFluxIn(self) -> float: ...
    """Total input flux (COM 'double')."""

    @property
    def TotalFluxOut(self) -> float: ...
    """Total output flux (COM 'double')."""

    @property
    def TotalRays(self) -> int: ...
    """Total number of rays in the analysis (COM 'uint')."""

    @property
    def TotalHits(self) -> int: ...
    """Total number of hits across all paths (COM 'uint')."""

    @property
    def NumPaths(self) -> int: ...
    """Number of paths in the analysis (COM 'uint')."""

    @property
    def PathNumber(self) -> int: ...
    """Current selected path number (COM 'uint')."""

    @PathNumber.setter
    def PathNumber(self, value: int) -> None: ...

    @property
    def PathBranches(self) -> int: ...
    """Number of branches for the selected path (COM 'uint')."""

    @property
    def PathSource(self) -> int: ...
    """Source object index for the selected path (COM 'uint')."""

    @property
    def LastObject(self) -> int: ...
    """Index of the last object in the path (COM 'uint')."""

    @property
    def LastFace(self) -> int: ...
    """Index of the last face in the path (COM 'uint')."""

    @property
    def PathFluxOut(self) -> float: ...
    """Output flux for the current path (COM 'double')."""

    @property
    def PathFluxPercent(self) -> float: ...
    """Flux percentage of the current path (COM 'double')."""

    @property
    def PathSequence(self) -> str: ...
    """Sequence string representing the path (COM 'string')."""

    @property
    def Paths(self) -> Sequence[IAR_PathAnalysisEntry]: ...
    """Collection of IAR_PathAnalysisEntry objects for all paths."""
