from __future__ import annotations
from typing import Protocol, runtime_checkable, Callable, Any, Type
from zempy.zosapi.core.enum_base import ZosEnumBase
from zempy.zosapi.enums import (LicenseStatusType, SystemType, SessionModes,
                                LensUpdateMode, STARUpdateMode, UpdateStatus, ZOSAPIMode)


class _AnalysisNS(Protocol):
    AnalysisIDM: type[ZosEnumBase]  # enum class
class _CommonNS(Protocol): ...
class _EditorsNS(Protocol): ...
class _PreferencesNS(Protocol): ...
class _SystemDataNS(Protocol): ...
class _WizardsNS(Protocol): ...
class _ToolsGeneralNS(Protocol):
    QuickFocusCriterion: type[ZosEnumBase]  # enum class
class _ToolsNS(Protocol):
    General: _ToolsGeneralNS
class _ConnectionCtor(Protocol):
    def __call__(self) -> Any: ...

OpticalSystemStatusChangedHandler = Callable[[int, str], None]

@runtime_checkable
class IZosapi(Protocol):
    """   Minimal, typed facade for the .NET ZOSAPI namespace:
    - Namespaces (Analysis, Tools, Editors, Preferences, SystemData, Wizards, Common)
    - Key classes/interfaces (IZOSAPI_Connection, IZOSAPI_Application, IOpticalSystem, ...)
    - Enumerations (SystemType, LicenseStatusType, UpdateStatus, ZOSAPI_Mode, LensUpdateMode, SessionModes, STARUpdateMode)
    - ZOSAPI_Connection constructor and the status-changed delegate type
    """
    Analysis: _AnalysisNS
    Common: _CommonNS
    Editors: _EditorsNS
    Preferences: _PreferencesNS
    SystemData: _SystemDataNS
    Tools: _ToolsNS
    Wizards: _WizardsNS

    IOpticalSystem: Type[Any]
    IPreferences: Type[Any]
    ISTARMaterials: Type[Any]
    ISTARSubsystem: Type[Any]
    IZOSAPI_Application: Type[Any]
    IZOSAPI_Connection: Type[Any]
    IZOSAPI_Events: Type[Any]
    ZOSAPI_Connection: _ConnectionCtor


    SystemType: SystemType
    LicenseStatusType: LicenseStatusType
    UpdateStatus: UpdateStatus
    ZOSAPI_Mode: ZOSAPIMode
    LensUpdateMode: LensUpdateMode
    SessionModes: SessionModes
    STARUpdateMode: STARUpdateMode

    OpticalSystemStatusChangedHandler: Type[Any]  # .NET delegate type
