from __future__ import annotations
from typing import Protocol, runtime_checkable
from zempy.zosapi.analysis.data.protocols.iar_rgb import IAR_Rgb


@runtime_checkable
class IAR_ScatterPointRgb(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_ScatterPointRgb."""

    @property
    def X(self) -> float: ...
    @property
    def Y(self) -> float: ...
    @property
    def Value(self) -> IAR_Rgb: ...
