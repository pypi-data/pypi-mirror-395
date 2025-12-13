from __future__ import annotations
from typing import Optional
from .clr import CLR as _CLR
from .dot_net import DotNet as _DotNet

# Private caches
__dn: Optional[_DotNet] = None
__clr_ready: Optional[bool] = None

def clr_ready() -> bool:
    """Lazy check/init of pythonnet. Returns True iff initialized (no raise)."""
    global __clr_ready
    if __clr_ready is None:
        __clr_ready = _CLR.ensure_initialized()
    return bool(__clr_ready)

def dotnet() -> _DotNet:
    """Return the shared DotNet singleton (initializes on first call)."""
    global __dn
    if __dn is None:
        __dn = _DotNet.get()
    return __dn

# Optional: fast shortcuts bound at first use (kept lazy)
def System():
    return dotnet().System

def Array():
    return dotnet().Array

def Int32():
    return dotnet().Int32

def Double():
    return dotnet().Double

# Testing/override hooks (handy for unit tests/mocks)
def _set_dotnet_override(fake: _DotNet | None) -> None:
    global __dn
    __dn = fake

def _reset() -> None:
    """Clear cached singletons (tests only)."""
    global __dn, __clr_ready
    __dn = None
    __clr_ready = None
