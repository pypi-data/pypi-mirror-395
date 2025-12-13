import numpy as np
from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.etl.load.encoders.encoders import decide_encoder


class VolumeData3dCategory(CIFCategoryDesc):
    name = "volume_data_3d"

    @staticmethod
    def get_row_count(data: np.ndarray) -> int:
        return data.size

    @staticmethod
    def get_field_descriptors(data: np.ndarray):
        encoder, dtype = decide_encoder(data)
        return [
            CIFFieldDesc.number_array(
                name="values",
                dtype=dtype,
                encoder=lambda _: encoder,
                array=lambda volume: volume,
            ),
        ]
