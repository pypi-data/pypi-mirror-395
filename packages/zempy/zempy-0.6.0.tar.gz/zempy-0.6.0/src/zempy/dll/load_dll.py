from __future__ import annotations
import time
from typing import Tuple, Sequence
from pathlib import Path
import numpy as np
from zempy.dotnet.clr import CLR

def load_dll(anchor: Path, dll_name: str) -> None:
    """
    Load your custom raytrace DLL via your CLR helper.
    After loading, the managed namespace (e.g., BatchRayTrace) is importable.
    """
    dll_path = (anchor / ".." / "DLL" / dll_name).resolve()
    if not dll_path.is_file():
        raise FileNotFoundError(f"{dll_name} not found at: {dll_path}")
    if not CLR.add_reference(str(dll_path)):
        raise RuntimeError(f"Failed to add reference: {dll_path}")  # uses your CLR helper  # :contentReference[oaicite:5]{index=5}
    # Import the managed assembly namespace (if you need to touch its symbols explicitly)
    try:
        import batch_ray_trace  # noqa: F401
    except Exception as e:
        raise RuntimeError(f"Assembly loaded but namespace import failed: {e}")