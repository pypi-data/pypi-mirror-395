from __future__ import annotations
from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from zempy.zosapi.editors.protocols.i_editor_cell import IEditorCell
    from zempy.zosapi.editors.protocols.i_editor import IEditor


@runtime_checkable
class IEditorRow(Protocol):
    """Protocol for ZOSAPI.Editors.IEditorRow.

    Base interface for all five editor row types.
    Provides access to general row information and the parent editor.
    """

    # --- Methods ---

    def GetCellAt(self, pos: int) -> "IEditorCell":
        """Gets the cell at the specified column index (IEditor.MinColumn to IEditor.MaxColumn)."""
        ...

    # --- Properties ---

    @property
    def Editor(self) -> "IEditor":
        """Gets the editor this row was retrieved from."""
        ...

    @property
    def IsValidRow(self) -> bool:
        """True if this row instance is still valid."""
        ...

    @property
    def RowIndex(self) -> int:
        """Index of this row in the editor."""
        ...

    @property
    def RowTypeName(self) -> str:
        """Descriptive type of this row (surface/object, etc.)."""
        ...

    @property
    def Bookmark(self) -> str:
        """Gets or sets the bookmark label for this row."""
        ...

    @Bookmark.setter
    def Bookmark(self, value: str) -> None:
        ...
