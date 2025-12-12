from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class StructureBaseVolume(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    # identifier
    timeframe_id: int
    channel_id: str

    # files
    storage_key: str | None = None


class StructureIsosurfaceVolume(StructureBaseVolume):
    kind: Literal["isosurface"] = "isosurface"


class StructureGridSliceVolume(StructureBaseVolume):
    kind: Literal["grid_slice"] = "grid_slice"


StructureVolume = StructureIsosurfaceVolume | StructureGridSliceVolume
