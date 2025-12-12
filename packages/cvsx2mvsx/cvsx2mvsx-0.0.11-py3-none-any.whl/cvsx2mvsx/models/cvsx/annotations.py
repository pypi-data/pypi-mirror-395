from typing import Any, Literal, Optional

from pydantic import BaseModel

from cvsx2mvsx.models.cvsx.common import EntryId


class ChannelAnnotation(BaseModel):
    channel_id: str
    color: Optional[tuple[float, float, float, float]]
    label: Optional[str]


class SegmentAnnotationData(BaseModel):
    id: Optional[str]
    segment_kind: Literal["lattice", "mesh", "primitive"]
    segment_id: int
    segmentation_id: str
    color: Optional[tuple[float, float, float, float]]
    time: Optional[int | list[int | tuple[int, int]]]


class ExternalReference(BaseModel):
    id: Optional[str]
    resource: Optional[str]
    accession: Optional[str]
    label: Optional[str]
    description: Optional[str]
    url: Optional[str]


class TargetId(BaseModel):
    segmentation_id: str
    segment_id: int


class DetailsText(BaseModel):
    format: Literal["text", "markdown"]
    text: str


class DescriptionData(BaseModel):
    id: Optional[str]
    target_kind: Literal["lattice", "mesh", "primitive", "entry"]
    target_id: Optional[TargetId]
    name: Optional[str | int]
    external_references: Optional[list[ExternalReference]]
    is_hidden: Optional[bool]
    time: Optional[int | list[int | tuple[int, int]]]
    details: Optional[DetailsText]
    metadata: dict[str, Any] | None


class CVSXAnnotations(BaseModel):
    entry_id: EntryId
    name: Optional[str]
    details: Optional[str]
    descriptions: dict[str, DescriptionData]
    volume_channels_annotations: Optional[list[ChannelAnnotation]]
    segment_annotations: list[SegmentAnnotationData]
