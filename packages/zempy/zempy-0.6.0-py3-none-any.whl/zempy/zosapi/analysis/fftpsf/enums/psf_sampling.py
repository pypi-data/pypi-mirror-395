from enum import Enum
from zempy.zosapi.core.enum_base import ZosEnumBase

class PsfSampling(ZosEnumBase):
    PsfS_32x32     = "PsfS_32x32"
    PsfS_64x64     = "PsfS_64x64"
    PsfS_128x128   = "PsfS_128x128"
    PsfS_256x256   = "PsfS_256x256"
    PsfS_512x512   = "PsfS_512x512"
    PsfS_1024x1024 = "PsfS_1024x1024"
    PsfS_2048x2048 = "PsfS_2048x2048"
    PsfS_4096x4096 = "PsfS_4096x4096"
    PsfS_8192x8192 = "PsfS_8192x8192"
    PsfS_16384x16384 = "PsfS_16384x16384"

PsfSampling._NATIVE_PATH = "ZOSAPI.Analysis.Settings.Psf.PsfSampling"
PsfSampling._ALIASES_EXTRA = {
    "PsfS_32x32": ("S_32x32",),
    "PsfS_64x64": ("S_64x64",),
    "PsfS_128x128": ("S_128x128",),
    "PsfS_256x256": ("S_256x256",),
    "PsfS_512x512": ("S_512x512",),
    "PsfS_1024x1024": ("S_1024x1024",),
    "PsfS_2048x2048": ("S_2048x2048",),
    "PsfS_4096x4096": ("S_4096x4096",),
    "PsfS_8192x8192": ("S_8192x8192",),
    "PsfS_16384x16384": ("S_16384x16384",),
}

__all__ = ["PsfSampling"]
