from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_base import PropertyBase, maybe_ensure
from zempy.zosapi.core.types_var import *


class PropertySequence(PropertyBase, Generic[T]):
    __slots__ = ("_coerce_item", "_container")

    def __init__(self, native_attr: str, *, coerce_item: Callable[[Any], T], container=list):
        super().__init__(native_attr)
        self._coerce_item = coerce_item
        self._container = container

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        parent_native = self._require_native_parent(instance)
        maybe_ensure(instance)
        raw = run_native(self._tag("get"), lambda: getattr(parent_native, self._native_attr))
        if raw is None:
            return self._container()
        return self._container(self._coerce_item(x) for x in raw)
