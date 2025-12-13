from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.tools.raytrace.results.ray import Ray

@dataclass(frozen=True)
class RayUnpolarized(Ray):
    vignetteCode: int
    X: float
    Y: float
    Z: float
    L: float
    M: float
    N: float
    l2: float
    m2: float
    n2: float
    intensity: float

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base}"
            f"vig = {self.vignetteCode}\n"
            f"XYZ = ({self.X:.4f}, {self.Y:.4f}, {self.Z:.4f})\n"
            f"LMN = ({self.L:.5f}, {self.M:.5f}, {self.N:.5f})\n"
            f"LMN2 = ({self.l2:.5f}, {self.m2:.5f}, {self.n2:.5f})\n"
            f"Intensity = {self.intensity:.3f}>\n"
        )
