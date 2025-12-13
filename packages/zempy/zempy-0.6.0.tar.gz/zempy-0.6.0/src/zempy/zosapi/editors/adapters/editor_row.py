from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.editors.adapters.editor_cell import EditorCell
from zempy.zosapi.editors.adapters.editor import Editor as EditorAdapter


@dataclass
class EditorRow(BaseAdapter[Z, N]):
    """   Adapter for ZOSAPI.Editors.IEditorRow"""

    Editor = property_adapter("Editor", adapter=EditorAdapter)
    IsValidRow = PropertyScalar("IsValidRow", coerce_get=bool)
    RowIndex = PropertyScalar("RowIndex", coerce_get=int)
    RowTypeName = PropertyScalar("RowTypeName", coerce_get=str)
    Bookmark = PropertyScalar("Bookmark", coerce_get=str, coerce_set=str)

    def GetCellAt(self, pos: int) -> EditorCell:
        """Gets the cell at the specified index (IEditor.MinColumn .. IEditor.MaxColumn)."""
        native = run_native("EditorRow.GetCellAt", lambda: self.native.GetCellAt(int(pos)), ensure=self.ensure_native)
        return EditorCell.from_native(self.zosapi, native)
