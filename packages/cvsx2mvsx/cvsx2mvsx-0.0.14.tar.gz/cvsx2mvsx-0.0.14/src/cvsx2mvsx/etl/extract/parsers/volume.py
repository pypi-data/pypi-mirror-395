from ciftools.serialization import loads

from cvsx2mvsx.etl.extract.parsers.common import find_block, find_category, to_item
from cvsx2mvsx.etl.extract.parsers.interface import Parser
from cvsx2mvsx.models.cvsx.common import (
    VolumeData3dInfo,
)
from cvsx2mvsx.models.cvsx.volume import VolumeBlock, VolumeCif


class VolumeParser(Parser[VolumeCif]):
    def parse(self, data: bytes) -> VolumeCif:
        cif_file = loads(data, lazy=True)

        volume_block = find_block(cif_file, "VOLUME")
        if volume_block is None:
            raise ValueError("VOLUME data block not found in CIF file")

        vol3dinfo = find_category(volume_block, "volume_data_3d_info")

        if not vol3dinfo:
            raise ValueError("Segmentation data block is missing a category.")

        volume_data_3d_info = VolumeData3dInfo(
            name=to_item(vol3dinfo, "name"),
            axis_order_0=to_item(vol3dinfo, "axis_order[0]"),
            axis_order_1=to_item(vol3dinfo, "axis_order[1]"),
            axis_order_2=to_item(vol3dinfo, "axis_order[2]"),
            origin_0=to_item(vol3dinfo, "origin[0]"),
            origin_1=to_item(vol3dinfo, "origin[1]"),
            origin_2=to_item(vol3dinfo, "origin[2]"),
            dimensions_0=to_item(vol3dinfo, "dimensions[0]"),
            dimensions_1=to_item(vol3dinfo, "dimensions[1]"),
            dimensions_2=to_item(vol3dinfo, "dimensions[2]"),
            sample_rate=to_item(vol3dinfo, "sample_rate"),
            sample_count_0=to_item(vol3dinfo, "sample_count[0]"),
            sample_count_1=to_item(vol3dinfo, "sample_count[1]"),
            sample_count_2=to_item(vol3dinfo, "sample_count[2]"),
            spacegroup_number=to_item(vol3dinfo, "spacegroup_number"),
            spacegroup_cell_size_0=to_item(vol3dinfo, "spacegroup_cell_size[0]"),
            spacegroup_cell_size_1=to_item(vol3dinfo, "spacegroup_cell_size[1]"),
            spacegroup_cell_size_2=to_item(vol3dinfo, "spacegroup_cell_size[2]"),
            spacegroup_cell_angles_0=to_item(vol3dinfo, "spacegroup_cell_angles[0]"),
            spacegroup_cell_angles_1=to_item(vol3dinfo, "spacegroup_cell_angles[1]"),
            spacegroup_cell_angles_2=to_item(vol3dinfo, "spacegroup_cell_angles[2]"),
            mean_source=to_item(vol3dinfo, "mean_source"),
            mean_sampled=to_item(vol3dinfo, "mean_sampled"),
            sigma_source=to_item(vol3dinfo, "sigma_source"),
            sigma_sampled=to_item(vol3dinfo, "sigma_sampled"),
            min_source=to_item(vol3dinfo, "min_source"),
            min_sampled=to_item(vol3dinfo, "min_sampled"),
            max_source=to_item(vol3dinfo, "max_source"),
            max_sampled=to_item(vol3dinfo, "max_sampled"),
        )

        volume_block = VolumeBlock(
            volume_data_3d_info=volume_data_3d_info,
        )

        return VolumeCif(
            volume_block=volume_block,
        )
