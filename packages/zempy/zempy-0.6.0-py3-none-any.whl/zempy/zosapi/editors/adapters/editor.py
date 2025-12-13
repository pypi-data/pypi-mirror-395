from __future__ import annotations
from dataclasses import dataclass

from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.editors.enums.editor_type import EditorType
from zempy.zosapi.editors.adapters.editor_row import EditorRow


@dataclass
class Editor(BaseAdapter[Z, N]):
    """Adapter for ZOSAPI.Editors.IEditor."""


    Editor = property_enum("Editor", EditorType)
    NumberOfRows = PropertyScalar("NumberOfRows", coerce_get=int)
    MinColumn = PropertyScalar("MinColumn", coerce_get=int)
    MaxColumn = PropertyScalar("MaxColumn", coerce_get=int)

    def GetRowAt(self, pos: int) -> EditorRow:
        native = run_native("Editor.GetRowAt",
                            lambda: self.native.GetRowAt(int(pos)),
                            ensure=self.ensure_native)
        return EditorRow.from_native(self.zosapi, native)

    def InsertRowAt(self, pos: int) -> EditorRow:
        native = run_native("Editor.InsertRowAt",
                            lambda: self.native.InsertRowAt(int(pos)),
                            ensure=self.ensure_native)
        return EditorRow.from_native(self.zosapi, native)

    def AddRow(self) -> EditorRow:
        native = run_native("Editor.AddRow",
                            lambda: self.native.AddRow(),
                            ensure=self.ensure_native)
        return EditorRow.from_native(self.zosapi, native)

    def DeleteRowAt(self, pos: int) -> bool:
        return bool(run_native("Editor.DeleteRowAt",
                               lambda: self.native.DeleteRowAt(int(pos)),
                               ensure=self.ensure_native))

    def DeleteRowsAt(self, pos: int, numberOfRows: int) -> int:
        return int(run_native("Editor.DeleteRowsAt",
                              lambda: self.native.DeleteRowsAt(int(pos), int(numberOfRows)),
                              ensure=self.ensure_native))

    def DeleteAllRows(self) -> int:
        return int(run_native("Editor.DeleteAllRows",
                              lambda: self.native.DeleteAllRows(),
                              ensure=self.ensure_native))

    def ShowEditor(self) -> bool:
        return bool(run_native("Editor.ShowEditor",
                               lambda: self.native.ShowEditor(),
                               ensure=self.ensure_native))

    def HideEditor(self) -> None:
        run_native("Editor.HideEditor",
                   lambda: self.native.HideEditor(),
                   ensure=self.ensure_native)


__all__ = ["Editor"]
