"""
Convert Lance datasets to MCAP format.

MCAP (https://mcap.dev/) is a modular container format for multimodal log data.
This module provides utilities to export AVCloud Lance datasets to MCAP files
for use with tools like Foxglove Studio.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import lance
import numpy as np
from mcap.writer import Writer as McapWriter
from rosbags.typesys import Stores, get_typestore

# Initialize typestore
_typestore = get_typestore(Stores.ROS2_HUMBLE)

# Add custom foxglove_msgs/msg/CompressedVideo type
_typestore.types["foxglove_msgs/msg/CompressedVideo"] = type(
    "CompressedVideo",
    (),
    {
        "__init__": lambda self, timestamp=None, frame_id="", format="", data=None: setattr(
            self, "timestamp", timestamp
        )
        or setattr(self, "frame_id", frame_id)
        or setattr(self, "format", format)
        or setattr(self, "data", data)
    },
)

# Add message definition for CDR serialization
from rosbags.serde.cdr import Nodetype

_typestore.fielddefs["foxglove_msgs/msg/CompressedVideo"] = (
    [],
    [
        ("timestamp", (Nodetype.NAME, "builtin_interfaces/msg/Time")),
        ("frame_id", (Nodetype.BASE, ("string", 0))),
        ("data", (Nodetype.SEQUENCE, ((Nodetype.BASE, ("uint8", 0)), 0))),
        ("format", (Nodetype.BASE, ("string", 0))),
    ],
)


def _sensor_ts_to_ns(ts_val: Any) -> int:
    """
    Convert a sensor timestamp to nanoseconds.

    Raises:
        TypeError: If the timestamp type is not supported.
    """
    if isinstance(ts_val, (int, float)):
        return int(ts_val)
    elif isinstance(ts_val, (datetime, np.datetime64)):
        return int(ts_val.timestamp() * 1_000_000_000)

    raise TypeError(f"Unsupported timestamp type: {type(ts_val)}")


def _ensure_channel(writer: McapWriter, cache: Dict[str, int], topic: str, msg_type: str):
    """Ensure a channel exists for the given topic and message type."""
    if topic in cache:
        return cache[topic]

    # Register schema with CDR encoding
    schema_id = writer.register_schema(
        name=msg_type, encoding="ros2msg", data=_get_msgdef_text(msg_type).encode()
    )

    # Register channel
    channel_id = writer.register_channel(
        topic=topic,
        message_encoding="cdr",
        schema_id=schema_id,
    )

    cache[topic] = channel_id
    return channel_id


def _get_msgdef_text(msg_type: str) -> str:
    """Get complete message definition text with all dependencies for a ROS2 message type."""
    if msg_type == "std_msgs/msg/String":
        return """string data"""

    elif msg_type == "sensor_msgs/msg/Imu":
        return """# This is a message to hold data from an IMU (Inertial Measurement Unit)

std_msgs/Header header

geometry_msgs/Quaternion orientation
float64[9] orientation_covariance # Row major about x, y, z axes

geometry_msgs/Vector3 angular_velocity
float64[9] angular_velocity_covariance # Row major about x, y, z axes

geometry_msgs/Vector3 linear_acceleration
float64[9] linear_acceleration_covariance # Row major x, y z

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
builtin_interfaces/Time stamp
string frame_id

================================================================================
MSG: builtin_interfaces/Time
# Time primitive type
int32 sec
uint32 nanosec

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x 0
float64 y 0
float64 z 0
float64 w 1

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space.

float64 x
float64 y
float64 z"""

    elif msg_type == "tf2_msgs/msg/TFMessage":
        return """geometry_msgs/TransformStamped[] transforms

================================================================================
MSG: geometry_msgs/TransformStamped
# This expresses a transform from coordinate frame header.frame_id
# to the coordinate frame child_frame_id
#
# This message is mostly used by the
# <a href="https://wiki.ros.org/tf2">tf2</a> package.
# See its documentation for more information.

std_msgs/Header header
string child_frame_id # the frame id of the child frame
geometry_msgs/Transform transform

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
builtin_interfaces/Time stamp
string frame_id

================================================================================
MSG: builtin_interfaces/Time
# Time primitive type
int32 sec
uint32 nanosec

================================================================================
MSG: geometry_msgs/Transform
# This represents the transform between two coordinate frames in free space.

geometry_msgs/Vector3 translation
geometry_msgs/Quaternion rotation

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space.
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.
float64 x 0
float64 y 0
float64 z 0
float64 w 1"""

    elif msg_type == "sensor_msgs/msg/NavSatFix":
        return """# Navigation Satellite fix for any Global Navigation Satellite System

std_msgs/Header header

# Satellite fix status information.
sensor_msgs/NavSatStatus status

# Latitude [degrees]. Positive is north of equator; negative is south.
float64 latitude

# Longitude [degrees]. Positive is east of prime meridian; negative is west.
float64 longitude

# Altitude [m]. Positive is above the WGS 84 ellipsoid
float64 altitude

# Position covariance [m^2] defined relative to a tangential plane
# through the reported position. The components are East, North, and
# Up (ENU), in row-major order.
float64[9] position_covariance

# If the covariance of the fix is known, fill it in completely. If the
# GPS receiver provides the variance of each measurement, put them
# along the diagonal. If only Dilution of Precision is available,
# estimate the covariance from that.
uint8 COVARIANCE_TYPE_UNKNOWN = 0
uint8 COVARIANCE_TYPE_APPROXIMATED = 1
uint8 COVARIANCE_TYPE_DIAGONAL_KNOWN = 2
uint8 COVARIANCE_TYPE_KNOWN = 3

uint8 position_covariance_type

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
builtin_interfaces/Time stamp
string frame_id

================================================================================
MSG: builtin_interfaces/Time
# Time primitive type
int32 sec
uint32 nanosec

================================================================================
MSG: sensor_msgs/NavSatStatus
# Navigation Satellite fix status for any Global Navigation Satellite System.

# Whether to output an augmented fix is determined by both the fix
# type and the last time differential corrections were received.  A
# fix is valid when status >= STATUS_FIX.

int8 STATUS_NO_FIX =  -1        # unable to fix position
int8 STATUS_FIX =      0        # unaugmented fix
int8 STATUS_SBAS_FIX = 1        # with satellite-based augmentation
int8 STATUS_GBAS_FIX = 2        # with ground-based augmentation

int8 status

# Bits defining which Global Navigation Satellite System signals were
# used by the receiver.
uint16 SERVICE_GPS =      1
uint16 SERVICE_GLONASS =  2
uint16 SERVICE_COMPASS =  4      # includes BeiDou.
uint16 SERVICE_GALILEO =  8

uint16 service"""

    elif msg_type == "sensor_msgs/msg/CameraInfo":
        return """# This message defines meta information for a camera. It should be in a
# camera namespace on topic "camera_info" and accompanied by up to five
# image topics named:
#   image_raw - raw data from the camera driver, possibly Bayer encoded
#   image            - monochrome, distorted
#   image_color      - color, distorted
#   image_rect       - monochrome, rectified
#   image_rect_color - color, rectified

std_msgs/Header header

# The image dimensions with which the camera was calibrated. Normally
# this will be the full camera resolution in pixels.
uint32 height
uint32 width

# The distortion model used. Supported models are listed in
# sensor_msgs/distortion_models.h. For most cameras, "plumb_bob" - a
# simple model of radial and tangential distortion - is sufficient.
string distortion_model

# The distortion parameters, size depending on the distortion model.
# For "plumb_bob", the 5 parameters are: (k1, k2, t1, t2, k3).
float64[] d

# Intrinsic camera matrix for the raw (distorted) images.
#     [fx  0 cx]
# K = [ 0 fy cy]
#     [ 0  0  1]
# Projects 3D points in the camera coordinate frame to 2D pixel
# coordinates using the focal lengths (fx, fy) and principal point
# (cx, cy).
float64[9] k

# Rectification matrix (stereo cameras only)
# A rotation matrix aligning the camera coordinate system to the ideal
# stereo image plane so that epipolar lines in both stereo images are
# parallel.
float64[9] r

# Projection/camera matrix
#     [fx'  0  cx' Tx]
# P = [ 0  fy' cy' Ty]
#     [ 0   0   1   0]
# By convention, this matrix specifies the intrinsic (camera) matrix
#  of the processed (rectified) image. That is, the left 3x3 portion
#  is the normal camera intrinsic matrix for the rectified image.
# It projects 3D points in the camera coordinate frame to 2D pixel
#  coordinates using the focal lengths (fx', fy') and principal point
#  (cx', cy') - these may differ from the values in K.
# For monocular cameras, Tx = Ty = 0. Normally, monocular cameras will
#  also have R = the identity and P[1:3,1:3] = K.
# For a stereo pair, the fourth column [Tx Ty 0]' is related to the
#  position of the optical center of the second camera in the first
#  camera's frame. We assume Tz = 0 so both cameras are in the same
#  stereo image plane. The first camera always has Tx = Ty = 0. For
#  the right (second) camera of a horizontal stereo pair, Ty = 0 and
#  Tx = -fx' * B, where B is the baseline between the cameras.
# Given a 3D point [X Y Z]', the projection (x, y) of the point onto
#  the rectified image is given by:
#  [u v w]' = P * [X Y Z 1]'
#         x = u / w
#         y = v / w
#  This holds for both images of a stereo pair.
float64[12] p

# Binning refers to any camera setting which combines rectangular
#  neighborhoods of pixels into larger "super-pixels." It reduces the
#  resolution of the output image to
#  (width / binning_x) x (height / binning_y).
# The default values binning_x = binning_y = 0 is considered the same
#  as binning_x = binning_y = 1 (no subsampling).
uint32 binning_x
uint32 binning_y

# Region of interest (subwindow of full camera resolution), given in
#  full resolution (unbinned) image coordinates. A particular ROI
#  always denotes the same window of pixels on the camera sensor,
#  regardless of binning settings.
# The default setting of roi (all values 0) is considered the same as
#  full resolution (roi.width = width, roi.height = height).
sensor_msgs/RegionOfInterest roi

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
builtin_interfaces/Time stamp
string frame_id

================================================================================
MSG: builtin_interfaces/Time
# Time primitive type
int32 sec
uint32 nanosec

================================================================================
MSG: sensor_msgs/RegionOfInterest
# This message is used to specify a region of interest within an image.
#
# When used to specify the ROI setting of the camera when the image was
# taken, the height and width fields should either both be zero to
# indicate that the full resolution image was captured, or both be
# non-zero to indicate that a partial image was captured.

uint32 x_offset  # Leftmost pixel of the ROI
                 # (0 if the ROI includes the left edge of the image)
uint32 y_offset  # Topmost pixel of the ROI
                 # (0 if the ROI includes the top edge of the image)
uint32 height    # Height of ROI
uint32 width     # Width of ROI

# True if a distinct rectified ROI should be calculated from the "raw"
# ROI in this message. Typically this should be False if the full image
# is captured (ROI not used), and True if a subwindow is captured (ROI
# used).
bool do_rectify"""

    elif msg_type == "foxglove_msgs/msg/CompressedVideo":
        return """# This contains the representation of compressed video

builtin_interfaces/Time timestamp
string frame_id
uint8[] data
string format

================================================================================
MSG: builtin_interfaces/Time
# Time primitive type
int32 sec
uint32 nanosec"""

    elif msg_type == "nav_msgs/msg/Odometry":
        return """# This represents an estimate of a position and velocity in free space.

std_msgs/Header header
string child_frame_id
geometry_msgs/PoseWithCovariance pose
geometry_msgs/TwistWithCovariance twist

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
builtin_interfaces/Time stamp
string frame_id

================================================================================
MSG: builtin_interfaces/Time
# Time primitive type
int32 sec
uint32 nanosec

================================================================================
MSG: geometry_msgs/PoseWithCovariance
# This represents a pose in free space with uncertainty.

geometry_msgs/Pose pose

# Row-major representation of the 6x6 covariance matrix
# The orientation parameters use a fixed-axis representation.
# In order, the parameters are:
# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)
float64[36] covariance

================================================================================
MSG: geometry_msgs/Pose
# A representation of position and orientation in free space.

geometry_msgs/Point position
geometry_msgs/Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.
float64 x 0
float64 y 0
float64 z 0
float64 w 1

================================================================================
MSG: geometry_msgs/TwistWithCovariance
# This expresses velocity in free space with uncertainty.

geometry_msgs/Twist twist

# Row-major representation of the 6x6 covariance matrix
# The orientation parameters use a fixed-axis representation.
# In order, the parameters are:
# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)
float64[36] covariance

================================================================================
MSG: geometry_msgs/Twist
# This expresses velocity in free space broken into its linear and angular parts.

geometry_msgs/Vector3  linear
geometry_msgs/Vector3  angular

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space.
float64 x
float64 y
float64 z"""

    elif msg_type == "sensor_msgs/msg/PointCloud2":
        return """# This message holds a collection of N-dimensional points, which may
# contain additional information such as normals, intensity, etc. The
# point data is stored as a binary blob, its format described by the
# contents of the "fields" array.

std_msgs/Header header

# 2D structure of the point cloud. If the cloud is unordered, height is
# 1 and width is the length of the point cloud.
uint32 height
uint32 width

# Describes the channels and their layout in the binary data blob.
sensor_msgs/PointField[] fields

bool    is_bigendian # Is this data bigendian?
uint32  point_step   # Length of a point in bytes
uint32  row_step     # Length of a row in bytes
uint8[] data         # Actual point data, size is (row_step*height)

bool is_dense        # True if there are no invalid points

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data
# in a particular coordinate frame.

builtin_interfaces/Time stamp
string frame_id

================================================================================
MSG: builtin_interfaces/Time
# Time primitive type
int32 sec
uint32 nanosec

================================================================================
MSG: sensor_msgs/PointField
# This message holds the description of one point entry in the
# PointCloud2 message format.
uint8 INT8    = 1
uint8 UINT8   = 2
uint8 INT16   = 3
uint8 UINT16  = 4
uint8 INT32   = 5
uint8 UINT32  = 6
uint8 FLOAT32 = 7
uint8 FLOAT64 = 8

string name      # Name of field
uint32 offset    # Offset from start of point struct
uint8  datatype  # Datatype enumeration, see above
uint32 count     # How many elements in the field"""

    else:
        return ""


# ================================================= #
# ------------------ START Message Constructors -------------------- #
# ================================================= #
def _build_compressed_video(ns: int, frame: str, video: bytes, video_format: str) -> Any:
    """Build a compressed video foxglove message from video bytes."""
    sec, nsec = divmod(ns, 1_000_000_000)

    msg = _typestore.types["foxglove_msgs/msg/CompressedVideo"](
        timestamp=_typestore.types["builtin_interfaces/msg/Time"](sec=sec, nanosec=nsec),
        frame_id=frame,
        format=video_format,
        data=np.frombuffer(video, dtype=np.uint8),
    )
    return msg


def _build_camera_info(ns: int, frame: str, calibration: Dict[str, Any]):
    """Build CameraInfo message from calibration data"""
    sec, nsec = divmod(ns, 1_000_000_000)

    header = _typestore.types["std_msgs/msg/Header"](
        stamp=_typestore.types["builtin_interfaces/msg/Time"](sec=sec, nanosec=nsec), frame_id=frame
    )

    # Extract intrinsics if available
    intrinsics = calibration.get("intrinsics", {})
    width = (
        intrinsics.get("width") if "width" in intrinsics and intrinsics.get("width") != 0 else 1920
    )
    height = (
        intrinsics.get("height")
        if "height" in intrinsics and intrinsics.get("height") != 0
        else 1080
    )
    fx = intrinsics.get("fx", 1000.0)
    fy = intrinsics.get("fy", 1000.0)
    cx = intrinsics.get("cx", width / 2.0)
    cy = intrinsics.get("cy", height / 2.0)

    # Camera matrix K
    K = np.array([fx, 0, cx, 0, fy, cy, 0, 0, 1], dtype=np.float64)

    # Projection matrix P (assuming monocular camera)
    P = np.array([fx, 0, cx, 0, 0, fy, cy, 0, 0, 0, 1, 0], dtype=np.float64)

    # Identity rectification matrix R
    R = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1], dtype=np.float64)

    # ROI (Region of Interest) - default full image
    roi = _typestore.types["sensor_msgs/msg/RegionOfInterest"](
        x_offset=0,
        y_offset=0,
        height=0,  # 0 means full resolution
        width=0,  # 0 means full resolution
        do_rectify=False,
    )

    msg = _typestore.types["sensor_msgs/msg/CameraInfo"](
        header=header,
        height=height,
        width=width,
        distortion_model="",  # Empty distortion model since no distortion data provided
        d=np.array([], dtype=np.float64),  # Empty distortion coefficients
        k=K,
        r=R,
        p=P,
        binning_x=0,
        binning_y=0,
        roi=roi,
    )
    return msg


def _build_pointcloud2(ns: int, frame: str, xyz_i: np.ndarray):
    """Build PointCloud2 message from xyz_i array.
    Assumes xyz_i: (N,4) float32 [x y z intensity]
    """
    sec, nsec = divmod(ns, 1_000_000_000)

    # Create header
    header = _typestore.types["std_msgs/msg/Header"](
        stamp=_typestore.types["builtin_interfaces/msg/Time"](sec=sec, nanosec=nsec), frame_id=frame
    )

    # PointField list
    names = ["x", "y", "z", "intensity"]
    fields = []
    for i, n in enumerate(names):
        pf = _typestore.types["sensor_msgs/msg/PointField"](
            name=n,
            offset=i * 4,
            datatype=7,  # 7 = float32
            count=1,
        )
        fields.append(pf)

    msg = _typestore.types["sensor_msgs/msg/PointCloud2"](
        header=header,
        height=1,
        width=xyz_i.shape[0],
        fields=fields,
        is_bigendian=False,
        point_step=16,  # 4 float32 numbers * 4 bytes each
        row_step=16 * xyz_i.shape[0],
        data=np.frombuffer(xyz_i.astype(np.float32).tobytes(), dtype=np.uint8),
        is_dense=True,
    )

    return msg


def _build_wheel_odometry(ns: int, wheel_odometry_dict: Dict[str, Any]):
    """Build WheelOdometry message from wheel_odometry_dict."""
    vel = wheel_odometry_dict.get("velocity", {})
    vals = [
        vel.get(k)
        for k in ("front_left", "front_right", "rear_left", "rear_right")
        if vel.get(k) is not None
    ]
    if not vals:
        vals = [0]

    sec, nsec = divmod(ns, 1_000_000_000)

    header = _typestore.types["std_msgs/msg/Header"](
        stamp=_typestore.types["builtin_interfaces/msg/Time"](sec=sec, nanosec=nsec),
        frame_id="vehicle_base",
    )

    # Build pose with covariance
    position = (
        wheel_odometry_dict.get("position")
        if wheel_odometry_dict.get("position")
        else {"x": 0.0, "y": 0.0, "z": 0.0}
    )

    pose = _typestore.types["geometry_msgs/msg/Pose"](
        position=_typestore.types["geometry_msgs/msg/Point"](
            x=position.get("x", 0.0), y=position.get("y", 0.0), z=position.get("z", 0.0)
        ),
        orientation=_typestore.types["geometry_msgs/msg/Quaternion"](x=0.0, y=0.0, z=0.0, w=1.0),
    )
    pose_with_cov = _typestore.types["geometry_msgs/msg/PoseWithCovariance"](
        pose=pose, covariance=np.zeros(36, dtype=np.float64)
    )

    # Build twist with covariance
    linear_vel = _typestore.types["geometry_msgs/msg/Vector3"](x=float(np.mean(vals)), y=0.0, z=0.0)
    angular_vel = _typestore.types["geometry_msgs/msg/Vector3"](
        x=0.0, y=0.0, z=wheel_odometry_dict.get("steering_tire_angle", 0.0)
    )
    twist = _typestore.types["geometry_msgs/msg/Twist"](linear=linear_vel, angular=angular_vel)
    twist_with_cov = _typestore.types["geometry_msgs/msg/TwistWithCovariance"](
        twist=twist, covariance=np.zeros(36, dtype=np.float64)
    )

    msg = _typestore.types["nav_msgs/msg/Odometry"](
        header=header, child_frame_id="vehicle_base", pose=pose_with_cov, twist=twist_with_cov
    )
    return msg


def _build_vehicle_state(ns: int, vehicle_state_dict: Dict[str, Any]):
    """Build VehicleState message from vehicle_state_dict."""
    msg = _typestore.types["std_msgs/msg/String"](data=json.dumps(vehicle_state_dict, default=str))
    return msg


def _build_imu(ns: int, imu_dict: Dict[str, Any]):
    """Build IMU message from imu_dict."""
    sec, nsec = divmod(ns, 1_000_000_000)

    header = _typestore.types["std_msgs/msg/Header"](
        stamp=_typestore.types["builtin_interfaces/msg/Time"](sec=sec, nanosec=nsec),
        frame_id="vehicle_base",
    )

    # Default values
    orientation = _typestore.types["geometry_msgs/msg/Quaternion"](x=0.0, y=0.0, z=0.0, w=1.0)
    angular_velocity = _typestore.types["geometry_msgs/msg/Vector3"](x=0.0, y=0.0, z=0.0)
    linear_acceleration = _typestore.types["geometry_msgs/msg/Vector3"](x=0.0, y=0.0, z=0.0)

    # Update with actual values if available
    if o := imu_dict.get("orientation"):
        orientation = _typestore.types["geometry_msgs/msg/Quaternion"](
            x=o.get("x", 0.0), y=o.get("y", 0.0), z=o.get("z", 0.0), w=o.get("w", 1.0)
        )

    if av := imu_dict.get("angular_velocity"):
        # Angular velocity is already in radians/second from format_script_generic.py
        angular_velocity = _typestore.types["geometry_msgs/msg/Vector3"](
            x=av.get("x", 0.0), y=av.get("y", 0.0), z=av.get("z", 0.0)
        )

    if la := imu_dict.get("linear_acceleration"):
        # Linear acceleration is already in m/s² with gravity correction from format_script_generic.py
        linear_acceleration = _typestore.types["geometry_msgs/msg/Vector3"](
            x=la.get("x", 0.0), y=la.get("y", 0.0), z=la.get("z", 0.0)
        )

    # Zero covariances
    cov = np.zeros(9, dtype=np.float64)

    msg = _typestore.types["sensor_msgs/msg/Imu"](
        header=header,
        orientation=orientation,
        orientation_covariance=cov,
        angular_velocity=angular_velocity,
        angular_velocity_covariance=cov,
        linear_acceleration=linear_acceleration,
        linear_acceleration_covariance=cov,
    )

    return msg


def _build_tf(
    parent_frame_id: str,
    child_frame_id: str,
    stamp_ns: int,
    position: Dict[str, Any],
    orientation: Dict[str, Any],
):
    """Build TransformStamped message from parent_frame_id, child_frame_id, stamp_ns, position, orientation.

    Assumes position is the x, y, z transform and and orientation is a quaternion (x, y, z, w).
    """
    sec, nsec = divmod(stamp_ns, 1_000_000_000)

    #  header.frame_id = parent_frame, child_frame_id = child_frame
    header = _typestore.types["std_msgs/msg/Header"](
        stamp=_typestore.types["builtin_interfaces/msg/Time"](sec=sec, nanosec=nsec),
        frame_id=parent_frame_id,
    )

    tx = position.get("x", 0.0)
    ty = position.get("y", 0.0)
    tz = position.get("z", 0.0)

    qx = orientation.get("x", 0.0)
    qy = orientation.get("y", 0.0)
    qz = orientation.get("z", 0.0)
    qw = orientation.get("w", 1.0)

    transform = _typestore.types["geometry_msgs/msg/Transform"](
        translation=_typestore.types["geometry_msgs/msg/Vector3"](x=tx, y=ty, z=tz),
        rotation=_typestore.types["geometry_msgs/msg/Quaternion"](x=qx, y=qy, z=qz, w=qw),
    )

    tf = _typestore.types["geometry_msgs/msg/TransformStamped"](
        header=header, child_frame_id=child_frame_id, transform=transform
    )

    return tf


def _build_navsat(ns: int, gnss_dict: Dict[str, Any]):
    sec, nsec = divmod(ns, 1_000_000_000)

    header = _typestore.types["std_msgs/msg/Header"](
        stamp=_typestore.types["builtin_interfaces/msg/Time"](sec=sec, nanosec=nsec),
        frame_id="gnss_frame",
    )

    status = _typestore.types["sensor_msgs/msg/NavSatStatus"](status=0, service=0)
    if st := gnss_dict.get("status"):
        status = _typestore.types["sensor_msgs/msg/NavSatStatus"](
            status=st.get("status", 0), service=st.get("service", 0)
        )

    msg = _typestore.types["sensor_msgs/msg/NavSatFix"](
        header=header,
        status=status,
        latitude=gnss_dict.get("latitude", float("nan")),
        longitude=gnss_dict.get("longitude", float("nan")),
        altitude=gnss_dict.get("altitude", float("nan")),
        position_covariance=np.zeros(9, dtype=np.float64),
        position_covariance_type=0,  # COVARIANCE_TYPE_UNKNOWN
    )

    if cov := gnss_dict.get("position_covariance"):
        msg.position_covariance = np.array(cov, dtype=np.float64)
        msg.position_covariance_type = 3  # COVARIANCE_TYPE_KNOWN

    return msg


# ================================================= #
# ------------------ END Message Constructors -------------------- #
# ================================================= #


def _convert_camera(
    writer: McapWriter,
    channel_cache: Dict[str, int],
    base_path: Path,
    scene_id: Optional[str] = None,
) -> None:
    """Convert camera data to MCAP format.

    Expects the Camera.lance dataset to be in the base path.
    """
    print("[camera] 🎥 Converting camera dataset...")
    camera_dataset = lance.dataset(base_path / "Camera.lance")
    camera_table = camera_dataset.to_table(
        filter=None if not scene_id else f"scene_id = '{scene_id}'"
    )

    for row in camera_table.to_pylist():
        timestamp_ns = _sensor_ts_to_ns(row["sensor_timestamp"])
        if (camera := row.get("camera")) is None:
            raise ValueError(f"Camera data not found for row {row}")
        for cam_type, cam_bytes in camera.items():
            if cam_bytes is None:
                continue
            if (camera_format := row.get("format")) is None:
                raise ValueError(f"Camera format not found for row {row}")

            # Build and write the compressed video message
            compressed_video = _build_compressed_video(
                timestamp_ns, f"{cam_type}_frame", cam_bytes, camera_format.lower()
            )
            channel_id = _ensure_channel(
                writer,
                channel_cache,
                f"/camera/{cam_type}/compressed_video",
                "foxglove_msgs/msg/CompressedVideo",
            )
            msg_data = _typestore.serialize_cdr(
                compressed_video, "foxglove_msgs/msg/CompressedVideo"
            )
            writer.add_message(
                channel_id=channel_id,
                log_time=timestamp_ns,
                data=msg_data,
                publish_time=timestamp_ns,
            )

            # Build and write the camera info message
            calibration = row.get("calibration", {})
            info_msg = _build_camera_info(timestamp_ns, f"{cam_type}_frame", calibration)
            channel_id = _ensure_channel(
                writer,
                channel_cache,
                f"/camera/{cam_type}/camera_info",
                "sensor_msgs/msg/CameraInfo",
            )
            msg_data = _typestore.serialize_cdr(info_msg, "sensor_msgs/msg/CameraInfo")
            writer.add_message(
                channel_id=channel_id,
                log_time=timestamp_ns,
                data=msg_data,
                publish_time=timestamp_ns,
            )

    print("[camera] ✅ Successfully converted camera dataset")


def _convert_lidar(
    writer: McapWriter,
    channel_cache: Dict[str, int],
    base_path: Path,
    scene_id: Optional[str] = None,
) -> None:
    """Convert Lidar data to MCAP format.
    Expects the Lidar.lance dataset to be in the base path.

    """
    print("[lidar] 📡 Converting lidar dataset...")

    LIDAR_FRAME_ID = "lidar_front_frame"

    lidar_dataset = lance.dataset(base_path / "Lidar.lance")
    lidar_table = lidar_dataset.to_table(
        filter=None if not scene_id else f"scene_id = '{scene_id}'"
    )

    for lidar_row in lidar_table.to_pylist():
        timestamp_ns = _sensor_ts_to_ns(lidar_row["sensor_timestamp"])

        if (lidar_data := lidar_row.get("lidar")) is None:
            raise ValueError(f"Lidar data not found for row {lidar_row}")
        if (lidar_front := lidar_data.get("front")) is None:
            raise ValueError(f"Lidar front data not found for row {lidar_row}")

        # Parse structured PCD data: x, y, z, intensity, time_hi, time_lo (6 fields, 24 bytes per point)
        # The Lance dataset stores raw PCD binary data with all 6 fields
        float_data = np.frombuffer(lidar_front, dtype=np.float32)
        if len(float_data) % 6 != 0:
            raise ValueError(f"Lidar front data has invalid length for row {lidar_row}")

        # Reshape to (N, 6) to get: [x, y, z, intensity, time_hi, time_lo]
        full_data = float_data.reshape(-1, 6)
        # Extract only the coordinate and intensity fields (first 4 columns)
        xyz_i = full_data[:, :4]  # [x, y, z, intensity]

        pointcloud2_msg = _build_pointcloud2(timestamp_ns, LIDAR_FRAME_ID, xyz_i)

        channel_id = _ensure_channel(
            writer, channel_cache, "/lidar/points", "sensor_msgs/msg/PointCloud2"
        )
        msg_data = _typestore.serialize_cdr(pointcloud2_msg, "sensor_msgs/msg/PointCloud2")
        writer.add_message(
            channel_id=channel_id,
            log_time=timestamp_ns,
            data=msg_data,
            publish_time=timestamp_ns,
        )

    print("[lidar] ✅ Successfully converted lidar dataset")


def _convert_imu(
    writer: McapWriter,
    channel_cache: Dict[str, int],
    base_path: Path,
    scene_id: Optional[str] = None,
) -> None:
    """Convert IMU data to MCAP format.
    Expects the Imu.lance dataset to be in the base path.
    """
    print("[imu] 🧭 Converting IMU dataset...")

    imu_dataset = lance.dataset(base_path / "Imu.lance")
    imu_table = imu_dataset.to_table(filter=None if not scene_id else f"scene_id = '{scene_id}'")

    for imu_row in imu_table.to_pylist():
        timestamp_ns = _sensor_ts_to_ns(imu_row["sensor_timestamp"])

        if (imu := imu_row.get("imu")) is None:
            raise ValueError(f"IMU not found for row {imu_row}")

        imu_msg = _build_imu(timestamp_ns, imu)
        channel_id = _ensure_channel(writer, channel_cache, "/imu/data", "sensor_msgs/msg/Imu")
        msg_data = _typestore.serialize_cdr(imu_msg, "sensor_msgs/msg/Imu")
        writer.add_message(
            channel_id=channel_id,
            log_time=timestamp_ns,
            data=msg_data,
            publish_time=timestamp_ns,
        )

    print("[imu] ✅ Successfully converted IMU dataset")


def _convert_gnss(
    writer: McapWriter,
    channel_cache: Dict[str, int],
    base_path: Path,
    scene_id: Optional[str] = None,
) -> None:
    """Convert GNSS data to MCAP format.
    Expects the Gnss.lance dataset to be in the base path.
    """
    print("[gnss] 🛰️ Converting GNSS dataset...")

    gnss_dataset = lance.dataset(base_path / "Gnss.lance")
    gnss_table = gnss_dataset.to_table(filter=None if not scene_id else f"scene_id = '{scene_id}'")

    for gnss_row in gnss_table.to_pylist():
        timestamp_ns = _sensor_ts_to_ns(gnss_row["sensor_timestamp"])
        if (gnss := gnss_row.get("gnss")) is None:
            raise ValueError(f"GNSS not found for row {gnss_row}")

        navsat_msg = _build_navsat(timestamp_ns, gnss)
        channel_id = _ensure_channel(
            writer, channel_cache, "/gnss/fix", "sensor_msgs/msg/NavSatFix"
        )
        msg_data = _typestore.serialize_cdr(navsat_msg, "sensor_msgs/msg/NavSatFix")
        writer.add_message(
            channel_id=channel_id,
            log_time=timestamp_ns,
            data=msg_data,
            publish_time=timestamp_ns,
        )

    print("[gnss] ✅ Successfully converted GNSS dataset")


def _convert_vehicle_state(
    writer: McapWriter,
    channel_cache: Dict[str, int],
    base_path: Path,
    scene_id: Optional[str] = None,
) -> None:
    """Convert VehicleState data to MCAP format.
    Expects the VehicleState.lance dataset to be in the base path.
    """
    print("[vehicle_state] 🚗 Converting vehicle state dataset...")

    vehicle_state_dataset = lance.dataset(base_path / "VehicleState.lance")
    vehicle_state_table = vehicle_state_dataset.to_table(
        filter=None if not scene_id else f"scene_id = '{scene_id}'"
    )

    for vehicle_state_row in vehicle_state_table.to_pylist():
        timestamp_ns = _sensor_ts_to_ns(vehicle_state_row["sensor_timestamp"])

        if (vehicle_state := vehicle_state_row.get("vehicle_state")) is None:
            raise ValueError(f"Vehicle state not found for row {vehicle_state_row}")

        vehicle_state_msg = _build_vehicle_state(timestamp_ns, vehicle_state)
        channel_id = _ensure_channel(writer, channel_cache, "/vehicle_state", "std_msgs/msg/String")
        msg_data = _typestore.serialize_cdr(vehicle_state_msg, "std_msgs/msg/String")
        writer.add_message(
            channel_id=channel_id,
            log_time=timestamp_ns,
            data=msg_data,
            publish_time=timestamp_ns,
        )

    print("[vehicle_state] ✅ Successfully converted vehicle state dataset")


def _convert_wheel_odometry(
    writer: McapWriter,
    channel_cache: Dict[str, int],
    base_path: Path,
    scene_id: Optional[str] = None,
) -> None:
    """Convert WheelOdometry data to MCAP format.
    Expects the WheelOdometry.lance dataset to be in the base path.
    """
    print("[wheel_odometry] 🛞 Converting wheel odometry dataset...")

    wheel_dataset = lance.dataset(base_path / "WheelOdometry.lance")
    wheel_table = wheel_dataset.to_table(
        filter=None if not scene_id else f"scene_id = '{scene_id}'"
    )

    for wheel_row in wheel_table.to_pylist():
        timestamp_ns = _sensor_ts_to_ns(wheel_row["sensor_timestamp"])
        if (wheel_odometry := wheel_row.get("wheel_odometry")) is None:
            raise ValueError(f"Wheel odometry not found for row {wheel_row}")

        wheel_msg = _build_wheel_odometry(timestamp_ns, wheel_odometry)
        channel_id = _ensure_channel(
            writer, channel_cache, "/wheel/odometry", "nav_msgs/msg/Odometry"
        )
        msg_data = _typestore.serialize_cdr(wheel_msg, "nav_msgs/msg/Odometry")
        writer.add_message(
            channel_id=channel_id,
            log_time=timestamp_ns,
            data=msg_data,
            publish_time=timestamp_ns,
        )

    print("[wheel_odometry] ✅ Successfully converted wheel odometry dataset")


def _convert_transform(
    writer: McapWriter,
    channel_cache: Dict[str, int],
    base_path: Path,
    scene_id: Optional[str] = None,
) -> None:
    print("[transform] 🔄 Converting transform dataset...")

    static_tf_transforms = []
    static_transform_ts = 0

    transform_dataset = lance.dataset(base_path / "Transform.lance")
    transform_table = transform_dataset.to_table(
        filter=None if not scene_id else f"scene_id = '{scene_id}'"
    )

    for transform_row in transform_table.to_pylist():
        timestamp_ns = _sensor_ts_to_ns(transform_row["frame_timestamp"])

        if transform_row.get("is_static", False):
            if (transform := transform_row.get("transform")) is None:
                raise ValueError(f"Transform not found for row {transform_row}")
            if (position := transform.get("position")) is None:
                raise ValueError(f"Transform position not found for row {transform_row}")
            if (orientation := transform.get("orientation")) is None:
                raise ValueError(f"Transform orientation not found for row {transform_row}")

            # Assuming all transforms are at the same timestamp
            static_transform_ts = timestamp_ns

            tf = _build_tf(
                transform_row.get("parent_frame_id"),
                transform_row.get("child_frame_id"),
                timestamp_ns,
                position,
                orientation,
            )
            static_tf_transforms.append(tf)

    # PUBLISH TF
    if static_tf_transforms:
        tf_message = _typestore.types["tf2_msgs/msg/TFMessage"](transforms=static_tf_transforms)
        channel_id_static = _ensure_channel(
            writer, channel_cache, "/tf_static", "tf2_msgs/msg/TFMessage"
        )
        serialized_tf_raw = _typestore.serialize_cdr(tf_message, "tf2_msgs/msg/TFMessage")

        writer.add_message(
            channel_id=channel_id_static,
            log_time=static_transform_ts,
            data=bytes(serialized_tf_raw),
            publish_time=static_transform_ts,
        )

    print("[transform] ✅ Successfully converted transform dataset")


def _build_mcap(
    base_path: Path, output_path: Path, components: List[str], scene_id: Optional[str] = None
) -> None:
    print(f"\n{'=' * 70}")
    print("LANCE TO MCAP CONVERSION")
    print(f"{'=' * 70}")
    print(f"Input:  {base_path}")
    print(f"Output: {output_path}")
    if scene_id:
        print(f"Scene:  {scene_id}")
    print(f"Components: {', '.join(components)}")
    print(f"{'=' * 70}\n")

    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(str(output_path), "wb") as fd:
        writer = McapWriter(fd)
        writer.start()

        channel_cache: Dict[str, int] = {}

        if "camera" in components:
            _convert_camera(writer, channel_cache, base_path, scene_id)
        if "lidar" in components:
            _convert_lidar(writer, channel_cache, base_path, scene_id)
        if "imu" in components:
            _convert_imu(writer, channel_cache, base_path, scene_id)
        if "gnss" in components:
            _convert_gnss(writer, channel_cache, base_path, scene_id)
        if "vehicle_state" in components:
            _convert_vehicle_state(writer, channel_cache, base_path, scene_id)
        if "wheel_odometry" in components:
            _convert_wheel_odometry(writer, channel_cache, base_path, scene_id)
        if "transform" in components:
            _convert_transform(writer, channel_cache, base_path, scene_id)

        writer.finish()

    print(f"\n{'=' * 70}")
    print("✅ CONVERSION COMPLETE")
    print(f"{'=' * 70}")
    print(f"Successfully created MCAP file: {output_path}")
    print(f"{'=' * 70}\n")


def lance_to_mcap(
    base_path: str,
    output_base_path: Optional[str] = None,
    output_file_path: Optional[str] = None,
    scene_id: Optional[str] = None,
    components: Optional[List[str]] = [
        "camera",
        "lidar",
        "imu",
        "gnss",
        "vehicle_state",
        "wheel_odometry",
        "transform",
    ],
) -> None:
    """Convert Lance dataset to MCAP format.

    Exports selected components and scenes from Lance dataset to a single
    MCAP file for visualization and analysis in tools like Foxglove Studio.

    Args:
        base_path: Path to downloaded Lance dataset directory
        output_base_path: Output base path (e.g., "/output"). If not provided, output_file_path must be provided.
        output_file_path: Output file path (e.g., "data.mcap"). If provided, output_base_path is ignored.
        scene_id: Optional scene ID to export (default: all scenes).
        components: Optional list of components to export (default: all components). Available components: camera, lidar, imu, gnss, vehicle_state, wheel_odometry, transform.

    Returns:
        None. Writes MCAP file to output_path.

    Examples:
        # Export all data
        lance_to_mcap("/data", "/output/dataset.mcap")

        # Export specific scene and components
        lance_to_mcap(
            "/data",
            output_file_path="/out/my_scene001.mcap",
            scene_id="scene_001",
            components=["camera", "lidar"],
        )

    Notes:
        - MCAP format preserves timestamps and supports efficient streaming
        - Camera images are encoded as compressed_video messages
        - Lidar point clouds are encoded as PointCloud2 messages
        - IMU data follows standard sensor_msgs/Imu format
        Supported topics:
            /camera/<camera_type>/compressed_video   foxglove_msgs/CompressedVideo
            /camera/<camera_type>/camera_info  sensor_msgs/CameraInfo
            /lidar/points              sensor_msgs/PointCloud2
            /imu/data                  sensor_msgs/Imu
            /gnss/fix                  sensor_msgs/NavSatFix
            /wheel/odometry            nav_msgs/Odometry
            /vehicle/state             std_msgs/String
            /tf_static                 tf2_msgs/TFMessage

    See also:
        - MCAP specification: https://mcap.dev/spec
        - Foxglove Studio: https://foxglove.dev/
    """
    if not output_file_path and not (output_base_path and scene_id):
        raise ValueError(
            "Either output_base_path and scene_id or output_file_path must be provided"
        )

    file_path = (
        Path(output_file_path) if output_file_path else Path(output_base_path) / f"{scene_id}.mcap"
    )

    _build_mcap(Path(base_path), Path(file_path), components, scene_id)
