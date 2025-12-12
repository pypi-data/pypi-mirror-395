from __future__ import annotations

import pyarrow as pa
from google.protobuf.descriptor import Descriptor, FieldDescriptor  # type: ignore

from . import av_schema_pb2 as pb

_SCALAR_TYPE_MAP = {
    FieldDescriptor.TYPE_BOOL: pa.bool_(),
    FieldDescriptor.TYPE_INT32: pa.int32(),
    FieldDescriptor.TYPE_INT64: pa.int64(),
    FieldDescriptor.TYPE_UINT32: pa.int32(),
    FieldDescriptor.TYPE_UINT64: pa.uint64(),
    FieldDescriptor.TYPE_SINT32: pa.int32(),
    FieldDescriptor.TYPE_SINT64: pa.int64(),
    FieldDescriptor.TYPE_FLOAT: pa.float32(),
    FieldDescriptor.TYPE_DOUBLE: pa.float64(),
    FieldDescriptor.TYPE_STRING: pa.string(),
    FieldDescriptor.TYPE_BYTES: pa.binary(),
    FieldDescriptor.TYPE_ENUM: pa.int32(),  # Enums are stored as int32
}


def _is_timestamp(descriptor: Descriptor) -> bool:
    return descriptor.full_name in ("google.protobuf.Timestamp",)


def _field_to_arrow(field: FieldDescriptor) -> pa.Field:
    # Nullability policy:
    # - message fields: nullable=True (nested structs are optional)
    # - repeated fields: nullable=True (lists may be missing)
    # - scalar fields: nullable=True (0 is meaningful; null is distinct)
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        msg = field.message_type
        if _is_timestamp(msg):
            dtype = pa.timestamp("us")
            # Match original PyArrow defaults (nullable unless specified)
            return pa.field(field.name, dtype, nullable=True)
        # nested struct
        dtype = _message_to_struct(msg)
        nullable = True
        if field.label == FieldDescriptor.LABEL_REPEATED:
            return pa.field(field.name, pa.list_(dtype), nullable=True)
        return pa.field(field.name, dtype, nullable=nullable)

    # scalar or bytes/string
    dtype = _SCALAR_TYPE_MAP.get(field.type)
    if dtype is None:
        raise TypeError(f"Unsupported proto field type: {field.type} ({field.name})")
    if field.label == FieldDescriptor.LABEL_REPEATED:
        return pa.field(field.name, pa.list_(dtype), nullable=True)
    return pa.field(field.name, dtype, nullable=True)


def _message_to_struct(desc: Descriptor) -> pa.DataType:
    fields = [_field_to_arrow(f) for f in desc.fields]
    return pa.struct(fields)


def message_to_schema(desc: Descriptor) -> pa.Schema:
    return pa.schema([_field_to_arrow(f) for f in desc.fields])


def camera_schema() -> pa.Schema:
    return message_to_schema(pb.Camera.DESCRIPTOR)


def lidar_schema() -> pa.Schema:
    return message_to_schema(pb.Lidar.DESCRIPTOR)


def imu_schema() -> pa.Schema:
    return message_to_schema(pb.Imu.DESCRIPTOR)


def gnss_schema() -> pa.Schema:
    return message_to_schema(pb.Gnss.DESCRIPTOR)


def wheel_odometry_schema() -> pa.Schema:
    return message_to_schema(pb.WheelOdometry.DESCRIPTOR)


def vehicle_state_schema() -> pa.Schema:
    return message_to_schema(pb.VehicleState.DESCRIPTOR)


def pose_schema() -> pa.Schema:
    return message_to_schema(pb.Pose.DESCRIPTOR)


def odd_schema() -> pa.Schema:
    return message_to_schema(pb.Odd.DESCRIPTOR)


def summary_schema() -> pa.Schema:
    from . import summary_msg_pb2

    return message_to_schema(summary_msg_pb2.Summary.DESCRIPTOR)


def camera_labels_schema() -> pa.Schema:
    return message_to_schema(pb.CameraLabels.DESCRIPTOR)


def lidar_labels_schema() -> pa.Schema:
    return message_to_schema(pb.LidarLabels.DESCRIPTOR)


def laser_map_schema() -> pa.Schema:
    return message_to_schema(pb.LaserMap.DESCRIPTOR)


def path_point_schema() -> pa.Schema:
    return message_to_schema(pb.PathPoint.DESCRIPTOR)


def transform_schema() -> pa.Schema:
    return message_to_schema(pb.Transform.DESCRIPTOR)


def radar_schema() -> pa.Schema:
    return message_to_schema(pb.Radar.DESCRIPTOR)


def misc_data_schema() -> pa.Schema:
    return message_to_schema(pb.MiscData.DESCRIPTOR)
