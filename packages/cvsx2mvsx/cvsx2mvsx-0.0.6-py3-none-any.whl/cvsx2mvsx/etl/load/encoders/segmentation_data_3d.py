from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cif.read.lattice import SegmentationData3d
from cvsx2mvsx.src.models.cif.write.encoders import decide_encoder


class SegmentationData3dCategory(CIFCategoryDesc):
    name = "segmentation_data_3d"

    @staticmethod
    def get_row_count(data: SegmentationData3d) -> int:
        return data.values.size

    @staticmethod
    def get_field_descriptors(data: SegmentationData3d):
        encoder, dtype = decide_encoder(data, "SegmentationData3d")
        return [
            CIFFieldDesc.number_array(
                name="values",
                dtype=dtype,
                encoder=lambda: encoder,
                array=lambda d: d.values,
            ),
        ]
