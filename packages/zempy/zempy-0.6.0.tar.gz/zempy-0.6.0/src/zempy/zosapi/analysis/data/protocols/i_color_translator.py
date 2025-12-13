from __future__ import annotations
from typing import Protocol, runtime_checkable, Sequence, MutableSequence, Tuple, TYPE_CHECKING
from zempy.zosapi.analysis.enums.color_palette_type import ColorPaletteType

@runtime_checkable
class IColorTranslator(Protocol):
    """
    ZOSAPI.Analysis.IColorTranslator
    Translates scalar data to RGB colors using a configured palette/scaling.
    """

    # ----------------------------
    # Single-value conversion
    # ----------------------------
    def GetSingleRGB(self, x: float) -> Tuple[bool, int, int, int]:
        """
        Convert a single scalar value to 8-bit RGB.
        Returns (ok, R, G, B) where ok indicates success.
        """

    def GetSingleRGBFloat(self, x: float) -> Tuple[bool, float, float, float]:
        """
        Convert a single scalar value to float RGB.
        Returns (ok, R, G, B) where ok indicates success.
        """

    # ----------------------------
    # Array conversions (safe copies)
    # ----------------------------
    def GetRGB2DSafe(self, vals: "Sequence[Sequence[float]]") -> "Sequence[Sequence[Sequence[int]]]":
        """
        Convert a 2D array of doubles to a 3D int array [rows][cols][3] (8-bit RGB).
        Mirrors .NET int[,,] GetRGB2DSafe(double[,]).
        """

    def GetRGBSafe(self, vals: "Sequence[float]") -> "Sequence[Sequence[int]]":
        """
        Convert a 1D array of doubles to a 2D int array [N][3] (8-bit RGB).
        Mirrors .NET int[,] GetRGBSafe(double[]).
        """

    def GetRGB2DFloatSafe(self, vals: "Sequence[Sequence[float]]") -> "Sequence[Sequence[Sequence[float]]]":
        """
        Convert a 2D array of doubles to a 3D float array [rows][cols][3] (float RGB).
        Mirrors .NET float[,,] GetRGB2DFloatSafe(double[,]).
        """

    def GetRGBFloatSafe(self, vals: "Sequence[float]") -> "Sequence[Sequence[float]]":
        """
        Convert a 1D array of doubles to a 2D float array [N][3] (float RGB).
        Mirrors .NET float[,] GetRGBFloatSafe(double[]).
        """

    # ----------------------------
    # Array conversions (in-place fill)
    # ----------------------------
    def GetRGB(
        self,
        fullSize: int,
        data: "Sequence[float]",
        rData: "MutableSequence[int]",
        gData: "MutableSequence[int]",
        bData: "MutableSequence[int]",
    ) -> None:
        """
        Fill preallocated 1D buffers with 8-bit RGB for `data` (length == fullSize).
        Mirrors .NET GetRGB(uint, double[], int[], int[], int[]).
        """

    def GetRGBFloat(
        self,
        fullSize: int,
        data: "Sequence[float]",
        rData: "MutableSequence[float]",
        gData: "MutableSequence[float]",
        bData: "MutableSequence[float]",
    ) -> None:
        """
        Fill preallocated 1D buffers with float RGB for `data` (length == fullSize).
        Mirrors .NET GetRGBFloat(uint, double[], float[], float[], float[]).
        """

    # ----------------------------
    # Properties
    # ----------------------------
    @property
    def Palette(self) -> ColorPaletteType:
        """Current color palette (enum)."""

    @property
    def IsInversePalette(self) -> bool:
        """True if the palette is inverted."""

    @property
    def IsAutoScaled(self) -> bool:
        """True if scaling is automatic."""

    @property
    def NumberOfShades(self) -> int:
        """Number of discrete palette shades."""

    @property
    def MinValue(self) -> float:
        """Minimum scalar value for mapping."""

    @property
    def MaxValue(self) -> float:
        """Maximum scalar value for mapping."""

    @property
    def IsLog(self) -> bool:
        """True if logarithmic mapping is enabled."""

    @property
    def LogBase(self) -> float:
        """Logarithm base (if IsLog is True)."""

    @property
    def CanConvertSingleValue(self) -> bool:
        """True if single-value conversion methods are available."""
