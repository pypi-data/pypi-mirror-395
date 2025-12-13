from __future__ import annotations
from dataclasses import dataclass
from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z

@dataclass
class CoatingParameter(BaseAdapter[Z, N]):
    pass