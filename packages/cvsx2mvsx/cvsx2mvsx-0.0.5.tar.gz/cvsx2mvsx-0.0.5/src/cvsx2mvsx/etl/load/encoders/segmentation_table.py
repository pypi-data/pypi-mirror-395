from ciftools.binary.data_types import DataType, DataTypeEnum
from ciftools.models.writer import CIFCategoryDesc
from ciftools.models.writer import CIFFieldDesc as Field

from cvsx2mvsx.models.cif.read.lattice import SegmentationDataTable
from cvsx2mvsx.models.cif.write.encoders import bytearray_encoder, delta_rl_encoder


class SegmentationDataTableCategory(CIFCategoryDesc):
    name = "segmentation_data_table"

    @staticmethod
    def get_row_count(data: SegmentationDataTable) -> int:
        return data.set_id.size

    @staticmethod
    def get_field_descriptors(data: SegmentationDataTable):
        dtype = DataType.to_dtype(DataTypeEnum.Int32)
        return [
            Field.number_array(
                name="set_id",
                dtype=dtype,
                encoder=delta_rl_encoder,
                array=lambda d: d.set_id,
            ),
            Field.number_array(
                name="segment_id",
                dtype=dtype,
                encoder=bytearray_encoder,
                array=lambda d: d.segment_id,
            ),
        ]
