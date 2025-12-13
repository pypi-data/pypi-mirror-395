from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional, Union
from zempy.bridge import zemax_exceptions as _exc

log = logging.getLogger(__name__)
class ZemaxFileSession:
    """
    High-level helper that opens a Zemax file (ZMX/ZOS) for the duration of a context
    and optionally saves it on close.

    Policy decisions handled here:
      - Resolve relative paths (default: against sample_dir)
      - Optionally create parent directories on save_as
      - Control overwrite behavior on save_as
    """
    def __init__(
        self,
        zs,
        zos_file: Union[str, Path],
        *,
        save_on_close: bool = False,
        default_dir: Optional[Path] = None,
    ) -> None:
        self.zs = zs
        self.zos_file = Path(zos_file)
        self.save_on_close = bool(save_on_close)
        self._default_dir = default_dir
        self._opened = False
        self._resolved_in: Optional[Path] = None

    def _resolve_input(self, p: Union[str, Path]) -> Path:
        """Resolve an input file path using policy (defaults to sample_dir)."""
        path = Path(p)
        if not path.is_absolute():
            base = self._default_dir or self.zs.sample_dir()
            if self._default_dir is not None and not Path(self._default_dir).exists():
                raise _exc.ZemaxFileMissing(
                    f"Default directory does not exist: {self._default_dir}"
                )
            path = Path(base) / path
        return path

    def _resolve_output(
        self,
        p: Union[str, Path],
        *,
        create_dirs: bool = True,
        overwrite: bool = True,
        base: Optional[Path] = None,
    ) -> Path:
        """Resolve a target path for save_as according to policy."""
        out = Path(p)
        if not out.is_absolute():
            root = base or self._default_dir or Path.cwd()
            out = root / out

        parent = out.parent
        if create_dirs:
            parent.mkdir(parents=True, exist_ok=True)
        else:
            if not parent.exists():
                raise FileNotFoundError(f"Output directory does not exist: {parent}")

        if out.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {out}")

        return out


    # Context manager
    def __enter__(self) -> ZemaxFileSession:
        """Open the specified file and load it into the active Zemax system."""
        if not self.zs.is_connected:
            raise _exc.ZemaxInitializationError("Zemax is not connected. Call zs.connect() first.")
        self._resolved_in = self._resolve_input(self.zos_file)
        log.info("Opening file: %s (save_on_close=%s)", self._resolved_in, self.save_on_close)

        if not self._resolved_in.exists():
            raise _exc.ZemaxFileMissing(f"File does not exist: {self._resolved_in}")
        self.zs.open_file(self._resolved_in, save_if_needed=False)
        self._opened = True
        return self


    def __exit__(self, exc_type, exc, tb) -> None:
        log.debug(
            "Exiting file session (saved=%s)%s",
            self.save_on_close,
            f": {self._resolved_in}" if self._resolved_in else "")
        if self._opened and self.save_on_close:
            try:
                self.save()
            except Exception as e:
                log.warning("system save during file session exit failed %r", e)
            finally:
                log.info("Closed file session (saved=%s)%s",
                         self.save_on_close,
                         f": {self._resolved_in}" if self._resolved_in else "")
                self._opened = False
                self._resolved_in = None

    def save(self) -> None:
        """Save the current system in-place."""
        if not self.zs.is_connected or self.zs.system is None:
            raise _exc.ZemaxSystemError("Not connected / system unavailable.")
        log.info("Saving current system (policy layer).")
        self.zs.system.save()

    def save_as(
        self,
        target: Union[str, Path],
        *,
        create_dirs: bool = True,
        overwrite: bool = True,
        base: Optional[Path] = None,
    ) -> Path:
        """Save the current system to a resolved path and return that path."""
        if not self.zs.is_connected or self.zs.system is None:
            raise _exc.ZemaxSystemError("Not connected / system unavailable.")

        out = self._resolve_output(
            target,
            create_dirs=create_dirs,
            overwrite=overwrite,
            base=base,
        )
        log.info("Saving system as: %s", out)
        self.zs.system.save_as(out)
        return out

    def __repr__(self) -> str:
        return (
            f"<ZemaxFileSession opened={self._opened} "
            f"file={self._resolved_in or self.zos_file}>"
        )
