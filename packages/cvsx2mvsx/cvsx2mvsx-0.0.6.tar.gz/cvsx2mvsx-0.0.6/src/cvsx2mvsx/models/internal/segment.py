from typing import Literal

from pydantic import BaseModel

from cvsx2mvsx.models.internal.types import Mat4, Vec3


class InternalBaseSegment(BaseModel):
    source_filepath: str | None = None

    timeframe_id: int
    segmentation_id: str
    segment_id: int

    color: str | None = None
    opacity: float | None = None
    instance: Mat4[float] | None = None


class InternalVolumeSegment(InternalBaseSegment):
    kind: Literal["volume"] = "volume"

    relative_isovalue: float | None = None


class InternalMeshSegment(InternalBaseSegment):
    kind: Literal["mesh"] = "mesh"


class InternalPyramidSegment(InternalBaseSegment):
    kind: Literal["pyramid"] = "pyramid"

    vertices: list[float]
    indices: list[int]
    triangle_groups: list[int]


class InternalEllipsoidSegment(InternalBaseSegment):
    kind: Literal["ellipsoid"] = "ellipsoid"

    center: Vec3[float]
    major_axis: Vec3[float]
    minor_axis: Vec3[float]
    radius: Vec3[float] | float


class InternalSphereSegment(InternalBaseSegment):
    kind: Literal["sphere"] = "sphere"

    center: Vec3[float]
    radius: float


class InternalBoxSegment(InternalBaseSegment):
    kind: Literal["box"] = "box"

    center: Vec3[float]
    extent: Vec3[float]


class InternalTubeSegment(InternalBaseSegment):
    kind: Literal["tube"] = "tube"

    start: Vec3[float]
    end: Vec3[float]
    radius: float


InternalGeometricSegment = (
    InternalPyramidSegment
    | InternalEllipsoidSegment
    | InternalSphereSegment
    | InternalBoxSegment
    | InternalTubeSegment
)


InternalSegment = InternalVolumeSegment | InternalMeshSegment | InternalGeometricSegment
