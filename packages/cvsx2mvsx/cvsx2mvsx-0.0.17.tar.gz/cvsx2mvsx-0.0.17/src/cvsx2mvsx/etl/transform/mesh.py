# The Transformer imports everything
import os

import msgpack
import numpy as np

from cvsx2mvsx.etl.transform.common import (
    get_hex_color,
    get_opacity,
    get_segment_description,
    get_segment_label,
    get_segment_tooltip,
    get_segmentation_annotations,
    get_segmentation_descriptions,
)
from cvsx2mvsx.models.cvsx.entry import CVSXEntry
from cvsx2mvsx.models.cvsx.lattice import LatticeCif
from cvsx2mvsx.models.cvsx.mesh import MeshCif
from cvsx2mvsx.models.cvsx.metadata import CVSXMetadata
from cvsx2mvsx.models.internal.segment import InternalMeshSegment
from cvsx2mvsx.models.internal.segmentation import InternalMeshSegmentation


class MeshTransformer:
    def __init__(self, cvsx_entry: CVSXEntry, out_dir_path: str) -> None:
        self._cvsx_entry = cvsx_entry
        self._out_dir_path = out_dir_path

    def run(self) -> list[InternalMeshSegmentation]:
        if not self._cvsx_entry.files_proxy.mesh_segmentations:
            return []

        segmentation_annotations = get_segmentation_annotations(self._cvsx_entry)

        segments: list[InternalMeshSegment] = []
        for proxy in self._cvsx_entry.files_proxy.mesh_segmentations:
            segmentation_id = proxy.metadata.segmentationId
            timeframe_id = proxy.metadata.timeframeIndex
            segment_id = self._get_segment_id(os.path.basename(proxy.filepath))
            mesh_cif: LatticeCif = proxy.load()

            annotation = segmentation_annotations.get((segmentation_id, segment_id))
            color = get_hex_color(annotation)
            opacity = get_opacity(annotation)

            vertices, indices, triangle_groups = self.get_mesh_data(mesh_cif)

            instance = self.create_instance_matrix(mesh_cif, self._cvsx_entry.metadata)

            # save mesh results in working directory for the internal model
            source_filepath = f"segmentations/mesh/{timeframe_id}_{segmentation_id}_{segment_id}.msgpack"
            fullpath = os.path.join(self._out_dir_path, source_filepath)
            dirname = os.path.dirname(fullpath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            with open(fullpath, "wb") as f:
                msgpack.pack(
                    {
                        "vertices": vertices.ravel().tolist(),
                        "indices": indices.ravel().tolist(),
                        "triangle_groups": triangle_groups.ravel().tolist(),
                    },
                    f,
                )
            cvsx_desciptions = get_segmentation_descriptions(
                self._cvsx_entry,
                "mesh",
                segmentation_id,
                segment_id,
            )
            if len(cvsx_desciptions) == 0:
                label = None
                tooltip = None
                description = None
            else:
                label = get_segment_label(cvsx_desciptions)
                tooltip = get_segment_tooltip(
                    cvsx_desciptions,
                    segmentation_id,
                    segment_id,
                )
                description = get_segment_description(
                    cvsx_desciptions,
                    segmentation_id,
                    segment_id,
                )

            segments.append(
                InternalMeshSegment(
                    source_filepath=source_filepath,
                    timeframe_id=timeframe_id,
                    segmentation_id=segmentation_id,
                    segment_id=segment_id,
                    color=color,
                    opacity=opacity,
                    instance=instance,
                    label=label,
                    tooltip=tooltip,
                    description=description,
                )
            )

        mvsx_segmentations: list[InternalMeshSegmentation] = []
        for segmentation_id in {s.segmentation_id for s in segments}:
            mvsx_segmentation = InternalMeshSegmentation(
                timeframe_id=timeframe_id,
                segmentation_id=segmentation_id,
                segments=segments,
            )
            mvsx_segmentations.append(mvsx_segmentation)

        return mvsx_segmentations

    def _get_segment_id(self, filepath: str) -> int:
        parts = filepath.split("_")
        return int(parts[1])

    def get_mesh_segment_ids_from_metadata(
        self,
        metadata: CVSXMetadata,
        segmentation_id: str,
        timeframe_id: int,
    ) -> list[int]:
        """
        Returns the list of segment IDs for a given segmentation + timeframe,
        based on mesh metadata (not filenames).
        """
        mesh_seg_sets = metadata.segmentation_meshes
        if mesh_seg_sets is None:
            return []

        meshes_meta = mesh_seg_sets.segmentation_metadata.get(segmentation_id)
        if meshes_meta is None:
            return []

        frame = meshes_meta.mesh_timeframes.get(timeframe_id)
        if frame is None:
            return []

        return list(frame.segment_ids.keys())

    def needs_winding_flip(self, vertices, indices, num_tests=50):
        """
        Test whether triangle normals point inward.
        If most of the sampled triangles point toward the centroid,
        the winding order is reversed.
        """
        triangles = indices.reshape(-1, 3)
        centroid = vertices.mean(axis=0)

        inward_count = 0
        test_tris = triangles[: min(num_tests, len(triangles))]

        for tri in test_tris:
            a, b, c = tri
            A, B, C = vertices[a], vertices[b], vertices[c]

            normal = np.cross(B - A, C - A)  # CCW normal
            to_center = centroid - A

            # If normal points toward the inside, count it
            if np.dot(normal, to_center) > 0:
                inward_count += 1

        return inward_count > (len(test_tris) // 2)

    def get_mesh_data(
        self, mesh_cif: MeshCif
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        block = mesh_cif.mesh_block

        # Indices + triangle group ids
        indices = block.mesh_triangle.vertex_id
        triangle_groups = block.mesh_triangle.mesh_id

        # Vertex rounding (to 0.01)
        verts = np.column_stack(
            [
                np.round(block.mesh_vertex.x, 2),
                np.round(block.mesh_vertex.y, 2),
                np.round(block.mesh_vertex.z, 2),
            ]
        ).astype(np.float32)

        # Always flip winding (your original code always did `[0, 2, 1]`)
        triangles = indices.reshape(-1, 3)[:, [0, 2, 1]]

        verts_rounded = np.round(verts.astype(np.float64), 2)

        return verts_rounded, triangles, triangle_groups

    def create_instance_matrix(
        self,
        mesh_cif: MeshCif,
        cvsx_metadata: CVSXMetadata,
    ) -> list[float]:
        """Create the voxel->world transform matrix for this lattice."""
        downsampling_level = mesh_cif.mesh_block.volume_data_3d_info.sample_rate
        sampling_info = cvsx_metadata.volumes.volume_sampling_info.boxes.get(
            downsampling_level
        )
        if sampling_info is None:
            raise ValueError(f"Downsampling level {downsampling_level} not found.")

        vx, vy, vz = sampling_info.voxel_size

        matrix = np.array(
            [
                [vx, 0, 0, 0],
                [0, vy, 0, 0],
                [0, 0, vz, 0],
                [0, 0, 0, 1],
            ],
            dtype=np.float64,
        )

        # Flatten for MVS
        matrix = np.round(matrix.astype(np.float64), 2)
        instance = matrix.T.flatten().tolist()

        return instance
