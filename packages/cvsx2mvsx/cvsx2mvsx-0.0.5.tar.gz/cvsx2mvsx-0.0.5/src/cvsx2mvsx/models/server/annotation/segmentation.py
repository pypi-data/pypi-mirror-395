from typing import Annotated, Literal

from pydantic import BaseModel, Field


class VolumeSegmentationAnnotation(BaseModel):
    kind: Literal["segmentation"] = "segmentation"
    type: Literal["volume"] = "volume"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    tooltip: str | None = None


class MeshSegmentationAnnotation(BaseModel):
    kind: Literal["segmentation"] = "segmentation"
    type: Literal["mesh"] = "mesh"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    tooltip: str | None = None


class GeometricSegmentationAnnotation(BaseModel):
    kind: Literal["segmentation"] = "segmentation"
    type: Literal["geometric"] = "geometric"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    tooltip: str | None = None


SegmentationAnnotation = Annotated[
    VolumeSegmentationAnnotation
    | MeshSegmentationAnnotation
    | GeometricSegmentationAnnotation,
    Field(discriminator="type"),
]
