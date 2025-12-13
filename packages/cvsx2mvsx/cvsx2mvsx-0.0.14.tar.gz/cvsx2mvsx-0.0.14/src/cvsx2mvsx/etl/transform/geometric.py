# Updated Import Path

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
from cvsx2mvsx.models.cvsx.geometric import (
    BoxShape,
    CylinderShape,
    EllipsoidShape,
    PyramidShape,
    ShapePrimitiveData,
    SphereShape,
    Vector3,
)
from cvsx2mvsx.models.internal.segment import (
    InternalBaseSegment,
    InternalBoxSegment,
    InternalEllipsoidSegment,
    InternalGeometricSegment,
    InternalMeshSegment,
    InternalSphereSegment,
    InternalTubeSegment,
)
from cvsx2mvsx.models.internal.segmentation import InternalGeometricSegmentation


class GeometricTransformer:
    def __init__(self, cvsx_entry: CVSXEntry, out_dir_path: str) -> None:
        self._cvsx_entry = cvsx_entry
        self._out_dir_path = out_dir_path

    def run(self) -> list[InternalGeometricSegmentation]:
        if not self._cvsx_entry.index.geometricSegmentations:
            return []

        segmentation_annotations = get_segmentation_annotations(self._cvsx_entry)

        mvsx_segmentations: list[InternalGeometricSegmentation] = []

        for proxy in self._cvsx_entry.files_proxy.geometric_segmentations:
            segmentation_id = proxy.metadata.segmentationId
            timeframe_id = proxy.metadata.timeframeIndex
            shape_data: ShapePrimitiveData = proxy.load()

            mvsx_segments: list[InternalGeometricSegment] = []
            for shape in shape_data.shape_primitive_list:
                segment_id = shape.id

                annotation = segmentation_annotations.get((segmentation_id, segment_id))

                color = get_hex_color(annotation)
                opacity = get_opacity(annotation)

                if color is None:
                    color = "white"
                if opacity is None:
                    opacity = 1

                cvsx_desciptions = get_segmentation_descriptions(
                    self._cvsx_entry,
                    "primitive",
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

                segmentation_base = InternalBaseSegment(
                    timeframe_id=timeframe_id,
                    segmentation_id=segmentation_id,
                    segment_id=segment_id,
                    color=color,
                    opacity=opacity,
                    label=label,
                    tooltip=tooltip,
                    description=description,
                )

                if shape.kind == "box":
                    mvsx_segment = self.create_box(segmentation_base, shape)
                elif shape.kind == "sphere":
                    mvsx_segment = self.create_sphere(segmentation_base, shape)
                elif shape.kind == "cylinder":
                    mvsx_segment = self.create_cylinder(segmentation_base, shape)
                elif shape.kind == "ellipsoid":
                    mvsx_segment = self.create_ellipsoid(segmentation_base, shape)
                elif shape.kind == "pyramid":
                    mvsx_segment = self.create_pyramid(segmentation_base, shape)

                mvsx_segments.append(mvsx_segment)

            source_filepath = (
                f"segmentations/geometric/{timeframe_id}_{segmentation_id}.json"
            )

            mvsx_segmentation = InternalGeometricSegmentation(
                source_filepath=source_filepath,
                timeframe_id=timeframe_id,
                segmentation_id=segmentation_id,
                segments=mvsx_segments,
            )
            mvsx_segmentations.append(mvsx_segmentation)

        return mvsx_segmentations

    def axis_angle_to_rotation_matrix(self, axis: Vector3, angle: float) -> np.ndarray:
        axis = np.array(axis)
        axis = axis / np.linalg.norm(axis)  # Normalize

        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        K = np.array(
            [[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]]
        )
        rotation_matrix = np.eye(3) + sin_angle * K + (1 - cos_angle) * np.dot(K, K)
        return rotation_matrix

    def create_transform_matrix(
        self,
        rotation_matrix: np.ndarray,
        translation: Vector3,
    ) -> np.ndarray:
        transform_matrix = np.eye(4)
        transform_matrix[:3, :3] = rotation_matrix
        transform_matrix[:3, 3] = translation
        return transform_matrix

    def create_box(
        self,
        segmentation_base: InternalBaseSegment,
        shape: BoxShape,
    ):
        center = (0, 0, 0)
        extent = tuple(s / 2 for s in shape.scaling)

        return InternalBoxSegment(
            **segmentation_base.model_dump(),
            center=center,
            extent=extent,
        )

    def create_sphere(
        self,
        segmentation_base: InternalBaseSegment,
        shape: SphereShape,
    ):
        return InternalSphereSegment(
            **segmentation_base.model_dump(),
            center=shape.center,
            radius=shape.radius,
        )

    def generate_cylinder_mesh(
        self,
        start: Vector3,
        end: Vector3,
        radius_bottom: float,
        radius_top: float,
        num_segments: int = 32,
    ) -> tuple[list[float], list[int]]:
        start = np.array(start)
        end = np.array(end)

        direction = end - start
        height = np.linalg.norm(direction)
        direction = direction / height

        vertices = []
        indices = []

        # Generate circle points for bottom and top
        angles = np.linspace(0, 2 * np.pi, num_segments, endpoint=False)

        # Find perpendicular vectors for circle generation
        if abs(direction[2]) < 0.9:
            perp1 = np.cross(direction, [0, 0, 1])
        else:
            perp1 = np.cross(direction, [1, 0, 0])
        perp1 = perp1 / np.linalg.norm(perp1)
        perp2 = np.cross(direction, perp1)

        # Bottom circle vertices
        for angle in angles:
            x = start + (perp1 * np.cos(angle) + perp2 * np.sin(angle)) * radius_bottom
            vertices.extend(x.tolist())

        # Top circle vertices
        for angle in angles:
            x = end + (perp1 * np.cos(angle) + perp2 * np.sin(angle)) * radius_top
            vertices.extend(x.tolist())

        # Add center points for caps
        bottom_center_idx = len(vertices) // 3
        vertices.extend(start.tolist())
        top_center_idx = len(vertices) // 3
        vertices.extend(end.tolist())

        # Create triangles for sides
        for i in range(num_segments):
            next_i = (i + 1) % num_segments
            # Two triangles per segment
            indices.extend([i, next_i, i + num_segments])
            indices.extend([next_i, next_i + num_segments, i + num_segments])

        # Bottom cap
        for i in range(num_segments):
            next_i = (i + 1) % num_segments
            indices.extend([bottom_center_idx, next_i, i])

        # Top cap
        for i in range(num_segments):
            next_i = (i + 1) % num_segments
            indices.extend([top_center_idx, i + num_segments, next_i + num_segments])

        triangle_groups = [0] * len(vertices)

        vertices = np.round(vertices.astype(np.float64), 2)

        return vertices, indices, triangle_groups

    def create_cylinder(
        self,
        segmentation_base: InternalBaseSegment,
        shape: CylinderShape,
    ):
        start = np.array(shape.start)
        end = np.array(shape.end)
        radius_bottom = shape.radius_bottom
        radius_top = shape.radius_top

        # Uniform cylinder - use tube
        if np.isclose(radius_bottom, radius_top):
            return InternalTubeSegment(
                **segmentation_base.model_dump(),
                start=tuple(start),
                end=tuple(end),
                radius=radius_bottom,
            )

        # Tapered cylinder (cone/frustum) - create custom mesh
        vertices, indices, triangle_groups = self.generate_cylinder_mesh(
            shape.start,
            shape.end,
            radius_bottom,
            radius_top,
        )

        return InternalMeshSegment(
            **segmentation_base.model_dump(),
            vertices=vertices,
            indices=indices,
            triangle_groups=triangle_groups,
        )

    def create_ellipsoid(
        self,
        segmentation_base: InternalBaseSegment,
        shape: EllipsoidShape,
    ):
        return InternalEllipsoidSegment(
            **segmentation_base.model_dump(),
            center=shape.center,
            major_axis=shape.dir_major,
            minor_axis=shape.dir_minor,
            radius=shape.radius_scale,
        )

    def generate_pyramid_mesh(
        self,
        translation: Vector3,
        scaling: Vector3,
        rotation_axis: Vector3,
        rotation_angle: float,
    ) -> tuple[list[float], list[int]]:
        translation = np.array(translation)
        scaling = np.array(scaling)

        # Create rotation matrix
        rotation_matrix = self.axis_angle_to_rotation_matrix(
            rotation_axis, rotation_angle
        )

        # Define pyramid vertices (apex at top, square base at bottom)
        base_verts = np.array(
            [
                [-0.5, -0.5, 0],
                [0.5, -0.5, 0],
                [0.5, 0.5, 0],
                [-0.5, 0.5, 0],
            ]
        )
        apex = np.array([[0, 0, 1]])

        # Apply scaling
        pyramid_verts = np.vstack([base_verts, apex]) * scaling

        # Apply rotation and translation
        pyramid_verts = (rotation_matrix @ pyramid_verts.T).T + translation

        # Create triangular faces with correct winding order (counter-clockwise from outside)
        indices = [
            # Base (2 triangles) - looking from below, counter-clockwise
            0,
            2,
            1,
            0,
            3,
            2,
            # Sides (4 triangles) - looking from outside, counter-clockwise
            0,
            1,
            4,
            1,
            2,
            4,
            2,
            3,
            4,
            3,
            0,
            4,
        ]

        pyramid_verts = np.round(pyramid_verts.astype(np.float64), 2)

        vertices = pyramid_verts.flatten().tolist()
        triangle_groups = [0] * len(vertices)

        return vertices, indices, triangle_groups

    def create_pyramid(
        self,
        segmentation_base: InternalBaseSegment,
        shape: PyramidShape,
    ):
        vertices, indices, triangle_groups = self.generate_pyramid_mesh(
            shape.translation,
            shape.scaling,
            shape.rotation.axis,
            shape.rotation.radians,
        )

        return InternalMeshSegment(
            **segmentation_base.model_dump(),
            vertices=vertices,
            indices=indices,
            triangle_groups=triangle_groups,
        )
