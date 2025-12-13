from typing import Protocol, runtime_checkable

@runtime_checkable
class ISDTitleNotes(Protocol):
    """
    Protocol mirror of ZOSAPI.SystemData.ISDTitleNotes.
    System Explorer → Notes data (accessible via ISystemData).
    """

    @property
    def Title(self) -> str:
        ...
    @Title.setter
    def Title(self, value: str) -> None:
        ...

    @property
    def Notes(self) -> str:
        ...
    @Notes.setter
    def Notes(self, value: str) -> None:
        ...

    @property
    def Author(self) -> str:
        ...
    @Author.setter
    def Author(self, value: str) -> None:
        ...
