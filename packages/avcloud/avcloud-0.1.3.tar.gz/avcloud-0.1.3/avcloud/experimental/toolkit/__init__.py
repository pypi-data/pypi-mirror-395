"""
AVCloud Toolkit - Waymo-style API for working with Lance datasets

Usage:
    from avcloud.experimental.toolkit import read_component, merge
    from avcloud.experimental.toolkit import components

    # Read components
    camera_table = read_component('/data', 'camera')
    lidar_table = read_component('/data', 'lidar')

    # Merge by matching keys
    merged = merge(camera_table, lidar_table)

    # Access with type safety (Pydantic models)
    for row in merged.to_pylist():
        camera = from_dict('Camera', row)  # Handles timestamp conversion
        print(f"Scene {camera.scene_id} at {camera.frame_timestamp}")
"""

from avcloud.experimental.toolkit import components
from avcloud.experimental.toolkit.calibration import (
    get_camera_extrinsics,
    # Camera-specific convenience functions
    get_camera_intrinsics,
    get_camera_oem_calibration,
    get_camera_oem_extrinsics,
    get_camera_transform,
    get_extrinsics,
    # Generic calibration (works with any sensor)
    get_intrinsics,
    get_projection_matrix,
    get_transform_matrix,
    project_points_to_image,
    transform_points,
    undistort_image,
)
from avcloud.experimental.toolkit.camera import (
    decode_video_column,
    decode_video_frame,
    encode_camera_to_video,
    get_video_info,
    stitch_camera_to_video,
)
from avcloud.experimental.toolkit.components import ComponentRow, from_dict
from avcloud.experimental.toolkit.io import get_schema, read_component, read_components

# Video/MCAP/Calibration utilities
from avcloud.experimental.toolkit.lance2mcap import lance_to_mcap
from avcloud.experimental.toolkit.merge import merge, merge_temporal, merge_temporal_window

__all__ = [
    # Core I/O
    "read_component",
    "read_components",
    "get_schema",
    # Merge operations
    "merge",
    "merge_temporal",
    "merge_temporal_window",
    # Components
    "components",
    "from_dict",
    "ComponentRow",
    # Video/Camera
    "stitch_camera_to_video",
    "encode_camera_to_video",
    "decode_video_column",
    "decode_video_frame",
    "get_video_info",
    # Generic Calibration (any sensor)
    "get_intrinsics",
    "get_extrinsics",
    "get_transform_matrix",
    "transform_points",
    # Camera-specific Calibration
    "get_camera_intrinsics",
    "get_camera_extrinsics",
    "get_camera_transform",
    "get_camera_oem_extrinsics",
    "get_camera_oem_calibration",
    "project_points_to_image",
    "undistort_image",
    "get_projection_matrix",
    # MCAP conversion
    "lance_to_mcap",
]
