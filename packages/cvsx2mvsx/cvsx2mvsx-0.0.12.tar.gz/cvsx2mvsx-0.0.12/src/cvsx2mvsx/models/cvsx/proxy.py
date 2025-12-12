from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from cvsx2mvsx.etl.extract.parsers.interface import Parser
from cvsx2mvsx.models.cvsx.geometric import ShapePrimitiveData
from cvsx2mvsx.models.cvsx.index import (
    MeshSegmentationFilesInfo,
    SegmentationFileInfo,
    VolumeFileInfo,
)
from cvsx2mvsx.models.cvsx.lattice import LatticeCif
from cvsx2mvsx.models.cvsx.mesh import MeshCif
from cvsx2mvsx.models.cvsx.volume import VolumeCif

T = TypeVar("T")
M = TypeVar("M")


class FileProxy(Generic[T, M]):
    def __init__(
        self,
        filepath: str,
        metadata: M,
        parser: Parser[T],
    ):
        self.filepath = filepath
        self.metadata = metadata
        self._parser = parser

    def load(self) -> T:
        with open(self.filepath, "rb") as f:
            data = f.read()
            return self._parser.parse(data)


class CVSXFilesProxy(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    volumes: list[
        FileProxy[
            VolumeCif,
            VolumeFileInfo,
        ]
    ] = []
    lattice_segmentations: list[
        FileProxy[
            LatticeCif,
            SegmentationFileInfo,
        ]
    ] = []
    mesh_segmentations: list[
        FileProxy[
            MeshCif,
            MeshSegmentationFilesInfo,
        ]
    ] = []
    geometric_segmentations: list[
        FileProxy[
            ShapePrimitiveData,
            SegmentationFileInfo,
        ]
    ] = []
