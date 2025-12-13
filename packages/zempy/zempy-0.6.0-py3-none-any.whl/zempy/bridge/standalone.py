from __future__ import annotations
import sys
import logging
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING
from allytools.win import DetectOut, detect_into, require_paths
from zempy.bridge.zemax_exceptions import *
from zempy.bridge.zemax_reg import ZEMAX_REGISTRY_CANDIDATES
from zempy.dll.dlls import ZOSAPI_DLL_NAME, NET_HELPER_SUFFIX,ZOSAPI_IF_DLL_NAME
from zempy.dotnet.runtime import dotnet
from zempy.zosapi.core.zosapi import ZOSAPI
from zempy.zosapi.application.adapters.application import ZOSApplication
from zempy.zosapi.system.protocols.i_optical_system import IOpticalSystem
if TYPE_CHECKING:

    from zempy.zosapi.core.i_zosapi import IZosapi
    from zempy.zosapi.application.protocols.i_application import IApplication

log = logging.getLogger(__name__)
class StandAlone:
    """High-level context wrapper for launching and managing an OpticStudio instance via ZOSAPI."""
    def __init__(self) -> None:
        self._zosapi_loaded: bool = False
        self._connection_established: bool = False
        self._closed: bool = False
        self.zosapi_connection: Any = None
        self.zosapi: Optional[IZosapi] = None
        self.system: Optional[IOpticalSystem] = None
        self.application: Optional[IApplication] = None
        self.zemax_dir: Optional[Path] = None
        self.zemax_reg: DetectOut = DetectOut()
        self.license_type: Optional[str] = None

    # Context management
    def __enter__(self) -> StandAlone:
        if not self._zosapi_loaded:
            log.debug("Auto-initializing inside __enter__")
            self.initialize()
        if not self._connection_established:
            log.debug("Auto-connecting inside __enter__")
            self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def start(
        self, install_dir: Optional[Path] = None, create_if_needed: bool = True
    ) -> StandAlone:
        """Convenience shortcut: initialize() + connect()."""
        return self.initialize(install_dir).connect(create_if_needed)

    def require(self) -> StandAlone:
        """Ensure Zemax registry entry exists."""
        if detect_into(ZEMAX_REGISTRY_CANDIDATES, self.zemax_reg):
            log.debug("Zemax registry detected at: %s", self.zemax_reg.path)
            return self
        tried = "\n  - " + "\n  - ".join(map(str, ZEMAX_REGISTRY_CANDIDATES))
        raise ZemaxNotFound(
            "Zemax/OpticStudio not found in registry. Tried:" + tried
        )

    def _get_net_helper_path(self) -> Path:
        """Return path to ZOSAPI_NetHelper.dll."""
        self.require()
        p = Path(self.zemax_reg.path) / NET_HELPER_SUFFIX
        require_paths(p)
        log.debug("Using ZOSAPI NetHelper at: %s", p)
        return p

    def initialize(self, install_dir: Optional[Path] = None) -> StandAlone:
        """Load pythonnet and add references to ZOSAPI assemblies."""
        if self._zosapi_loaded:
            if install_dir is not None:
                new_dir = Path(install_dir).resolve()
                if self.zemax_dir and new_dir != self.zemax_dir.resolve():
                    log.warning(
                        "%s.initialize() called again with a different install_dir:\n"
                        "  existing=%s\n  new=%s\n"
                        "Re-initialization skipped; keeping existing environment.",
                        self.__class__.__name__,
                        self.zemax_dir,
                        new_dir,
                    )
            log.debug("initialize() skipped: already loaded")
            return self
        from zempy.dotnet.clr import CLR
        if not CLR.ensure_initialized():
            raise ZemaxInitializationError(
                "pythonnet (clr) not available/initialized."
            ) from CLR.last_error()
        net_helper_path = self._get_net_helper_path()
        if not CLR.add_reference(str(net_helper_path)):
            raise ZemaxInitializationError(f"Failed to add reference: {net_helper_path}")
        import ZOSAPI_NetHelper  # type: ignore
        ok = (
            ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()
            if install_dir is None
            else ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(str(install_dir))
        )
        if not ok:
            raise ZemaxInitializationError("ZOSAPI_Initializer.Initialize(...) returned False.")
        zemax_dir_str = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
        if not zemax_dir_str:
            raise ZemaxInitializationError("GetZemaxDirectory() returned empty path.")
        self.zemax_dir = Path(zemax_dir_str)
        log.info("Zemax directory: %s", self.zemax_dir)
        if not CLR.add_reference(str(self.zemax_dir / ZOSAPI_DLL_NAME)):
            raise ZemaxInitializationError("Failed to add reference to ZOSAPI.dll")
        if not CLR.add_reference(str(self.zemax_dir / ZOSAPI_IF_DLL_NAME)):
            raise ZemaxInitializationError("Failed to add reference to ZOSAPI_Interfaces.dll")
        self._zosapi_loaded = True
        log.debug("ZOSAPI loaded successfully")
        dotnet()
        log.debug("DotNet created")
        self._closed = False
        return self

    def connect(self, create_if_needed: bool = True) -> StandAlone:
        """Connect to an existing or new OpticStudio instance."""
        if not self._zosapi_loaded:
            raise ZemaxInitializationError("Call initialize() before connect().")
        self.zosapi = ZOSAPI.load()
        self.zosapi_connection = ZOSAPI.connection()
        if self.zosapi_connection is None:
            log.error("ZOSAPI_Connection() returned None")
            raise ZemaxConnectError("Unable to initialize .NET connection to ZOSAPI.")

        app = None
        if not create_if_needed:
            try:
                app = self.zosapi_connection.ConnectToApplication()
                log.info("Connected to existing OpticStudio instance.")
            except Exception as e:
                log.debug("No existing OpticStudio instance found: %r", e)

        if app is None:
            app = self.zosapi_connection.CreateNewApplication()
            log.info("Created new OpticStudio instance.")
        if app is None:
            raise ZemaxInitializationError("Unable to acquire ZOSAPI application.")
        if not app.IsValidLicenseForAPI:
            status = getattr(app, "LicenseStatus", "Unknown")
            raise ZemaxLicenseError(f"License is not valid for ZOSAPI use (status={status}).")
        self.application = ZOSApplication(self.zosapi, app)
        try:
            self.system = self.application.PrimarySystem
            log.info("Primary optical system acquired successfully.")
        except RuntimeError as e:
            raise ZemaxSystemError(f"Unable to acquire Primary system: {e}") from e

        self._connection_established = True
        self.license_type = self.application.LicenseStatus
        log.info("Connected; license=%s", self.license_type.name.title().replace("_", " "))
        return self

    def close(self) -> None:
        log.debug(f"{self.__class__.__name__} closing")
        if self._closed:
            log.debug("close() skipped: already closed")
            return
        if self.application is not None:
            try:
                n = self.application.NumberOfOpticalSystems or 0
                log.debug(f"{self.__class__.__name__} found {self.application.NumberOfOpticalSystems} open systems in application")
                for i in range(int(n) - 1, 0, -1):  # !!! Min system index in Zemax is 1
                    try:
                        ok = self.application.CloseSystemAt(i)
                        if not ok:
                            log.warning("CloseSystemAt(%d) returned False", i)
                    except Exception as e:
                        log.warning("Failed to close system %d: %s", i, e)
            except Exception as e:
                log.debug("Could not enumerate or close systems cleanly: %s", e)
            try:
                self.application.close()
                log.info("OpticStudio application closed.")
            except Exception as e:
                log.warning("CloseApplication raised: %s", e)
            finally:
                self.system = None  # type: ignore[assignment]
                self.application = None  # type: ignore[assignment]
                self.zosapi_connection = None
                self._connection_established = False
                self._closed = True

        log.debug(f"{self.__class__.__name__}.close() completed successfully ")

    def __del__(self) -> None:
        """Ensure graceful cleanup on object deletion."""
        try:
            if sys.is_finalizing():
                return
            try:
                self.close()
            except Exception:
                try:
                    log.warning("Suppressed exception during __del__ while closing",exc_info=True)
                except Exception:
                    pass
        except Exception:
            pass

    def open_file(self, filepath: Path, save_if_needed: bool) -> None:
        """Load a .ZMX/.ZOS file into the current optical system."""
        if not self._connection_established or self.system is None:
            raise ZemaxSystemError(f"Unable to open file; system is not available. Path={filepath}")
        self.system.LoadFile(str(filepath), save_if_needed)

    def sample_dir(self) -> Path:
        """Return the OpticStudio Samples directory."""
        if not self.is_connected or self.application is None:
            raise ZemaxSystemError("Application not available; call connect() first.")
        p = Path(self.application.SamplesDir)
        if not p.exists():
            raise ZemaxSystemError(f"Samples directory does not exist: {p}")
        return p

    @property
    def is_initialized(self) -> bool:
        return self._zosapi_loaded

    @property
    def is_connected(self) -> bool:
        return self._connection_established

    def __repr__(self) -> str:
        return (
            f"<StandAlone initialized={self._zosapi_loaded} "
            f"connected={self._connection_established} closed={self._closed} "
            f"license={self.license_type!r} "
            f"zemax_dir={str(self.zemax_dir) if self.zemax_dir else None}>"
        )
