from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.analysis.adapters.message import Message
from zempy.zosapi.analysis.data.adapters.header_data import HeaderData
from zempy.zosapi.analysis.data.adapters.data_grid import DataGrid
from zempy.zosapi.analysis.data.adapters.data_series import DataSeries
from zempy.zosapi.analysis.data.adapters.critical_ray_data import CriticalRayData
from zempy.zosapi.analysis.data.adapters.path_analysis_data import PathAnalysisData
from zempy.zosapi.analysis.data.adapters.meta_data import MetaData
from zempy.zosapi.analysis.data.adapters.ray_data import RayData
from zempy.zosapi.analysis.data.adapters.nsc_single_ray_trace_data import NSCSingleRayTraceData
from zempy.zosapi.analysis.data.adapters.spot_data_result_matrix import SpotDataResultMatrix  # if present

if TYPE_CHECKING:
    from zempy.zosapi.analysis.data.protocols.iar_data_grid import IAR_DataGrid
    from zempy.zosapi.analysis.data.protocols.iar_data_grid_rgb import IAR_DataGridRgb
    from zempy.zosapi.analysis.data.protocols.iar_data_series import IAR_DataSeries
    from zempy.zosapi.analysis.data.protocols.iar_data_series_rgb import IAR_DataSeriesRgb
    from zempy.zosapi.analysis.data.protocols.iar_data_scatter_points import IAR_DataScatterPoints
    from zempy.zosapi.analysis.data.protocols.iar_data_scatter_points_rgb import IAR_DataScatterPointsRgb
    from zempy.zosapi.analysis.data.protocols.iar_ray_data import IAR_RayData
    from zempy.zosapi.analysis.data.protocols.iar_path_analysis_data import IAR_PathAnalysisData
    from zempy.zosapi.analysis.data.protocols.iar_spot_data_result_matrix import IAR_SpotDataResultMatrix
    from zempy.zosapi.analysis.data.protocols.iar_nsc_single_ray_trace_data import IAR_NSCSingleRayTraceData
    from zempy.zosapi.analysis.data.protocols.iar_header_data import IAR_HeaderData
    from zempy.zosapi.analysis.data.protocols.iar_meta_data import IAR_MetaData
    from zempy.zosapi.analysis.protocols.i_message import IMessage


@dataclass
class IAR(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Analysis.Data.IAR_."""

    NumberOfDataGrids = PropertyScalar("NumberOfDataGrids", coerce_get=int)
    NumberOfDataGridsRgb = PropertyScalar("NumberOfDataGridsRgb", coerce_get=int)
    NumberOfDataSeries = PropertyScalar("NumberOfDataSeries", coerce_get=int)
    NumberOfDataSeriesRgb = PropertyScalar("NumberOfDataSeriesRgb", coerce_get=int)
    NumberOfDataScatterPoints = PropertyScalar("NumberOfDataScatterPoints", coerce_get=int)
    NumberOfDataScatterPointsRgb = PropertyScalar("NumberOfDataScatterPointsRgb", coerce_get=int)
    NumberOfRayData = PropertyScalar("NumberOfRayData", coerce_get=int)
    NumberOfMessages = PropertyScalar("NumberOfMessages", coerce_get=int)
    MetaData = property_adapter("MetaData", MetaData)
    HeaderData = property_adapter("HeaderData", HeaderData)
    CriticalRayData = property_adapter("CriticalRayData", CriticalRayData)
    PathAnalysisData = property_adapter("PathAnalysisData", PathAnalysisData)
    SpotData = property_adapter("SpotData", SpotDataResultMatrix)
    NSCSingleRayTraceData = property_adapter("NSCSingleRayTraceData", NSCSingleRayTraceData)


    def GetDataGrid(self, index: int) -> "IAR_DataGrid":
        if index >= self.NumberOfDataGrids:
            logging.exception(f"IAR has no grid at index {index} (n_grids={self.NumberOfDataGrids}).")
        native = run_native(
            "IAR.GetDataGrid",
            lambda: self.native.GetDataGrid(int(index)),
            ensure=self.ensure_native,
        )
        return DataGrid.from_native(self.zosapi, native)

    def GetDataGridRgb(self, index: int) -> "IAR_DataGridRgb":
        return run_native(
            "IAR.GetDataGridRgb",
            lambda: self.native.GetDataGridRgb(int(index)),
            ensure=self.ensure_native,
        )

    def GetDataSeries(self, index: int) -> "IAR_DataSeries":
        native = run_native(
            "IAR.GetDataSeries",
            lambda: self.native.GetDataSeries(int(index)),
            ensure=self.ensure_native,
        )
        return DataSeries.from_native(self.zosapi, native)

    def GetDataSeriesRgb(self, index: int) -> "IAR_DataSeriesRgb":
        return run_native(
            "IAR.GetDataSeriesRgb",
            lambda: self.native.GetDataSeriesRgb(int(index)),
            ensure=self.ensure_native,
        )

    def GetDataScatterPoint(self, index: int) -> "IAR_DataScatterPoints":
        return run_native(
            "IAR.GetDataScatterPoint",
            lambda: self.native.GetDataScatterPoint(int(index)),
            ensure=self.ensure_native,
        )

    def GetDataScatterPointRgb(self, index: int) -> "IAR_DataScatterPointsRgb":
        return run_native(
            "IAR.GetDataScatterPointRgb",
            lambda: self.native.GetDataScatterPointRgb(int(index)),
            ensure=self.ensure_native,
        )

    def GetRayData(self, index: int) -> "IAR_RayData":
        native = run_native(
            "IAR.GetRayData",
            lambda: self.native.GetRayData(int(index)),
            ensure=self.ensure_native,
        )
        return RayData.from_native(self.zosapi, native)

    def GetMessageAt(self, index: int) -> "IMessage":
        native = run_native(
            "IAR.GetMessageAt",
            lambda: self.native.GetMessageAt(int(index)),
            ensure=self.ensure_native,
        )
        return Message.from_native(native)

    def GetTextFile(self, Filename: str) -> bool:
        return bool(
            run_native(
                "IAR.GetTextFile",
                lambda: self.native.GetTextFile(str(Filename)),
                ensure=self.ensure_native,
            )
        )

    @property
    def DataGrids(self) -> Sequence["IAR_DataGrid"]:
        return [self.GetDataGrid(i) for i in range(self.NumberOfDataGrids)]

    @property
    def DataGridsRgb(self) -> Sequence["IAR_DataGridRgb"]:
        return [self.GetDataGridRgb(i) for i in range(self.NumberOfDataGridsRgb)]

    @property
    def DataSeries(self) -> Sequence["IAR_DataSeries"]:
        return [self.GetDataSeries(i) for i in range(self.NumberOfDataSeries)]

    @property
    def DataSeriesRgb(self) -> Sequence["IAR_DataSeriesRgb"]:
        return [self.GetDataSeriesRgb(i) for i in range(self.NumberOfDataSeriesRgb)]

    @property
    def DataScatterPoints(self) -> Sequence["IAR_DataScatterPoints"]:
        return [self.GetDataScatterPoint(i) for i in range(self.NumberOfDataScatterPoints)]

    @property
    def DataScatterPointsRgb(self) -> Sequence["IAR_DataScatterPointsRgb"]:
        return [self.GetDataScatterPointRgb(i) for i in range(self.NumberOfDataScatterPointsRgb)]

    @property
    def RayData(self) -> Sequence["IAR_RayData"]:
        return [self.GetRayData(i) for i in range(self.NumberOfRayData)]

    @property
    def Messages(self) -> Sequence["IMessage"]:
        return [self.GetMessageAt(i) for i in range(self.NumberOfMessages)]

    # ---- repr ----
    def __repr__(self) -> str:
        try:
            return (
                f"IAR("
                f"Grids={self.NumberOfDataGrids}, GridsRgb={self.NumberOfDataGridsRgb}, "
                f"Series={self.NumberOfDataSeries}, SeriesRgb={self.NumberOfDataSeriesRgb}, "
                f"ScatterPts={self.NumberOfDataScatterPoints}, ScatterPtsRgb={self.NumberOfDataScatterPointsRgb}, "
                f"RayData={self.NumberOfRayData}, Messages={self.NumberOfMessages})"
            )
        except Exception:
            return "IAR(<unavailable>)"
