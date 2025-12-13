from __future__ import annotations
from typing import Protocol, runtime_checkable

from zempy.zosapi.editors.enums.editor_type import EditorType

if False:  # TYPE_CHECKING guard without importing at runtime
    from zempy.zosapi.editors.protocols.i_editor_row import IEditorRow


@runtime_checkable
class IEditor(Protocol):
    """Protocol for ZOSAPI.Editors.IEditor.
    Base interface for all five editor types.
    """

    # --- Methods ---

    def GetRowAt(self, pos: int) -> "IEditorRow":
        """Gets the row at the specified index (0 .. NumberOfRows-1)."""
        ...

    def InsertRowAt(self, pos: int) -> "IEditorRow":
        """Inserts a new row at the specified index (0 .. NumberOfRows)."""
        ...

    def AddRow(self) -> "IEditorRow":
        """Adds a new row at the end of the editor."""
        ...

    def DeleteRowAt(self, pos: int) -> bool:
        """Deletes a single row at the specified index (0 .. NumberOfRows-1)."""
        ...

    def DeleteRowsAt(self, pos: int, numberOfRows: int) -> int:
        """Deletes one or more rows starting at index (0 .. NumberOfRows-1). Returns rows deleted."""
        ...

    def DeleteAllRows(self) -> int:
        """Deletes all rows from the current editor. Returns rows deleted."""
        ...

    def ShowEditor(self) -> bool:
        """Shows this editor in the UI (effective in Plugin mode)."""
        ...

    def HideEditor(self) -> None:
        """Closes this editor in the UI (effective in Plugin mode)."""
        ...

    # --- Properties ---

    @property
    def Editor(self) -> EditorType:
        """Gets the type of this editor instance."""
        ...

    @property
    def NumberOfRows(self) -> int:
        """Number of rows (surfaces/objects/operands depending on editor type)."""
        ...

    @property
    def MinColumn(self) -> int:
        """Minimum column index allowed for IEditorRow.GetCellAt."""
        ...

    @property
    def MaxColumn(self) -> int:
        """Maximum column index allowed for IEditorRow.GetCellAt."""
        ...
