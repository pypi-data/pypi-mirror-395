from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.editors.lde.adapters.coating_parameter import CoatingParameter

@dataclass
class CoatingPerformanceData (BaseAdapter[Z, N]):

    SurfaceNumber = PropertyScalar("SurfaceNumber", coerce_get=int)
    Reflection    = property_adapter("Reflection",    CoatingParameter)
    Transmission  = property_adapter("Transmission",  CoatingParameter)
    Absorption    = property_adapter("Absorption",    CoatingParameter)
    Diattenuation = property_adapter("Diattenuation", CoatingParameter)
    Phase         = property_adapter("Phase",         CoatingParameter)
    Retardation   = property_adapter("Retardation",   CoatingParameter)

    def GetCoatingPerformance(self, AOI: float, wavelen: float, direction: Any) -> None:
        """
        Compute/refresh coating performance for given AOI (deg), wavelength (same units as model),
        and ray travel direction (your enum instance).
        """
        run_native(
            "ICoatingPerformanceData.GetCoatingPerformance",
            lambda: self.native.GetCoatingPerformance(float(AOI), float(wavelen), direction),
            ensure=self.ensure_native,
        )

    # ---- repr ----
    def __repr__(self) -> str:
        try:
            return f"CoatingPerformanceData(Surface={self.SurfaceNumber})"
        except Exception:
            return "CoatingPerformanceData(<unavailable>)"
