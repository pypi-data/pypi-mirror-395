import numpy as np
from pydantic import BaseModel, ConfigDict

from cvsx2mvsx.models.cvsx.common import (
    VolumeData3dInfo,
    VolumeDataTimeAndChannelInfo,
)


class SegmentationDataTable(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    set_id: np.ndarray[int]
    segment_id: np.ndarray[int]


class SegmentationData3d(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    values: np.ndarray[float]


class SegmentationBlock(BaseModel):
    volume_data_3d_info: VolumeData3dInfo
    volume_data_time_and_channel_info: VolumeDataTimeAndChannelInfo
    segmentation_data_table: SegmentationDataTable
    segmentation_data_3d: SegmentationData3d


class LatticeCif(BaseModel):
    segmentation_block: SegmentationBlock
