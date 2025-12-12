from typing import Literal, Mapping

from pydantic import BaseModel

Vector3 = tuple[float, float, float]


class ShapePrimitiveBase(BaseModel):
    id: int


class RotationParameters(BaseModel):
    axis: Vector3
    radians: float


class SphereShape(ShapePrimitiveBase):
    kind: Literal["sphere"] = "sphere"
    center: Vector3
    radius: float


class BoxShape(ShapePrimitiveBase):
    kind: Literal["box"] = "box"
    translation: Vector3
    scaling: Vector3
    rotation: RotationParameters


class CylinderShape(ShapePrimitiveBase):
    kind: Literal["cylinder"] = "cylinder"
    start: Vector3
    end: Vector3
    radius_bottom: float
    radius_top: float


class EllipsoidShape(ShapePrimitiveBase):
    kind: Literal["ellipsoid"] = "ellipsoid"
    dir_major: Vector3
    dir_minor: Vector3
    center: Vector3
    radius_scale: Vector3


class PyramidShape(ShapePrimitiveBase):
    kind: Literal["pyramid"] = "pyramid"
    translation: Vector3
    scaling: Vector3
    rotation: RotationParameters


ShapePrimitive = SphereShape | BoxShape | CylinderShape | EllipsoidShape | PyramidShape


class ShapePrimitiveData(BaseModel):
    shape_primitive_list: list[ShapePrimitive]


class GeometricSegmentationData(BaseModel):
    segmentation_id: str
    primitives: Mapping[int, ShapePrimitiveData]
