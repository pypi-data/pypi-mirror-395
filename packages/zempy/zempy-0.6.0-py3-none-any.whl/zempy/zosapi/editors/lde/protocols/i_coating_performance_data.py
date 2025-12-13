from __future__ import annotations
from typing import Protocol, runtime_checkable, Any
from zempy.zosapi.editors.lde.protocols.i_coating_parameter import ICoatingParameter


@runtime_checkable
class ICoatingPerformanceData(Protocol):
    # ZOSAPI.Editors.LDE.ICoatingPerformanceData
    def GetCoatingPerformance(self, AOI: float, wavelen: float, direction: Any) -> None: ...

    @property
    def SurfaceNumber(self) -> int: ...

    @property
    def Reflection(self) -> ICoatingParameter: ...

    @property
    def Transmission(self) -> ICoatingParameter: ...

    @property
    def Absorption(self) -> ICoatingParameter: ...

    @property
    def Diattenuation(self) -> ICoatingParameter: ...

    @property
    def Phase(self) -> ICoatingParameter: ...

    @property
    def Retardation(self) -> ICoatingParameter: ...