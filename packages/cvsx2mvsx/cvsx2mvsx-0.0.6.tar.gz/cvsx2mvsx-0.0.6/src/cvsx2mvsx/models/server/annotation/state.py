from typing import Annotated

from pydantic import BaseModel, Field

from cvsx2mvsx.models.server.annotation.entry import ServerEntryAnnotation
from cvsx2mvsx.models.server.annotation.segment import SegmentAnnotation
from cvsx2mvsx.models.server.annotation.segmentation import (
    SegmentationAnnotation,
)
from cvsx2mvsx.models.server.annotation.timeframe import (
    TimeframeAnnotation,
)
from cvsx2mvsx.models.server.annotation.volume import VolumeAnnotation

AnnotationItem = Annotated[
    ServerEntryAnnotation
    | TimeframeAnnotation
    | VolumeAnnotation
    | SegmentationAnnotation
    | SegmentAnnotation,
    Field(discriminator="kind"),
]


class AnnotationState(BaseModel):
    state: dict[str, AnnotationItem] = {}


SEPARATOR = "::"


def _sanitize(value: str | int) -> str:
    return str(value).replace(SEPARATOR, "__")


def make_entry_id(entry_id: str | int) -> str:
    return f"entry{SEPARATOR}{_sanitize(entry_id)}"


def make_timeframe_id(timeframe: int) -> str:
    return f"timeframe{SEPARATOR}{_sanitize(timeframe)}"


def make_volume_id(timeframe: int, channel: str) -> str:
    return f"volume{SEPARATOR}{_sanitize(timeframe)}{SEPARATOR}{_sanitize(channel)}"


def make_segmentation_id(timeframe: int, segmentation: str) -> str:
    return f"segmentation{SEPARATOR}{_sanitize(timeframe)}{SEPARATOR}{_sanitize(segmentation)}"


def make_segment_id(timeframe: int, segmentation: str, segment: int) -> str:
    return f"segment{SEPARATOR}{_sanitize(timeframe)}{SEPARATOR}{_sanitize(segmentation)}{SEPARATOR}{_sanitize(segment)}"
