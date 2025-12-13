from __future__ import annotations
import logging, inspect
from typing import Callable, Optional, Any, Protocol
from pathlib import Path
from zempy.bridge import zemax_exceptions as _exc
from zempy.dotnet.dot_net import DotNet
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.types_var import *


log = logging.getLogger(__name__)

class _HasRaw(Protocol):
    @property
    def raw(self) -> Any: ...

def update_status(system: Any) -> str:
    s = system.raw.UpdateStatus()
    return "" if s is None else s

def _safe_status(system: Any) -> str:
    try:
        return update_status(system)
    except Exception:
        return ""


def run_op(
    *,
    system: N,
    what: str,
    call: Callable[[], R],
    check: Optional[Callable[[R], bool]] = None,
) -> R:
    frm = inspect.stack()[1]
    where = f"{Path(frm.filename).name}:{frm.lineno}#{frm.function}"

    status_before = _safe_status(system)
    def _call() -> R:
        try:
            return call()
        except Exception as e:
            if DotNet.is_exception(e):
                raise
            raise

    result = run_native(what, _call)

    ok = True
    if check is not None:
        try:
            ok = bool(check(result))
        except Exception as e:
            log.debug("run_op: check(result) raised %r; treating as failure", e)
            ok = False

    status_after = _safe_status(system)
    if not ok:
        raise _exc.ZemaxSystemError(
            f"{what} failed (API returned unsuccessful result). "
            f"status_before={status_before or '-'} "
            f"status_after={status_after or '-'}"
        )

    log.debug("[%s] %s OK", where, what)
    return result
