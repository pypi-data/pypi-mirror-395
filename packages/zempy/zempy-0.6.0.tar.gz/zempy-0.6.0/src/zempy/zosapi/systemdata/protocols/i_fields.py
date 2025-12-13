from __future__ import annotations
from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from zempy.zosapi.systemdata.protocols.i_field import IField
    from zempy.zosapi.analysis.protocols.i_message import IMessage
    from zempy.zosapi.systemdata.enums.field_type import FieldType
    from zempy.zosapi.systemdata.enums.field_pattern import FieldPattern
    from zempy.zosapi.systemdata.enums.field_normalization_type import FieldNormalizationType

@runtime_checkable
class IFields(Protocol):
    """
    System Explorer - Fields Data.
    Accessed via ISystemData.Fields.
    """

    # Query / access
    def GetField(self, position: int) -> IField:
        """Gets the specified field (1-based index in ZOSAPI)."""

    # Mutations – add/insert/delete
    def AddField(self, X: float, Y: float, Weight: float) -> IField:
        """Add a new field after all current fields."""

    def RemoveField(self, position: int) -> bool:
        """Remove the specified field (legacy; prefer Delete* APIs where available)."""

    def InsertFieldAt(self, fieldNumber: int) -> IField:
        """Insert a new field at the given position (shifts existing items)."""

    def DeleteFieldAt(self, fieldNumber: int) -> bool:
        """Delete the field at the given position."""

    def DeleteFieldsAt(self, fieldNumber: int, numberOfFields: int) -> int:
        """Delete a run of fields starting at position; returns number removed."""

    def DeleteAllFields(self) -> int:
        """Delete all fields; returns number removed."""

    # Vignetting helpers
    def SetVignetting(self) -> None: ...
    def ClearVignetting(self) -> None: ...

    # Field type get/set
    def GetFieldType(self) -> FieldType: ...
    def SetFieldType(self, type: FieldType) -> None:
        """Set the field definition mode for all fields."""

    # Generators / wizards
    def MakeEqualAreaFields(self, numberOfFields: int, maximumField: float) -> bool:
        """
        Replace existing fields with equal-area distributed fields
        up to maximumField (units depend on FieldType).
        """

    def ApplyFieldWizard(
        self,
        pattern: FieldPattern,
        numberOfYFields: int,
        maxFieldY: float,
        numberOfXFields: int,
        maxFieldX: float,
        startAt: int,
        overwrite: bool,
        includePickups: bool,
    ) -> IMessage:
        """
        Add fields per the specified pattern. Exact semantics mirror ZOSAPI.
        """

    def ConvertToFieldType(self, type: FieldType) -> IMessage:
        """Convert existing fields to a different FieldType."""

    @property
    def NumberOfFields(self) -> int: ...

    @property
    def Normalization (self) -> FieldNormalizationType: ...
    @Normalization.setter
    def Normalization(self, v: FieldNormalizationType) -> None: ...
