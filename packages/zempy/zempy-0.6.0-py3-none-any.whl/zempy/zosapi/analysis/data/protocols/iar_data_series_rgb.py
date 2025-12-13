from __future__ import annotations
from typing import List, Protocol, Sequence, runtime_checkable
from zempy.zosapi.common.protocols.i_vector_data import IVectorData
from zempy.zosapi.analysis.data.protocols.iar_rgb import IAR_Rgb

@runtime_checkable
class IAR_DataSeriesRgb(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_DataSeriesRgb."""

    # ---- Methods ----
    def GetYPoint(self, row: int, col: int) -> IAR_Rgb: ...
    def FillYValues(
        self,
        fullSize: int,          # COM 'uint'; use int in Python
        rData: List[float],     # in/out buffer
        gData: List[float],     # in/out buffer
        bData: List[float],     # in/out buffer
    ) -> None: ...

    # ---- Properties ----
    @property
    def Description(self) -> str: ...

    @property
    def NumSeries(self) -> int: ...        # COM 'uint'; int in Python

    @property
    def XData(self) -> IVectorData: ...

    @property
    def NumberOfRows(self) -> int: ...     # COM 'uint'; int in Python

    @property
    def YVals(self) -> Sequence[Sequence[IAR_Rgb]]: ...  # 2D array of RGB points

    @property
    def XLabel(self) -> str: ...

    @property
    def SeriesLabels(self) -> Sequence[str]: ...
