from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class StructureBaseSegment(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    # identifier
    timeframe_id: int
    segmentation_id: str
    segment_id: int


class StructureVolumeSegment(StructureBaseSegment):
    kind: Literal["volume"] = "volume"

    # file
    storage_key: str | None = None


class StructureMeshSegment(StructureBaseSegment):
    kind: Literal["mesh"] = "mesh"

    # file
    storage_key: str | None = None


# geometric segments don't have storage_key because
# they are stored in a single segmentation file


class StructurePyramidSegment(StructureBaseSegment):
    kind: Literal["pyramid"] = "pyramid"


class StructureEllipsoidSegment(StructureBaseSegment):
    kind: Literal["ellipsoid"] = "ellipsoid"


class StructureSphereSegment(StructureBaseSegment):
    kind: Literal["sphere"] = "sphere"


class StructureBoxSegment(StructureBaseSegment):
    kind: Literal["box"] = "box"


class StructureTubeSegment(StructureBaseSegment):
    kind: Literal["tube"] = "tube"


StructureGeometricSegment = (
    StructurePyramidSegment
    | StructureEllipsoidSegment
    | StructureSphereSegment
    | StructureBoxSegment
    | StructureTubeSegment
)


StructureSegment = (
    StructureVolumeSegment | StructureMeshSegment | StructureGeometricSegment
)
