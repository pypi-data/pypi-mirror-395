from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Any, Callable, Optional
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.analysis.adapters.messages import Messages
from zempy.zosapi.analysis.protocols.i_messages import IMessages
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.analysis.ias.adapters.ias_field import IAS_Field as IAS_FieldAdapter
from zempy.zosapi.analysis.ias.adapters.ias_surface import IAS_Surface as IAS_SurfaceAdapter
from zempy.zosapi.analysis.ias.adapters.ias_wavelength import IAS_Wavelength as IAS_WavelengthAdapter

@dataclass
class IAS(BaseAdapter[Z, N]):
    """
    Generic IAS adapter base: wraps Analysis Settings interfaces that expose
    Field / Surface / Wavelength sub-interfaces and a Verify/Save/Load API.
    """

    REQUIRED_NATIVE_ATTRS: ClassVar[tuple[str, ...]] = ("Field", "Surface", "Wavelength")
    NATIVE_COERCER: ClassVar[Optional[Callable[[Any], Any]]] = None

    Field      = property_adapter("Field",      IAS_FieldAdapter)
    Surface    = property_adapter("Surface",    IAS_SurfaceAdapter)
    Wavelength = property_adapter("Wavelength", IAS_WavelengthAdapter)

    # --- Methods ---
    def Verify(self) -> IMessages:
        native_messages = run_native("IAS.Verify", lambda: self.native.Verify(), ensure=self.ensure_native)
        # Prefer from_native when available; fall back to direct construction
        try:
            return Messages.from_native(self.zosapi, native_messages)  # type: ignore[attr-defined]
        except Exception:
            return Messages(self.zosapi, native_messages)

    def Save(self) -> None:
        run_native("IAS.Save", lambda: self.native.Save(), ensure=self.ensure_native)

    def Load(self) -> None:
        run_native("IAS.Load", lambda: self.native.Load(), ensure=self.ensure_native)

    def Reset(self) -> None:
        run_native("IAS.Reset", lambda: self.native.Reset(), ensure=self.ensure_native)

    def SaveTo(self, settingsFile: str) -> bool:
        return bool(run_native("IAS.SaveTo", lambda: self.native.SaveTo(str(settingsFile)), ensure=self.ensure_native))

    def LoadFrom(self, settingsFile: str) -> bool:
        return bool(run_native("IAS.LoadFrom", lambda: self.native.LoadFrom(str(settingsFile)), ensure=self.ensure_native))

    def ModifySettings(self, settingsFile: str, typeCode: str, newValue: str) -> bool:
        return bool(run_native(
            "IAS.ModifySettings",
            lambda: self.native.ModifySettings(str(settingsFile), str(typeCode), str(newValue)),
            ensure=self.ensure_native,
        ))

class IAS_Generic(IAS[Z, N]):
    # Generic passthrough: no required attrs beyond base (can be overridden upstream)
    REQUIRED_NATIVE_ATTRS: ClassVar[tuple[str, ...]] = ()
