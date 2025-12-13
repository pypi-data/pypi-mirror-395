from __future__ import annotations
from typing import Protocol, runtime_checkable, Generic, ClassVar, Any, Optional, Callable

@runtime_checkable
class ICoatingParameter(Protocol):
    # ZOSAPI.Editors.ICoatingParameter
    @property
    def S(self) -> float: ...
    @S.setter
    def S(self, value: float) -> None: ...

    @property
    def P(self) -> float: ...
    @P.setter
    def P(self, value: float) -> None: ...

