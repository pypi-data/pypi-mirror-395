from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Dict, Mapping, Optional, Tuple, Type

from google.protobuf.descriptor import Descriptor, FieldDescriptor
from pydantic import BaseModel, create_model

from . import av_schema_pb2 as schema_pb

PRIMITIVE_TYPE_MAP: Dict[int, type[Any]] = {
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SFIXED32: int,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_FIXED32: int,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_SINT64: int,
    FieldDescriptor.TYPE_SFIXED64: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_FIXED64: int,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_BYTES: bytes,
    FieldDescriptor.TYPE_ENUM: int,
}


@dataclass
class _ModelCache:
    models: Dict[str, Type[BaseModel]] = field(default_factory=dict)
    nested: Dict[str, Type[BaseModel]] = field(default_factory=dict)


_CACHE = _ModelCache()


def _is_timestamp_message(desc: Descriptor) -> bool:
    return desc.full_name == "google.protobuf.Timestamp"


def _python_type_for_field(field: FieldDescriptor) -> type[Any]:
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        if _is_timestamp_message(field.message_type):
            return int
        return _build_model(field.message_type)
    primitive = PRIMITIVE_TYPE_MAP.get(field.type)
    if primitive is None:
        raise TypeError(f"Unsupported field type {field.type} in {field.full_name}")
    return primitive


def _build_field_annotation(field: FieldDescriptor) -> Tuple[type[Any], Any]:
    base_type = _python_type_for_field(field)
    nullable_type = Optional[base_type]  # type: ignore[valid-type]
    if field.label == FieldDescriptor.LABEL_REPEATED:
        return Optional[list[base_type]], None  # type: ignore[valid-type]
    return nullable_type, None


def _build_model(desc: Descriptor) -> Type[BaseModel]:
    if desc.full_name in _CACHE.models:
        return _CACHE.models[desc.full_name]

    fields: Dict[str, Tuple[type[Any], Any]] = {}
    for field in desc.fields:
        annotation, default = _build_field_annotation(field)
        fields[field.name] = (annotation, default if default is not None else None)

    model = create_model(desc.name, **fields)  # type: ignore[arg-type]
    _CACHE.models[desc.full_name] = model
    _CACHE.nested[desc.full_name] = model
    return model


@lru_cache(maxsize=None)
def get_dataset_pydantic_models() -> Dict[str, Type[BaseModel]]:
    descriptors: Dict[str, Descriptor] = {
        "Camera": schema_pb.Camera.DESCRIPTOR,
        "Lidar": schema_pb.Lidar.DESCRIPTOR,
        "Imu": schema_pb.Imu.DESCRIPTOR,
        "Gnss": schema_pb.Gnss.DESCRIPTOR,
        "WheelOdometry": schema_pb.WheelOdometry.DESCRIPTOR,
        "VehicleState": schema_pb.VehicleState.DESCRIPTOR,
        "Pose": schema_pb.Pose.DESCRIPTOR,
        "Summary": schema_pb.Summary.DESCRIPTOR,
        "CameraLabels": schema_pb.CameraLabels.DESCRIPTOR,
        "LidarLabels": schema_pb.LidarLabels.DESCRIPTOR,
        "LaserMap": schema_pb.LaserMap.DESCRIPTOR,
        "PathPoint": schema_pb.PathPoint.DESCRIPTOR,
        "Transform": schema_pb.Transform.DESCRIPTOR,
        "Radar": schema_pb.Radar.DESCRIPTOR,
        "MiscData": schema_pb.MiscData.DESCRIPTOR,
    }

    return {name: _build_model(desc) for name, desc in descriptors.items()}


def get_dataset_typed_dicts() -> Dict[str, Type[Any]]:
    return {name: model for name, model in get_dataset_pydantic_models().items()}


def get_nested_models() -> Dict[str, Type[BaseModel]]:
    get_dataset_pydantic_models()
    return dict(_CACHE.nested)


def build_dataset_row(name: str, values: Mapping[str, Any]) -> BaseModel:
    models = get_dataset_pydantic_models()
    if name not in models:
        raise KeyError(f"Unknown dataset name: {name}")
    return models[name](**values)
