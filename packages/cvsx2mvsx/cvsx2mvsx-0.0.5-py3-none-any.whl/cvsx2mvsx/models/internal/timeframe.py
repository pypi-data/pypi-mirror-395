from pydantic import BaseModel

from cvsx2mvsx.models.internal.segmentation import InternalSegmentation
from cvsx2mvsx.models.internal.volume import InternalVolume


class InternalTimeframe(BaseModel):
    timeframe_id: int

    volumes: dict[str, InternalVolume]
    segmentations: dict[str, InternalSegmentation]
