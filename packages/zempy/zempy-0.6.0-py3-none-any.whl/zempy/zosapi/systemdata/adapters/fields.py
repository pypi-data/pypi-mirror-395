from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum
from zempy.zosapi.systemdata.enums.field_type import FieldType
from zempy.zosapi.systemdata.enums.field_normalization_type import FieldNormalizationType
from zempy.zosapi.systemdata.adapters.field import Field
from zempy.zosapi.analysis.adapters.message import Message


@dataclass
class Fields(BaseAdapter):
    """Adapter for ZOSAPI.SystemData.IFields"""

    # Scalars (read-only)
    NumberOfFields = PropertyScalar("NumberOfFields", coerce_get=int)

    # Enum property (read/write)
    Normalization  = property_enum("Normalization", FieldNormalizationType, read_only=False)


    # ------- Field access / mutation -------
    def GetField(self, position: int) -> Field:
        """Return Field at 1-based index `position`."""
        native_field = self._rn("Fields.GetField", lambda: self.native.GetField(int(position)))
        return Field.from_native(self.zosapi, native_field)

    def AddField(self, x: float, y: float, weight: float = 1.0) -> Field:
        """Add a field (x, y, weight) and return its adapter."""
        native_field = self._rn(
            "Fields.AddField",
            lambda: self.native.AddField(float(x), float(y), float(weight)),
        )
        return Field.from_native(self.zosapi, native_field)

    def InsertFieldAt(self, field_number: int) -> Field:
        """Insert a new field row at 1-based index and return it."""
        native_field = self._rn("Fields.InsertFieldAt", lambda: self.native.InsertFieldAt(int(field_number)))
        return Field.from_native(self.zosapi, native_field)

    def RemoveField(self, position: int) -> bool:
        """Remove field at 1-based index."""
        result = self._rn("Fields.RemoveField", lambda: self.native.RemoveField(int(position)))
        return bool(result)

    def DeleteFieldAt(self, field_number: int) -> bool:
        """Delete a single field at 1-based index (ZOSAPI naming)."""
        result = self._rn("Fields.DeleteFieldAt", lambda: self.native.DeleteFieldAt(int(field_number)))
        return bool(result)

    def DeleteFieldsAt(self, field_number: int, number_of_fields: int) -> int:
        """Delete multiple fields starting at 1-based index."""
        result = self._rn(
            "Fields.DeleteFieldsAt",
            lambda: self.native.DeleteFieldsAt(int(field_number), int(number_of_fields)),
        )
        return int(result)

    def DeleteAllFields(self) -> int:
        """Delete all fields; returns the number removed."""
        result = self._rn("Fields.DeleteAllFields", lambda: self.native.DeleteAllFields())
        return int(result)

    # ------- Vignetting -------
    def SetVignetting(self) -> None:
        self._rn("Fields.SetVignetting", lambda: self.native.SetVignetting())

    def ClearVignetting(self) -> None:
        self._rn("Fields.ClearVignetting", lambda: self.native.ClearVignetting())

    # ------- Field type (enum) -------
    def SetFieldType(self, ft: FieldType) -> None:
        native = FieldType.to_native(self.zosapi, ft)
        self._rn("Fields.SetFieldType", lambda: self.native.SetFieldType(native))

    def GetFieldType(self) -> FieldType:
        raw = self._rn("Fields.GetFieldType", lambda: self.native.GetFieldType())
        return FieldType.from_native(self.zosapi, raw)

    def ConvertToFieldType(self, ft: FieldType) -> Message:
        native = FieldType.to_native(self.zosapi, ft)
        zos_msg = self._rn("Fields.ConvertToFieldType", lambda: self.native.ConvertToFieldType(native))
        return Message.from_native(zos_msg)

    # ------- Wizards / patterns -------
    def MakeEqualAreaFields(self, number_of_fields: int, maximum_field: float) -> bool:
        result = self._rn(
            "Fields.MakeEqualAreaFields",
            lambda: self.native.MakeEqualAreaFields(int(number_of_fields), float(maximum_field)),
        )
        return bool(result)

    def ApplyFieldWizard(
        self,
        pattern: Any,
        number_of_y_fields: int,
        max_field_y: float,
        number_of_x_fields: int,
        max_field_x: float,
        start_at: int = 1,
        overwrite: bool = False,
        include_pickups: bool = True,
    ) -> Message:
        zos_msg = self._rn(
            "Fields.ApplyFieldWizard",
            lambda: self.native.ApplyFieldWizard(
                pattern,
                int(number_of_y_fields),
                float(max_field_y),
                int(number_of_x_fields),
                float(max_field_x),
                int(start_at),
                bool(overwrite),
                bool(include_pickups),
            ),
        )
        return Message.from_native(zos_msg)

    # ------- Pythonic conveniences -------
    def __len__(self) -> int:
        return self.NumberOfFields

    def last_index(self) -> int:
        return self.NumberOfFields

    def indices(self) -> range:
        return range(1, self.NumberOfFields + 1)



    # ------- Convenience -------
    def as_list(self) -> List[Field]:
        return [self.GetField(i) for i in self.indices()]
