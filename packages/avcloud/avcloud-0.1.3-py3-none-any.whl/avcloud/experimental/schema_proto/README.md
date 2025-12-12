# AV Schema Management

`av_schema.proto` aggregates AV dataset schemas via public imports. Individual schemas live in `*_msg.proto` files.
`pyarrow.Schema` objects are **derived at runtime** from the generated `pb2` descriptors.

---

## Contents
- **`av_schema.proto`**: dataset schemas
  - `Camera`
  - `Lidar`
  - `Imu`
  - `Gnss`
  - `WheelOdometry`
  - `VehicleState`
  - `Pose`
  - `Odd`
  - `CameraLabels`
  - `LidarLabels`
  - `LaserMap`
  - `PathPoint`
  - `Transform`
  - `Radar`
  - `MiscData`
  - `Summary`
- **`geometry_msg.proto`**: shared primitives (`Vector3`, `FloatVector3`, `Quaternion`, `Twist`, `Pose3D`)
- **`calibration_msg.proto`**: camera intrinsics and sensor extrinsics
- **`transform_msg.proto`**: coordinate frame transforms
- **`registry_meta.proto`**: minimal registry metadata (`name`, `version`, `revision`)
- **`av_schema_to_arrow.py`**: convert proto descriptors → `pyarrow.Schema`
- **`registry.py`**: persist/load the schema registry as `.pb`
- **`build_registry.py`**: register current schemas and write the registry file

---

## Quick Start

**Prerequisites:** Install required packages
```bash
pip install grpcio-tools protobuf pyarrow pydantic
```

1) **Compile Protos** (run from `/home/user/pearl`)
```bash
cd /home/user/pearl
python3 -m grpc_tools.protoc \
  --proto_path=experimental/data_format/schema_proto \
  --python_out=experimental/data_format/schema_proto \
  geometry_msg.proto \
  calibration_msg.proto \
  label_msg.proto \
  camera_msg.proto \
  lidar_msg.proto \
  imu_msg.proto \
  gnss_msg.proto \
  wheel_odometry_msg.proto \
  vehicle_state_msg.proto \
  pose_msg.proto \
  odd_msg.proto \
  transform_msg.proto \
  radar_msg.proto \
  misc_data_msg.proto \
  summary_msg.proto \
  av_schema.proto \
  registry_meta.proto
```

2) **Build registry** (run from `/home/user/pearl`)
```bash
cd /home/user/pearl
PYTHONPATH=/home/user/pearl/experimental/data_format/schema_proto:/home/user/pearl:${PYTHONPATH:-} \
python3 -m experimental.data_format.schema_proto.build_registry \
  --out /home/user/pearl/schema_registry.pb \
  --version 1.0.0 \
  --revision 1
```

3) **Use registry**
```python
from experimental.data_format.schema_proto.registry import SchemaRegistry
reg = SchemaRegistry.load("/home/user/pearl/schema_registry.pb")
camera_schema = reg.get("Camera")  # pyarrow.Schema
```

Example output
```python
>>> print(camera_schema)
frame_timestamp: timestamp[us]
frame_id: string
device_type: string
hashed_device_id: string
sensor_timestamp: timestamp[us]
sensor_frame_id: string
log_id: string
scene_id: string
raw_path: string
camera: struct<front: binary, front_narrow: binary, rear_right: binary, front_right: binary, rear: binary, f (... 145 chars omitted)
  child 0, front: binary
  child 1, front_narrow: binary
  child 2, rear_right: binary
  child 3, front_right: binary
  child 4, rear: binary
  child 5, front_left: binary
  child 6, rear_left: binary
  child 7, surround_corner_rear: binary
  child 8, surround_corner_front: binary
  child 9, surround_left: binary
  child 10, surround_right: binary
is_keyframe: bool
format: string
calibration: struct<intrinsics: struct<fx: double, fy: double, cx: double, cy: double, distortion: list<item: dou (... 135 chars omitted)
  child 0, intrinsics: struct<fx: double, fy: double, cx: double, cy: double, distortion: list<item: double>, width: uint32 (... 17 chars omitted)
      child 0, fx: double
      child 1, fy: double
      child 2, cx: double
      child 3, cy: double
      child 4, distortion: list<item: double>
          child 0, item: double
      child 5, width: uint32
      child 6, height: uint32
  child 1, extrinsics: struct<tx: double, ty: double, tz: double, roll: double, pitch: double, yaw: double>
      child 0, tx: double
      child 1, ty: double
      child 2, tz: double
      child 3, roll: double
      child 4, pitch: double
      child 5, yaw: double
```
