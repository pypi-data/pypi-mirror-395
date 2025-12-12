from collections import defaultdict
from typing import Literal, Optional, Protocol, TypeVar

from cvsx2mvsx.models.cvsx.annotations import (
    DescriptionData,
    SegmentAnnotationData,
)
from cvsx2mvsx.models.cvsx.entry import CVSXEntry


class HasColor(Protocol):
    color: Optional[tuple[float, float, float, float]]


T = TypeVar("T", bound=HasColor)


def get_hex_color(annotation: T | None) -> str | None:
    if not annotation or not annotation.color:
        return None
    r, g, b, _ = annotation.color
    return "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))


def get_opacity(annotation: T | None) -> float | None:
    if not annotation or not annotation.color:
        return None
    return annotation.color[3]


SegmentationId = tuple[str, int]


def get_segmentation_annotations(
    cvsx_file: CVSXEntry,
) -> dict[SegmentationId, SegmentAnnotationData]:
    annotations_map: dict[SegmentationId, SegmentAnnotationData] = {}
    for annotation in cvsx_file.annotations.segment_annotations:
        segmentation_id = annotation.segmentation_id
        segment_id = annotation.segment_id
        annotations_map[(segmentation_id, segment_id)] = annotation
    return annotations_map


def get_segmentation_descriptions(
    cvsx_file: CVSXEntry,
    target_kind: Literal["lattice", "mesh", "primitive"],
) -> dict[SegmentationId, list[DescriptionData]]:
    descriptions_map: dict[SegmentationId, list[DescriptionData]] = defaultdict(list)

    for desc in cvsx_file.annotations.descriptions.values():
        if desc.target_kind != target_kind or not desc.target_id:
            continue
        key = (desc.target_id.segmentation_id, desc.target_id.segment_id)
        descriptions_map[key].append(desc)

    return descriptions_map
