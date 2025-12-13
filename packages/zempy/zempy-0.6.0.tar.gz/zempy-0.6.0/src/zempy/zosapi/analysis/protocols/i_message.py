from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class IMessage(Protocol):
    """Protocol for ZOSAPI.Analysis.IMessage interface.

    Represents a message returned by a ZOS analysis or system call,
    containing an error code and descriptive text.
    """

    @property
    def ErrorCode(self) -> int:
        """Gets the error type or code associated with this message."""
        ...

    @property
    def Text(self) -> str:
        """Gets the message text description."""
        ...
