from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence, Tuple, TYPE_CHECKING

from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc

if TYPE_CHECKING:
    from zempy.zosapi.analysis.data.protocols.iar_path_analysis_entry import IAR_PathAnalysisEntry


@dataclass(frozen=True, slots=True)
class PathAnalysisEntry:
    """Adapter for ZOSAPI.Analysis.Data.IAR_PathAnalysisEntry."""
    zosapi: object
    native: object

    # --- Factory ---
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "PathAnalysisEntry":
        if native is None:
            raise ValueError("PathAnalysisEntry.from_native: native is None")
        return cls(zosapi, native)

    # --- Validation ---
    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="PathAnalysisEntry.native", exc_type=_exc.ZemaxObjectGone)

    # --- Methods ---
    def GetPathObjectNumber(self, objectNumber: int) -> int:
        return int(run_native(
            "PathAnalysisEntry.GetPathObjectNumber",
            lambda: self.native.GetPathObjectNumber(int(objectNumber)),
            ensure=self.ensure_native
        ))

    # --- Properties (scalars) ---
    @property
    def PathNumber(self) -> int:
        return int(run_native("PathAnalysisEntry.PathNumber get",
                              lambda: self.native.PathNumber,
                              ensure=self.ensure_native))

    @property
    def RaysInPath(self) -> int:
        # COM UInt64 → Python int
        return int(run_native("PathAnalysisEntry.RaysInPath get",
                              lambda: self.native.RaysInPath,
                              ensure=self.ensure_native))

    @property
    def HitsInPath(self) -> int:
        return int(run_native("PathAnalysisEntry.HitsInPath get",
                              lambda: self.native.HitsInPath,
                              ensure=self.ensure_native))

    @property
    def GhostsInPath(self) -> int:
        return int(run_native("PathAnalysisEntry.GhostsInPath get",
                              lambda: self.native.GhostsInPath,
                              ensure=self.ensure_native))

    @property
    def UniqueObjectsInPath(self) -> int:
        return int(run_native("PathAnalysisEntry.UniqueObjectsInPath get",
                              lambda: self.native.UniqueObjectsInPath,
                              ensure=self.ensure_native))

    @property
    def TotalPathFlux(self) -> float:
        return float(run_native("PathAnalysisEntry.TotalPathFlux get",
                                lambda: self.native.TotalPathFlux,
                                ensure=self.ensure_native))

    @property
    def NumberOfObjectsInPath(self) -> int:
        return int(run_native("PathAnalysisEntry.NumberOfObjectsInPath get",
                              lambda: self.native.NumberOfObjectsInPath,
                              ensure=self.ensure_native))

    @property
    def PathSource(self) -> int:
        return int(run_native("PathAnalysisEntry.PathSource get",
                              lambda: self.native.PathSource,
                              ensure=self._ensure_native))

    # --- Properties (sequences) ---
    @property
    def PathObjectList(self) -> Sequence[int]:
        raw = run_native("PathAnalysisEntry.PathObjectList get",
                         lambda: self.native.PathObjectList,
                         ensure=self._ensure_native)
        if raw is None:
            return []
        # Coerce any iterable of numbers to a list[int]
        return [int(x) for x in raw]

    @property
    def PathObjectAndFaceList(self) -> Sequence[Tuple[int, int]]:
        """
        Returns a list of (object, face) pairs.
        COM often exposes this as int[,]; pythonnet surfaces it as a nested iterable.
        """
        raw2d = run_native("PathAnalysisEntry.PathObjectAndFaceList get",
                           lambda: self.native.PathObjectAndFaceList,
                           ensure=self._ensure_native)
        out: List[Tuple[int, int]] = []
        if raw2d is None:
            return out

        # Handle common shapes: sequence of pairs OR 2D array-like
        try:
            for pair in raw2d:
                # pair could be (obj, face) or a small sequence
                if isinstance(pair, (list, tuple)) and len(pair) >= 2:
                    out.append((int(pair[0]), int(pair[1])))
                else:
                    # Some runtimes yield elements with indexers (e.g., pair[0], pair[1])
                    o = int(pair[0])  # type: ignore[index]
                    f = int(pair[1])  # type: ignore[index]
                    out.append((o, f))
        except Exception:
            # Fallback: try to materialize as a flat list and group by 2
            flat = list(raw2d)
            for i in range(0, len(flat), 2):
                out.append((int(flat[i]), int(flat[i + 1])))
        return out

    # --- Representation ---
    def __repr__(self) -> str:
        try:
            return (f"PathAnalysisEntry(Path={self.PathNumber}, "
                    f"Rays={self.RaysInPath}, Hits={self.HitsInPath}, "
                    f"Flux={self.TotalPathFlux:.3g})")
        except Exception:
            return "PathAnalysisEntry(<unavailable>)"
