import logging
import threading
from typing import Optional
from zempy.dotnet.clr import CLR

log = logging.getLogger(__name__)

class DotNet:
    _instance: Optional["DotNet"] = None
    _lock = threading.Lock()

    _system = None
    _error: Optional[Exception] = None
    _initialized = False

    Array   = None
    Int32   = None
    String  = None
    Object  = None
    Byte    = None
    Boolean = None
    Double  = None

    def __new__(cls):
        if cls._instance is not None:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return
        if not CLR.ensure_initialized():
            self.__class__._error = RuntimeError("CLR not initialized; .NET System unavailable.")
            raise self.__class__._error
        try:
            import System  # type: ignore
            self.__class__._system = System
            self.__class__.Array = System.Array
            self.__class__.Int32 = System.Int32
            self.__class__.String = System.String
            self.__class__.Byte = System.Byte
            self.__class__.Boolean = System.Boolean
            self.__class__.Double = System.Double
            self.__class__.Object = System.Object
            self.__class__._initialized = True
        except Exception as e:
            self.__class__._error = e
            log.debug(".NET System namespace not available: %s", e)
            raise RuntimeError("Failed to import .NET 'System'") from e

    @classmethod
    def get(cls) -> "DotNet":
        return cls()

    @property
    def System(self):
        if self._system is None:
            if self._error:
                raise RuntimeError("System namespace unavailable") from self._error
            raise RuntimeError("System namespace not initialized.")
        return self._system

    def __getattr__(self, name: str):
        return getattr(self.System, name)

    # --- Your utilities ---

    @classmethod
    def is_exception(cls, exc: BaseException) -> bool:
        """
        True if `exc` is a managed System.Exception (proxied by pythonnet) and CLR is active.
        Pure Python exceptions will return False.
        """
        try:
            dn = cls.get()
        except Exception:
            return False
        try:
            return isinstance(exc, dn.System.Exception)  # type: ignore[attr-defined]
        except Exception as e:
            log.debug("CLR isinstance check failed: %s", e)
            return False

    @classmethod
    def last_error(cls) -> Optional[Exception]:
        """Return the last initialization/import error (if any)."""
        return cls._error

    @classmethod
    def collect_garbage(cls, *, aggressive: bool = True) -> bool:
        """
        Trigger .NET GC if available. Returns True on success, False otherwise.
        Aggressive=True runs a second Collect() after finalizers.
        """
        try:
            dn = cls.get()
            GC = dn.System.GC  # type: ignore[attr-defined]
            GC.Collect()
            GC.WaitForPendingFinalizers()
            if aggressive:
                GC.Collect()
            return True
        except Exception as e:
            log.debug("GC invocation failed or CLR unavailable: %s", e)
            return False