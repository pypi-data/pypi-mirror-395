import json
import os

import msgpack

from cvsx2mvsx.models.internal.entry import InternalEntry
from cvsx2mvsx.models.internal.segment import InternalSegment
from cvsx2mvsx.models.internal.segmentation import (
    InternalMeshSegmentation,
    InternalVolumeSegmentation,
)
from cvsx2mvsx.models.internal.volume import InternalVolume
from cvsx2mvsx.models.mvsx.states import MVSXEntry
from cvsx2mvsx.models.stories.model import (
    SceneAsset,
    SceneData,
    Story,
    StoryContainer,
    StoryMetadata,
)


class StoriesTransformer:
    def __init__(self, internal_entry: InternalEntry) -> None:
        self._internal_entry = internal_entry

    def run(self) -> MVSXEntry:
        assets = self._collect_all_assets()
        global_code = self._get_global_code()

        scenes: list[SceneData] = []
        for timeframe in self._internal_entry.timeframes:
            scene_code = ""
            for volume in timeframe.volumes:
                scene_code += "/* Volumes */\n"
                scene_code += self.add_volume_to_scene_code(volume)
            for segmentation in timeframe.segmentations:
                scene_code += "\n/* Segmentations */\n"
                if segmentation.kind == "volume":
                    scene_code += self._add_volume_segmentation_to_scene_code(
                        segmentation
                    )
                elif segmentation.kind == "mesh":
                    scene_code += self._add_mesh_segmentation_to_scene_code(
                        segmentation
                    )
                elif segmentation.kind == "geometric":
                    scene_code += self._add_geometric_segmentation_to_scene_code(
                        segmentation
                    )
            scene = SceneData(
                id=str(timeframe.timeframe_id),
                header=f"Timeframe {timeframe.timeframe_id}",
                key=f"timeframe-{timeframe.timeframe_id}",
                description="",
                javascript=scene_code,
            )
            scenes.append(scene)

        metadata = StoryMetadata(
            title=self._internal_entry.name or "Converted Volumes & Segmentations",
        )

        story = Story(
            metadata=metadata,
            javascript=global_code,
            scenes=scenes,
            assets=assets,
        )
        return StoryContainer(story=story)

    def _collect_all_assets(self) -> list[SceneAsset]:
        assets: list[SceneAsset] = []
        for timeframe in self._internal_entry.timeframes:
            for volume in timeframe.volumes:
                assets += [self._create_volume_asset(volume)]
                for segmentation in timeframe.segmentations:
                    if segmentation.kind == "volume":
                        assets += self._create_volume_segmentation_asset(segmentation)
        return assets

    def _create_volume_asset(self, volume: InternalVolume) -> SceneAsset:
        source_filepath = os.path.join(
            self._internal_entry.assets_directory, volume.source_filepath
        )
        return SceneAsset(name=volume.source_filepath, file_path=source_filepath)

    def _create_volume_segmentation_asset(
        self,
        segmentation: InternalVolumeSegmentation,
    ) -> SceneAsset:
        assets: list[SceneAsset] = []
        for segment in segmentation.segments:
            source_filepath = os.path.join(
                self._internal_entry.assets_directory, segment.source_filepath
            )
            asset = SceneAsset(name=segment.source_filepath, file_path=source_filepath)
            assets.append(asset)

        return assets

    def _get_global_code(self) -> None:
        global_code = ""
        for timeframe in self._internal_entry.timeframes:
            for segmentation in timeframe.segmentations:
                if segmentation.kind == "mesh":
                    global_code += self._get_mesh_segmentation_code(segmentation)
        return global_code

    def _get_mesh_segmentation_code(
        self,
        segmentation: InternalMeshSegmentation,
    ) -> None:
        code = ""

        for segment in segmentation.segments:
            source_filepath = os.path.join(
                self._internal_entry.assets_directory, segment.source_filepath
            )
            with open(source_filepath, "rb") as f:
                data_dict = msgpack.unpack(f, raw=False)

            data = json.dumps(data_dict)
            variable = self._get_segment_variable_name(segment)
            code += f"""
const {variable} = {data}
"""

        return code

    def add_volume_to_scene_code(self, volume: InternalVolume) -> str:
        if volume.kind == "isosurface":
            code = f"""
// Volume "{volume.channel_id}"
builder.download({{
    url: "{volume.source_filepath}"
}}).parse({{
    format: "bcif"
}}).volume({{
    channel_id: "{volume.channel_id}"
}}).representation({{
    type: "isosurface",
    absolute_isovalue: {volume.absolute_isovalue},
    relative_isovalue: {volume.relative_isovalue},
    show_faces: {to_js_bool(volume.show_faces)},
    show_wireframe: {to_js_bool(volume.show_wireframe)},
}}).color({{
    color: "{volume.color}",
}}).opacity({{
    opacity: {volume.opacity},
}})
"""
        else:
            code = f"""
builder.download({{
    url: "{volume.source_filepath}"
}}).parse({{
    format: "bcif"
}}).volume({{
    channel_id: "{volume.channel_id}"
}}).representation({{
    type: "grid_slice",
    absolute_isovalue: {volume.absolute_isovalue},
    relative_isovalue: {volume.relative_isovalue},
    dimension: "{volume.dimension}",
    absolute_index: 0
}}).color({{
    color: "{volume.color}",
}}).opacity({{
    opacity: {volume.opacity},
}})
"""
        return code

    def _add_volume_segmentation_to_scene_code(
        self,
        segmentation: InternalVolumeSegmentation,
    ) -> str:
        code = ""
        for segment in segmentation.segments:
            code += f"""
// Volume segmentation '{segment.segmentation_id}', segment '{segment.segment_id}'
builder.download({{
    url: "{segment.source_filepath}"
}}).parse({{
    format: "bcif"
}}).volume({{
    channel_id: "{segment.channel_id}"
}}).representation({{
    type: "isosurface",
    absolute_isovalue: {segment.absolute_isovalue},
    relative_isovalue: {segment.relative_isovalue},
    show_faces: {to_js_bool(segment.show_faces)},
    show_wireframe: {to_js_bool(segment.show_wireframe)},
}}).color({{
    color: "{segment.color}",
}}).opacity({{
    opacity: {segment.opacity},
}})
"""
        return code

    def _add_mesh_segmentation_to_scene_code(
        self,
        segmentation: InternalVolumeSegmentation,
    ) -> str:
        code = ""
        for segment in segmentation.segments:
            variable = self._get_segment_variable_name(segment)
            code += f"""
// Mesh segmentation '{segment.segmentation_id}', segment '{segment.segment_id}'
builder.primitives({{
    color: "{segment.color}",
    opacity: {segment.opacity},
    tooltip: {handle_tooltip(segment.tooltip)},
    instances: [{list(segment.instance)}]
}}).mesh({{
    vertices: {variable}.vertices,
    indices: {variable}.indices,
    triangle_groups: {variable}.triangle_groups
}})
"""
        return code

    def _add_geometric_segmentation_to_scene_code(
        self,
        segmentation: InternalVolumeSegmentation,
    ) -> str:
        opacity = or_undefined(segmentation.opacity)
        code = f"""
// Geometric segmentation '{segmentation.segmentation_id}'
builder.primitives({{
    opacity: {opacity},
}})
"""
        for segment in segmentation.segments:
            code += self._add_geometric_segment_to_scene_code(segment)
        return code

    def _add_geometric_segment_to_scene_code(self, segment: InternalSegment) -> None:
        code = "// Segment '{segment.segment_id}'\n"
        if segment.kind == "mesh":
            code += f"""
.mesh({{
    vertices: {segment.vertices.ravel().tolist()},
    indices: {segment.indices.ravel().tolist()},
    triangle_groups: {segment.triangle_groups.ravel().tolist()},
    color: '{segment.color}',
    tooltip: {handle_tooltip(segment.tooltip)},
}})
"""
        elif segment.kind == "ellipsoid":
            code += f""".ellipsoid({{
    center: {list(segment.center)},
    major_axis: {list(segment.major_axis)},
    minor_axis: {list(segment.minor_axis)},
    radius: {segment.radius},
    color: '{segment.color}',
    tooltip: {handle_tooltip(segment.tooltip)},
}})
"""
        elif segment.kind == "sphere":
            code += f""".sphere({{
    center: {list(segment.center)},
    radius: {segment.radius},
    color: '{segment.color}',
    tooltip: {handle_tooltip(segment.tooltip)},
}})
"""
        elif segment.kind == "box":
            code += f""".box({{
    center: {list(segment.center)},
    extent: {list(segment.extent)},
    color: '{segment.color}',
    tooltip: {handle_tooltip(segment.tooltip)},
}})
"""
        elif segment.kind == "tube":
            code += f""".tube({{
    start: {list(segment.start)},
    end: {list(segment.end)},
    radius: {segment.radius},
    color: '{segment.color}',
    tooltip: {handle_tooltip(segment.tooltip)},
}})
"""
        return code

    def _get_segment_variable_name(self, segment: InternalSegment) -> str:
        kind = segment.kind
        t_id = segment.timeframe_id
        s_id = segment.segmentation_id
        ss_id = segment.segment_id
        return f"{kind}_{t_id}_{s_id}_{ss_id}"


def or_undefined(value: str | None) -> str:
    if value is None:
        return "undefined"
    return value


def handle_tooltip(value: str | None) -> str:
    if value is None:
        return "undefined"
    return f"`{value}`"


def to_js_bool(value: bool) -> str:
    return str(value).lower()
