from __future__ import annotations
from enum import Enum
from typing import ClassVar, Mapping, Sequence, TypeVar, Type, Iterable, TYPE_CHECKING, cast, Any
from functools import reduce
from allytools.types import coerce_to_str
from contextlib import suppress

if TYPE_CHECKING:
    from zempy.zosapi.core.i_zosapi import IZosapi

E = TypeVar("E", bound="ZosEnumBase")

class _ZosEnumMixin:
    """Logic-only mixin; not itself an Enum."""
    _NATIVE_PATH: ClassVar[str]
    _ALIASES_EXTRA: ClassVar[Mapping[str, Sequence[str]]] = {}

    @classmethod
    def _native_enum(cls, zosapi: "IZosapi"):
        """Resolve the native ZOSAPI enum object."""
        paths = getattr(cls, "_NATIVE_PATHS", [cls._NATIVE_PATH])
        last = None
        for p in paths:
            parts = p.split(".")
            if parts and parts[0].startswith("ZOSAPI"):
                parts = parts[1:]
            try:
                return reduce(getattr, parts, zosapi)
            except AttributeError as e:
                last = e
        raise last or AttributeError(f"No native enum for {cls.__name__}")

    @classmethod
    def _aliases(cls, name: str) -> Iterable[str]:
        """Yield all acceptable alias names for an enum member."""
        yield name
        yield name.title().replace("_", "")
        for extra in cls._ALIASES_EXTRA.get(name, ()):
            yield extra

    @classmethod
    def to_native(cls: Type[E], zosapi: "IZosapi", value: E):
        """Convert Python enum to the matching native ZOSAPI enum."""
        native_enum = cls._native_enum(zosapi)
        for attr in cls._aliases(value.name):
            if hasattr(native_enum, attr):
                return getattr(native_enum, attr)
        raise AttributeError(f"Native {cls.__name__} for {value.name!r} not found.")

    @classmethod
    def from_native(cls: Type[E], zosapi: IZosapi, raw: Any) -> E:
        """Convert a native ZOSAPI enum (or primitive) into a Python enum."""
        #1️⃣ direct match
        if isinstance(raw, cls):
            return raw

        name = coerce_to_str(raw)
        key: str = ""
        member_name: str = ""
        aliases: Sequence[str] = ()

        #2️⃣ try string name
        if name:
            key = name.strip()
            with suppress(KeyError):
                return cls[key.upper()]

            for member_name, aliases in getattr(cls, "_ALIASES_EXTRA", {}).items():
                if key in aliases:
                    return getattr(cls, member_name)

        #3️⃣try integer value
        with suppress(TypeError, ValueError):
            ival = int(raw)
            for m in cast(Iterable[E], cls):
                if m.value == ival:
                    return m

        #4️⃣try object identity / equality in native enum
        with suppress(AttributeError):
            native_enum = cls._native_enum(zosapi)
            for m in cast(Iterable[E], cls):
                if getattr(native_enum, m.name, None) == raw:
                    return m

        raise ValueError(f"{cls.__name__}: cannot map native value {raw!r}")


class ZosEnumBase(_ZosEnumMixin, Enum):
    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    def __str__(self) -> str:
        return self.label

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
    pass

    def __format__(self, spec: str) -> str:
        if spec == "label":
            return self.label
        if spec == "raw":
            return self.name
        return format(str(self), spec)

