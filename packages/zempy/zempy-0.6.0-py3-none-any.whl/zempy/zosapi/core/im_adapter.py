# zempy/zosapi/core/im_adapter.py
"""
Lightweight facade for adapter modules.

Import this in adapter files to keep imports short and stable:
    from zempy.zosapi.core.im_adapter import (
        BaseAdapter, Z, N, run_native, validate_cast,
        PropertyScalar, property_enum, property_adapter, PropertySequence,
        dataclass, Optional, TYPE_CHECKING, logging,
    )
"""

from __future__ import annotations  # harmless on 3.11/3.12, helpful on 3.8–3.10
import logging
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

from allytools.types import validate_cast

from zempy.zosapi.core.base_adapter import BaseAdapter
from zempy.zosapi.core.types_var import N, Z, R, A, E, P, T
from zempy.zosapi.core.interop import run_native
from zempy.zosapi.core.property_object import property_adapter
from zempy.zosapi.core.property_scalar import PropertyScalar
from zempy.zosapi.core.property_enum import property_enum, PropertyEnum
from zempy.zosapi.core.property_sequence import PropertySequence

__all__ = ["logging", "dataclass", "Optional", "TYPE_CHECKING",
           "validate_cast",
           "BaseAdapter",
           "Z","N", "R", "A", "E", "P", "T",
           "run_native",
           "property_adapter",
           "PropertyScalar",
           "PropertyEnum",
           "property_enum",
           "PropertySequence",
]

