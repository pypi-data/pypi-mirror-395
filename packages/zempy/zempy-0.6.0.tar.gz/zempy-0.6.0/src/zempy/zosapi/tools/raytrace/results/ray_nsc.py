"""
NSC rays are segmented and structurally different from sequential rays.
Their records are kept as tuple aliases for performance and because they don't
share the same (X,Y,Z,L,M,N) single-record structure.
"""
from typing import Tuple

RayNSCResult = Tuple[
    bool,  # ok
    int,   # rayNumber
    int,   # ErrorCode
    int,   # wave
    int,   # numSegments
]

RayNSCSegment = Tuple[
    bool,  # ok
    int,   # segmentLevel
    int,   # segmentParent
    int,   # hitObj
    int,   # InsideOf
    float, float, float,  # X, Y, Z
    float, float, float,  # L, M, N
    float, float,         # exr, exi
    float, float,         # eyr, eyi
    float, float,         # ezr, ezi
    float,                # intensity
    float,                # pathLength
]
