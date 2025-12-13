import numpy as np
from pydantic import BaseModel, ConfigDict

from cvsx2mvsx.models.cvsx.common import (
    VolumeData3dInfo,
)


class VolumeData3d(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    values: np.ndarray[float]


class VolumeBlock(BaseModel):
    volume_data_3d_info: VolumeData3dInfo
    # # unused
    # volume_data_time_and_channel_info: VolumeDataTimeAndChannelInfo
    # volume_data_3d: VolumeData3d


class VolumeCif(BaseModel):
    volume_block: VolumeBlock
