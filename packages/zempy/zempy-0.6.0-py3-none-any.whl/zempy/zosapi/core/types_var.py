from typing import TypeVar, ParamSpec
from zempy.zosapi.core.enum_base import ZosEnumBase
from zempy.zosapi.core.i_zosapi import IZosapi

# ---------------------------------------------------------------------------
# Type variables used throughout ZemPy's ZOSAPI adapter layer
# ---------------------------------------------------------------------------

# N — "Native" type
# Represents the **underlying COM / .NET ZOSAPI interface** object.
# For example: an instance of IAR_PathAnalysisData or IA_AnalysisSettings.
# Anything coming directly from pythonnet (ZOSAPI) lives under this type.
N = TypeVar("N")

# A — "Adapter" type
# Represents the **Python wrapper** (adapter or selector) that exposes
# a friendlier API around the native COM object. This is what end users
# interact with in ZemPy (e.g., PathAnalysisData, IAS_Field, etc.).
A = TypeVar("A")

# T — "Generic" value type
# A generic placeholder for any arbitrary return or input value.
# Used in helpers like `run_native` or `ensure_not_none` where the type
# depends entirely on the wrapped function’s return value.
T = TypeVar("T")

# E — "Enum" type
# Represents a ZemPy enumeration class derived from ZosEnumBase.
# Used when working with strongly-typed enum properties (e.g., polarization states).
E = TypeVar("E", bound=ZosEnumBase)

# P — Parameter specification
# Captures *args/**kwargs signatures for decorators that preserve the
# wrapped function’s call signature, e.g. native_call().
P = ParamSpec("P")

# Z — "ZOSAPI module" type
# Represents the **active, loaded ZOSAPI module instance** itself,
# which provides access to all ZOSAPI namespaces and interfaces.
# This is typically passed down from the root (e.g., zosapi = ZOSAPI.ZOSAPI_Connection())
# and used by adapters to construct typed sub-objects and enums.
Z = TypeVar("Z", bound="IZosapi")  # the loaded ZOSAPI module

# R — "Result" type
# A generic placeholder for **function or operation results**,
# distinct from `T` to improve readability in run_op / run_native
# helpers that wrap callable execution and return a checked or
# transformed value. Represents the final, validated return type.
R = TypeVar("R")
# ---------------------------------------------------------------------------
# Exported symbols
# ---------------------------------------------------------------------------
__all__ = ["N", "A", "T", "E", "P", "Z", "R"]
