# Uber's AV Data V2 Schema Documentation (Experimental)

> ⚠️ **EXPERIMENTAL VERSION** - This schema is under active development and subject to change.

## Table of Contents
- [Overview](#overview)
- [Dataset Capabilities](#dataset-capabilities)
- [Dataset Model](#dataset-model)
- [Core Concepts](#core-concepts)
- [Summary (Search & Discovery)](#summary-search--discovery)
- [Sensor Data Blocks](#sensor-data-blocks)
  - [Camera](#camera)
  - [LiDAR](#lidar)
  - [Radar](#radar)
  - [IMU](#imu)
  - [GNSS](#gnss)
  - [Wheel Odometry](#wheel-odometry)
  - [Vehicle State](#vehicle-state)
- [Transforms](#transforms)
- [Calibrations](#calibrations)
- [MiscData](#miscdata)
- [Time Alignment](#time-alignment)
- [Data Types Reference](#data-types-reference)

---

## Overview

This document defines Uber's Autonomous Driving Schema using Lance format V2. It explains field meanings, payload reading, sensor alignment, and common task accomplishment.

**⚠️ This is an experimental schema version. Fields, types, and structure may change in future releases.**

## Dataset Capabilities

**What you can do with this dataset:**
- **Playback & Diagnosis** - Review and analyze recorded data
- **Simulation & Replay** - Re-run scenarios for testing
- **Training & Testing** - Machine learning model development
- **Data Mining & Retrieval** - Extract insights and patterns

## Dataset Model

- **Dataset** = single topic/component. Available datasets: `Camera`, `Lidar`, `Radar`, `Imu`, `Gnss`, `WheelOdometry`, `VehicleState`, `Transform`, `Summary`, `MiscData`
- **Entry** = one message on a logical topic at `sensor_timestamp`
- **Frame** = each entry includes pre-aligned `frame_timestamp` for 10Hz sensor sync
- **Scene** = ~20 second segment of continuous data
- **Summary** = metadata dataset enabling search on scenes; will support more ODD (Operational Design Domain) search in upcoming versions

---

## Core Concepts

### Required Fields

| Field | Description | Type | Usage |
|-------|-------------|------|-------|
| `frame_timestamp` | **Pre-alignment tag** for lidar-centric sync | `timestamp[us]` | 10Hz grouping |
| `frame_id` | **Pre-alignment identifier** paired with frame_timestamp (starts from '00', '01', ...) | `string` | Frame grouping |
| `device_type` | **Physical device family** (vehicle setup type) | `string` | Device type selection |
| `hashed_device_id` | **Stable platform identifier** for vehicle grouping | `string` | Vehicle tracking |
| `scene_id` | **Segment identifier** within run (~20 s) | `string` | Scene segmentation |
| `run_id` | **Grouping key** for continuous long running scenes (gap<1s) | `string` | Run grouping |
| `sensor_timestamp` | **Authoritative measurement time** (for sensor messages) | `timestamp[us]` | Precise alignment |
| `sensor_frame_id` | Deterministic per-sensor-frame key (for camera/lidar) | `string` | Unique frame identifier |

---

## Summary (Search & Discovery)

The Summary dataset enables searching and filtering scenes before loading sensor data. Use this dataset to discover relevant scenes based on location, device, and time criteria.

**Table:** `Summary`

| Field | Description | Type |
|-------|-------------|------|
| `create_timestamp` | Record create timestamp | `timestamp[us]` |
| `update_timestamp` | Record update timestamp | `timestamp[us]` |
| `delete_timestamp` | Record delete timestamp | `timestamp[us]` |
| `scene_start_timestamp` | Scene start timestamp | `timestamp[us]` |
| `scene_end_timestamp` | Scene end timestamp | `timestamp[us]` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Run identifier | `string` |
| `device_type` | Device type (see values below) | `string` |
| `device_id` | Device identifier | `string` |
| `city` | City name (see values below) | `string` |
| `country` | Country name (see values below) | `string` |

**Available Values:**
- `device_type`: `LUCID_AIR`
- `city`: `Chicago`, `Atlanta`
- `country`: `US`

---

## Sensor Data Blocks

### Camera

**Table:** `Camera`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Pre-aligned 10Hz frame timestamp | `timestamp[us]` |
| `frame_id` | Dataset frame tag | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `sensor_timestamp` | Authoritative measurement time | `timestamp[us]` |
| `sensor_frame_id` | Unique frame identifier | `string` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `sensor_type` | Camera type (see values below) | `string` |
| `camera` | Compressed video frame data | `struct<CameraData>` |
| `is_keyframe` | Whether the frame is a keyframe for the current sensor_type | `bool_` |
| `format` | Video codec (e.g., H264, H265) | `string` |
| `calibration` | Camera calibration data provided by OEM | `struct<CameraCalibration>` |

**CameraData Fields:**

| Field | Description | Type |
|-------|-------------|------|
| `front` | cam_02_fwc_c, dashcam | `binary` |
| `front_narrow` | cam_03_fnc | `binary` |
| `rear_right` | cam_04_rnc_r | `binary` |
| `front_right` | cam_05_fwc_r | `binary` |
| `rear` | cam_06_rnc_c | `binary` |
| `front_left` | cam_07_fwc_l | `binary` |
| `rear_left` | cam_08_rnc_l | `binary` |
| `surround_corner_rear` | cam_09_svc_cr | `binary` |
| `surround_corner_front` | cam_10_svc_cf | `binary` |
| `surround_left` | cam_11_svc_l | `binary` |
| `surround_right` | cam_12_svc_r | `binary` |

**sensor_type Values:**
- `front`, `front_narrow`, `rear_right`, `front_right`, `rear`, `front_left`, `rear_left`, `surround_corner_rear`, `surround_corner_front`, `surround_left`, `surround_right`

**Key Points:**
- Compressed video frames (AnnexB Access Unit); decode per `format` (H264/H265).
- `is_keyframe` identifies keyframes for auto pre-roll and decoding
- Calibration is constant per-scene (see [Calibrations](#calibrations)).

---

### LiDAR

**Table:** `Lidar`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Pre-aligned 10Hz frame timestamp | `timestamp[us]` |
| `frame_id` | Dataset frame tag | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `sensor_timestamp` | Authoritative measurement time | `timestamp[us]` |
| `sensor_frame_id` | Unique frame identifier | `string` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `lidar` | Point cloud data binary | `struct<LidarData>` |
| `calibration` | Lidar calibration data provided by OEM | `struct<LidarCalibration>` |

**LidarData Fields:**

| Field | Description | Type |
|-------|-------------|------|
| `front` | Point cloud (PCD binary) | `binary` |

**Key Points:**
- Use per-scene extrinsics for sensor→vehicle_base transforms.

---

### Radar

**Table:** `Radar`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Pre-aligned 10Hz frame timestamp | `timestamp[us]` |
| `frame_id` | Dataset frame tag | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `sensor_timestamp` | Authoritative measurement time | `timestamp[us]` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `radar` | Radar data | `struct<RadarData>` |

**RadarData Fields:**

| Field | Description | Type |
|-------|-------------|------|
| `front_srr_left` | Front short-range radar left | `list<struct<DynamicTrack>>` |
| `front_srr_right` | Front short-range radar right | `list<struct<DynamicTrack>>` |
| `rear_srr_left` | Rear short-range radar left | `list<struct<DynamicTrack>>` |
| `rear_srr_right` | Rear short-range radar right | `list<struct<DynamicTrack>>` |
| `lrr_fc` | Long-range radar front center | `list<struct<DynamicTrack>>` |
| `lrr_tja_target` | TJA target object | `struct<DynamicTrack>` |
| `lrr_ooi` | Object of Interest | `struct<DynamicTrack>` |

**DynamicTrack Fields:**

| Field | Description | Type |
|-------|-------------|------|
| `id` | Track ID (-1 = invalid) | `int32` |
| `bbox_lwh` | Bounding box [length, width, height] | `list<float64>` |
| `position_ego` | Relative position in ego XYZ frame | `struct<Point>` |
| `rpy_ego` | Relative roll/pitch/yaw in ego frame | `struct<Vector3>` |
| `speed` | Speed magnitude sqrt(vx²+vy²+vz²) | `float64` |
| `vel_angle_actor_xy` | Velocity angle wrt actor frame (beta) | `float64` |
| `distance` | Radial distance from ego | `float64` |
| `distance_rate` | Distance rate of change | `float64` |
| `azimuth` | Angle between ego x-axis and actor origin | `float64` |
| `azimuth_rate` | Azimuth rate of change | `float64` |
| `linear_velocity` | Ground velocity | `struct<Vector3>` |
| `angular_velocity` | Ground angular velocity | `struct<Vector3>` |
| `linear_acceleration` | Ground acceleration | `struct<Vector3>` |
| `angular_acceleration` | Ground angular acceleration | `struct<Vector3>` |
| `type` | DynamicTrackType (see enum values) | `int32` |
| `motion_status` | DynamicTrackMotionStatus (see enum values) | `int32` |
| `track_status` | DynamicTrackStatus (see enum values) | `int32` |
| `age` | Track age | `int32` |
| `poe` | Probability of existence (0-100) | `float32` |
| `confidence` | Track confidence (0-100) | `float32` |
| `covariance_xy` | x,vx,ax,y,vy,ay covariance (len=36) | `list<float32>` |
| `covariance_z` | z,vz,az covariance (len=9) | `list<float32>` |
| `var_length` | Bbox length estimate variance | `float32` |
| `var_width` | Bbox width estimate variance | `float32` |
| `var_height` | Bbox height estimate variance | `float32` |
| `var_heading` | Heading estimate variance | `float32` |
| `actor_intent` | Left/straight/right intent (len=3) | `list<float32>` |
| `is_tja` | TJA object indicator | `bool_` |
| `born_time` | First detection timestamp | `timestamp[us]` |
| `track_input_present` | Input sources present (len=7) | `list<bool_>` |
| `track_input_id` | Input source IDs (len=7) | `list<int32>` |

**DynamicTrackType Values:**
- `0` = UNKNOWN, `1` = VEHICLE, `2` = TRUCK, `3` = BUS, `4` = MOTORCYCLE, `5` = BICYCLE, `6` = PEDESTRIAN, `7` = OTHER

**DynamicTrackMotionStatus Values:**
- `0` = UNKNOWN, `1` = MOVING, `2` = STATIONARY

**DynamicTrackStatus Values:**
- `0` = UNKNOWN, `1` = NEW, `2` = UPDATED, `3` = COASTED

---

### IMU

**Table:** `Imu`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Pre-aligned 10Hz frame timestamp | `timestamp[us]` |
| `frame_id` | Dataset frame tag | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `sensor_timestamp` | Authoritative measurement time | `timestamp[us]` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `imu` | IMU data | `struct<ImuData>` |

**ImuData Fields:**

| Field | Description | Unit |
|-------|-------------|------|
| `orientation` | Quaternion rotation (`struct<Quaternion>`) | unitless |
| `angular_velocity` | Angular rates (`struct<Vector3>`) | rad/s |
| `linear_acceleration` | Linear acceleration (`struct<Vector3>`) | m/s² |

---

### GNSS

**Table:** `Gnss`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Pre-aligned 10Hz frame timestamp | `timestamp[us]` |
| `frame_id` | Dataset frame tag | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `sensor_timestamp` | Authoritative measurement time | `timestamp[us]` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `gnss` | GNSS data | `struct<GnssData>` |

**GnssData Fields:**

| Field | Description | Type / Unit |
|-------|-------------|-------------|
| `latitude` | Geodetic latitude (WGS84) | `float64` / degrees |
| `longitude` | Geodetic longitude (WGS84) | `float64` / degrees |
| `altitude` | Ellipsoid height | `float64` / meters |
| `status` | NavSatStatus | `struct<NavSatStatus>` |
| `velocity` | ENU velocity {x,y,z} | `struct<Vector3>` / m/s |
| `vel_n` | NED north velocity | `float64` / m/s |
| `vel_e` | NED east velocity | `float64` / m/s |
| `vel_d` | NED down velocity | `float64` / m/s |
| `speed` | Ground speed | `float64` / m/s |
| `speed_accuracy` | Speed accuracy | `float64` / m/s |
| `heading` | Vehicle heading (fused) | `float64` / degrees |
| `heading_motion` | Motion direction heading | `float64` / degrees |
| `heading_accuracy` | Heading accuracy | `float64` / degrees |
| `roll` | Roll angle (from INS fusion) | `float64` / degrees |
| `pitch` | Pitch angle (from INS fusion) | `float64` / degrees |
| `num_satellites` | Satellites used in fix | `int32` |
| `h_acc` | Horizontal accuracy | `float64` / meters |
| `v_acc` | Vertical accuracy | `float64` / meters |
| `pdop` | Position dilution of precision | `float64` |
| `hdop` | Horizontal dilution of precision | `float64` |
| `vdop` | Vertical dilution of precision | `float64` |
| `extra` | Extra diagnostic fields | `struct<GnssExtra>` |

**NavSatStatus:**

| Field | Description | Type / Values |
|-------|-------------|---------------|
| `status` | Fix status | `int32` / -1=NO_FIX, 0=FIX, 1=SBAS_FIX, 2=GBAS_FIX |
| `service` | Service bitmask | `int32` / GPS=1, GLONASS=2, COMPASS=4, GALILEO=8 |

**GnssExtra Fields:**

| Field | Description | Type / Unit |
|-------|-------------|-------------|
| `mag_declination` | Magnetic declination | `float64` / degrees |
| `mag_declination_accuracy` | Magnetic declination accuracy | `float64` / degrees |
| `mag_declination_valid` | Validity flag | `bool_` |
| `fix_type` | GnssFixType (see values) | `int32` |
| `gnss_fix_ok` | Valid fix (within DOP & accuracy masks) | `bool_` |
| `diff_soln` | Differential corrections applied | `bool_` |
| `rtcm_enabled` | RTCM message received and valid | `bool_` |
| `heading_valid` | Vehicle heading valid | `bool_` |
| `fusion_mode` | FusionMode (see values) | `int32` |
| `roll_accuracy` | Roll accuracy | `float64` / degrees |
| `pitch_accuracy` | Pitch accuracy | `float64` / degrees |
| `altitude_msl` | Height above mean sea level | `float64` / meters |

**GnssFixType Values:**
- `0` = NO_FIX, `1` = DR_ONLY, `2` = TWO_FIX, `3` = THREE_FIX, `4` = GNSS_DR, `5` = TIME_FIX

**FusionMode Values:**
- `0` = INIT, `1` = ACTIVE, `2` = SUSPENDED, `3` = DISABLED

---

### Wheel Odometry

**Table:** `WheelOdometry`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Pre-aligned 10Hz frame timestamp | `timestamp[us]` |
| `frame_id` | Dataset frame tag | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `sensor_timestamp` | Authoritative measurement time | `timestamp[us]` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `wheel_odometry` | Wheel state data | `struct<WheelState>` |

**WheelState Fields:**

| Field | Description | Type / Unit |
|-------|-------------|-------------|
| `velocity` | Per-wheel speeds | `struct<WheelValues>` / m/s |
| `steering_tire_angle` | Steering angle | `float64` / rad |
| `steering_tire_angle_velocity` | Steering angle rate | `float64` / rad/s |
| `extra` | Extra diagnostic fields | `struct<WheelOdometryExtra>` |

**WheelValues:**

| Field | Description | Type |
|-------|-------------|------|
| `front_left` | Front left wheel | `float64` |
| `front_right` | Front right wheel | `float64` |
| `rear_left` | Rear left wheel | `float64` |
| `rear_right` | Rear right wheel | `float64` |

**WheelOdometryExtra Fields:**

| Field | Description | Type / Unit |
|-------|-------------|-------------|
| `slip` | Per-wheel slip ratio | `struct<WheelValues>` |
| `movement_status` | Per-wheel movement status | `struct<WheelStatusValues>` |
| `speed_qualifier` | Per-wheel speed qualifier | `struct<WheelStatusValues>` |
| `pulse_count_qualifier` | Per-wheel pulse count qualifier | `struct<WheelStatusValues>` |
| `road_wheel_angle` | Road wheel angle | `float64` / degrees |
| `road_wheel_angle_qualifier` | Road wheel angle qualifier | `string` |
| `road_wheel_angle_velocity` | Road wheel angle velocity | `float64` / degrees/s |
| `road_wheel_angle_velocity_qualifier` | Road wheel angle velocity qualifier | `string` |
| `pinion_angle` | Pinion angle | `float64` / degrees |
| `pinion_angle_qualifier` | Pinion angle qualifier | `string` |
| `pinion_angle_velocity` | Pinion angle velocity | `float64` / degrees/s |
| `pinion_angle_velocity_qualifier` | Pinion angle velocity qualifier | `string` |
| `driver_torque` | Driver torque | `float64` / Nm |
| `driver_torque_qualifier` | Driver torque qualifier | `string` |
| `road_wheel_angle_motor_torque` | Road wheel angle motor torque | `float64` / Nm |
| `road_wheel_angle_motor_torque_qualifier` | Motor torque qualifier | `string` |
| `acu_l2_if_status` | ACU L2 interface status | `string` |

---

### Vehicle State

**Table:** `VehicleState`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Pre-aligned 10Hz frame timestamp | `timestamp[us]` |
| `frame_id` | Dataset frame tag | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `sensor_timestamp` | Authoritative measurement time | `timestamp[us]` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `vehicle_state` | Vehicle state data | `struct<VehicleStateData>` |

**VehicleStateData Fields:**

| Field | Description | Type / Unit |
|-------|-------------|-------------|
| `gear` | Gear position (PARK, REVERSE, NEUTRAL, DRIVE, etc.) | `string` |
| `gear_status` | Gear signal status | `string` |
| `brake` | Brake pedal position | `float32` / 0-1 |
| `accelerator` | Accelerator pedal position | `float64` / 0-1 |
| `accelerator_qualifier` | Accelerator position qualifier | `string` |
| `turn_signal` | Turn signal status | `string` |
| `speed` | Vehicle speed | `float64` / m/s |
| `speed_status` | Speed signal status | `string` |
| `movement_status` | Vehicle movement direction (see values) | `int32` |
| `steering_angle` | Steering wheel angle | `float64` / degrees |
| `steering_angle_status` | Steering angle signal status | `string` |
| `steering_angle_validity` | Steering angle validity | `string` |

**VehicleMovementStatus Values:**
- `0` = UNKNOWN, `1` = STATIONARY, `2` = FORWARDS, `3` = BACKWARDS

---

## Transforms

**Table:** `Transform`

| Field | Description | Type |
|-------|-------------|------|
| `frame_timestamp` | Transform timestamp (pre-aligned 10Hz) | `timestamp[us]` |
| `frame_id` | Dataset frame tag (NOT TF parent) | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `scene_id` | Scene identifier | `string` |
| `run_id` | Grouping key for continuous long running scenes (gap<1s) | `string` |
| `parent_frame_id` | TF parent frame | `string` |
| `child_frame_id` | TF child frame | `string` |
| `transform` | Transform parent → child | `struct<Pose3D>` |
| `is_static` | True for tf_static rows | `bool_` |

**Key Points:**
- For runtime coordinate transforms, use the Transform dataset
- Calibration extrinsics are stored in raw format; Transform provides unified Quaternion format

---

## Calibrations

**CameraCalibration:**

| Field | Description | Type |
|-------|-------------|------|
| `intrinsics` | Camera intrinsics | `struct<IntrinsicsCamera>` |
| `extrinsics` | Raw extrinsics sensor → vehicle_base | `struct<ExtrinsicsRaw>` |

**IntrinsicsCamera Fields:**

| Field | Description | Type / Unit |
|-------|-------------|-------------|
| `fx` | Focal length X | `float64` / pixels |
| `fy` | Focal length Y | `float64` / pixels |
| `cx` | Principal point X | `float64` / pixels |
| `cy` | Principal point Y | `float64` / pixels |
| `distortion` | Distortion coefficients [k1,k2,t1,t2,k3] (plumb_bob) | `list<float64>` |
| `width` | Image width | `int32` / pixels |
| `height` | Image height | `int32` / pixels |

**LidarCalibration:**

| Field | Description | Type |
|-------|-------------|------|
| `extrinsics` | Raw extrinsics sensor → vehicle_base | `struct<ExtrinsicsRaw>` |

**ExtrinsicsRaw Fields:**

| Field | Description | Type / Unit |
|-------|-------------|-------------|
| `tx` | Translation X | `float64` / meters |
| `ty` | Translation Y | `float64` / meters |
| `tz` | Translation Z | `float64` / meters |
| `rotation_params` | Rotation parameters (3 values) | `list<float64>` |
| `rotation_format` | "EULER_RPY" or "AXIS_ANGLE" | `string` |

**Note:** `ExtrinsicsRaw` stores original calibration file data for reference/audit. For runtime transforms, use the Transform dataset which stores extrinsics in unified Quaternion format.

---

## MiscData

**Table:** `MiscData`

| Field | Description | Type |
|-------|-------------|------|
| `scene_id` | Scene identifier | `string` |
| `run_id` | Run identifier | `string` |
| `device_type` | Device type | `string` |
| `hashed_device_id` | Device identifier | `string` |
| `type` | Type/category of the miscellaneous data | `string` |
| `payload` | JSON string or other data payload | `string` |

---

## Time Alignment

### Pre-alignment (10Hz)
Group data by `frame_timestamp` + `frame_id` for lidar-centric synchronization.

### Precise Alignment
Join data by `sensor_timestamp` within application-specific tolerance for exact timing.

---

## Data Types Reference

### PyArrow Type Mapping

| PyArrow Type | Description |
|--------------|-------------|
| `timestamp[us]` | Microsecond timestamp (UTC) |
| `string` | UTF-8 string |
| `binary` | Binary data (bytes) |
| `bool_` | Boolean |
| `int32` | 32-bit signed integer |
| `int64` | 64-bit signed integer |
| `float32` | 32-bit floating point |
| `float64` | 64-bit floating point |
| `list<T>` | List/array of type T |
| `struct<T>` | Nested struct of type T |

### Geometry Primitives

| Type | Fields | Notes |
|------|--------|-------|
| **Vector3** | `x: float64`, `y: float64`, `z: float64` | meters, m/s, or rad/s depending on field |
| **Point** | `x: float64`, `y: float64`, `z: float64` | meters |
| **Quaternion** | `x: float64`, `y: float64`, `z: float64`, `w: float64` | normalized |
| **Twist** | `linear: struct<Vector3>`, `angular: struct<Vector3>` | linear and angular velocities |
| **Pose3D** | `position: struct<Vector3>`, `orientation: struct<Quaternion>`, `linear_velocity: struct<Vector3>`, `angular_velocity: struct<Vector3>` | Complete pose with kinematics |

---

**Schema Version:** V0.1.0 | **Document Status:** Living Document
