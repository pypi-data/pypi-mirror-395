from __future__ import annotations
from contextlib import contextmanager
from typing import Iterator, Optional
from pathlib import Path
import logging

from zempy.bridge.standalone import StandAlone
from zempy.bridge.zemax_file_session import ZemaxFileSession
from zempy.zosapi.system.adapters.optical_system import OpticalSystem

log = logging.getLogger(__name__)

@contextmanager
def zempy_session(
    filepath: Optional[Path | str] = None,
    *,
    save_on_close: bool = False,
    default_dir: Optional[Path] = None,
) -> Iterator[tuple[StandAlone, OpticalSystem]]:

    log.info("Starting Zemax session%s",
             f" with file: {filepath}" if filepath else " (empty system)")
    try:
        with StandAlone() as zs:
            if filepath is not None:
                with ZemaxFileSession(
                    zs,
                    Path(filepath),
                    save_on_close=save_on_close,
                    default_dir=default_dir,
                ):
                    yield zs, zs.system  # type: ignore[misc]
            else:
                yield zs, zs.system  # type: ignore[misc]
    except Exception:
        log.exception("Unhandled exception inside zemax_session body")
        raise
    finally:
        log.info("Zemax session closed%s",
                 f" (file: {filepath})" if filepath else "")
