from __future__ import annotations
import logging
from typing import Optional, Any, cast
from zempy.dotnet.clr import CLR
from zempy.bridge import zemax_exceptions as _exc
from zempy.zosapi.core.i_zosapi import IZosapi

log = logging.getLogger(__name__)
class ZOSAPI:
    """Lazy, process-wide loader for the managed ZOSAPI assembly."""
    _mod: Optional[IZosapi] = None
    _error: Optional[Exception] = None

    @classmethod
    def load(cls) -> IZosapi:
        """Import and return the ZOSAPI namespace, initializing CLR if needed."""
        if cls._mod is not None:
            return cls._mod

        # Make sure pythonnet is up
        if not CLR.ensure_initialized():
            err = CLR.last_error()
            cls._error = err
            raise _exc.ZemaxInitError("CLR not initialized for ZOSAPI.") from err

        try:
            import ZOSAPI as _Z  # type: ignore
            mod = cast(IZosapi, _Z)

            # Quick sanity checks for members you depend on
            _ = mod.LicenseStatusType
            _ = mod.Analysis

            cls._mod = mod
            return mod

        except Exception as e:
            cls._error = e
            log.debug("Failed to import ZOSAPI: %s", e)
            raise _exc.ZemaxInitError("Unable to import ZOSAPI.") from e

    # ------------------------------------------------------------------ #
    @classmethod
    def connection(cls) -> Any:
        """Shortcut for ZOSAPI.ZOSAPI_Connection()."""
        mod = cls.load()
        try:
            return mod.ZOSAPI_Connection()
        except Exception as e:
            raise _exc.ZemaxConnectError("Failed to create ZOSAPI_Connection.") from e

    # ------------------------------------------------------------------ #
    @classmethod
    def last_error(cls) -> Optional[Exception]:
        """Return the last import or initialization error, if any."""
        return cls._error
