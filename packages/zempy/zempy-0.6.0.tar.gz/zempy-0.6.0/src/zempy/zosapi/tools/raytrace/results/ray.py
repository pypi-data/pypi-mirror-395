from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Optional, Tuple


@dataclass(frozen=True)
class Ray(ABC):
    ok: bool
    rayNumber: int
    errorCode: int


    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} #{self.rayNumber}\n"
            f"ok = {self.ok} err = {self.errorCode}\n"
        )

