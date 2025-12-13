from __future__ import annotations
from typing import Any, Callable, Generic, Optional
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.types_var import *
from zempy.zosapi.core.property_base import PropertyBase, maybe_ensure

class PropertyScalar(PropertyBase, Generic[T]):
    """Descriptor for scalar ZOSAPI properties (int/float/bool/str)."""

    __slots__ = ("_coerce_get", "_coerce_set")

    def __init__(
        self,
        native_attr: str,
        *,
        coerce_get: Callable[[Any], T],
        coerce_set: Optional[Callable[[Any], Any]] = None,
    ) -> None:
        super().__init__(native_attr)
        self._coerce_get = coerce_get
        self._coerce_set = coerce_set

    def __get__(self, instance, owner=None) -> T:
        if instance is None:
            return self
        parent_native = self._require_native_parent(instance)
        maybe_ensure(instance)
        raw = run_native(self._tag("get"),lambda: getattr(parent_native, self._native_attr))
        return self._coerce_get(raw)

    def __set__(self, instance, value: T) -> None:
        if self._coerce_set is None:
            raise AttributeError(f"{self._tag('set')}: property is read-only")
        parent_native = self._require_native_parent(instance)
        maybe_ensure(instance)
        sv = self._coerce_set(value)
        run_native(self._tag("set"), lambda: setattr(parent_native, self._native_attr, sv))

