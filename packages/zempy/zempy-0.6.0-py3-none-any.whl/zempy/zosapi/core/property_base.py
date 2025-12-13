from __future__ import annotations
from typing import Any

def maybe_ensure(instance: Any) -> None:
    # only call public alias; if not present, skip (no linter warnings)
    ensure = getattr(instance, "ensure_native", None)
    if callable(ensure):
        ensure()

class PropertyBase:
    """Shared plumbing for ZOSAPI descriptors:
       - auto label via __set_name__
       - require instance.native
       - optional instance.ensure_native()
       - build 'Owner.prop.NativeAttr get/set' tags
    """
    __slots__ = ("_native_attr", "_label")

    def __init__(self, native_attr: str) -> None:
        self._native_attr = native_attr
        self._label: str = "<unbound>"

    def __set_name__(self, owner, name) -> None:
        self._label = f"{owner.__name__}.{name}"


    #instace  should have native property
    def _require_native_parent(self, instance: Any) -> Any:
        if not hasattr(instance, "native"):
            raise AttributeError(
                f"{type(instance).__name__}.{self._native_attr}: missing required 'native' attribute."
            )
        return instance.native

    def _tag(self, suffix: str) -> str:
        return f"{self._label}.{self._native_attr} {suffix}"
