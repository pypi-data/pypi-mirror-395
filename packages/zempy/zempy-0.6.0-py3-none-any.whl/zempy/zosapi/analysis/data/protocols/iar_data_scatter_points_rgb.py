from __future__ import annotations
from typing import List, Protocol, Sequence, runtime_checkable
from zempy.zosapi.analysis.data.protocols.iar_scatter_point_rgb import IAR_ScatterPointRgb

@runtime_checkable
class IAR_DataScatterPointsRgb(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_DataScatterPointsRgb."""

    # ---- Methods ----
    def GetPoint(self, idx: int) -> IAR_ScatterPointRgb: ...
    def FillPointValues(
        self,
        fullSize: int,        # COM 'uint' → int
        xData: List[float],   # in/out (double[])
        yData: List[float],   # in/out (double[])
        rData: List[float],   # in/out (float[])
        gData: List[float],   # in/out (float[])
        bData: List[float],   # in/out (float[])
    ) -> None: ...

    # ---- Properties ----
    @property
    def Description(self) -> str: ...

    @property
    def NumPoints(self) -> int: ...  # COM 'uint' → int

    @property
    def Points(self) -> Sequence[IAR_ScatterPointRgb]: ...

    @property
    def XLabel(self) -> str: ...

    @property
    def YLabel(self) -> str: ...

    @property
    def ValueLabel(self) -> str: ...
