from typing import Literal

from pydantic import BaseModel, ConfigDict


class InternalBaseVolume(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_filepath: str

    timeframe_id: int
    channel_id: str

    color: str
    opacity: float

    label: str | None
    description: str | None


class InternalIsosurfaceVolume(InternalBaseVolume):
    kind: Literal["isosurface"] = "isosurface"

    absolute_isovalue: float | None
    relative_isovalue: float
    show_faces: bool
    show_wireframe: bool


class InternalGridSliceVolume(InternalBaseVolume):
    kind: Literal["grid_slice"] = "grid_slice"

    absolute_isovalue: float | None
    relative_isovalue: float
    dimension: Literal["x", "y", "z"]
    absolute_index: int


InternalVolume = InternalIsosurfaceVolume | InternalGridSliceVolume
