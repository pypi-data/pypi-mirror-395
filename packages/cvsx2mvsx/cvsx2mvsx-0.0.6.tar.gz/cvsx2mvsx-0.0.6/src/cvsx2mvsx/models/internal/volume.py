from typing import Literal

from pydantic import BaseModel


class InternalBaseVolume(BaseModel):
    source_filepath: str

    timeframe_id: int
    channel_id: str

    color: str
    opacity: float
    relative_isovalue: float


class InternalIsosurfaceVolume(InternalBaseVolume):
    kind: Literal["isosurface"] = "isosurface"


class InternalGridSliceVolume(InternalBaseVolume):
    kind: Literal["grid_slice"] = "grid_slice"

    dimension: Literal["x", "y", "z"]


InternalVolume = InternalIsosurfaceVolume | InternalGridSliceVolume
