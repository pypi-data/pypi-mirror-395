from typing import Annotated, Literal

from pydantic import BaseModel, Field


class IsosurfaceVolumeAnnotation(BaseModel):
    kind: Literal["volume"] = "volume"
    type: Literal["isosurface"] = "isosurface"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    relative_isovalue: float | None = None


class GridSliceVolumeAnnotation(BaseModel):
    kind: Literal["volume"] = "volume"
    type: Literal["grid_slice"] = "grid_slice"

    name: str | None = None
    description: str | None = None

    color: str | None = None
    opacity: float | None = None
    relative_isovalue: float | None = None
    dimension: Literal["x", "y", "z"] | None = None


VolumeAnnotation = Annotated[
    IsosurfaceVolumeAnnotation | GridSliceVolumeAnnotation,
    Field(discriminator="type"),
]
