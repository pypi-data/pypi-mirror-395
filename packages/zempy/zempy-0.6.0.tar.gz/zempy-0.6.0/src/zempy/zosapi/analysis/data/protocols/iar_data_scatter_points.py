from __future__ import annotations
from typing import List, Protocol, Sequence, runtime_checkable
from zempy.zosapi.analysis.data.protocols.iar_scatter_point import IAR_ScatterPoint


@runtime_checkable
class IColorTranslator(Protocol): ...
@runtime_checkable
class IAR_DataScatterPointsRgb(Protocol): ...


@runtime_checkable
class IAR_DataScatterPoints(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_DataScatterPoints."""

    def GetPoint(self, idx: int) -> IAR_ScatterPoint: ...
    def FillPointValues(
        self,
        fullSize: int,
        xData: List[float],
        yData: List[float],
        valueData: List[float],
    ) -> None: ...
    def ConvertToRGB(
        self, translator: IColorTranslator
    ) -> IAR_DataScatterPointsRgb: ...

    @property
    def Description(self) -> str: ...
    @property
    def NumPoints(self) -> int: ...
    @property
    def Points(self) -> Sequence[IAR_ScatterPoint]: ...
    @property
    def XLabel(self) -> str: ...
    @property
    def YLabel(self) -> str: ...
    @property
    def ValueLabel(self) -> str: ...
