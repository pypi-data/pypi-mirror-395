from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from cvsx2mvsx.models.server.structure.segmentation import StructureSegmentation
from cvsx2mvsx.models.server.structure.volume import StructureVolume


class StructureTimeframe(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    # identifier
    timeframe_id: int

    volumes: dict[str, StructureVolume]
    segmentations: dict[str, StructureSegmentation]
