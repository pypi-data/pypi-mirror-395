from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class IAR_ScatterPoint(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_ScatterPoint."""

    @property
    def X(self) -> float: ...

    @property
    def Y(self) -> float: ...

    @property
    def Value(self) -> float: ...
