from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.models.cif.read.mesh import MeshVertex
from cvsx2mvsx.models.cif.write.encoders import coord_encoder, delta_rl_encoder


class MeshVertexCategory(CIFCategoryDesc):
    name = "mesh_vertex"

    @staticmethod
    def get_row_count(data: MeshVertex) -> int:
        return data.vertex_id.size

    @staticmethod
    def get_field_descriptors(data: MeshVertex):
        return [
            CIFFieldDesc.number_array(
                name="mesh_id",
                dtype=data.mesh_id.dtype,
                encoder=delta_rl_encoder,
                array=lambda d: d.mesha_id,
            ),
            CIFFieldDesc.number_array(
                name="vertex_id",
                dtype=data.vertex_id.dtype,
                encoder=delta_rl_encoder,
                array=lambda d: d.vertex_id,
            ),
            CIFFieldDesc.number_array(
                name="x",
                dtype=data.x.dtype,
                encoder=lambda d: coord_encoder(d.x),
                array=lambda d: d.x,
            ),
            CIFFieldDesc.number_array(
                name="y",
                dtype=data.y.dtype,
                encoder=lambda d: coord_encoder(d.y),
                array=lambda d: d.y,
            ),
            CIFFieldDesc.number_array(
                name="z",
                dtype=data.z.dtype,
                encoder=lambda d: coord_encoder(d.z),
                array=lambda d: d.z,
            ),
        ]
