from typing import Literal

from pydantic import BaseModel, field_validator


class CVSXFileInfo(BaseModel):
    type: Literal[
        "volume",
        "lattice",
        "mesh",
        "geometric-segmentation",
        "annotations",
        "metadata",
        "query",
    ]


class VolumeFileInfo(CVSXFileInfo):
    channelId: str
    timeframeIndex: int

    @field_validator("channelId", mode="before")
    @classmethod
    def convert_channel_id_to_string(cls, v):
        return str(v)


class SegmentationFileInfo(CVSXFileInfo):
    segmentationId: str
    timeframeIndex: int


class MeshSegmentationFilesInfo(SegmentationFileInfo):
    segmentsFilenames: list[str]


class CVSXIndex(BaseModel):
    query: str
    metadata: str
    annotations: str
    volumes: dict[str, VolumeFileInfo]
    meshSegmentations: list[MeshSegmentationFilesInfo] | None = None
    latticeSegmentations: dict[str, SegmentationFileInfo] | None = None
    geometricSegmentations: dict[str, SegmentationFileInfo] | None = None
