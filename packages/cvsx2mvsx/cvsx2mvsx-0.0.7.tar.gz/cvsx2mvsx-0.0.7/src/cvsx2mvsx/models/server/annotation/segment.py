from typing import Annotated, Literal

from pydantic import BaseModel, Field


class VolumeSegmentAnnotation(BaseModel):
    kind: Literal["segment"] = "segment"
    type: Literal["volume"] = "volume"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    tooltip: str | None = None


class MeshSegmentAnnotation(BaseModel):
    kind: Literal["segment"] = "segment"
    type: Literal["mesh"] = "mesh"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    tooltip: str | None = None


class GeometricSegmentAnnotation(BaseModel):
    kind: Literal["segment"] = "segment"
    type: Literal["geometric"] = "geometric"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    tooltip: str | None = None


SegmentAnnotation = Annotated[
    VolumeSegmentAnnotation | MeshSegmentAnnotation | GeometricSegmentAnnotation,
    Field(discriminator="type"),
]
