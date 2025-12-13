from __future__ import annotations
import numpy as np
from numpy.typing import NDArray
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from math import isclose
from dataclasses import dataclass
from typing import TYPE_CHECKING
from allytools.types import str_or_empty
from allytools.types.validate_cast import validate_cast
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.common.adapters.matrix_data import MatrixData

if TYPE_CHECKING:
    from zempy.zosapi.analysis.data.protocols.iar_data_grid_rgb import IAR_DataGridRgb
    from zempy.zosapi.analysis.data.protocols.iar_xyz import IAR_XYZ
    from zempy.zosapi.common.protocols.i_matrix_data import IMatrixData
    from zempy.zosapi.analysis.data.protocols.i_color_translator import IColorTranslator


@dataclass
class DataGrid (BaseAdapter[Z, N]):

    Description = PropertyScalar("Description", coerce_get=str_or_empty)
    XLabel      = PropertyScalar("XLabel",      coerce_get=str_or_empty)
    YLabel      = PropertyScalar("YLabel",      coerce_get=str_or_empty)
    ValueLabel  = PropertyScalar("ValueLabel",  coerce_get=str_or_empty)
    Nx          = PropertyScalar("Nx",          coerce_get=int)
    Ny          = PropertyScalar("Ny",          coerce_get=int)
    Dx          = PropertyScalar("Dx",          coerce_get=float)
    Dy          = PropertyScalar("Dy",          coerce_get=float)
    MinX        = PropertyScalar("MinX",        coerce_get=float)
    MinY        = PropertyScalar("MinY",        coerce_get=float)

    def X(self, rowX: int) -> float:
        return float(run_native(
            "DataGrid.X",
            lambda: self.native.X(int(rowX)),
            ensure=self.ensure_native
        ))

    def Y(self, colY: int) -> float:
        return float(run_native(
            "DataGrid.Y",
            lambda: self.native.Y(int(colY)),
            ensure=self.ensure_native
        ))

    def Z(self, rowX: int, colY: int) -> float:
        return float(run_native(
            "DataGrid.Z",
            lambda: self.native.Z(int(rowX), int(colY)),
            ensure=self.ensure_native
        ))

    def XYZ(self, rowX: int, colY: int) -> "IAR_XYZ":
        # Returns the native object (duck-typed). Wrap later if you add an XYZ adapter.
        return run_native(
            "DataGrid.XYZ",
            lambda: self.native.XYZ(int(rowX), int(colY)),
            ensure=self.ensure_native
        )

    def ConvertToRGB(self, translator: "IColorTranslator") -> "IAR_DataGridRgb":
        # Returns native RGB grid (duck-typed). Wrap later if you add an adapter.
        return run_native(
            "DataGrid.ConvertToRGB",
            lambda: self.native.ConvertToRGB(translator),
            ensure=self.ensure_native
        )

    # -------- 2D data matrix --------
    @property
    def Values(self) -> NDArray[np.float64]:
        """
        Returns the grid values as a contiguous float64 NumPy array.
        If native returns None, returns an empty (0, 0) array.
        """
        raw = run_native(
            "DataGrid.Values get",
            lambda: self.native.Values,
            ensure=self.ensure_native,
        )
        if raw is None:
            return np.empty((0, 0), dtype=np.float64)

        # COM 2D array -> NumPy float64, contiguous
        arr = np.asarray(raw, dtype=np.float64)
        return np.ascontiguousarray(arr)

    # Expose matrix view via your IMatrixData adapter
    @property
    def ValueData(self) -> "IMatrixData":
        native = run_native(
            "DataGrid.ValueData get",
            lambda: self.native.ValueData,
            ensure=self.ensure_native,
        )
        return validate_cast(MatrixData.from_native(self.zosapi, native), "IMatrixData")

    @property
    def shape(self) -> tuple[int, int]:
        """Grid shape as (Ny, Nx)."""
        return self.Ny, self.Nx

    @property
    def x_max(self) -> float:
        """Maximum X coordinate."""
        return self.MinX + (self.Nx - 1) * self.Dx

    @property
    def y_max(self) -> float:
        """Maximum Y coordinate."""
        return self.MinY + (self.Ny - 1) * self.Dy

    @property
    def x_coords(self) -> NDArray[np.float64]:
        """Array of X-axis coordinates."""
        return self.MinX + self.Dx * np.arange(self.Nx, dtype=np.float64)

    @property
    def y_coords(self) -> NDArray[np.float64]:
        """Array of Y-axis coordinates."""
        return self.MinY + self.Dy * np.arange(self.Ny, dtype=np.float64)

    @property
    def extent(self) -> tuple[float, float, float, float]:
        """Matplotlib-style (xmin, xmax, ymin, ymax) extent tuple."""
        return self.MinX, self.x_max, self.MinY, self.y_max

    @property
    def value_min(self) -> float:
        """Minimum (non-NaN) grid value."""
        try:
            return float(np.nanmin(self.Values))
        except ValueError:
            return float("nan")

    @property
    def value_max(self) -> float:
        """Maximum (non-NaN) grid value."""
        try:
            return float(np.nanmax(self.Values))
        except ValueError:
            return float("nan")

    # -------- Equality / repr --------
    def __eq__(self, other: object) -> bool:
        """Strict equality: only equal if both are the same class and all fields match exactly."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.Description == other.Description
            and self.XLabel == other.XLabel
            and self.YLabel == other.YLabel
            and self.ValueLabel == other.ValueLabel
            and int(self.Nx) == int(other.Nx)
            and int(self.Ny) == int(other.Ny)
            and isclose(float(self.MinX), float(other.MinX), rel_tol=0, abs_tol=1e-15)
            and isclose(float(self.MinY), float(other.MinY), rel_tol=0, abs_tol=1e-15)
            and isclose(float(self.Dx), float(other.Dx), rel_tol=0, abs_tol=1e-15)
            and isclose(float(self.Dy), float(other.Dy), rel_tol=0, abs_tol=1e-15)
            and np.array_equal(np.asarray(self.Values), np.asarray(other.Values))
        )

    def __str__(self) -> str:
        try:
            x_max = float(self.MinX + self.Dx * (self.Nx - 1))
            y_max = float(self.MinY + self.Dy * (self.Ny - 1))
            return (
                f"Grid: {self.Description}\n"
                f"X axis     : {self.XLabel}\n"
                f"Y axis     : {self.YLabel}\n"
                f"Value label: {self.ValueLabel}\n"
                f"Size       : {self.Nx} x {self.Ny}\n"
                f"Range X    : {self.MinX:.6f} to {x_max:.6f}\n"
                f"Range Y    : {self.MinY:.6f} to {y_max:.6f}\n"
                f"Value min  : {self.value_min:.6f}\n"
                f"Value max  : {self.value_max:.6f}"
            )
        except Exception:
            return "DataGrid(<unavailable>)"

    def __repr__(self) -> str:
        try:
            return f"DataGrid({self.Nx}x{self.Ny}, '{self.ValueLabel}' @ {self.XLabel}/{self.YLabel})"
        except Exception:
            return "DataGrid(<unavailable>)"
