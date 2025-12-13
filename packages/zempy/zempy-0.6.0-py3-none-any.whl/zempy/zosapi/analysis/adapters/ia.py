from __future__ import annotations
import logging
from contextlib import suppress
from typing import Any, Optional, TypeVar, Generic
from dataclasses import dataclass
from allytools.types import validate_cast
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.analysis.enums.analysis_idm import AnalysisIDM
from zempy.zosapi.analysis.iar.adapters.iar import IAR
from zempy.zosapi.analysis.ias.adapters.registry import get_settings_class
from zempy.zosapi.analysis.ias.protocols.ias_ import IAS_
from zempy.zosapi.analysis.adapters.message import Message
from zempy.zosapi.analysis.adapters.messages import Messages


S = TypeVar("S", bound=IAS_)

log = logging.getLogger(__name__)
class IA(Generic[S, Z, N], BaseAdapter[Z, N]):
    """Generic Analysis adapter (ZOSAPI.Analysis.IA_)."""

    __slots__ = ("idm", "_settings")

    idm: AnalysisIDM
    _settings: Optional[S]

    def __init__(self, zosapi: Z, native: N, idm: AnalysisIDM):
        super().__init__(zosapi, native)
        self.idm = idm
        self._settings = None
        try:
            self._build_settings()
        except Exception:
            log.exception("Could not initialize settings for %s", self.idm.name)

    # ---- Context management ----
    def __enter__(self) -> IA:
        return self

    def __exit__(self, exc_type, exc, tb):
        with suppress(Exception):
            self.Close()


    # ---- Internal helpers ----
    @staticmethod
    def _maybe_call(value: Any) -> Any:
        return value() if callable(value) else value

    def _build_settings(self) -> None:
        native_settings = run_native(
            "IA.GetSettings",
            lambda: self.native.GetSettings(),
            ensure=self.ensure_native,
        )
        SettingsCls = get_settings_class(self.idm)
        self._settings = SettingsCls.from_native(self.zosapi, native_settings)

    # ---- API: results / settings ----
    def GetResults(self) -> IAR:
        native_result = run_native(
            "IA.GetResults",
            lambda: self.native.GetResults(),
            ensure=self.ensure_native,
        )
        return IAR.from_native(self.zosapi, native_result)

    def GetSettings(self) -> IAS_:
        native_settings = run_native(
            "IA.GetSettings",
            lambda: self.native.GetSettings(),
            ensure=self.ensure_native,
        )
        SettingsCls = get_settings_class(self.idm)
        return validate_cast(SettingsCls.from_native(self.zosapi, native_settings), IAS_)

    # ---- Execution lifecycle ----
    def ApplyAndWaitForCompletion(self) -> None:
        run_native(
            "IA.ApplyAndWaitForCompletion",
            lambda: self.native.ApplyAndWaitForCompletion(),
            ensure=self.ensure_native,
        )

    def WaitForCompletion(self) -> None:
        run_native(
            "IA.WaitForCompletion",
            lambda: self.native.WaitForCompletion(),
            ensure=self.ensure_native,
        )

    def Terminate(self) -> None:
        run_native("IA.Terminate", lambda: self.native.Terminate(), ensure=self.ensure_native)

    # ---- Properties ----
    @property
    def settings(self) -> S:
        if self._settings is None:
            self._build_settings()
        return self._settings

    @property
    def HasAnalysisSpecificSettings(self) -> bool:
        return bool(
            run_native(
                "IA.HasAnalysisSpecificSettings get",
                lambda: self.native.HasAnalysisSpecificSettings,
                ensure=self.ensure_native,
            )
        )

    def run(self) -> IAR:
        """Apply, wait, and return results."""
        native_msg = run_native(
            "IA.ApplyAndWaitForCompletion",
            lambda: self.native.ApplyAndWaitForCompletion(),
            ensure=self.ensure_native,
        )
        try:
            _ = Message.from_native(self.zosapi, native_msg)
        except Exception:
            pass
            #TODO native_msg is None - class 'NoneType
            #log.debug("IA.ApplyAndWaitForCompletion returned unwrapped message")

        native_iar = run_native(
            "IA.GetResults",
            lambda: self.native.GetResults(),
            ensure=self.ensure_native,
        )
        return IAR.from_native(self.zosapi, native_iar)

    def IsRunning(self) -> bool:
        return bool(
            run_native(
                "IA.IsRunning get",
                lambda: self.native.IsRunning,
                ensure=self.ensure_native,
            )
        )

    def Apply(self) -> Message:
        native_msg = run_native("IA.Apply", lambda: self.native.Apply(), ensure=self.ensure_native)
        return Message.from_native(self.zosapi, native_msg)

    def Close(self) -> None:
        run_native("IA.Close", lambda: self.native.Close(), ensure=self.ensure_native)

    def Release(self) -> None:
        run_native("IA.Release", lambda: self.native.Release(), ensure=self.ensure_native)

    def ToFile(self, Filename: str, showSettings: bool = False, verify: bool = False) -> None:
        run_native(
            "IA.ToFile",
            lambda: self.native.ToFile(str(Filename), bool(showSettings), bool(verify)),
            ensure=self.ensure_native,
        )

    @property
    def Title(self) -> str:
        return str(run_native("IA.Title get", lambda: self.native.Title, ensure=self.ensure_native))

    @property
    def GetAnalysisName(self) -> str:
        val = run_native(
            "IA.GetAnalysisName",
            lambda: self._maybe_call(getattr(self.native, "GetAnalysisName")),
            ensure=self.ensure_native,
        )
        return str(val)

    @property
    def AnalysisType(self) -> AnalysisIDM:
        native_type = run_native(
            "IA.AnalysisType get",
            lambda: self.native.AnalysisType,
            ensure=self.ensure_native,
        )
        return AnalysisIDM.from_native(self.zosapi, native_type)

    @property
    def StatusMessages(self):
        native_msgs = run_native(
            "IA.StatusMessages get",
            lambda: self.native.StatusMessages,
            ensure=self.ensure_native,
        )
        try:
            return Messages.from_native(self.zosapi, native_msgs)
        except Exception:
            return native_msgs