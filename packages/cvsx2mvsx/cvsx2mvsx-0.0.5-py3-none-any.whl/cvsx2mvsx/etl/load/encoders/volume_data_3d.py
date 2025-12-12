from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cif.read.volume import VolumeData3d
from cvsx2mvsx.models.cif.write.encoders import decide_encoder


class VolumeData3dCategory(CIFCategoryDesc):
    name = "volume_data_3d"

    @staticmethod
    def get_row_count(data: VolumeData3d) -> int:
        return data.values.size

    @staticmethod
    def get_field_descriptors(data: VolumeData3d):
        encoder, dtype = decide_encoder(data.values, "VolumeData3d")
        return [
            CIFFieldDesc.number_array(
                name="values",
                dtype=dtype,
                encoder=lambda: encoder,
                array=lambda d: d.values,
            ),
        ]
