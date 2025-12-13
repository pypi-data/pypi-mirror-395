from __future__ import annotations
from typing import Protocol, runtime_checkable, Iterable, Optional, Union

ByteSeq = Union[bytes, bytearray, Iterable[int]]


@runtime_checkable
class IMetadata(Protocol):

    @property
    def number_of_keys(self) -> int:
        """Total count of keys (1-based)."""
        ...

    def get_key_name(self, key_number: int) -> str:
        """Return the key name by 1-based index."""
        ...

    def get(self, key: str) -> Optional[str]:
        """Get a value for `key`; returns None (or empty) if not present."""
        ...

    def set(self, key: str, value: str) -> None:
        """Set or update a key to a string value."""
        ...

    def remove(self, key: str) -> bool:
        """Remove a key. Returns True if removed, False if it did not exist."""
        ...

    def convert_from_binary(self, data: ByteSeq) -> str:
        """Convert byte[] → string using native API."""
        ...

    def convert_to_binary(self, s: str) -> ByteSeq:
        """Convert string → byte[] using native API (byte-like sequence)."""
        ...

    def create_guid(self) -> str:
        """Return a new GUID string from the native API."""
        ...


__all__ = ["IMetadata", "ByteSeq"]
