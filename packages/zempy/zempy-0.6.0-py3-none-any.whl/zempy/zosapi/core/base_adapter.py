from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Generic, Optional,Self
from zempy.zosapi.core.interop import run_native, ensure_not_none
from zempy.zosapi.core.types_var import T, N, Z

@dataclass
class BaseAdapter(Generic[Z, N]):
    """
    Shared base for ZOSAPI adapters.

    Features:
    - `zosapi` and `native` fields
    - `from_native()` with optional NATIVE_COERCER and REQUIRED_NATIVE_ATTRS validation
    - `ensure_native()` standard pre-check (used by descriptors via maybe_ensure)
    - `_ensure_native()` alias for enum descriptor which calls `self._ensure_native`
    - `_rn()` small helper around run_native(...)
    """

    zosapi: Z
    native: N

    REQUIRED_NATIVE_ATTRS: ClassVar[tuple[str, ...]] = ()
    NATIVE_COERCER: ClassVar[Optional[Callable[[Any], Any]]] = None

    @classmethod
    def from_native(cls, zosapi: Z, native: Any) -> Self:
        if native is None:
            raise ValueError(f"{cls.__name__}.from_native: native is None")
        if cls.NATIVE_COERCER is not None:
            native = cls.NATIVE_COERCER(native)
        if cls.REQUIRED_NATIVE_ATTRS:
            missing = tuple(
                a for a in cls.REQUIRED_NATIVE_ATTRS if not hasattr(native, a)
            )
            if missing:
                raise TypeError(
                    f"{cls.__name__} expected native with attributes {missing}, got {type(native).__name__}"
                )
        return cls(zosapi, native)

    def ensure_native(self) -> None:
        # Standardized guard your descriptors expect via maybe_ensure()
        from zempy.bridge import zemax_exceptions as _exc
        ensure_not_none(self.native, what=f"{type(self).__name__}.native", exc_type=_exc.ZemaxObjectGone)

    def _rn(self, what: str, call: Callable[[], T]) -> T:
        return run_native(what, call, ensure=self.ensure_native)
