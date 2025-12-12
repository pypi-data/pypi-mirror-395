import json
import os

import numpy as np
from skimage.measure import marching_cubes

from cvsx2mvsx.etl.transform.common import (
    get_hex_color,
    get_opacity,
    get_segmentation_annotations,
)
from cvsx2mvsx.models.cvsx.entry import CVSXEntry
from cvsx2mvsx.models.cvsx.lattice import LatticeCif
from cvsx2mvsx.models.internal.segment import InternalMeshSegment
from cvsx2mvsx.models.internal.segmentation import InternalMeshSegmentation


def find_objects(
    array: np.ndarray, max_label: int = 0
) -> list[tuple[slice, ...] | None]:
    """
    Pure NumPy implementation of scipy.ndimage.find_objects.
    Finds the bounding box of each labeled object in the array.
    """
    if max_label == 0:
        max_label = array.max()

    # Initialize result list with None
    objects = [None] * max_label

    # 1. Find coordinates of all non-zero pixels
    coords = np.nonzero(array)

    if len(coords[0]) == 0:
        return objects

    # 2. Get the label values at these coordinates
    values = array[coords]

    # 3. Sort indices by label value to group them
    # This allows processing one label at a time without rescanning the array
    sort_idx = np.argsort(values)
    sorted_values = values[sort_idx]

    # 4. Find where labels change in the sorted array
    unique_labels, split_indices = np.unique(sorted_values, return_index=True)

    ndim = array.ndim

    # 5. Iterate over unique labels found
    for i, label in enumerate(unique_labels):
        if label == 0:
            continue  # find_objects ignores 0 (background)

        if label > max_label:
            continue

        # Determine the range of indices in `coords` that belong to this label
        start_idx = split_indices[i]
        end_idx = (
            split_indices[i + 1] if i + 1 < len(split_indices) else len(sorted_values)
        )

        # Get the subset of sorting indices for this label
        group_indices = sort_idx[start_idx:end_idx]

        # Build the slice tuple for this label (min to max+1)
        slices = []
        for dim in range(ndim):
            dim_coords = coords[dim][group_indices]
            slices.append(slice(dim_coords.min(), dim_coords.max() + 1))

        objects[label - 1] = tuple(slices)

    return objects


def smooth_3d_volume_integer(volume: np.ndarray, iterations: int = 1) -> np.ndarray:
    """
    Integer-weighted smoothing.
    (Same efficient implementation as before)
    """
    if iterations <= 0:
        return volume

    current = volume.astype(np.uint16)
    scratch = np.zeros_like(current)

    for _ in range(iterations):
        padded = np.pad(current, pad_width=1, mode="edge")
        np.multiply(padded[1:-1, 1:-1, 1:-1], 2, out=scratch)
        scratch += padded[2:, 1:-1, 1:-1]
        scratch += padded[:-2, 1:-1, 1:-1]
        scratch += padded[1:-1, 2:, 1:-1]
        scratch += padded[1:-1, :-2, 1:-1]
        scratch += padded[1:-1, 1:-1, 2:]
        scratch += padded[1:-1, 1:-1, :-2]
        scratch += 4
        scratch //= 8
        current[:] = scratch

    return current.astype(np.uint8)


class LatticeTransformer:
    def __init__(
        self,
        cvsx_entry: CVSXEntry,
        out_dir_path: str,
        lattice_to_mesh: bool,
    ) -> None:
        self._cvsx_entry = cvsx_entry
        self._out_dir_path = out_dir_path
        self._lattice_to_mesh = lattice_to_mesh

    def run(self) -> list[InternalMeshSegmentation]:
        if not self._cvsx_entry.index.latticeSegmentations:
            return []

        mvsx_segmentations: list[InternalMeshSegmentation] = []
        segmentation_annotations = get_segmentation_annotations(self._cvsx_entry)

        for proxy in self._cvsx_entry.files_proxy.lattice_segmentations:
            segmentation_id = proxy.metadata.segmentationId
            timeframe_id = proxy.metadata.timeframeIndex
            lattice_cif: LatticeCif = proxy.load()

            # 1. Load the full volume ONCE (keep as integer type)
            full_volume_data = self._reshape_cif_to_xyz(
                lattice_cif.segmentation_block.segmentation_data_3d.values,
                lattice_cif.segmentation_block.volume_data_3d_info,
            )

            # 2. Find Bounding Boxes
            # find_objects returns a list of slices corresponding to values 1, 2, 3...
            # This scans the volume only ONCE to find where every segment lives.
            # Convert to float64/int32 explicitly if needed, but find_objects handles ints well.
            # Note: Max segment_id determines the size of this list.
            max_id = int(np.max(full_volume_data))
            slices = find_objects(full_volume_data, max_label=max_id)

            segment_ids = set(
                lattice_cif.segmentation_block.segmentation_data_table.segment_id
            )

            mvsx_segments: dict[int, InternalMeshSegment] = {}
            instance = self.create_instance_matrix(
                lattice_cif, self._cvsx_entry.metadata
            )

            for segment_id in segment_ids:
                if segment_id == 0:
                    continue

                # Get the slice for this specific segment
                # find_objects returns None if the ID is missing, or a tuple of slices
                # The list is 0-indexed, so ID 1 is at index 0
                obj_slice = (
                    slices[segment_id - 1] if (segment_id - 1) < len(slices) else None
                )

                if obj_slice is None:
                    continue  # Segment ID defined in table but not present in volume data

                annotation = segmentation_annotations.get((segmentation_id, segment_id))
                self._validate_annotation(
                    annotation, timeframe_id, segment_id, segmentation_id
                )

                color = get_hex_color(annotation)
                opacity = get_opacity(annotation)

                # 3. Process ONLY the cropped sub-volume
                vertices, indices, triangle_groups = self.get_mesh_data_cropped(
                    full_volume_data, segment_id, obj_slice
                )

                # If no vertices generated (e.g. segment too small/deleted by smoothing), skip
                if len(vertices) == 0:
                    continue

                # save mesh results in working directory for the internal model
                source_filepath = f"segmentations/lattice/{timeframe_id}_{segmentation_id}_{segment_id}.json"
                fullpath = os.path.join(self._out_dir_path, source_filepath)
                dirname = os.path.dirname(fullpath)
                if dirname:
                    os.makedirs(dirname, exist_ok=True)
                with open(fullpath, "w") as f:
                    data = json.dumps(
                        {
                            "vertices": vertices.ravel().tolist(),
                            "indices": indices.ravel().tolist(),
                            "triangle_groups": triangle_groups.ravel().tolist(),
                        },
                    )
                    f.write(data)

                mvsx_segment = InternalMeshSegment(
                    source_filepath=source_filepath,
                    timeframe_id=timeframe_id,
                    segmentation_id=segmentation_id,
                    segment_id=segment_id,
                    color=color,
                    opacity=opacity,
                    instance=instance,
                )
                mvsx_segments[segment_id] = mvsx_segment

            del full_volume_data
            del lattice_cif
            del slices

            mvsx_segmentation = InternalMeshSegmentation(
                timeframe_id=timeframe_id,
                segmentation_id=segmentation_id,
                segments=mvsx_segments,
            )
            mvsx_segmentations.append(mvsx_segmentation)

        return mvsx_segmentations

    def _reshape_cif_to_xyz(self, values, info):
        nx, ny, nz = info.sample_count_0, info.sample_count_1, info.sample_count_2
        # Keep native type (int)
        arr = np.asarray(values).reshape((nz, ny, nx))
        return arr.transpose((2, 1, 0))

    def get_mesh_data_cropped(
        self,
        full_data: np.ndarray,
        segment_id: int,
        obj_slice: tuple[slice, slice, slice],
        smooth_iterations: int = 1,
    ):
        """
        Extracts a tiny sub-volume, processes it, and adds the offset back.
        """
        # 1. Extract the sub-volume (View, no copy yet)
        cropped_view = full_data[obj_slice]

        # 2. Create Binary Mask (Copy, but TINY)
        #    Only size of the segment bounding box, not the whole world
        mask = (cropped_view == segment_id).astype(np.uint8) * 255

        # 3. Smooth (Tiny operation)
        if smooth_iterations and smooth_iterations > 0:
            mask = smooth_3d_volume_integer(mask, iterations=smooth_iterations)

        # 4. Pad (Tiny operation)
        padded_mask = np.pad(mask, 1, mode="constant")

        # 5. Marching Cubes
        try:
            verts, faces, *_ = marching_cubes(padded_mask, level=128)
        except (RuntimeError, ValueError):
            # Can happen if smoothing erodes the entire object
            return np.array([]), np.array([]), np.array([])

        # 6. Apply Offsets
        # Marching cubes output is relative to the padded_mask (0,0,0)

        # Subtract padding offset (-1)
        verts -= 1

        # Add Bounding Box offset
        # slice.start is the coordinate in the full volume where this chunk begins
        offset_x = obj_slice[0].start
        offset_y = obj_slice[1].start
        offset_z = obj_slice[2].start

        verts[:, 0] += offset_x
        verts[:, 1] += offset_y
        verts[:, 2] += offset_z

        # Round vertices
        verts_rounded = np.round(verts.astype(np.float64), 2)
        faces = faces[:, ::-1]  # Invert winding
        triangle_groups = np.zeros(len(faces), dtype=np.int32)

        return verts_rounded, faces, triangle_groups

    def create_instance_matrix(self, lattice_cif, cvsx_metadata) -> list[float]:
        # (Same as before)
        downsampling_level = (
            lattice_cif.segmentation_block.volume_data_3d_info.sample_rate
        )
        sampling_info = cvsx_metadata.volumes.volume_sampling_info.boxes.get(
            downsampling_level
        )
        if sampling_info is None:
            raise ValueError(f"Downsampling level {downsampling_level} not found.")

        vx, vy, vz = sampling_info.voxel_size
        ox, oy, oz = sampling_info.origin

        # Padding offset:
        # Since we handle padding locally in get_mesh_data_cropped and subtract it,
        # we do NOT need to adjust the instance matrix for padding anymore.
        # BUT: The original coordinate system logic in your file used -1.
        # Let's keep the transform simple:
        # The vertices are now in "Voxel Coordinates".
        # The matrix should purely transform Voxel -> World.

        # NOTE: Your previous logic had `px, py, pz = -1, -1, -1`.
        # Since I subtracted the padding manually in `verts -= 1.0` above,
        # We can set padding offsets to 0 here for clarity, OR keep it consistent.
        # Let's verify:
        # Old: Marching cubes returns coordinates shifted by +1 (due to padding). Matrix shifts by -1. Net = 0.
        # New: I explicitly did `verts -= 1.0`. So vertices are at net 0. Matrix should NOT shift by -1.

        px, py, pz = 0, 0, 0  # <--- CHANGED from -1

        matrix = np.array(
            [
                [vx, 0, 0, ox + vx * px],
                [0, vy, 0, oy + vy * py],
                [0, 0, vz, oz + vz * pz],
                [0, 0, 0, 1],
            ],
            dtype=np.float64,
        )

        matrix = np.round(matrix.astype(np.float64), 2)
        instance = matrix.T.flatten().tolist()
        return instance

    def _validate_annotation(
        self, annotation, timeframe_id, segment_id, segmentation_id
    ):
        """Ensure annotation matches lattice/timeframe; keep errors local."""
        if not annotation:
            return

        assert annotation.segment_kind == "lattice"
        assert annotation.segment_id == segment_id
        assert annotation.segmentation_id == segmentation_id

        t = annotation.time
        if isinstance(t, int):
            assert t == timeframe_id
        elif isinstance(t, list):
            if all(isinstance(x, int) for x in t):
                assert timeframe_id in t
            elif all(
                isinstance(x, tuple)
                and len(x) == 2
                and all(isinstance(i, int) for i in x)
                for x in t
            ):
                assert any(start <= timeframe_id <= end for start, end in t)
            else:
                raise TypeError("annotation.time list contains unsupported types")
        else:
            raise TypeError("annotation.time must be int or list")
