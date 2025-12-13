from __future__ import annotations
import logging
from typing import Any, Iterator, TYPE_CHECKING
from dataclasses import dataclass
from allytools.types import validate_cast
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.enums.license_status import LicenseStatusType
from zempy.zosapi.system.adapters.optical_system import OpticalSystem
from zempy.zosapi.analysis.adapters.message import Message
from zempy.dotnet.dot_net import DotNet
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.application.adapters.message_log_session import MessageLogSession

if TYPE_CHECKING:
    from zempy.zosapi.core.i_zosapi import IZosapi
    from zempy.zosapi.system.protocols.i_optical_system import IOpticalSystem

log = logging.getLogger(__name__)
@dataclass
class ZOSApplication(BaseAdapter[Z, N]):
    """Wrapper over ZOSAPI.IZOSAPI_Application using ZemPy descriptors."""
    __slots__ = ("_closed",)

    LicenseStatus          = property_enum("LicenseStatus", LicenseStatusType, read_only=True)
    PrimarySystem          = property_adapter("PrimarySystem", adapter=OpticalSystem)
    # Scalars (read-only unless coerce_set provided)
    IsValidLicenseForAPI    = PropertyScalar("IsValidLicenseForAPI",    coerce_get=bool)
    InitializationErrors    = PropertyScalar("InitializationErrors",    coerce_get=lambda s: str(s or ""))
    InitializationErrorCode = PropertyScalar("InitializationErrorCode", coerce_get=lambda s: str(s or ""))
    SerialCode              = PropertyScalar("SerialCode",              coerce_get=lambda s: str(s or ""))
    ZOSMajorVersion         = PropertyScalar("ZOSMajorVersion",         coerce_get=int)
    ZOSMinorVersion         = PropertyScalar("ZOSMinorVersion",         coerce_get=int)
    ZOSSPVersion            = PropertyScalar("ZOSSPVersion",            coerce_get=int)
    OpticStudioVersion      = PropertyScalar("OpticStudioVersion",      coerce_get=int)
    NumberOfOpticalSystems  = PropertyScalar("NumberOfOpticalSystems",  coerce_get=int)
    CheckForUpdatesStatus   = PropertyScalar("CheckForUpdatesStatus",   coerce_get=lambda x: x)
    CheckForUpdatesVersion  = PropertyScalar("CheckForUpdatesVersion",  coerce_get=int)
    CheckForUpdatesData     = PropertyScalar("CheckForUpdatesData",     coerce_get=lambda s: str(s or ""))
    Preferences             = PropertyScalar("Preferences",             coerce_get=lambda x: x)
    OperandResults          = PropertyScalar("OperandResults",          coerce_get=lambda x: x)
    UserAnalysisData        = PropertyScalar("UserAnalysisData",        coerce_get=lambda x: x)
    TerminateRequested      = PropertyScalar("TerminateRequested",      coerce_get=bool)
    ShowChangesInUI         = PropertyScalar("ShowChangesInUI",         coerce_get=bool,  coerce_set=bool)
    ProgressMessage         = PropertyScalar("ProgressMessage",         coerce_get=lambda s: str(s or ""), coerce_set=str)
    ProgressPercent         = PropertyScalar("ProgressPercent",         coerce_get=float, coerce_set=float)
    RunCommand              = PropertyScalar("RunCommand",              coerce_get=str)
    SamplesDir              = PropertyScalar("SamplesDir",              coerce_get=str)
    ProgramDir              = PropertyScalar("ProgramDir",              coerce_get=str)
    ZemaxDataDir            = PropertyScalar("ZemaxDataDir",            coerce_get=str)
    LensDir                 = PropertyScalar("LensDir",                 coerce_get=str)
    ObjectsDir              = PropertyScalar("ObjectsDir",              coerce_get=str)
    GlassDir                = PropertyScalar("ObjectsDir", coerce_get=str)
    ZPLDir = PropertyScalar("ZPLDir", coerce_get=str)
    CoatingDir = PropertyScalar("CoatingDir", coerce_get=str)
    POPDir =  PropertyScalar("POPDir", coerce_get=str)
    ImagesDir = PropertyScalar("ImagesDir", coerce_get=str)
    SolidWorksFilesDir =PropertyScalar("SolidWorksFilesDir", coerce_get=str)
    AutodeskInventorFilesDir = PropertyScalar("AutodeskInventorFilesDir", coerce_get=str)
    CreoParametricFilesDir =PropertyScalar("CreoParametricFilesDir", coerce_get=str)
    ScatterDir = PropertyScalar("ScatterDir", coerce_get=str)
    MATLABFilesDir = PropertyScalar("MATLABFilesDir", coerce_get=str)
    UndoDir =PropertyScalar("UndoDir", coerce_get=str)


    def __post_init__(self) -> None:
        self._closed = False

    def close(self) -> None:
        """Attempt to close OpticStudio; safe to call multiple times."""
        if self._closed:
            log.debug("ZOSApplication.close() skipped: already closed")
            return
        close_fn = getattr(self.native, "CloseApplication", None)
        if not callable(close_fn):
            log.debug("CloseApplication not available on native app; skipping.")
            self._closed = True
            return
        log.debug("Closing OpticStudio application")
        try:
            close_fn()
            log.info("OpticStudio application closed.")
        except (OSError, RuntimeError) as e:
            log.warning("CloseApplication raised a runtime/OS error: %s", e)
        except Exception as e:
            if DotNet.is_exception(e):
                log.warning("%s CLR exception: %s", e)
                raise _exc.ZemaxSystemError(f"Close application failed (CLR): {e}") from e
            raise
        finally:
            self._closed = True

    def __enter__(self) -> ZOSApplication:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close_system(self, index: int, *, save_if_needed: bool = False) -> bool:
        """Close an optical system by index, optionally saving changes first."""
        result = self._rn(
            "CloseSystemAt",
            lambda: self.native.CloseSystemAt(int(index), bool(save_if_needed)),
        )
        return bool(result)


    def date_string(self) -> str:
        """Return the current OpticStudio build date as a string."""
        result = run_native(
            "ZOSApplication.GetDate",
            lambda: self.native.GetDate(),
            ensure=self.ensure_native,
        )
        return str(result or "")

    def systems(self) -> Iterator[IOpticalSystem]:
        """Iterate over all open systems, wrapped as OpticalSystem adapter."""
        for i in range(self.NumberOfOpticalSystems):
            yield validate_cast(OpticalSystem(self.zosapi, self.native.GetSystemAt(i)), IOpticalSystem)

    def get_system(self, index: int) -> IOpticalSystem:
        if not (0 <= index < self.NumberOfOpticalSystems):
            raise IndexError(f"System index out of range: {index}")
        return validate_cast(
            OpticalSystem(self.zosapi, self.native.GetSystemAt(index)), IOpticalSystem
        )


    def load_lens(self, lens_file: str) -> IOpticalSystem:
        """Creates a new optical system and loads the lens file."""
        log.info("Loading lens: %s", lens_file)
        native_sys = self.native.LoadNewSystem(lens_file)
        return validate_cast(OpticalSystem(self.zosapi, native_sys), IOpticalSystem)

    def create_system(self, system_type: Any) -> IOpticalSystem:
        """Creates a new empty optical system of the given SystemType."""
        native_sys = self.native.CreateNewSystem(system_type)
        return validate_cast(OpticalSystem(self.zosapi, native_sys), IOpticalSystem)

    def update_file_lists(self) -> None:
        self.native.UpdateFileLists()

    # ---------- Updates / preferences ----------
    def check_for_updates(self) -> None:
        self.native.CheckForUpdates()

    # ---------- Message log ----------
    def clear_message_log(self) -> None:
        self.native.ClearMessageLog()

    def begin_message_logging(self) -> bool:
        return bool(self.native.BeginMessageLogging())

    def end_message_logging(self) -> bool:
        return bool(self.native.EndMessageLogging())

    def retrieve_log_messages(self) -> str:
        return str(self.native.RetrieveLogMessages())

    def message_log(self) -> MessageLogSession:
        return MessageLogSession(self.native)

    # ---------- Data files / settings ----------
    def create_settings(self) -> Any:
        return self.native.CreateSettings()

    def create_settings_from(self, parent: Any) -> Any:
        return self.native.CreateSettingsFromParent(parent)

    def copy_settings(self, src: Any, dst: Any) -> bool:
        return bool(self.native.CopySettingsData(src, dst))

    def open_data_file(self, filename: str) -> Any:
        return self.native.OpenDataFile(filename)

    def create_data_file(self, filename: str, file_type: Any, data1: int, data2: int) -> Any:
        return self.native.CreateDataFile(filename, file_type, int(data1), int(data2))

    # ---------- Callbacks (wrap IMessage -> ZOSMessage) ----------
    def load_c_callback(self, c_lib: str, callback_name: str, settings: Any) -> Any:
        return self.native.LoadCCallback(c_lib, callback_name, settings)

    def register_c_operand_callback(self, c_lib: str, callback_name: str, settings: Any) -> Message:
        msg = self.native.RegisterCOperandCallback(c_lib, callback_name, settings)
        return Message.from_native(msg)

    def load_net_callback(self, assembly: str, type_name: str, settings: Any) -> Any:
        return self.native.LoadNETCallback(assembly, type_name, settings)

    def register_net_operand_callback(self, assembly: str, type_name: str, settings: Any) -> Message:
        msg = self.native.RegisterNETOperandCallback(assembly, type_name, settings)
        return Message.from_native(msg)

    @classmethod
    def from_connection(cls, conn: Any, zosapi: IZosapi, *, create_new: bool = False, show_ui: bool = True) -> ZOSApplication:
        """
        Build from an IZOSAPI_Connection.
          - If create_new=True: conn.CreateNewApplication(show_ui)
          - Else:               conn.ConnectToApplication()
        """
        app = conn.CreateNewApplication(show_ui) if create_new else conn.ConnectToApplication()
        if app is None:
            raise RuntimeError("Failed to acquire IZOSAPI_Application from connection.")
        return cls(zosapi, app)


    # ---------- Convenience / computed ----------
    @property
    def is_closed(self) -> bool:
        return self._closed

    @property
    def version(self) -> tuple[int, int, int]:
        """(major, minor, sp) grouped from individual scalar props."""
        return self.ZOSMajorVersion, self.ZOSMinorVersion, self.ZOSSPVersion

    def __str__(self) -> str:
        """Human-readable summary for logging and debugging."""
        try:
            major, minor, sp = self.version
            lic = getattr(self.LicenseStatus, "name", self.LicenseStatus)
            return (
                f"<ZOSApplication "
                f"serial={self.SerialCode or '-'} "
                f"version={major}.{minor}.{sp} "
                f"license={lic} "
                f"systems={self.NumberOfOpticalSystems} "
                f"closed={self._closed}>"
            )
        except Exception as e:
            return f"<ZOSApplication (unavailable: {e!r})>"
