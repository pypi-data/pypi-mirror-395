from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Tuple, TYPE_CHECKING
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar


from zempy.zosapi.editors.lde.enums.conversion_order import ConversionOrder
from zempy.zosapi.editors.lde.enums.pupil_apodization_type import PupilApodizationType
from zempy.zosapi.editors.lde.enums.point_cloud_file_format import PointCloudFileFormat
from zempy.zosapi.systemdata.enums.zemax_aperture_type import ZemaxApertureType
from zempy.zosapi.editors.lde.enums.tilt_type import TiltType
if TYPE_CHECKING:
    from zempy.zosapi.editors.lde.protocols.ilde_row import ILDERow
    from zempy.zosapi.analysis.protocols.i_message import IMessage
    from zempy.zosapi.editors.lde.protocols.i_lens_data_editor import (ILDETool_AddCoatingsToAllSurfaces,
                                                                    CoordinateConversionResult,
                                                                    ILDETool_TiltDecenterElements) #TODO not implemented yet

@dataclass
class LensDataEditor(BaseAdapter[Z, N]):

    RowToSurfaceOffset           = PropertyScalar("RowToSurfaceOffset",           coerce_get=int)   # read-only
    NumberOfSurfaces            = PropertyScalar("NumberOfSurfaces",            coerce_get=int)
    NumberOfNonSequentialSurfaces = PropertyScalar("NumberOfNonSequentialSurfaces", coerce_get=int)
    # If you have a real enum class for SurfaceColumn, switch these to property_enum(...)
    FirstColumn                 = PropertyScalar("FirstColumn",                 coerce_get=lambda v: v)  # TODO: enum
    LastColumn                  = PropertyScalar("LastColumn",                  coerce_get=lambda v: v)  # TODO: enum
    StopSurface                 = PropertyScalar("StopSurface",                 coerce_get=int)

    # --- Methods (thin run_native wrappers) ---
    def GetSurfaceAt(self, SurfaceNumber: int) -> ILDERow:
        return run_native("ILDE.GetSurfaceAt", lambda: self.native.GetSurfaceAt(int(SurfaceNumber)), ensure=self.ensure_native)

    def InsertNewSurfaceAt(self, SurfaceNumber: int) -> ILDERow:
        return run_native("ILDE.InsertNewSurfaceAt", lambda: self.native.InsertNewSurfaceAt(int(SurfaceNumber)), ensure=self.ensure_native)

    def AddSurface(self) -> ILDERow:
        return run_native("ILDE.AddSurface", lambda: self.native.AddSurface(), ensure=self.ensure_native)

    def RemoveSurfaceAt(self, SurfaceNumber: int) -> bool:
        return bool(run_native("ILDE.RemoveSurfaceAt", lambda: self.native.RemoveSurfaceAt(int(SurfaceNumber)), ensure=self.ensure_native))

    def RemoveSurfacesAt(self, SurfaceNumber: int, numSurfaces: int) -> int:
        return int(run_native("ILDE.RemoveSurfacesAt", lambda: self.native.RemoveSurfacesAt(int(SurfaceNumber), int(numSurfaces)), ensure=self.ensure_native))

    def ShowLDE(self) -> bool:
        return bool(run_native("ILDE.ShowLDE", lambda: self.native.ShowLDE(), ensure=self.ensure_native))

    def HideLDE(self) -> None:
        run_native("ILDE.HideLDE", lambda: self.native.HideLDE(), ensure=self.ensure_native)

    def GetTool_AddCoatingsToAllSurfaces(self) -> ILDETool_AddCoatingsToAllSurfaces:
        return run_native("ILDE.GetTool_AddCoatingsToAllSurfaces", lambda: self.native.GetTool_AddCoatingsToAllSurfaces(), ensure=self.ensure_native)

    def RunTool_AddCoatingsToAllSurfaces(self, settings: ILDETool_AddCoatingsToAllSurfaces) -> None:
        run_native("ILDE.RunTool_AddCoatingsToAllSurfaces", lambda: self.native.RunTool_AddCoatingsToAllSurfaces(settings), ensure=self.ensure_native)

    def RunTool_RemoveAllApertures(self) -> None:
        run_native("ILDE.RunTool_RemoveAllApertures", lambda: self.native.RunTool_RemoveAllApertures(), ensure=self.ensure_native)

    def RunTool_ConvertSemiDiametersToCircularApertures(self) -> None:
        run_native("ILDE.RunTool_ConvertSemiDiametersToCircularApertures", lambda: self.native.RunTool_ConvertSemiDiametersToCircularApertures(), ensure=self.ensure_native)

    def RunTool_ConvertSemiDiametersToFloatingApertures(self) -> None:
        run_native("ILDE.RunTool_ConvertSemiDiametersToFloatingApertures", lambda: self.native.RunTool_ConvertSemiDiametersToFloatingApertures(), ensure=self.ensure_native)

    def RunTool_ConvertSemiDiametersToMaximumApertures(self) -> None:
        run_native("ILDE.RunTool_ConvertSemiDiametersToMaximumApertures", lambda: self.native.RunTool_ConvertSemiDiametersToMaximumApertures(), ensure=self.ensure_native)

    def RunTool_ReplaceVignettingWithApertures(self) -> None:
        run_native("ILDE.RunTool_ReplaceVignettingWithApertures", lambda: self.native.RunTool_ReplaceVignettingWithApertures(), ensure=self.ensure_native)

    def RunTool_ConvertGlobalToLocalCoordinates(self, FirstSurface: int, LastSurface: int, order: ConversionOrder) -> CoordinateConversionResult:
        return run_native("ILDE.ConvertGlobalToLocal", lambda: self.native.RunTool_ConvertGlobalToLocalCoordinates(int(FirstSurface), int(LastSurface), order), ensure=self.ensure_native)

    def RunTool_ConvertLocalToGlobalCoordinates(self, FirstSurface: int, LastSurface: int, referenceSurface: int) -> CoordinateConversionResult:
        return run_native("ILDE.ConvertLocalToGlobal", lambda: self.native.RunTool_ConvertLocalToGlobalCoordinates(int(FirstSurface), int(LastSurface), int(referenceSurface)), ensure=self.ensure_native)

    def GetApodization(self, px: float, py: float) -> float:
        return float(run_native("ILDE.GetApodization", lambda: self.native.GetApodization(float(px), float(py)), ensure=self.ensure_native))

    def GetFirstOrderData(self) -> Tuple[float, float, float, float, float]:
        def _call():
            # Depending on your runtime, this may be an out-params call; adapt if needed.
            # If the .NET signature uses 'out', your pythonnet binding likely returns a tuple.
            return self.native.GetFirstOrderData()
        EFL, pWFN, rWFN, pIH, pMag = run_native("ILDE.GetFirstOrderData", _call, ensure=self.ensure_native)
        return float(EFL), float(pWFN), float(rWFN), float(pIH), float(pMag)

    def GetGlass(self, Surface: int) -> Tuple[bool, str, float, float, float]:
        return run_native("ILDE.GetGlass", lambda: self.native.GetGlass(int(Surface)), ensure=self.ensure_native)

    def GetGlobalMatrix(self, Surface: int) -> Tuple[bool, float, float, float, float, float, float, float, float, float, float, float]:
        return run_native("ILDE.GetGlobalMatrix", lambda: self.native.GetGlobalMatrix(int(Surface)), ensure=self.ensure_native)

    def GetIndex(self, Surface: int, NumberOfWavelengths: int, indexAtWavelength: Sequence[float]) -> int:
        return int(run_native("ILDE.GetIndex", lambda: self.native.GetIndex(int(Surface), int(NumberOfWavelengths), indexAtWavelength), ensure=self.ensure_native))

    def SetLabel(self, Surface: int, label: int) -> bool:
        return bool(run_native("ILDE.SetLabel", lambda: self.native.SetLabel(int(Surface), int(label)), ensure=self.ensure_native))

    def GetLabel(self, Surface: int) -> Tuple[bool, int]:
        return run_native("ILDE.GetLabel", lambda: self.native.GetLabel(int(Surface)), ensure=self.ensure_native)

    def FindLabel(self, label: int) -> Tuple[bool, int]:
        return run_native("ILDE.FindLabel", lambda: self.native.FindLabel(int(label)), ensure=self.ensure_native)

    def GetPupil(self) -> Tuple[ZemaxApertureType, float, float, float, float, float, PupilApodizationType, float]:
        return run_native("ILDE.GetPupil", lambda: self.native.GetPupil(), ensure=self.ensure_native)

    def GetSag(self, Surface: int, X: float, Y: float) -> Tuple[bool, float, float]:
        return run_native("ILDE.GetSag", lambda: self.native.GetSag(int(Surface), float(X), float(Y)), ensure=self.ensure_native)

    def CopySurfaces(self, fromSurfaceNumber: int, NumberOfSurfaces: int, toSurfaceNumber: int) -> int:
        return int(run_native("ILDE.CopySurfaces", lambda: self.native.CopySurfaces(int(fromSurfaceNumber), int(NumberOfSurfaces), int(toSurfaceNumber)), ensure=self.ensure_native))

    def CopySurfacesFrom(self, fromEditor: ILensDataEditor, fromSurfaceNumber: int, NumberOfSurfaces: int, toSurfaceNumber: int) -> int:
        return int(run_native("ILDE.CopySurfacesFrom", lambda: self.native.CopySurfacesFrom(getattr(fromEditor, "native", fromEditor), int(fromSurfaceNumber), int(NumberOfSurfaces), int(toSurfaceNumber)), ensure=self.ensure_native))

    def RunTool_ReverseElements(self, firstSurface: int, lastSurface: int) -> IMessage:
        return run_native("ILDE.ReverseElements", lambda: self.native.RunTool_ReverseElements(int(firstSurface), int(lastSurface)), ensure=self.ensure_native)

    def RunTool_AddFoldMirror(self, Surface: int, tilt: TiltType, reflectAngle: float) -> IMessage:
        return run_native("ILDE.AddFoldMirror", lambda: self.native.RunTool_AddFoldMirror(int(Surface), tilt, float(reflectAngle)), ensure=self.ensure_native)

    def RunTool_DeleteFoldMirror(self, foldSurface: int) -> IMessage:
        return run_native("ILDE.DeleteFoldMirror", lambda: self.native.RunTool_DeleteFoldMirror(int(foldSurface)), ensure=self.ensure_native)

    def RunTool_MakeDoublePass(self, reflectAtSurface: int) -> IMessage:
        return run_native("ILDE.MakeDoublePass", lambda: self.native.RunTool_MakeDoublePass(int(reflectAtSurface)), ensure=self.ensure_native)

    def RunTool_MakeFocal(self, focalLength: float) -> IMessage:
        return run_native("ILDE.MakeFocal", lambda: self.native.RunTool_MakeFocal(float(focalLength)), ensure=self.ensure_native)

    def CanConvertSurfaceToFreeform(self, fromSurface: int) -> bool:
        return bool(run_native("ILDE.CanConvertSurfaceToFreeform", lambda: self.native.CanConvertSurfaceToFreeform(int(fromSurface)), ensure=self.ensure_native))

    def RunTool_ConvertSurfaceToFreeform(self, fromSurface: int, freeformSurface: int, gridNx: int, gridNy: int, limitToClearAperture: bool) -> IMessage:
        return run_native("ILDE.ConvertSurfaceToFreeform", lambda: self.native.RunTool_ConvertSurfaceToFreeform(int(fromSurface), int(freeformSurface), int(gridNx), int(gridNy), bool(limitToClearAperture)), ensure=self.ensure_native)

    def RunTool_ConvertSurfaceInPlaceToFreeform(self, fromSurface: int, gridNx: int, gridNy: int, limitToClearAperture: bool) -> IMessage:
        return run_native("ILDE.ConvertSurfaceInPlaceToFreeform", lambda: self.native.RunTool_ConvertSurfaceInPlaceToFreeform(int(fromSurface), int(gridNx), int(gridNy), bool(limitToClearAperture)), ensure=self.ensure_native)

    def CanExportPointCloud(self, Surface: int) -> bool:
        return bool(run_native("ILDE.CanExportPointCloud", lambda: self.native.CanExportPointCloud(int(Surface)), ensure=self.ensure_native))

    def RunTool_ExportPointCloudFile(self, Surface: int, filename: str, gridNx: int, gridNy: int, includeSurfaceNormals: bool, format: PointCloudFileFormat) -> IMessage:
        return run_native("ILDE.ExportPointCloudFile", lambda: self.native.RunTool_ExportPointCloudFile(int(Surface), str(filename), int(gridNx), int(gridNy), bool(includeSurfaceNormals), format), ensure=self.ensure_native)

    def GetClosestGlass(self, Surface: int) -> str:
        return str(run_native("ILDE.GetClosestGlass", lambda: self.native.GetClosestGlass(int(Surface)), ensure=self.ensure_native))

    def GetId(self, surface: int) -> int:
        return int(run_native("ILDE.GetId", lambda: self.native.GetId(int(surface)), ensure=self.ensure_native))

    def GetTool_TiltDecenterElements(self) -> ILDETool_TiltDecenterElements:
        return run_native("ILDE.GetTool_TiltDecenterElements", lambda: self.native.GetTool_TiltDecenterElements(), ensure=self.ensure_native)

    def RunTool_TiltDecenterElements(self, settings: ILDETool_TiltDecenterElements) -> IMessage:
        return run_native("ILDE.RunTool_TiltDecenterElements", lambda: self.native.RunTool_TiltDecenterElements(settings), ensure=self.ensure_native)
