from __future__ import annotations
from typing import Generic,Type
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_base import PropertyBase, maybe_ensure

from zempy.zosapi.core.types_var import *

class PropertyEnum(PropertyBase, Generic[E]):
    """Descriptor for enum-typed ZOSAPI properties."""

    __slots__ = ("_enum", "_read_only")

    def __init__(self, native_attr: str, enum: Type[E], *, read_only: bool = False) -> None:
        super().__init__(native_attr)
        self._enum: Type[E] = enum
        self._read_only: bool = read_only

    def __get__(self, instance, owner=None) -> E:
        if instance is None:
            return self  # type: ignore[return-value]
        parent_native = self._require_native_parent(instance)
        maybe_ensure(instance)
        raw = run_native(self._tag("get"), lambda: getattr(parent_native, self._native_attr))
        return self._enum.from_native(instance.zosapi, raw)  # type: ignore[attr-defined]

    def __set__(self, instance, value: E) -> None:
        if self._read_only:
            raise AttributeError(f"{self._tag('set')}: property is read-only")
        parent_native = self._require_native_parent(instance)
        maybe_ensure(instance)
        # enum.to_native(zosapi, value)
        sv = self._enum.to_native(instance.zosapi, value)  # type: ignore[attr-defined]
        run_native(self._tag("set"), lambda: setattr(parent_native, self._native_attr, sv))


def property_enum(native_attr: str, enum: Type[E], *, read_only: bool = False) -> PropertyEnum[E]:
    """Ergonomic helper to match PropertyScalar's style."""
    return PropertyEnum(native_attr, enum, read_only=read_only)
