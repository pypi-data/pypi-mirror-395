from __future__ import annotations
from typing import Any, Callable, Generic, Optional, Type
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.types_var import *  # N, A
from zempy.zosapi.core.property_base import PropertyBase, maybe_ensure

class PropertyObject(PropertyBase, Generic[N, A]):
    """Descriptor that wraps a native ZOSAPI sub-interface (COM/.NET) into a Python adapter."""

    __slots__ = ("_getter", "_setter", "_ensure_native")  # base already has _native_attr/_label

    def __init__(
        self,
        attr: str,
        *,
        getter: Callable[[Any, N], A],
        setter: Optional[Callable[[A], N]] = None,
        ensure_native: bool = True,
    ) -> None:
        super().__init__(attr)
        self._getter = getter
        self._setter = setter
        self._ensure_native = ensure_native

    def __get__(self, instance, owner=None) -> A:
        if instance is None:
            return self
        parent_native = self._require_native_parent(instance)
        if self._ensure_native:
           maybe_ensure(instance)

        native_child: N = run_native(
            self._tag("get"),
            lambda: getattr(parent_native, self._native_attr),
        )
        return self._getter(instance, native_child)

    def __set__(self, instance, value: A) -> None:
        if self._setter is None:
            raise AttributeError(f"{self._tag('set')}: sub-interface is read-only")
        native_value: N = self._setter(value)
        run_native(
            self._tag("set"),
            lambda: setattr(self._require_native_parent(instance), self._native_attr, native_value),
        )

def property_adapter(attr: str, adapter: Type[A]) -> PropertyObject[Any, A]:
    """Ergonomic sugar: wrap `instance.native.<attr>` with `adapter.from_native(instance.zosapi, native)`."""
    return PropertyObject(
        attr,
            getter=lambda inst, native: adapter.from_native(inst.zosapi, native),
    )
