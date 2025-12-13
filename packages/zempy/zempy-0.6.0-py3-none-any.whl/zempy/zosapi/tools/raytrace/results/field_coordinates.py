from typing import Tuple

# Result of GetDirectFieldCoordinates
FieldCoordinates = Tuple[
    bool,  # ok: True if coordinates computed successfully
    float, float, float,  # X, Y, Z
    float, float, float,  # L, M, N
]
