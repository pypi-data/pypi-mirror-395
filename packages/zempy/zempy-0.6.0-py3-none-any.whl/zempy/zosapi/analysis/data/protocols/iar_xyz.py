from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class IAR_XYZ(Protocol):
    """
    ZOSAPI.Analysis.Data.IAR_XYZ
    Simple 3D coordinate container used in grid and ray data.
    """

    @property
    def X(self) -> float: ...
    @property
    def Y(self) -> float: ...
    @property
    def Z(self) -> float: ...


__all__ = ["IAR_XYZ"]
