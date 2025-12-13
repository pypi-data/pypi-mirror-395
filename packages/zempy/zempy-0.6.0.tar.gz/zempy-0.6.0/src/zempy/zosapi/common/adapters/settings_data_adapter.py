from __future__ import annotations
from typing import Sequence

# This adapter wraps the native ZOSAPI.Common.ISettingsData (.NET) and exposes
# a Pythonic interface matching the ISettingsData Protocol you defined.
# It assumes pythonnet interop where .NET methods with out-parameters return
# Python tuples, e.g. (ok, value) for scalar getters and (ok, t, is_arr, n)
# for GetEntryType. For array getters, ZOSAPI expects the caller to allocate a
# .NET array; this adapter handles allocation and converts to Python lists.

try:
    from System import Array, Double, Int32, Single, Byte, Boolean, String
except Exception as _e:  # pragma: no cover
    # Defer import errors until the adapter is actually instantiated/used.
    Array = Double = Int32 = Single = Byte = Boolean = String = None  # type: ignore

from zempy.zosapi.common.enums.settings_data_type import SettingsDataType
from zempy.zosapi.common.protocols.i_settings_data import ISettingsData


class SettingsDataAdapter(ISettingsData):
    """Adapter over native ZOSAPI.Common.ISettingsData.

    Parameters
    ----------
    native : Any
        The underlying .NET object implementing ZOSAPI.Common.ISettingsData.
    """

    __slots__ = ("_native",)

    def __init__(self, native):
        if native is None:
            raise ValueError("native ISettingsData is None")
        self._native = native

    # --- Helpers ---
    @staticmethod
    def _ensure_system_imported():
        if Array is None:
            raise RuntimeError(
                "pythonnet System types are not available; ensure the .NET runtime is initialized"
            )

    @staticmethod
    def _to_list(net_array) -> list:
        # Convert a System.Array to a Python list without copying element-wise logic in user code
        return list(net_array) if net_array is not None else []

    @staticmethod
    def _arr_double(n: int):
        SettingsDataAdapter._ensure_system_imported()
        return Array.CreateInstance(Double, n)

    @staticmethod
    def _arr_int(n: int):
        SettingsDataAdapter._ensure_system_imported()
        return Array.CreateInstance(Int32, n)

    @staticmethod
    def _arr_float(n: int):  # ZOSAPI "float" == System.Single
        SettingsDataAdapter._ensure_system_imported()
        return Array.CreateInstance(Single, n)

    @staticmethod
    def _arr_byte(n: int):
        SettingsDataAdapter._ensure_system_imported()
        return Array.CreateInstance(Byte, n)

    @staticmethod
    def _arr_bool(n: int):
        SettingsDataAdapter._ensure_system_imported()
        return Array.CreateInstance(Boolean, n)

    # --- Properties ---
    @property
    def NumberOfSettings(self) -> int:  # type: ignore[override]
        return int(self._native.NumberOfSettings)

    # --- Keys & type info ---
    def GetKeys(self) -> list[str]:  # type: ignore[override]
        keys = self._native.GetKeys()
        # keys is a System.Array[String]
        return [str(k) for k in keys] if keys is not None else []

    def GetEntryType(self, key: str) -> tuple[bool, SettingsDataType, bool, int]:  # type: ignore[override]
        ok, t, is_arr, n = self._native.GetEntryType(key)
        # t is the native enum; cast to our SettingsDataType for typing friendliness.
        return bool(ok), SettingsDataType(int(t)), bool(is_arr), int(n)

    # --- Scalars ---
    def GetDoubleValue(self, key: str) -> tuple[bool, float]:  # type: ignore[override]
        ok, val = self._native.GetDoubleValue(key)
        return bool(ok), float(val) if ok else 0.0

    def GetIntegerValue(self, key: str) -> tuple[bool, int]:  # type: ignore[override]
        ok, val = self._native.GetIntegerValue(key)
        return bool(ok), int(val) if ok else 0

    def GetFloatValue(self, key: str) -> tuple[bool, float]:  # type: ignore[override]
        ok, val = self._native.GetFloatValue(key)
        return bool(ok), float(val) if ok else 0.0

    def GetStringValue(self, key: str) -> tuple[bool, str]:  # type: ignore[override]
        ok, val = self._native.GetStringValue(key)
        return bool(ok), (str(val) if ok and val is not None else "")

    def GetByteValue(self, key: str) -> tuple[bool, int]:  # type: ignore[override]
        ok, val = self._native.GetByteValue(key)
        return bool(ok), int(val) if ok else 0

    def GetBooleanValue(self, key: str) -> tuple[bool, bool]:  # type: ignore[override]
        ok, val = self._native.GetBooleanValue(key)
        return bool(ok), bool(val) if ok else False

    def SetDoubleValue(self, key: str, val: float) -> None:  # type: ignore[override]
        self._native.SetDoubleValue(key, float(val))

    def SetIntegerValue(self, key: str, val: int) -> None:  # type: ignore[override]
        self._native.SetIntegerValue(key, int(val))

    def SetFloatValue(self, key: str, val: float) -> None:  # type: ignore[override]
        self._native.SetFloatValue(key, float(val))

    def SetStringValue(self, key: str, val: str) -> None:  # type: ignore[override]
        self._native.SetStringValue(key, str(val))

    def SetByteValue(self, key: str, val: int) -> None:  # type: ignore[override]
        # Clamp to byte range just in case
        b = 0 if val < 0 else 255 if val > 255 else int(val)
        self._native.SetByteValue(key, b)

    def SetBooleanValue(self, key: str, val: bool) -> None:  # type: ignore[override]
        self._native.SetBooleanValue(key, bool(val))

    # --- Arrays ---
    def GetDoubleArray(self, key: str, Size: int) -> tuple[bool, list[float]]:  # type: ignore[override]
        buf = self._arr_double(Size)
        ok = self._native.GetDoubleArray(key, Size, buf)
        return bool(ok), [float(x) for x in self._to_list(buf[:Size])]

    def GetIntegerArray(self, key: str, Size: int) -> tuple[bool, list[int]]:  # type: ignore[override]
        buf = self._arr_int(Size)
        ok = self._native.GetIntegerArray(key, Size, buf)
        return bool(ok), [int(x) for x in self._to_list(buf[:Size])]

    def GetFloatArray(self, key: str, Size: int) -> tuple[bool, list[float]]:  # type: ignore[override]
        buf = self._arr_float(Size)
        ok = self._native.GetFloatArray(key, Size, buf)
        return bool(ok), [float(x) for x in self._to_list(buf[:Size])]

    def GetByteArray(self, key: str, Size: int) -> tuple[bool, list[int]]:  # type: ignore[override]
        buf = self._arr_byte(Size)
        ok = self._native.GetByteArray(key, Size, buf)
        return bool(ok), [int(x) for x in self._to_list(buf[:Size])]

    def GetBooleanArray(self, key: str, Size: int) -> tuple[bool, list[bool]]:  # type: ignore[override]
        buf = self._arr_bool(Size)
        ok = self._native.GetBooleanArray(key, Size, buf)
        return bool(ok), [bool(x) for x in self._to_list(buf[:Size])]

    def SetDoubleArray(self, key: str, Size: int, val: Sequence[float]) -> None:  # type: ignore[override]
        arr = self._arr_double(Size)
        for i, x in enumerate(val[:Size]):
            arr[i] = float(x)
        self._native.SetDoubleArray(key, Size, arr)

    def SetIntegerArray(self, key: str, Size: int, val: Sequence[int]) -> None:  # type: ignore[override]
        arr = self._arr_int(Size)
        for i, x in enumerate(val[:Size]):
            arr[i] = int(x)
        self._native.SetIntegerArray(key, Size, arr)

    def SetFloatArray(self, key: str, Size: int, val: Sequence[float]) -> None:  # type: ignore[override]
        arr = self._arr_float(Size)
        for i, x in enumerate(val[:Size]):
            arr[i] = float(x)
        self._native.SetFloatArray(key, Size, arr)

    def SetByteArray(self, key: str, Size: int, val: Sequence[int]) -> None:  # type: ignore[override]
        arr = self._arr_byte(Size)
        for i, x in enumerate(val[:Size]):
            # Ensure 0..255
            b = 0 if x < 0 else 255 if x > 255 else int(x)
            arr[i] = b
        self._native.SetByteArray(key, Size, arr)

    def SetBooleanArray(self, key: str, Size: int, val: Sequence[bool]) -> None:  # type: ignore[override]
        arr = self._arr_bool(Size)
        for i, x in enumerate(val[:Size]):
            arr[i] = bool(x)
        self._native.SetBooleanArray(key, Size, arr)
