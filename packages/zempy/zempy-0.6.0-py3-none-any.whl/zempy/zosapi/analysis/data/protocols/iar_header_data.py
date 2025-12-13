from __future__ import annotations
from typing import Sequence, Protocol, runtime_checkable


@runtime_checkable
class IAR_HeaderData(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_HeaderData."""

    @property
    def Lines(self) -> Sequence[str]: ...
    """List of header lines describing the analysis output (COM 'String[]')."""
