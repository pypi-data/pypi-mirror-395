from ciftools.serialization import loads

from cvsx2mvsx.etl.extract.parsers.common import (
    find_block,
    find_category,
    to_item,
    to_ndarray,
)
from cvsx2mvsx.etl.extract.parsers.interface import Parser
from cvsx2mvsx.models.cvsx.common import (
    VolumeData3dInfo,
    VolumeDataTimeAndChannelInfo,
)
from cvsx2mvsx.models.cvsx.lattice import (
    LatticeCif,
    SegmentationBlock,
    SegmentationData3d,
    SegmentationDataTable,
)


class LatticeParser(Parser[LatticeCif]):
    def parse(self, data: bytes) -> LatticeCif:
        cif_file = loads(data, lazy=True)

        segmentation_block = find_block(cif_file, "SEGMENTATION_DATA")
        if segmentation_block is None:
            raise ValueError("SEGMENTATION_DATA data block not found in CIF file")

        vol3d = find_category(segmentation_block, "volume_data_3d_info")
        time_ch = find_category(segmentation_block, "volume_data_time_and_channel_info")
        seg_table = find_category(segmentation_block, "segmentation_data_table")
        seg3d = find_category(segmentation_block, "segmentation_data_3d")

        if not all(
            [
                vol3d,
                time_ch,
                seg_table,
                seg3d,
            ]
        ):
            raise ValueError("Segmentation data block is missing a category.")

        volume_data_3d_info = VolumeData3dInfo(
            name=to_item(vol3d, "name"),
            axis_order_0=to_item(vol3d, "axis_order[0]"),
            axis_order_1=to_item(vol3d, "axis_order[1]"),
            axis_order_2=to_item(vol3d, "axis_order[2]"),
            origin_0=to_item(vol3d, "origin[0]"),
            origin_1=to_item(vol3d, "origin[1]"),
            origin_2=to_item(vol3d, "origin[2]"),
            dimensions_0=to_item(vol3d, "dimensions[0]"),
            dimensions_1=to_item(vol3d, "dimensions[1]"),
            dimensions_2=to_item(vol3d, "dimensions[2]"),
            sample_rate=to_item(vol3d, "sample_rate"),
            sample_count_0=to_item(vol3d, "sample_count[0]"),
            sample_count_1=to_item(vol3d, "sample_count[1]"),
            sample_count_2=to_item(vol3d, "sample_count[2]"),
            spacegroup_number=to_item(vol3d, "spacegroup_number"),
            spacegroup_cell_size_0=to_item(vol3d, "spacegroup_cell_size[0]"),
            spacegroup_cell_size_1=to_item(vol3d, "spacegroup_cell_size[1]"),
            spacegroup_cell_size_2=to_item(vol3d, "spacegroup_cell_size[2]"),
            spacegroup_cell_angles_0=to_item(vol3d, "spacegroup_cell_angles[0]"),
            spacegroup_cell_angles_1=to_item(vol3d, "spacegroup_cell_angles[1]"),
            spacegroup_cell_angles_2=to_item(vol3d, "spacegroup_cell_angles[2]"),
            mean_source=to_item(vol3d, "mean_source"),
            mean_sampled=to_item(vol3d, "mean_sampled"),
            sigma_source=to_item(vol3d, "sigma_source"),
            sigma_sampled=to_item(vol3d, "sigma_sampled"),
            min_source=to_item(vol3d, "min_source"),
            min_sampled=to_item(vol3d, "min_sampled"),
            max_source=to_item(vol3d, "max_source"),
            max_sampled=to_item(vol3d, "max_sampled"),
        )

        volume_data_time_and_channel_info = VolumeDataTimeAndChannelInfo(
            time_id=to_item(time_ch, "time_id"),
            channel_id=to_item(time_ch, "channel_id"),
        )

        segmentation_data_table = SegmentationDataTable(
            set_id=to_ndarray(seg_table, "set_id"),
            segment_id=to_ndarray(seg_table, "segment_id"),
        )

        segmentation_data_3d = SegmentationData3d(
            values=to_ndarray(seg3d, "values"),
        )

        segmentation_block = SegmentationBlock(
            volume_data_3d_info=volume_data_3d_info,
            volume_data_time_and_channel_info=volume_data_time_and_channel_info,
            segmentation_data_table=segmentation_data_table,
            segmentation_data_3d=segmentation_data_3d,
        )

        return LatticeCif(
            segmentation_block=segmentation_block,
        )
