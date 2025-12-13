from numpy import ndarray
from pydantic import BaseModel, ConfigDict

from cvsx2mvsx.models.cvsx.common import VolumeData3dInfo


class Mesh(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ndarray[int]


class MeshVertex(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    mesh_id: ndarray[int]
    vertex_id: ndarray[int]
    x: ndarray[float]
    y: ndarray[float]
    z: ndarray[float]


class MeshTriangle(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    mesh_id: ndarray[int]
    vertex_id: ndarray[int]


class MeshBlock(BaseModel):
    volume_data_3d_info: VolumeData3dInfo
    mesh: Mesh
    mesh_vertex: MeshVertex
    mesh_triangle: MeshTriangle


class MeshCif(BaseModel):
    mesh_block: MeshBlock
