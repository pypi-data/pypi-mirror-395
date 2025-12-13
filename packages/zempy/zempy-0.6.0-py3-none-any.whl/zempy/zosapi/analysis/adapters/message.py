from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.analysis.enums.error_types import ErrorType


@dataclass
class Message (BaseAdapter[Z, N]):
    """Python wrapper for ZOSAPI.Analysis.IMessage  interface."""

    Text = PropertyScalar("Text", coerce_get=str)
    ErrorCode = property_enum("ErrorCode", enum=ErrorType, read_only=True)

    @classmethod
    def from_error(cls, zosapi: Z, error_code: ErrorType, message_text: str) -> "Message":
        """Create a synthetic message when no native IMessage exists."""

        class _PseudoNative:
            def __init__(self, code, text):
                self.ErrorCode = code
                self.Text = text

        return cls(zosapi, _PseudoNative(error_code, message_text))

    @property
    def ok(self) -> bool:
        return self.ErrorCode is ErrorType.Success

    def __bool__(self) -> bool:
        return self.ok

    def __str__(self) -> str:
        return f"[{self.ErrorCode.name}] {self.Text}"