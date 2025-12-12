from typing import TypeVar

ScalarT = TypeVar("ScalarT", int, float)
Vec3 = tuple[ScalarT, ScalarT, ScalarT]
Mat4 = tuple[
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
    ScalarT,
]
