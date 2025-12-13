from __future__ import annotations
from typing import Protocol, runtime_checkable, Optional, Any, TYPE_CHECKING

from zempy.zosapi.enums.system_type import SystemType
from zempy.zosapi.enums.session_modes import SessionModes

if TYPE_CHECKING:
    from zempy.zosapi.application.protocols.i_application import IApplication  # IZOSAPI_Application owner
    from zempy.zosapi.analysis.protocols.i_analyses import IAnalyses
    from zempy.zosapi.system.protocols.i_metadata import IMetadata
    from zempy.zosapi.tools.protocols.i_optical_system_tools import IOpticalSystemTools
    from zempy.zosapi.systemdata.protocols.i_system_data import ISystemData
    from zempy.zosapi.editors.lde.protocols.i_lens_data_editor import ILensDataEditor

    # from zempy.zosapi.system.protocols.INonSeqEditor import INonSeqEditor
    # from zempy.zosapi.system.protocols.IToleranceDataEditor import IToleranceDataEditor
    # from zempy.zosapi.system.protocols.IMeritFunctionEditor import IMeritFunctionEditor
    # from zempy.zosapi.system.protocols.IMultiConfigEditor import IMultiConfigEditor

@runtime_checkable
class IOpticalSystem(Protocol):
    # ---------- Public Member Functions ----------
    def GetCurrentStatus(self) -> str: ...
    def UpdateStatus(self) -> str: ...
    def MakeSequential(self) -> bool: ...
    def MakeNonSequential(self) -> bool: ...
    def LoadFile(self, LensFile: str, saveIfNeeded: bool) -> bool: ...
    def New(self, saveIfNeeded: bool) -> None: ...
    def Save(self) -> None: ...
    def SaveAs(self, fileName: str) -> None: ...
    def Close(self, saveIfNeeded: bool) -> bool: ...
    def CopySystem(self) -> IOpticalSystem: ...
    def UpdateFileLists(self) -> None: ...
    def ConvertToProjectDirectory(self, folderPath: str) -> bool: ...
    def TurnOffProjectDirectory(self) -> bool: ...
    def GetMetadata(self) -> Optional[IMetadata]: ...

    # ---------- Properties ----------
    @property
    def SystemName(self) -> str: ...
    @SystemName.setter
    def SystemName(self, value: str) -> None: ...

    @property
    def SystemID(self) -> int: ...

    @property
    def Mode(self) -> SystemType: ...

    @property
    def SystemFile(self) -> str: ...

    @property
    def IsNonAxial(self) -> bool: ...

    @property
    def NeedsSave(self) -> bool: ...

    @property
    def SystemData(self) -> ISystemData: ...

    @property
    def LDE(self) -> ILensDataEditor: ...

    @property
    def NCE(self) -> Any: ...         # INonSeqEditor

    @property
    def TDE(self) -> Any: ...         # IToleranceDataEditor

    @property
    def MFE(self) -> Any: ...         # IMeritFunctionEditor

    @property
    def MCE(self) -> Any: ...         # IMultiConfigEditor

    @property
    def Analyses(self) -> IAnalyses: ...

    @property
    def Tools(self) -> IOpticalSystemTools: ...

    @property
    def TheApplication(self) -> IApplication: ...

    @property
    def UpdateMode(self) -> Any: ...  # LensUpdateMode
    @UpdateMode.setter
    def UpdateMode(self, value: Any) -> None: ...

    @property
    def SessionMode(self) -> SessionModes: ...
    @SessionMode.setter
    def SessionMode(self, value: SessionModes) -> None: ...

    @property
    def STARSubsystem(self) -> Any: ...  # ISTARSubsystem

    @property
    def IsProjectDirectory(self) -> bool: ...


__all__ = ["IOpticalSystem"]
