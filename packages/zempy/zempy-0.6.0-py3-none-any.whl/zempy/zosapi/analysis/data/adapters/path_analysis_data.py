from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence, TYPE_CHECKING
from allytools.types import str_or_empty
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar

if TYPE_CHECKING:
    from zempy.zosapi.analysis.data.protocols.iar_path_analysis_data import IAR_PathAnalysisData
    from zempy.zosapi.analysis.data.protocols.iar_path_analysis_entry import IAR_PathAnalysisEntry
    from zempy.zosapi.analysis.data.adapters.path_analysis_entry import PathAnalysisEntry


@dataclass(frozen=True, slots=True)
class PathAnalysisData:
    """Adapter for ZOSAPI.Analysis.Data.IAR_PathAnalysisData."""
    zosapi: object
    native: object

    # --- Factory ---
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "PathAnalysisData":
        if native is None:
            raise ValueError("PathAnalysisData.from_native: native is None")
        return cls(zosapi, native)

    # --- Validation ---
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="PathAnalysisData.native", exc_type=_exc.ZemaxObjectGone)

    # --- Methods ---
    def GetPathNumber(self, idx: int) -> "IAR_PathAnalysisEntry":
        from zempy.zosapi.analysis.data.adapters.path_analysis_entry import PathAnalysisEntry
        native = run_native(
            "PathAnalysisData.GetPathNumber",
            lambda: self.native.GetPathNumber(int(idx)),
            ensure=self.ensure_native,
        )
        return PathAnalysisEntry.from_native(self.zosapi, native)

    def GetPathUncategorized(self) -> "IAR_PathAnalysisEntry":
        from zempy.zosapi.analysis.data.adapters.path_analysis_entry import PathAnalysisEntry
        native = run_native(
            "PathAnalysisData.GetPathUncategorized",
            lambda: self.native.GetPathUncategorized(),
            ensure=self.ensure_native,
        )
        return PathAnalysisEntry.from_native(self.zosapi, native)

    TotalFluxIn   = PropertyScalar("TotalFluxIn",   coerce_get=float)
    TotalFluxOut  = PropertyScalar("TotalFluxOut",  coerce_get=float)
    TotalRays     = PropertyScalar("TotalRays",     coerce_get=int)
    TotalHits     = PropertyScalar("TotalHits",     coerce_get=int)
    NumPaths      = PropertyScalar("NumPaths",      coerce_get=int)
    PathNumber    = PropertyScalar("PathNumber",    coerce_get=int, coerce_set=int)
    PathBranches  = PropertyScalar("PathBranches",  coerce_get=int)
    PathSource    = PropertyScalar("PathSource",    coerce_get=int)
    LastObject    = PropertyScalar("LastObject",    coerce_get=int)
    LastFace      = PropertyScalar("LastFace",      coerce_get=int)
    PathFluxOut   = PropertyScalar("PathFluxOut",   coerce_get=float)
    PathFluxPercent = PropertyScalar("PathFluxPercent", coerce_get=float)
    PathSequence  = PropertyScalar("PathSequence",  coerce_get=str_or_empty)

    # --- Collections ---
    @property
    def Paths(self) -> Sequence["IAR_PathAnalysisEntry"]:
        from zempy.zosapi.analysis.data.adapters.path_analysis_entry import PathAnalysisEntry
        raw_seq = run_native(
            "PathAnalysisData.Paths get",
            lambda: self.native.Paths,
            ensure=self.ensure_native,
        )
        out: List[PathAnalysisEntry] = []
        if raw_seq:
            for native_entry in raw_seq:
                out.append(PathAnalysisEntry.from_native(self.zosapi, native_entry))
        return out

    def __repr__(self) -> str:
        try:
            return (f"PathAnalysisData(NumPaths={self.NumPaths}, "
                    f"FluxIn={self.TotalFluxIn:.3g}, FluxOut={self.TotalFluxOut:.3g})")
        except Exception:
            return "PathAnalysisData(<unavailable>)"
