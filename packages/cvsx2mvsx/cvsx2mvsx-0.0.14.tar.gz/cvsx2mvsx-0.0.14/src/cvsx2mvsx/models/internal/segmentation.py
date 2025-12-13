from typing import Literal

from pydantic import BaseModel, ConfigDict

from cvsx2mvsx.models.internal.segment import (
    InternalGeometricSegment,
    InternalMeshSegment,
    InternalVolumeSegment,
)


class InternalBaseSegmentation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_filepath: str | None = None

    timeframe_id: int
    segmentation_id: str

    color: str | None = None
    opacity: float | None = None


class InternalVolumeSegmentation(InternalBaseSegmentation):
    kind: Literal["volume"] = "volume"

    segments: list[InternalVolumeSegment]


class InternalMeshSegmentation(InternalBaseSegmentation):
    kind: Literal["mesh"] = "mesh"

    segments: list[InternalMeshSegment]


class InternalGeometricSegmentation(InternalBaseSegmentation):
    kind: Literal["geometric"] = "geometric"

    segments: list[InternalGeometricSegment]


InternalSegmentation = (
    InternalVolumeSegmentation
    | InternalMeshSegmentation
    | InternalGeometricSegmentation
)
