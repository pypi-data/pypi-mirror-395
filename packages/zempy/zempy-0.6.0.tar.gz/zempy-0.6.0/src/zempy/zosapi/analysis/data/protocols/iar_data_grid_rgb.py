from __future__ import annotations
from typing import Protocol, runtime_checkable, Sequence
from zempy.zosapi.analysis.data.protocols.iar_rgb import  IAR_Rgb

@runtime_checkable
class IAR_DataGridRgb(Protocol):
    """
    ZOSAPI.Analysis.Data.IAR_DataGridRgb
    RGB data grid container returned by color-capable analyses
    (e.g., Detector Viewer in TrueColor/FalseColor mode).
    """

    # ----------------------------
    # Methods
    # ----------------------------
    def GetValue(self, x: int, y: int) -> "IAR_Rgb":
        """Return RGB value at specified grid coordinates."""
        ...

    def FillValues(
        self,
        fullSize: int,
        rData: Sequence[float],
        gData: Sequence[float],
        bData: Sequence[float],
    ) -> None:
        """
        Retrieve all RGB data into preallocated float arrays.
        Each array must be large enough for fullSize = Nx * Ny.
        """
        ...

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
    def Nx(self) -> int: ...        # uint in .NET; int in Python
    @property
    def Ny(self) -> int: ...        # uint in .NET; int in Python
    @property
    def Dx(self) -> float: ...
    @property
    def Dy(self) -> float: ...
    @property
    def MinX(self) -> float: ...
    @property
    def MinY(self) -> float: ...

    @property
    def Values(self) -> "Sequence[Sequence[IAR_Rgb]]":
        """2D grid of RGB values (IAR_Rgb[,])"""
        ...


__all__ = ["IAR_DataGridRgb"]
