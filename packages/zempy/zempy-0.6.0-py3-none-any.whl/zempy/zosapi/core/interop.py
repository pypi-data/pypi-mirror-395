from __future__ import annotations
import logging
from typing import Callable, Optional, Any
from functools import wraps
from zempy.dotnet.dot_net import DotNet
from zempy.zosapi.core.types_var import P, T
log = logging.getLogger(__name__)

def ensure_not_none(value: Any, *, what: str, exc_type: type[BaseException], message: Optional[str] = None) -> None:
    """
    Raise `exc_type` if `value` is None. Standardizes native object presence checks.
    """
    if value is None:
        msg = message or f"{what} is not available."
        raise exc_type(msg)

def run_native(what: str, call: Callable[[], T], *, ensure: Optional[Callable[[], None]] = None) -> T:
    """
    Execute a native (COM/.NET) call with unified exception translation & optional pre-check.

    Parameters
    ----------
    what   : str
        Human-readable operation name for logs and error context.
    call   : Callable[[], T]
        Zero-argument function that performs the actual native call.
    ensure : Optional[Callable[[], None]]
        Optional callable that validates preconditions (e.g., native object presence).

    Returns
    -------
    The result of `call()`.
    """
    # Avoid cyclic import if interop imports early
    from zempy.bridge import zemax_exceptions as _exc

    if ensure is not None:
        ensure()
    try:
        return call()
    except (OSError, RuntimeError) as e:
        log.warning("%s runtime/OS error: %s", what, e)
        raise _exc.ZemaxSystemError(f"{what} failed (runtime/OS): {e}") from e
    except Exception as e:
        # Check if CLR is active and exception is a .NET System.Exception
        if DotNet.is_exception(e):
            log.warning("%s CLR exception: %s", what, e)
            raise _exc.ZemaxSystemError(f"{what} failed (CLR): {e}") from e

        raise

def native_call(what: str, ensure: Optional[Callable[[], None]] = None):
    """
    Decorator form of `run_native`. Wraps a zero-arg function body.

    Example
    -------
    @native_call("IMetadata.NumberOfKeys get", ensure=self.ensure_native)
    def _get_keys():
        return self.native_meta.NumberOfKeys
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return run_native(what, lambda: func(*args, **kwargs), ensure=ensure)
        return wrapper
    return decorator
