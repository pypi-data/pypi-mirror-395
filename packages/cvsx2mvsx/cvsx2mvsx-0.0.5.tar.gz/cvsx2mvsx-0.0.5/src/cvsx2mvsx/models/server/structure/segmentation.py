from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cvsx2mvsx.models.server.structure.segment import (
    StructureGeometricSegment,
    StructureMeshSegment,
    StructureVolumeSegment,
)


class StructureBaseSegmentation(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    # identifier
    timeframe_id: int
    segmentation_id: str


class StructureVolumeSegmentation(StructureBaseSegmentation):
    kind: Literal["volume"] = "volume"

    segments: dict[int, StructureVolumeSegment]


class StructureMeshSegmentation(StructureBaseSegmentation):
    kind: Literal["mesh"] = "mesh"

    segments: dict[int, StructureMeshSegment]


class StructureGeometricSegmentation(StructureBaseSegmentation):
    kind: Literal["geometric"] = "geometric"

    # file
    storage_key: str | None = None

    segments: dict[int, StructureGeometricSegment]


StructureSegmentation = (
    StructureVolumeSegmentation
    | StructureMeshSegmentation
    | StructureGeometricSegmentation
)
