from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING
from allytools.types import str_or_empty
from allytools.types.validate_cast import validate_cast
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.common.adapters.vector_data import VectorData
from zempy.zosapi.common.adapters.matrix_data import MatrixData

if TYPE_CHECKING:
    from zempy.zosapi.common.protocols.i_vector_data import IVectorData
    from zempy.zosapi.common.protocols.i_matrix_data import IMatrixData
    from zempy.zosapi.analysis.data.protocols.i_color_translator import IColorTranslator
    from zempy.zosapi.analysis.data.protocols.iar_data_series_rgb import IAR_DataSeriesRgb


@dataclass(frozen=True, slots=True)
class DataSeries:
    """
    Adapter for ZOSAPI.Analysis.Data.IAR_DataSeries.

    Exposes:
      - Methods: ConvertToRGB(translator)
      - Properties: Description, XLabel, XData, SeriesLabels, NumSeries, YData
    """
    zosapi: object
    native: object

    # -------- lifecycle --------
    @classmethod
    def from_native(cls, zosapi: object, native: object) -> "DataSeries":
        if native is None:
            raise ValueError("DataSeries.from_native: native is None")
        return cls(zosapi, native)

    def ensure_native(self) -> None:
        ensure_not_none(self.native, what="DataSeries.native", exc_type=_exc.ZemaxObjectGone)

    # -------- methods --------
    def ConvertToRGB(self, translator: "IColorTranslator") -> "IAR_DataSeriesRgb":
        """Convert the series to an RGB series (returns native or your RGB adapter if you add one)."""
        return run_native(
            "DataSeries.ConvertToRGB",
            lambda: self.native.ConvertToRGB(translator),
            ensure=self.ensure_native,
        )

    # -------- scalar properties (descriptors) --------
    Description = PropertyScalar("Description", coerce_get=str_or_empty)
    XLabel      = PropertyScalar("XLabel",      coerce_get=str_or_empty)
    NumSeries   = PropertyScalar("NumSeries",   coerce_get=int)

    # -------- complex properties --------
    @property
    def XData(self) -> "IVectorData":
        native = run_native(
            "DataSeries.XData get",
            lambda: self.native.XData,
            ensure=self.ensure_native,
        )
        return validate_cast(VectorData.from_native(self.zosapi, native), "IVectorData")

    @property
    def YData(self) -> "IMatrixData":
        native = run_native(
            "DataSeries.YData get",
            lambda: self.native.YData,
            ensure=self.ensure_native,
        )
        return validate_cast(MatrixData.from_native(self.zosapi, native), "IMatrixData")

    @property
    def SeriesLabels(self) -> Sequence[str]:
        labels = run_native(
            "DataSeries.SeriesLabels get",
            lambda: self.native.SeriesLabels,
            ensure=self.ensure_native,
        )
        return [] if labels is None else [str_or_empty(s) for s in labels]

    # -------- conveniences --------
    def __len__(self) -> int:
        return self.NumSeries

    def __repr__(self) -> str:
        try:
            labels = self.SeriesLabels
            preview = ", ".join(labels[:3])
            more = "…" if len(labels) > 3 else ""
            return f"DataSeries(NumSeries={self.NumSeries}, XLabel='{self.XLabel}', SeriesLabels=[{preview}{more}])"
        except Exception:
            return "DataSeries(<unavailable>)"
