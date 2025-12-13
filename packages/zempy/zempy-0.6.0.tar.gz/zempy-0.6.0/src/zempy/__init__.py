from __future__ import annotations
import importlib
from importlib.metadata import PackageNotFoundError, version
from typing import Any, TYPE_CHECKING

try:
    __version__ = version("zempy")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__: list[str] = ["__version__", "zempy_session"]


def __getattr__(name: str) -> Any:
    if name == "zempy_session":
        mod = importlib.import_module("zempy.bridge.zempy_session")
        return getattr(mod, "zempy_session")
    raise AttributeError(f"module 'zempy' has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)

if TYPE_CHECKING:
    from zempy.bridge.zempy_session import zempy_session
