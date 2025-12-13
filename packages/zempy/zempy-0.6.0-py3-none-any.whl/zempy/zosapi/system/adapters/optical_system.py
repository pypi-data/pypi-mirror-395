from __future__ import annotations
import logging
from typing import Optional, TYPE_CHECKING
from pathlib import Path
from dataclasses import dataclass
from allytools.types import validate_cast
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.enums.session_modes import SessionModes
from zempy.zosapi.enums.system_type import SystemType
from zempy.zosapi.system.helper import run_op
from zempy.zosapi.analysis.adapters.analyses import Analyses
from zempy.zosapi.tools.adapters.optical_system_tools import OpticalSystemTools
from zempy.zosapi.system.adapters.metadata import Metadata
from zempy.zosapi.editors.lde.adapters.lens_data_editor import LensDataEditor
from zempy.zosapi.systemdata.adapters.system_data import SystemData

# from zempy.zosapi.editors.nce.adapters.NonSeqEditor import NonSeqEditor
# from zempy.zosapi.editors.tde.adapters.ToleranceDataEditor import ToleranceDataEditor
# from zempy.zosapi.editors.mfe.adapters.MeritFunctionEditor import MeritFunctionEditor
# from zempy.zosapi.editors.mce.adapters.MultiConfigEditor import MultiConfigEditor
# from zempy.zosapi.system.adapters.SystemData import SystemData
# from zempy.zosapi.enums.system_update_mode import SystemUpdateMode

if TYPE_CHECKING:
    from zempy.zosapi.system.protocols.i_optical_system import IOpticalSystem
    from zempy.zosapi.system.protocols.i_metadata import IMetadata

log = logging.getLogger(__name__)


def _application_adapter():
    from zempy.zosapi.application.adapters.application import ZOSApplication
    return ZOSApplication


@dataclass
class OpticalSystem(BaseAdapter[Z, N]):

    LDE             = property_adapter("LDE", adapter=LensDataEditor)
    Tools           = property_adapter("Tools", adapter=OpticalSystemTools)
    TheApplication  = property_adapter("TheApplication", adapter=_application_adapter)
    Analyses        = property_adapter("Analyses", adapter=Analyses)
    # If you have adapters for these, swap Any->adapters:
    # NCE        = property_adapter("NCE", adapter=NonSeqEditor)
    # TDE        = property_adapter("TDE", adapter=ToleranceDataEditor)
    # MFE        = property_adapter("MFE", adapter=MeritFunctionEditor)
    # MCE        = property_adapter("MCE", adapter=MultiConfigEditor)
    SystemData      = property_adapter("SystemData", adapter=SystemData)

    SystemName    = PropertyScalar("SystemName", coerce_get=str,  coerce_set=str)   # read/write
    SystemID      = PropertyScalar("SystemID",   coerce_get=int)                    # read-only
    SystemFile    = PropertyScalar("SystemFile", coerce_get=str)                    # read-only
    NeedsSave     = PropertyScalar("NeedsSave",  coerce_get=bool)                   # read-only
    IsNonAxial    = PropertyScalar("IsNonAxial", coerce_get=bool)                   # read-only
    IsProjectDirectory = PropertyScalar("IsProjectDirectory", coerce_get=bool)      # read-only
    Mode          = property_enum("Mode", SystemType, read_only=True)
    SessionMode = property_enum("SessionMode", SessionModes)  # read/write enum

    def copy(self) -> IOpticalSystem:
        """Create a duplicate of the current optical system."""
        native_copy = run_native(
            "OpticalSystem.CopySystem",
            lambda: self.native.CopySystem(),
            ensure=self.ensure_native,
        )
        return validate_cast(OpticalSystem(self.zosapi, native_copy), IOpticalSystem)

    def get_current_status(self) -> str:
        """Return the current system status as a string."""
        status = run_native(
            "OpticalSystem.GetCurrentStatus",
            lambda: self.native.GetCurrentStatus(),
            ensure=self.ensure_native,
        )
        return "" if status is None else str(status)

    def update_status(self) -> str:
        """Force OpticStudio to update and return the current system status."""
        status = run_native(
            "OpticalSystem.UpdateStatus",
            lambda: self.native.UpdateStatus(),
            ensure=self.ensure_native,
        )
        return "" if status is None else str(status)

    def set_mode(self, mode: SystemType) -> bool:
        if mode is SystemType.SEQUENTIAL:
            self.native.MakeSequential()
        elif mode is SystemType.NON_SEQUENTIAL:
            self.native.MakeNonSequential()
        else:
            raise ValueError(f"Unsupported SystemType: {mode!r}")
        return True

    def LoadFile(self, lens_file: str | Path, save_if_needed: bool = False) -> None:
        p = Path(lens_file)
        run_op(system=self,
               what=f"LoadFile({p}, save_if_needed={bool(save_if_needed)})",
               call=lambda: self.native.LoadFile(str(p), bool(save_if_needed)),
               check=bool)

    def New(self, save_if_needed: bool = False) -> None:
        run_op(system=self,
               what=f"New(save_if_needed={bool(save_if_needed)})",
               call=lambda: self.native.New(bool(save_if_needed)))

    def Save(self) -> None:
        run_op(system=self, what="Save()", call=lambda: self.native.Save())

    def SaveAs(self, target: str | Path) -> None:
        p = Path(target)
        run_op(system=self, what=f"SaveAs({p})", call=lambda: self.native.SaveAs(str(p)))

    def close_all_analyses(self) -> None:
        try:
            analyses = self.Analyses
            n = int(getattr(analyses, "NumberOfAnalyses", 0) or 0)
            for idx in range(n, 0, -1):
                try:
                    analyses.CloseAnalysis(idx)
                except Exception as e:
                    log.warning("CloseAnalysis(%d) raised: %s", idx, e)
        except Exception as e:
            log.debug("Enumerating/closing analyses failed: %s", e)

    def Close(self, save_if_needed: bool = False) -> None:
        run_op(
            system=self,
            what=f"Close(save_if_needed={bool(save_if_needed)})",
            call=lambda: self.native.Close(bool(save_if_needed)),
            check=lambda r: r is True,
        )

    def UpdateFileLists(self) -> None:
        run_op(
            system=self,
            what="UpdateFileLists()",
            call=lambda: self.native.UpdateFileLists(),
        )

    def ConvertToProjectDirectory(self, folder_path: str) -> bool:
        r = run_op(
            system=self,
            what="ConvertToProjectDirectory()",
            call=lambda: self.native.ConvertToProjectDirectory(),
        )
        return bool(r)

    def TurnOffProjectDirectory(self) -> bool:
        r = run_op(system=self, what="TurnOffProjectDirectory()", call=lambda: self.native.TurnOffProjectDirectory())
        return bool(r)

    def get_metadata(self) -> Optional[IMetadata]:
        native_meta = run_op(system=self, what="GetMetadata()", call=lambda: self.native.GetMetadata())
        if native_meta is None:
            log.debug("GetMetadata() returned None.")
            return None
        log.debug("IMetadata object retrieved successfully.")
        return Metadata(native_meta)
