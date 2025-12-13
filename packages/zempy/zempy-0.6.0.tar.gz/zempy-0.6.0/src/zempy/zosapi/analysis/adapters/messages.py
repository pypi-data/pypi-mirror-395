from __future__ import annotations
from typing import Any, Iterator, TYPE_CHECKING, cast
from dataclasses import dataclass
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.interop import run_native, ensure_not_none

if TYPE_CHECKING:
    from zempy.zosapi.analysis.protocols.i_message import IMessage
@dataclass()
class Messages(BaseAdapter[Z, N]):  # conforms to IMessages Protocol


    # ---- collection-like behavior ----
    def __len__(self) -> int:
        return run_native(
            "IMessages.Count get",
            lambda: int(getattr(self.native, "Count", len(self.native))),
            ensure=self.ensure_native,
        )

    def __getitem__(self, index: int) -> "IMessage":
        item = run_native(
            "IMessages.__getitem__",
            lambda: self.native[index],
            ensure=self.ensure_native,
        )
        # Optional: wrap with your IMessage adapter if you have one:
        # from zempy.zosapi.analysis.adapters.message import Message
        # return cast("IMessage", Message(self.system, item))
        return cast("IMessage", item)

    def __iter__(self) -> Iterator["IMessage"]:
        # Simple index-based iterator (robust across different native enumerables)
        n = self.__len__()
        for i in range(n):
            yield self[i]

    # ---- API methods ----
    def WriteLine(self, s: str, userV: object, settingsV: object) -> None:
        run_native(
            "IMessages.WriteLine",
            lambda: self.native.WriteLine(s, userV, settingsV),
            ensure=self.ensure_native,
        )

    def AllToString(self) -> str:
        return run_native(
            "IMessages.AllToString",
            lambda: self.native.AllToString(),
            ensure=self._ensure_native,
        )

    # ---- conveniences (optional) ----
    def to_list(self) -> list["IMessage"]:
        """Collect messages into a Python list."""
        return list(self)

    def __repr__(self) -> str:
        try:
            return f"<Messages n={len(self)}>"
        except Exception:
            return "<Messages n=?>"
