from typing import Literal

from pydantic import BaseModel

from cvsx2mvsx.models.internal.segment import (
    InternalGeometricSegment,
    InternalMeshSegment,
    InternalVolumeSegment,
)


class InternalBaseSegmentation(BaseModel):
    source_filepath: str | None = None

    timeframe_id: int
    segmentation_id: str

    color: str | None = None
    opacity: float | None = None


class InternalVolumeSegmentation(InternalBaseSegmentation):
    kind: Literal["volume"] = "volume"

    segments: dict[int, InternalVolumeSegment]


class InternalMeshSegmentation(InternalBaseSegmentation):
    kind: Literal["mesh"] = "mesh"

    segments: dict[int, InternalMeshSegment]


class InternalGeometricSegmentation(InternalBaseSegmentation):
    kind: Literal["geometric"] = "geometric"

    segments: dict[int, InternalGeometricSegment]


InternalSegmentation = (
    InternalVolumeSegmentation
    | InternalMeshSegmentation
    | InternalGeometricSegmentation
)
