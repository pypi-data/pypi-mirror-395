from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cif.read.common import VolumeData3dInfo
from cvsx2mvsx.models.cif.write.encoders import bytearray_encoder


class VolumeData3dInfoCategory(CIFCategoryDesc):
    name = "volume_data_3d_info"

    @staticmethod
    def get_row_count(data: VolumeData3dInfo) -> int:
        return 1

    @staticmethod
    def get_field_descriptors(data: VolumeData3dInfo):
        return [
            CIFFieldDesc.strings(
                name="name",
                value=lambda d: d.name,
            ),
            CIFFieldDesc.numbers(
                name="axis_order[0]",
                value=lambda d: d.axis_order_0,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="axis_order[1]",
                value=lambda d: d.axis_order_1,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="axis_order[2]",
                value=lambda d: d.axis_order_2,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="origin[0]",
                value=lambda d: d.origin_0,
                dtype="f4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="origin[1]",
                value=lambda d: d.origin_1,
                dtype="f4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="origin[2]",
                value=lambda d: d.origin_2,
                dtype="f4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="dimensions[0]",
                value=lambda d: d.dimensions_0,
                dtype="f4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="dimensions[1]",
                value=lambda d: d.dimensions_1,
                dtype="f4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="dimensions[2]",
                value=lambda d: d.dimensions_2,
                dtype="f4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="sample_rate",
                value=lambda d: d.sample_rate,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="sample_count[0]",
                value=lambda d: d.sample_count_0,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="sample_count[1]",
                value=lambda d: d.sample_count_1,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="sample_count[2]",
                value=lambda d: d.sample_count_2,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_number",
                value=lambda d: d.spacegroup_number,
                dtype="i4",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_size[0]",
                value=lambda d: d.spacegroup_cell_size_0,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_size[1]",
                value=lambda d: d.spacegroup_cell_size_1,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_size[2]",
                value=lambda d: d.spacegroup_cell_size_2,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_angles[0]",
                value=lambda d: d.spacegroup_cell_angles_0,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_angles[1]",
                value=lambda d: d.spacegroup_cell_angles_1,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_angles[2]",
                value=lambda d: d.spacegroup_cell_angles_2,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="mean_source",
                value=lambda d: d.mean_source,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="mean_sampled",
                value=lambda d: d.mean_sampled,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="sigma_source",
                value=lambda d: d.sigma_source,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="sigma_sampled",
                value=lambda d: d.sigma_sampled,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="min_source",
                value=lambda d: d.min_source,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="min_sampled",
                value=lambda d: d.min_sampled,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="max_source",
                value=lambda d: d.max_source,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
            CIFFieldDesc.numbers(
                name="max_sampled",
                value=lambda d: d.max_sampled,
                dtype="f8",
                encoder=bytearray_encoder,
            ),
        ]
