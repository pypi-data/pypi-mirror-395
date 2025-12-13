from __future__ import annotations
from typing import Protocol, runtime_checkable, Sequence
from zempy.zosapi.analysis.data.protocols.iar_xyz import IAR_XYZ
from zempy.zosapi.analysis.data.protocols.iar_data_grid_rgb import IAR_DataGridRgb
from zempy.zosapi.common.protocols.i_matrix_data import IMatrixData
from zempy.zosapi.analysis.data.protocols.i_color_translator import IColorTranslator

@runtime_checkable
class IAR_DataGrid(Protocol):
    """
    ZOSAPI.Analysis.Data.IAR_DataGrid
    Regular (scalar) data grid returned by many analyses.
    """

    def X(self, rowX: int) -> float: ...
    def Y(self, colY: int) -> float: ...
    def Z(self, rowX: int, colY: int) -> float: ...
    def XYZ(self, rowX: int, colY: int) -> "IAR_XYZ": ...
    def ConvertToRGB(self, translator: "IColorTranslator") -> "IAR_DataGridRgb": ...

    # ----------------------------
    # Properties
    # ----------------------------
    @property
    def Description(self) -> str: ...
    @property
    def XLabel(self) -> str: ...
    @property
    def YLabel(self) -> str: ...
    @property
    def ValueLabel(self) -> str: ...

    @property
    def Nx(self) -> int: ...              # uint in .NET; int in Python
    @property
    def Ny(self) -> int: ...              # uint in .NET; int in Python
    @property
    def Dx(self) -> float: ...
    @property
    def Dy(self) -> float: ...
    @property
    def MinX(self) -> float: ...
    @property
    def MinY(self) -> float: ...

    @property
    def Values(self) -> "Sequence[Sequence[float]]":
        ...

    @property
    def ValueData(self) -> "IMatrixData":
        ...

    @property
    def value_min(self) -> "float": ...

    @property
    def value_max(self) -> "float":
        ...

    @property
    def extent(self) -> tuple[float, float, float, float]:
        ...

__all__ = ["IAR_DataGrid"]
