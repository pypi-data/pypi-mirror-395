from typing import Literal

from pydantic import BaseModel

SegmentationKind = Literal["mesh", "lattice", "geometric-segmentation"]


class CVSXQuery(BaseModel):
    entry_id: str
    source_db: str
    segmentation_kind: SegmentationKind | None = None
    time: int | None = None
    channel_id: str | None = None
    segmentation_id: str | None = None
    detail_lvl: int | None = None
    max_points: int | None = None
