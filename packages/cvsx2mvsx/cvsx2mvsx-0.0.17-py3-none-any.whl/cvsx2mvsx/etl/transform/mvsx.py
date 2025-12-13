import os
import shutil

import msgpack

from cvsx2mvsx.models.internal.entry import InternalEntry
from cvsx2mvsx.models.internal.segment import InternalSegment
from cvsx2mvsx.models.internal.segmentation import (
    InternalGeometricSegmentation,
    InternalMeshSegmentation,
    InternalSegmentation,
    InternalVolumeSegmentation,
)
from cvsx2mvsx.models.internal.volume import InternalVolume
from cvsx2mvsx.models.mvsx.states import MVSXEntry
from cvsx2mvsx.molviewspec.builder import Primitives, Root, create_builder
from cvsx2mvsx.molviewspec.nodes import GlobalMetadata, Snapshot, States


class MVSXTransformer:
    def __init__(self, internal_entry: InternalEntry, out_dir_path: str) -> None:
        self._internal_entry = internal_entry
        self._out_dir_path = out_dir_path

    def run(self) -> MVSXEntry:
        self._write_assets()

        snapshots: list[Snapshot] = []
        for timeframe in self._internal_entry.timeframes:
            builder = create_builder()
            for volume in timeframe.volumes:
                self.add_volume_to_mvs(builder, volume)
            for segmentation in timeframe.segmentations:
                self.add_segmentation_to_mvs(builder, segmentation)
            snapshot = builder.get_snapshot(
                title=f"Timeframe: {timeframe.timeframe_id}",
            )
            snapshots.append(snapshot)

        states = States(
            metadata=GlobalMetadata(),
            snapshots=snapshots,
        )

        return MVSXEntry(
            states=states,
            asset_dir=self._out_dir_path,
        )

    def _write_assets(self):
        """Extracts binary data from source and writes to temp destination."""
        for timeframe in self._internal_entry.timeframes:
            for volume in timeframe.volumes:
                self.save_volume(volume)
            for segmentation in timeframe.segmentations:
                if segmentation.kind == "volume":
                    self.save_volume_segmentation(segmentation)
                elif segmentation.kind == "mesh":
                    self.save_mesh_segmentation(segmentation)
                elif segmentation.kind == "geometric":
                    self.save_geometric_segmentation(segmentation)

    def save_volume(self, volume: InternalVolume) -> None:
        source_filepath = os.path.join(
            self._internal_entry.assets_directory, volume.source_filepath
        )
        destination_filepath = os.path.join(self._out_dir_path, volume.source_filepath)
        dirname = os.path.dirname(destination_filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        shutil.move(source_filepath, destination_filepath)

    def save_volume_segmentation(
        self,
        segmentation: InternalVolumeSegmentation,
    ) -> None:
        for segment in segmentation.segments:
            source_filepath = os.path.join(
                self._internal_entry.assets_directory, segment.source_filepath
            )
            destination_filepath = os.path.join(
                self._out_dir_path, segment.source_filepath
            )
            dirname = os.path.dirname(destination_filepath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            shutil.move(source_filepath, destination_filepath)

    def save_mesh_segmentation(self, segmentation: InternalMeshSegmentation) -> None:
        for segment in segmentation.segments:
            primitives = Root().primitives(
                color=segment.color,
                opacity=segment.opacity,
                tooltip=segment.tooltip,
                instances=[segment.instance],
            )

            source_filepath = os.path.join(
                self._internal_entry.assets_directory, segment.source_filepath
            )

            with open(source_filepath, "rb") as f:
                data = msgpack.unpack(f, raw=False)

            primitives.mesh(
                vertices=data["vertices"],
                indices=data["indices"],
                triangle_groups=data["triangle_groups"],
            )

            destination_filepath = os.path.join(
                self._out_dir_path, segment.source_filepath
            )
            dirname = os.path.dirname(destination_filepath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            with open(destination_filepath, "w") as f:
                data = primitives._node.model_dump_json(exclude_none=True)
                f.write(data)

    def save_geometric_segmentation(
        self, segmentation: InternalGeometricSegmentation
    ) -> None:
        primitives = Root().primitives(
            opacity=segmentation.opacity,
        )
        for segment in segmentation.segments:
            self.add_geometric_primitive(primitives, segment)

        destination_filepath = os.path.join(
            self._out_dir_path, segmentation.source_filepath
        )
        dirname = os.path.dirname(destination_filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        with open(destination_filepath, "w") as f:
            data = primitives._node.model_dump_json(exclude_none=True)
            f.write(data)

    def add_volume_to_mvs(self, root: Root, volume: InternalVolume) -> None:
        volume_raw = root.download(url=volume.source_filepath)
        volume_cif = volume_raw.parse(format="bcif")
        volume_data = volume_cif.volume(channel_id=volume.channel_id)

        if volume.kind == "isosurface":
            volume_representation = volume_data.representation(
                type="isosurface",
                absolute_isovalue=volume.absolute_isovalue,
                relative_isovalue=volume.relative_isovalue,
                show_faces=volume.show_faces,
                show_wireframe=volume.show_wireframe,
            )
        else:
            volume_representation = volume_data.representation(
                type="grid_slice",
                absolute_isovalue=volume.absolute_isovalue,
                relative_isovalue=volume.relative_isovalue,
                dimension=volume.dimension,
                absolute_index=0,
            )

        volume_representation.color(color=volume.color)
        volume_representation.opacity(opacity=volume.opacity)

    def add_segmentation_to_mvs(
        self, root: Root, segmentation: InternalSegmentation
    ) -> None:
        if segmentation.kind == "volume":
            for segment in segmentation.segments:
                download = root.download(url=segment.source_filepath)
                parse = download.parse(format="bcif")
                volume = parse.volume(channel_id=segment.channel_id)
                volume_representation = volume.representation(
                    type="isosurface",
                    absolute_isovalue=segment.absolute_isovalue,
                    relative_isovalue=segment.relative_isovalue,
                    show_faces=segment.show_faces,
                    show_wireframe=segment.show_wireframe,
                )
                volume_representation.color(color=segment.color)
                volume_representation.opacity(opacity=segment.opacity)
        elif segmentation.kind == "mesh":
            for segment in segmentation.segments:
                root.primitives_from_uri(uri=segment.source_filepath)
        elif segmentation.kind == "geometric":
            root.primitives_from_uri(uri=segmentation.source_filepath)

    def add_geometric_primitive(
        self, primitives: Primitives, segment: InternalSegment
    ) -> None:
        if segment.kind == "mesh":
            primitives.mesh(
                vertices=segment.vertices.ravel().tolist(),
                indices=segment.indices.ravel().tolist(),
                triangle_groups=segment.triangle_groups.ravel().tolist(),
                color=segment.color,
                tooltip=segment.tooltip,
            )
        elif segment.kind == "ellipsoid":
            primitives.ellipsoid(
                center=segment.center,
                major_axis=segment.major_axis,
                minor_axis=segment.minor_axis,
                radius=segment.radius,
                color=segment.color,
                tooltip=segment.tooltip,
            )
        elif segment.kind == "sphere":
            primitives.sphere(
                center=segment.center,
                radius=segment.radius,
                color=segment.color,
                tooltip=segment.tooltip,
            )
        elif segment.kind == "box":
            primitives.box(
                center=segment.center,
                extent=segment.extent,
                color=segment.color,
                tooltip=segment.tooltip,
            )
        elif segment.kind == "tube":
            primitives.tube(
                start=segment.start,
                end=segment.end,
                radius=segment.radius,
                color=segment.color,
                tooltip=segment.tooltip,
            )
