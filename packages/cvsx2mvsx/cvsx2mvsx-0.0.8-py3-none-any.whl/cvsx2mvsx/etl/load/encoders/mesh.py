from ciftools.models.writer import CIFCategoryDesc, CIFFieldDesc

from cvsx2mvsx.src.models.cif.read.mesh import Mesh
from cvsx2mvsx.src.models.cif.write.encoders import bytearray_encoder


class MeshCategory(CIFCategoryDesc):
    name = "mesh"

    @staticmethod
    def get_row_count(data: Mesh) -> int:
        return data.id.size

    @staticmethod
    def get_field_descriptors(data: Mesh):
        return [
            CIFFieldDesc.number_array(
                name="id",
                dtype=data.id.dtype,
                encoder=bytearray_encoder,
                array=lambda d: d.id,
            ),
        ]
