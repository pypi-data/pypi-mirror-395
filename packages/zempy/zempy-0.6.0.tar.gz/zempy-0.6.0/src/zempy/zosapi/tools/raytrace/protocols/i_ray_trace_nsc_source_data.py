from __future__ import annotations
from typing import Protocol
from zempy.zosapi.tools.raytrace.enums import NSCTraceOptions

from zempy.zosapi.tools.raytrace.ray_nsc import RayNSCResult, RayNSCSegment


class IRayTraceNSCSourceData(Protocol):
    """Protocol mirroring **ZOSAPI.Tools.RayTrace.IRayTraceNSCSourceData**.

    Interface for defining and reading non-sequential source ray data.
    Enables wavelength control, per-source tracing, and reading back traced
    segments using :meth:`ReadNextResult` and :meth:`ReadNextSegment`.
    """

    # --- wavelength control ---
    def UsePrimaryWavelength(self) -> None: ...

    def UseAnyWavelength(self) -> None: ...

    # --- results API ---
    def StartReadingResults(self) -> bool: ...

    def ReadNextResult(self) -> RayNSCResult: ...

    def ReadNextSegment(self) -> RayNSCSegment: ...

    # --- properties ---
    @property
    def UseSingleSource(self) -> bool: ...

    @UseSingleSource.setter
    def UseSingleSource(self, value: bool) -> None: ...

    @property
    def SurfaceNumber(self) -> int: ...

    @SurfaceNumber.setter
    def SurfaceNumber(self, value: int) -> None: ...

    @property
    def ObjectNumber(self) -> int: ...

    @ObjectNumber.setter
    def ObjectNumber(self, value: int) -> None: ...

    @property
    def MaxRays(self) -> int: ...

    @MaxRays.setter
    def MaxRays(self, value: int) -> None: ...

    @property
    def TraceOptions(self) -> NSCTraceOptions: ...

    @TraceOptions.setter
    def TraceOptions(self, value: NSCTraceOptions) -> None: ...

    @property
    def Wavelength(self) -> int: ...

    @Wavelength.setter
    def Wavelength(self, value: int) -> None: ...

    @property
    def HasResultData(self) -> bool: ...
