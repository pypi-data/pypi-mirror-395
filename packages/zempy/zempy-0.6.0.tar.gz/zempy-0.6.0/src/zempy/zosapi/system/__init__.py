from __future__ import annotations
from typing import TYPE_CHECKING

__all__ = ("OpticalSystem",)

def __getattr__(name: str):
    if name == "OpticalSystem":
        from zemax.zos.system.adapters.optical_system import OpticalSystem
        return OpticalSystem
    raise AttributeError(name)

if TYPE_CHECKING:
    from zemax.zos.system.adapters.optical_system import OpticalSystem