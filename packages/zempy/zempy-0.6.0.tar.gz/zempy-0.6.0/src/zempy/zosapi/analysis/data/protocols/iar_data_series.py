from __future__ import annotations
from typing import Protocol, runtime_checkable, Sequence
from zempy.zosapi.common.protocols.i_vector_data import IVectorData
from zempy.zosapi.common.protocols.i_matrix_data import IMatrixData
from zempy.zosapi.analysis.data.protocols.i_color_translator import IColorTranslator
from zempy.zosapi.analysis.data.protocols.iar_data_series_rgb import IAR_DataSeriesRgb

@runtime_checkable
class IAR_DataSeries(Protocol):
    """Protocol matching ZOSAPI.Analysis.Data.IAR_DataSeries."""

    # ---- Methods ----
    def ConvertToRGB(self, translator: IColorTranslator) -> IAR_DataSeriesRgb: ...

    # ---- Properties ----
    @property
    def Description(self) -> str: ...

    @property
    def XLabel(self) -> str: ...

    @property
    def XData(self) -> IVectorData: ...

    @property
    def SeriesLabels(self) -> Sequence[str]: ...

    @property
    def NumSeries(self) -> int: ...

    @property
    def YData(self) -> IMatrixData: ...
