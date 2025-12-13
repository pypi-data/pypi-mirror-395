from __future__ import annotations
from typing import Protocol, runtime_checkable,Optional
from datetime import datetime


@runtime_checkable
class IAR_MetaData(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_MetaData."""

    @property
    def FeatureDescription(self) -> str: ...
    """Description of the analysis feature or type."""

    @property
    def LensFile(self) -> str: ...
    """Full path to the lens file used for this analysis."""

    @property
    def LensTitle(self) -> str: ...
    """Title of the optical system under analysis."""

    @property
    def Date(self) -> datetime: ...
    """Date and time when the analysis data were generated."""

    @property
    def DateISO(self) -> Optional[str]:      ...

