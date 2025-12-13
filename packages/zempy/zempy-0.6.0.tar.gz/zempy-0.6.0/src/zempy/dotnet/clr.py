from __future__ import annotations
import importlib
import logging
import threading
from pathlib import Path
from typing import Optional, Union, Iterable

log = logging.getLogger(__name__)

_PathLike = Union[str, Path]


class CLR:
    """
    Small helper around pythonnet's 'clr' module.

    Features:
    - Thread-safe, idempotent initialization
    - 'require' variant that raises on failure
    - Flexible AddReference: strong-name, file, or directory search path
    - Caches last error and version string
    """

    _loaded: bool = False
    _error: Optional[Exception] = None
    _version: Optional[str] = None
    _lock = threading.Lock()
    _clr = None  # cached module handle after init

    # ---------- Status / init ----------

    @classmethod
    def is_available(cls) -> bool:
        """Fast probe whether the 'clr' module can be imported (not initializing it)."""
        try:
            importlib.import_module("clr")
            return True
        except Exception:
            return False

    @classmethod
    def ensure_initialized(cls) -> bool:
        """Initialize pythonnet once; return True on success."""
        if cls._loaded:
            return True
        with cls._lock:
            if cls._loaded:
                return True
            try:
                import clr  # type: ignore
                cls._clr = clr
                # Best-effort version capture (pythonnet 3 exposes __version__)
                cls._version = getattr(clr, "__version__", None)
                cls._loaded = True
                log.debug("pythonnet 'clr' initialized%s",
                          f" (v{cls._version})" if cls._version else "")
                return True
            except Exception as e:
                cls._error = e
                log.debug("pythonnet 'clr' not available: %s", e)
                return False

    @classmethod
    def require_initialized(cls) -> None:
        """Like ensure_initialized but raises on failure."""
        if not cls.ensure_initialized():
            raise RuntimeError("pythonnet 'clr' is not available") from cls._error

    # ---------- References ----------

    @classmethod
    def add_reference(cls, ref: _PathLike) -> bool:
        """
        Add a reference by strong name or by file path (.dll).
        Returns True on success, False on failure (and caches last error).
        """
        if not cls.ensure_initialized():
            return False
        try:
            clr = cls._clr
            ref_str = str(ref)
            # If it's a file path, prefer file load; else assume strong name
            p = Path(ref_str)
            if p.suffix.lower() == ".dll" or p.exists():
                clr.AddReference(ref_str)  # type: ignore[attr-defined]
            else:
                clr.AddReference(ref_str)  # strong name
            return True
        except Exception as e:
            cls._error = e
            log.debug("clr.AddReference(%r) failed: %s", ref, e)
            return False

    @classmethod
    def add_reference_path(cls, *paths: _PathLike) -> int:
        """
        Add one or more directories to the assembly search path.
        Returns number of paths successfully added.
        """
        if not cls.ensure_initialized():
            return 0
        ok = 0
        clr = cls._clr
        for p in paths:
            try:
                d = str(Path(p))
                clr.AddReferencePath(d)  # type: ignore[attr-defined]
                ok += 1
            except Exception as e:
                cls._error = e
                log.debug("clr.AddReferencePath(%r) failed: %s", p, e)
        return ok

    @classmethod
    def add_references(cls, refs: Iterable[_PathLike]) -> int:
        """Convenience: add multiple references; returns count of successes."""
        n = 0
        for r in refs:
            if cls.add_reference(r):
                n += 1
        return n

    # ---------- Introspection ----------

    @classmethod
    def is_loaded(cls) -> bool:
        return cls._loaded

    @classmethod
    def version(cls) -> Optional[str]:
        return cls._version

    @classmethod
    def last_error(cls) -> Optional[Exception]:
        return cls._error
