from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from cvsx2mvsx.models.internal.types import Mat4, Vec3


class InternalBaseSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_filepath: str | None = Field(default=None)

    timeframe_id: int
    segmentation_id: str
    segment_id: int

    color: str
    opacity: float

    label: str | None
    tooltip: str | None
    description: str | None


class InternalVolumeSegment(InternalBaseSegment):
    kind: Literal["volume"] = "volume"

    channel_id: str
    absolute_isovalue: float | None
    relative_isovalue: float
    show_faces: bool
    show_wireframe: bool


class InternalMeshSegment(InternalBaseSegment):
    kind: Literal["mesh"] = "mesh"

    instance: Mat4[float] | None = Field(default=None)
    vertices: list[float] = []
    indices: list[int] = []
    triangle_groups: list[int] = []


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
    InternalMeshSegment
    | InternalEllipsoidSegment
    | InternalSphereSegment
    | InternalBoxSegment
    | InternalTubeSegment
)


InternalSegment = InternalVolumeSegment | InternalMeshSegment | InternalGeometricSegment
