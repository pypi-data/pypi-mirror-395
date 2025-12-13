# The Transformer imports everything
import os
import shutil
from typing import Literal

from cvsx2mvsx.etl.transform.common import (
    fetch_contour_level,
    get_hex_color,
    get_opacity,
)
from cvsx2mvsx.models.cvsx.annotations import ChannelAnnotation
from cvsx2mvsx.models.cvsx.entry import CVSXEntry
from cvsx2mvsx.models.cvsx.metadata import CVSXMetadata
from cvsx2mvsx.models.cvsx.volume import VolumeCif
from cvsx2mvsx.models.internal.volume import (
    InternalGridSliceVolume,
    InternalIsosurfaceVolume,
    InternalVolume,
)


class VolumeTransformer:
    def __init__(self, cvsx_entry: CVSXEntry, out_dir_path: str) -> None:
        self._cvsx_entry = cvsx_entry
        self._out_dir_path = out_dir_path

    def run(self) -> list[InternalVolume]:
        mvsx_volumes = []
        annotations = self._get_volume_annotations(self._cvsx_entry)

        for proxy in self._cvsx_entry.files_proxy.volumes:
            channel_id = proxy.metadata.channelId
            timeframe_id = proxy.metadata.timeframeIndex
            annotation = annotations.get(channel_id)

            color = get_hex_color(annotation)
            opacity = get_opacity(annotation)

            if color is None:
                color = "white"
            if opacity is None:
                opacity = 0.2

            volume_cif: VolumeCif = proxy.load()

            dimension_level = volume_cif.volume_block.volume_data_3d_info.sample_rate
            kind, dimension = self._classify_volume(
                metadata=self._cvsx_entry.metadata,
                channel_id=channel_id,
                downsampling_level=dimension_level,
            )

            source_filepath = f"volumes/{timeframe_id}_{channel_id}.bcif"
            fullpath = os.path.join(self._out_dir_path, source_filepath)
            dirname = os.path.dirname(fullpath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            shutil.move(proxy.filepath, fullpath)

            if not self._cvsx_entry.annotations.volume_channels_annotations:
                label = None
            else:
                x = [
                    x
                    for x in self._cvsx_entry.annotations.volume_channels_annotations
                    if x.channel_id == channel_id
                ]
                if len(x) > 0:
                    label = x[0].label
                else:
                    label = None

            absolute_isovalue = fetch_contour_level(self._cvsx_entry)

            if kind == "isosurface":
                mvsx_volume = InternalIsosurfaceVolume(
                    source_filepath=source_filepath,
                    channel_id=channel_id,
                    timeframe_id=timeframe_id,
                    color=color,
                    opacity=opacity,
                    absolute_isovalue=absolute_isovalue,
                    relative_isovalue=1,
                    show_faces=True,
                    show_wireframe=False,
                    label=label,
                    description=None,
                )
            else:
                mvsx_volume = InternalGridSliceVolume(
                    source_filepath=source_filepath,
                    channel_id=channel_id,
                    timeframe_id=timeframe_id,
                    color=color,
                    opacity=1,
                    absolute_isovalue=absolute_isovalue,
                    relative_isovalue=0,
                    dimension=dimension,
                    absolute_index=0,
                    label=label,
                    description=None,
                )

            mvsx_volumes.append(mvsx_volume)

        return mvsx_volumes

    def _get_volume_annotations(
        self, cvsx_entry: CVSXEntry
    ) -> dict[str, ChannelAnnotation]:
        if not cvsx_entry.annotations.volume_channels_annotations:
            return {}
        annotations_map = {}
        for annotation in cvsx_entry.annotations.volume_channels_annotations:
            annotations_map[annotation.channel_id] = annotation
        return annotations_map

    def _classify_volume(
        self,
        metadata: CVSXMetadata,
        channel_id: str,
        downsampling_level: int,
    ) -> (
        tuple[Literal["isosurface"], None]
        | tuple[Literal["slice"], Literal["x", "y", "z"]]
    ):
        if channel_id not in metadata.volumes.channel_ids:
            raise ValueError(
                f"Channel ID '{channel_id}' not found in volumes metadata."
            )

        box = metadata.volumes.volume_sampling_info.boxes.get(downsampling_level)
        if box is None:
            raise ValueError(
                f"Downsampling level {downsampling_level} not found in volume sampling info."
            )

        for dim_index, size in enumerate(box.grid_dimensions):
            if size == 1:
                dimension = ["x", "y", "z"][dim_index]
                return "slice", dimension

        return "isosurface", None
