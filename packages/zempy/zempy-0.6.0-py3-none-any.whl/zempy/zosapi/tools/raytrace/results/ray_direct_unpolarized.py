from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.tools.raytrace.results.ray_unpolarized import RayUnpolarized

@dataclass(frozen=True)
class RayDirectUnpolarized(RayUnpolarized):
    def __str__(self) -> str:
        base = super().__str__()
        return f"{base}"