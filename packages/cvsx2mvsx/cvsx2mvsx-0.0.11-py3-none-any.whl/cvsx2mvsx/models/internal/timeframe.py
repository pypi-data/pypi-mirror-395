from pydantic import BaseModel, ConfigDict

from cvsx2mvsx.models.internal.segmentation import InternalSegmentation
from cvsx2mvsx.models.internal.volume import InternalVolume


class InternalTimeframe(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timeframe_id: int

    volumes: list[InternalVolume]
    segmentations: list[InternalSegmentation]
