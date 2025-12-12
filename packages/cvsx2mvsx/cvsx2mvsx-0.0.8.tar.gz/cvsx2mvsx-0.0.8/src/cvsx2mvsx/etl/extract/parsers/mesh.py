from ciftools.serialization import loads

from cvsx2mvsx.etl.extract.parsers.common import (
    find_block,
    find_category,
    to_item,
    to_ndarray,
)
from cvsx2mvsx.etl.extract.parsers.interface import Parser
from cvsx2mvsx.models.cvsx.common import VolumeData3dInfo
from cvsx2mvsx.models.cvsx.mesh import (
    Mesh,
    MeshBlock,
    MeshCif,
    MeshTriangle,
    MeshVertex,
)


class MeshParser(Parser[MeshCif]):
    def parse(self, data: bytes) -> MeshCif:
        cif_file = loads(data, lazy=True)

        volume_info_block = find_block(cif_file, "VOLUME_INFO")
        meshes_block = find_block(cif_file, "MESHES")

        if volume_info_block is None:
            raise ValueError("VOLUME_INFO data block not found in CIF file")
        if meshes_block is None:
            raise ValueError("MESHES data block not found in CIF file")

        volume_data_3d_info_category = find_category(
            volume_info_block, "volume_data_3d_info"
        )
        mesh_category = find_category(meshes_block, "mesh")
        mesh_vertex_category = find_category(meshes_block, "mesh_vertex")
        mesh_triangle_category = find_category(meshes_block, "mesh_triangle")

        if not volume_data_3d_info_category:
            raise ValueError(
                "Segmentation data block is missing category 'volume_data_3d_info'."
            )
        if not mesh_category:
            raise ValueError("Segmentation data block is missing category 'mesh'.")
        if not mesh_vertex_category:
            raise ValueError(
                "Segmentation data block is missing category 'mesh_vertex'."
            )
        if not mesh_triangle_category:
            raise ValueError(
                "Segmentation data block is missing category ' mesh_triangle'."
            )

        volume_data_3d_info_data = VolumeData3dInfo(
            name=to_item(volume_data_3d_info_category, "name"),
            axis_order_0=to_item(volume_data_3d_info_category, "axis_order[0]"),
            axis_order_1=to_item(volume_data_3d_info_category, "axis_order[1]"),
            axis_order_2=to_item(volume_data_3d_info_category, "axis_order[2]"),
            origin_0=to_item(volume_data_3d_info_category, "origin[0]"),
            origin_1=to_item(volume_data_3d_info_category, "origin[1]"),
            origin_2=to_item(volume_data_3d_info_category, "origin[2]"),
            dimensions_0=to_item(volume_data_3d_info_category, "dimensions[0]"),
            dimensions_1=to_item(volume_data_3d_info_category, "dimensions[1]"),
            dimensions_2=to_item(volume_data_3d_info_category, "dimensions[2]"),
            sample_rate=to_item(volume_data_3d_info_category, "sample_rate"),
            sample_count_0=to_item(volume_data_3d_info_category, "sample_count[0]"),
            sample_count_1=to_item(volume_data_3d_info_category, "sample_count[1]"),
            sample_count_2=to_item(volume_data_3d_info_category, "sample_count[2]"),
            spacegroup_number=to_item(
                volume_data_3d_info_category, "spacegroup_number"
            ),
            spacegroup_cell_size_0=to_item(
                volume_data_3d_info_category, "spacegroup_cell_size[0]"
            ),
            spacegroup_cell_size_1=to_item(
                volume_data_3d_info_category, "spacegroup_cell_size[1]"
            ),
            spacegroup_cell_size_2=to_item(
                volume_data_3d_info_category, "spacegroup_cell_size[2]"
            ),
            spacegroup_cell_angles_0=to_item(
                volume_data_3d_info_category, "spacegroup_cell_angles[0]"
            ),
            spacegroup_cell_angles_1=to_item(
                volume_data_3d_info_category, "spacegroup_cell_angles[1]"
            ),
            spacegroup_cell_angles_2=to_item(
                volume_data_3d_info_category, "spacegroup_cell_angles[2]"
            ),
            mean_source=to_item(volume_data_3d_info_category, "mean_source"),
            mean_sampled=to_item(volume_data_3d_info_category, "mean_sampled"),
            sigma_source=to_item(volume_data_3d_info_category, "sigma_source"),
            sigma_sampled=to_item(volume_data_3d_info_category, "sigma_sampled"),
            min_source=to_item(volume_data_3d_info_category, "min_source"),
            min_sampled=to_item(volume_data_3d_info_category, "min_sampled"),
            max_source=to_item(volume_data_3d_info_category, "max_source"),
            max_sampled=to_item(volume_data_3d_info_category, "max_sampled"),
        )

        mesh_data = Mesh(
            id=to_ndarray(mesh_category, "id"),
        )

        mesh_vertex_data = MeshVertex(
            mesh_id=to_ndarray(mesh_vertex_category, "mesh_id"),
            vertex_id=to_ndarray(mesh_vertex_category, "vertex_id"),
            x=to_ndarray(mesh_vertex_category, "x"),
            y=to_ndarray(mesh_vertex_category, "y"),
            z=to_ndarray(mesh_vertex_category, "z"),
        )

        mesh_triangle_data = MeshTriangle(
            mesh_id=to_ndarray(mesh_triangle_category, "mesh_id"),
            vertex_id=to_ndarray(mesh_triangle_category, "vertex_id"),
        )

        mesh_block_data = MeshBlock(
            volume_data_3d_info=volume_data_3d_info_data,
            mesh=mesh_data,
            mesh_vertex=mesh_vertex_data,
            mesh_triangle=mesh_triangle_data,
        )

        return MeshCif(
            filename="PLACEHOLDER",
            mesh_block=mesh_block_data,
        )
