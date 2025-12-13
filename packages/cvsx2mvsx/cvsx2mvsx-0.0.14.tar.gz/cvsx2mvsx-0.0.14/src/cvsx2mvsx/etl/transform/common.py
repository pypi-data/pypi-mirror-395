from typing import Literal, Optional, Protocol, TypeVar

import requests

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


def get_segment_label(
    cvsx_desciptions: list[DescriptionData],
) -> str:
    return str(cvsx_desciptions[0].name)


def get_segment_tooltip(
    cvsx_desciptions: list[DescriptionData],
    segmentation_id: str,
    segment_id: int,
) -> str:
    label = get_segment_label(cvsx_desciptions)
    tooltip = f"Segmentation '{segmentation_id}' | Segment '{segment_id}'"
    tooltip += f"\n\n{label}"
    for desc in cvsx_desciptions:
        if not desc.external_references:
            continue
        for reference in desc.external_references:
            tooltip += (
                f"\n\n{reference.label} [{reference.resource}:{reference.accession}]"
            )
    return tooltip


def get_segment_description(
    cvsx_desciptions: list[DescriptionData],
    segmentation_id: str,
    segment_id: int,
) -> str:
    label = get_segment_label(cvsx_desciptions)
    tooltip = f"**Segment '{segment_id}' from segmentation '{segmentation_id}':**"
    tooltip += f"\n\n**{label}**"
    for desc in cvsx_desciptions:
        if not desc.external_references:
            continue
        for reference in desc.external_references:
            tooltip += (
                f"\n\n[{reference.resource}:{reference.accession}]({reference.url})"
            )
            tooltip += f"\n\n**{reference.label}**"
            tooltip += f"\n\n{reference.description}"
    return tooltip


def get_segmentation_descriptions(
    cvsx_entry: CVSXEntry,
    target_kind: Literal["lattice", "mesh", "primitive"],
    segmentation_id: str,
    segment_id: int,
) -> list[DescriptionData]:
    descriptions_map: list[DescriptionData] = []

    for desc in cvsx_entry.annotations.descriptions.values():
        if desc.target_kind != target_kind or not desc.target_id:
            continue
        if (
            desc.target_id.segmentation_id != segmentation_id
            or desc.target_id.segment_id != segment_id
        ):
            continue
        descriptions_map.append(desc)

    return descriptions_map


def fetch_contour_level(cvsx_entry: CVSXEntry) -> float | None:
    options = []
    if cvsx_entry.metadata.entry_id.source_db_id is not None:
        entry = cvsx_entry.metadata.entry_id.source_db_id
        options.append(entry.split("-", 1))
    elif cvsx_entry.annotations.entry_id.source_db_id is not None:
        entry = cvsx_entry.annotations.entry_id.source_db_id
        options.append(entry.split("-", 1))
    elif (
        cvsx_entry.query.entry_id is not None and cvsx_entry.query.source_db is not None
    ):
        options.append([cvsx_entry.query.source_db, cvsx_entry.query.entry_id])

    entry_id = None
    for opt in options:
        if len(opt) == 2 and opt[0] in ["emd", "emdb"]:
            entry_id = opt[1]

    try:
        url = f"https://www.ebi.ac.uk/emdb/api/entry/map/{entry_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        contours = data.get("map", {}).get("contour_list", {}).get("contour")
        if contours and len(contours) > 0:
            the_contour = next((c for c in contours if c.get("primary")), contours[0])

            if "level" not in the_contour:
                raise ValueError("EMDB API response missing contour level.")

            return float(the_contour["level"])
    except Exception:
        pass

    return None


def split_entry_id(entry: str):
    PREFIX_TO_SOURCE = {"empiar": "empiar", "emd": "emdb", "idr": "idr"}
    prefix, entry = entry.split("-", 1)
    return PREFIX_TO_SOURCE[prefix], entry
