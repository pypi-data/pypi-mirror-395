from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cvsx.common import VolumeData3dInfo


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
                value=lambda d, i: data.name,
            ),
            CIFFieldDesc.numbers(
                name="axis_order[0]",
                value=lambda d, i: data.axis_order_0,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="axis_order[1]",
                value=lambda d, i: data.axis_order_1,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="axis_order[2]",
                value=lambda d, i: data.axis_order_2,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="origin[0]",
                value=lambda d, i: data.origin_0,
                dtype="f4",
            ),
            CIFFieldDesc.numbers(
                name="origin[1]",
                value=lambda d, i: data.origin_1,
                dtype="f4",
            ),
            CIFFieldDesc.numbers(
                name="origin[2]",
                value=lambda d, i: data.origin_2,
                dtype="f4",
            ),
            CIFFieldDesc.numbers(
                name="dimensions[0]",
                value=lambda d, i: data.dimensions_0,
                dtype="f4",
            ),
            CIFFieldDesc.numbers(
                name="dimensions[1]",
                value=lambda d, i: data.dimensions_1,
                dtype="f4",
            ),
            CIFFieldDesc.numbers(
                name="dimensions[2]",
                value=lambda d, i: data.dimensions_2,
                dtype="f4",
            ),
            CIFFieldDesc.numbers(
                name="sample_rate",
                value=lambda d, i: data.sample_rate,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="sample_count[0]",
                value=lambda d, i: data.sample_count_0,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="sample_count[1]",
                value=lambda d, i: data.sample_count_1,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="sample_count[2]",
                value=lambda d, i: data.sample_count_2,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_number",
                value=lambda d, i: data.spacegroup_number,
                dtype="i4",
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_size[0]",
                value=lambda d, i: data.spacegroup_cell_size_0,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_size[1]",
                value=lambda d, i: data.spacegroup_cell_size_1,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_size[2]",
                value=lambda d, i: data.spacegroup_cell_size_2,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_angles[0]",
                value=lambda d, i: data.spacegroup_cell_angles_0,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_angles[1]",
                value=lambda d, i: data.spacegroup_cell_angles_1,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="spacegroup_cell_angles[2]",
                value=lambda d, i: data.spacegroup_cell_angles_2,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="mean_source",
                value=lambda d, i: data.mean_source,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="mean_sampled",
                value=lambda d, i: data.mean_sampled,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="sigma_source",
                value=lambda d, i: data.sigma_source,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="sigma_sampled",
                value=lambda d, i: data.sigma_sampled,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="min_source",
                value=lambda d, i: data.min_source,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="min_sampled",
                value=lambda d, i: data.min_sampled,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="max_source",
                value=lambda d, i: data.max_source,
                dtype="f8",
            ),
            CIFFieldDesc.numbers(
                name="max_sampled",
                value=lambda d, i: data.max_sampled,
                dtype="f8",
            ),
        ]
