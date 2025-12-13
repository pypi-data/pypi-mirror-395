from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.tools.raytrace.results.ray import Ray

@dataclass(frozen=True)
class RayPolarized(Ray):
    exr: float
    exi: float
    eyr: float
    eyi: float
    ezr: float
    ezi: float
    intensity: float

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base}"
            f"E-field:\n"
            f"  Ex = ({self.exr:.5e}, {self.exi:.5e})\n"
            f"  Ey = ({self.eyr:.5e}, {self.eyi:.5e})\n"
            f"  Ez = ({self.ezr:.5e}, {self.ezi:.5e})\n"
            f"Intensity = {self.intensity:.3e}>\n"
        )


