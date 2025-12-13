from __future__ import annotations
from typing import Protocol, runtime_checkable, Sequence, Any, TYPE_CHECKING
from zempy.zosapi.editors.enums.surface_type import SurfaceType
from zempy.zosapi.editors.lde.enums.surface_column import SurfaceColumn
if TYPE_CHECKING:
    from zempy.zosapi.editors.protocols.i_editor_cell import IEditorCell
    from zempy.zosapi.editors.lde.protocols.i_surface_type_settings import ISurfaceTypeSettings
    from zempy.zosapi.editors.lde.protocols.i_surface import ISurface
    from zempy.zosapi.editors.lde.protocols.i_coating_performance_data import ICoatingPerformanceData
    from zempy.zosapi.common.protocols.i_meta_data import IMetadata


@runtime_checkable
class ILDETypeData(Protocol):
    ...

@runtime_checkable
class ILDEDrawData(Protocol):
    ...

@runtime_checkable
class ILDEApertureData(Protocol):
    ...

@runtime_checkable
class ILDEScatteringData(Protocol):
    ...

@runtime_checkable
class ILDETiltDecenterData(Protocol):
    ...

@runtime_checkable
class ILDEPhysicalOpticsData(Protocol):
    ...

@runtime_checkable
class ILDECoatingData(Protocol):
    ...

@runtime_checkable
class ILDEImportData(Protocol):
    ...

@runtime_checkable
class ILDECompositeData(Protocol):
    ...

@runtime_checkable
class ISTAR_Data(Protocol):
    ...


@runtime_checkable
class ILDERow(Protocol):
    """
    Protocol mirror of ZOSAPI.Editors.LDE.ILDERow.
    Represents all Lens Data Editor (LDE) data for a single surface row.
    """

    # -------- Methods (Public Member Functions) --------
    def GetSurfaceCell(self, Col: SurfaceColumn) -> IEditorCell:
        """Gets the specified surface cell data (by column)."""
        ...

    def AvailableSurfaceTypes(self) -> Sequence[SurfaceType]:
        """Returns all available surface types for this row."""
        ...

    def GetSurfaceTypeSettings(self, type: SurfaceType) -> ISurfaceTypeSettings:
        """Create settings for the specified surface type (e.g., external files)."""
        ...

    def ChangeType(self, settings: ISurfaceTypeSettings) -> bool:
        """Change the current surface to the specified type using the given settings."""
        ...

    def GetMetadata(self) -> IMetadata:
        """Get metadata associated with this row/surface."""
        ...

    def GetCoatingPerformanceData(self) -> ICoatingPerformanceData:
        """Get coating performance data for this surface."""
        ...

    # -------- Properties --------
    @property
    def IsActive(self) -> bool:
        """True if this row refers to a valid surface in the system."""
        ...

    @property
    def SurfaceNumber(self) -> int:
        """Surface number for this row (1-based in LDE)."""
        ...

    @property
    def TypeName(self) -> str:
        """Full name of the current surface Type."""
        ...

    @property
    def Type(self) -> SurfaceType:
        """Current surface type."""
        ...

    @property
    def CurrentTypeSettings(self) -> ISurfaceTypeSettings:
        """Settings for the current type (external files, etc.)."""
        ...

    @property
    def IsObject(self) -> bool:
        """True if this is the object surface."""
        ...

    @property
    def IsImage(self) -> bool:
        """True if this is the image surface."""
        ...

    @property
    def IsStop(self) -> bool:
        """True if this is the stop surface."""
        ...

    @IsStop.setter
    def IsStop(self, value: bool) -> None:
        ...

    @property
    def SurfaceData(self) -> ISurface:
        """Access the surface data object."""
        ...

    @property
    def TypeData(self) -> ILDETypeData:
        """Surface Type data."""
        ...

    @property
    def DrawData(self) -> ILDEDrawData:
        """Surface draw data."""
        ...

    @property
    def ApertureData(self) -> ILDEApertureData:
        """Surface aperture data."""
        ...

    @property
    def ScatteringData(self) -> ILDEScatteringData:
        """Surface scattering data."""
        ...

    @property
    def TiltDecenterData(self) -> ILDETiltDecenterData:
        """Surface tilt/decenter data."""
        ...

    @property
    def PhysicalOpticsData(self) -> ILDEPhysicalOpticsData:
        """Surface physical optics data."""
        ...

    @property
    def CoatingData(self) -> ILDECoatingData:
        """Surface coating data."""
        ...

    @property
    def ImportData(self) -> ILDEImportData:
        """Surface import data."""
        ...

    @property
    def CompositeData(self) -> ILDECompositeData:
        """Surface composite data."""
        ...

    @property
    def Comment(self) -> str:
        ...

    @Comment.setter
    def Comment(self, value: str) -> None:
        ...

    @property
    def CommentCell(self) -> IEditorCell:
        ...

    @property
    def Radius(self) -> float:
        ...

    @Radius.setter
    def Radius(self, value: float) -> None:
        ...

    @property
    def RadiusCell(self) -> IEditorCell:
        ...

    @property
    def Thickness(self) -> float:
        """Surface thickness."""
        ...

    @Thickness.setter
    def Thickness(self, value: float) -> None:
        ...

    @property
    def ThicknessCell(self) -> IEditorCell:
        ...

    @property
    def Material(self) -> str:
        ...

    @Material.setter
    def Material(self, value: str) -> None:
        ...

    @property
    def MaterialCell(self) -> IEditorCell:
        ...

    @property
    def Coating(self) -> str:
        ...

    @Coating.setter
    def Coating(self, value: str) -> None:
        ...

    @property
    def CoatingCell(self) -> IEditorCell:
        ...

    @property
    def SemiDiameter(self) -> float:
        ...

    @SemiDiameter.setter
    def SemiDiameter(self, value: float) -> None:
        ...

    @property
    def SemiDiameterCell(self) -> IEditorCell:
        ...

    @property
    def ChipZone(self) -> float:
        ...

    @ChipZone.setter
    def ChipZone(self, value: float) -> None:
        ...

    @property
    def ChipZoneCell(self) -> IEditorCell:
        ...

    @property
    def MechanicalSemiDiameter(self) -> float:
        ...

    @MechanicalSemiDiameter.setter
    def MechanicalSemiDiameter(self, value: float) -> None:
        ...

    @property
    def MechanicalSemiDiameterCell(self) -> IEditorCell:
        ...

    @property
    def Conic(self) -> float:
        ...

    @Conic.setter
    def Conic(self, value: float) -> None:
        ...

    @property
    def ConicCell(self) -> IEditorCell:
        ...

    @property
    def TCE(self) -> float:
        ...

    @TCE.setter
    def TCE(self, value: float) -> None:
        ...

    @property
    def TCECell(self) -> IEditorCell:
        ...

    @property
    def SurfaceId(self) -> int:
        ...

    @property
    def STARData(self) -> ISTAR_Data:
        ...

    @property
    def MaterialCatalog(self) -> str:
        ...
