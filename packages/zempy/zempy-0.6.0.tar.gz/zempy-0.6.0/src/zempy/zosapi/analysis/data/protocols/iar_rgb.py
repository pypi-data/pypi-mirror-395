from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class IAR_Rgb(Protocol):
    """
    ZOSAPI.Analysis.Data.IAR_Rgb
    Simple RGB color container (float components in range 0–1 or 0–255 depending on context).
    """

    @property
    def R(self) -> float: ...
    @property
    def G(self) -> float: ...
    @property
    def B(self) -> float: ...


__all__ = ["IAR_Rgb"]