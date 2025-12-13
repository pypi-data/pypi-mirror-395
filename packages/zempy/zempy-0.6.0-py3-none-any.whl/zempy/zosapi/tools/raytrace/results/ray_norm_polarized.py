from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.tools.raytrace.results.ray_polarized import RayPolarized

@dataclass(frozen=True)
class RayNormPolarized(RayPolarized):
    def __str__(self) -> str:
        base = super().__str__()
        return (f"{base}")

@dataclass(frozen=True)
class RayNormPolarizedFull(RayPolarized):
    xo: float
    yo: float
    zo: float
    lo: float
    mo: float
    no: float


    def __str__(self) -> str:
        base = super().__str__()
        return (f"{base}"
                f"LMN_obj = ({self.lo:.5f}, {self.mo:.5f}, {self.no:.5f})\n")
