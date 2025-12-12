from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cif.read.mesh import MeshTriangle
from cvsx2mvsx.models.cif.write.encoders import bytearray_encoder, delta_rl_encoder


class MeshTriangleCategory(CIFCategoryDesc):
    name = "mesh_triangle"

    @staticmethod
    def get_row_count(data: MeshTriangle) -> int:
        return data.mesh_id.size

    @staticmethod
    def get_field_descriptors(data: MeshTriangle):
        return [
            CIFFieldDesc.number_array(
                name="mesh_id",
                dtype=data.mesh_id.dtype,
                encoder=delta_rl_encoder,
                array=lambda d: d.mesh_id,
            ),
            CIFFieldDesc.number_array(
                name="vertex_id",
                dtype=data.vertex_id.dtype,
                encoder=bytearray_encoder,
                array=lambda d: d.vertex_id,
            ),
        ]
