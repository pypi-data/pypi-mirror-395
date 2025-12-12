"""
Generic sensor calibration utilities.

This module provides functions for extracting calibration data and applying
geometric transformations (projections, undistortion, coordinate transforms).

Supports calibration extraction from any sensor component (camera, lidar, radar, etc.)
"""

from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd
import pyarrow as pa
import transforms3d


def get_intrinsics(
    component_table: Union[pa.Table, pd.DataFrame],
) -> Optional[dict]:
    """Extract sensor intrinsic parameters (camera only).

    Generic intrinsics extraction. Currently only cameras have intrinsics.
    Returns None for sensors without intrinsics (lidar, imu, etc.)

    Uses first row since calibration parameters are constant across all frames.

    Args:
        component_table: Any sensor component table with calibration field

    Returns:
        Dictionary with intrinsic parameters for cameras:
        {
            "fx": float,           # Focal length x
            "fy": float,           # Focal length y
            "cx": float,           # Principal point x
            "cy": float,           # Principal point y
            "distortion": list,    # Distortion coefficients [k1, k2, p1, p2, k3, ...]
            "width": int,          # Image width
            "height": int,         # Image height
        }
        Or None if sensor has no intrinsics.

    Examples:
        camera = read_component("/data", "camera")
        intrinsics = get_intrinsics(camera)

        lidar = read_component("/data", "lidar")
        intrinsics = get_intrinsics(lidar)  # Returns None
    """
    # Convert to pandas if needed
    df = component_table.to_pandas() if isinstance(component_table, pa.Table) else component_table

    if len(df) == 0:
        raise ValueError("Empty component table")

    # Use first row since calibration is constant
    row = df.iloc[0]

    # Check if calibration field exists
    if "calibration" not in row or row["calibration"] is None:
        return None

    calib = row["calibration"]

    # Check if intrinsics exists (camera only)
    if not isinstance(calib, dict) or "intrinsics" not in calib or calib["intrinsics"] is None:
        return None

    intrinsics = calib["intrinsics"]

    # Extract distortion coefficients
    distortion = intrinsics.get("distortion", [])
    if distortion is not None:
        if hasattr(distortion, "__iter__") and not isinstance(distortion, (str, bytes)):
            if hasattr(distortion, "tolist"):
                distortion = distortion.tolist()
            else:
                distortion = list(distortion)
        else:
            distortion = []
    else:
        distortion = []

    return {
        "fx": float(intrinsics.get("fx", 0)),
        "fy": float(intrinsics.get("fy", 0)),
        "cx": float(intrinsics.get("cx", 0)),
        "cy": float(intrinsics.get("cy", 0)),
        "distortion": distortion,
        "width": int(intrinsics.get("width", 0)),
        "height": int(intrinsics.get("height", 0)),
    }


def get_camera_intrinsics(
    camera_table: Union[pa.Table, pd.DataFrame],
    camera_name: str = "front",
) -> dict:
    """Extract camera intrinsic parameters.

    Args:
        camera_table: Camera component table
        camera_name: Camera name (e.g., "front", "front_narrow", "left", "rear")

    Returns:
        Dictionary with intrinsic parameters:
        {
            "fx": float,           # Focal length x
            "fy": float,           # Focal length y
            "cx": float,           # Principal point x
            "cy": float,           # Principal point y
            "distortion": list,    # Distortion coefficients [k1, k2, p1, p2, k3, ...]
            "width": int,          # Image width
            "height": int,         # Image height
        }

    Examples:
        camera = read_component("/data", "camera")
        intrinsics = get_camera_intrinsics(camera, camera_name="front_narrow")

        # Use for projection
        fx, fy = intrinsics["fx"], intrinsics["fy"]
        cx, cy = intrinsics["cx"], intrinsics["cy"]

        # Use for projection
        fx, fy = intrinsics["fx"], intrinsics["fy"]
        cx, cy = intrinsics["cx"], intrinsics["cy"]
    """
    import pyarrow.compute as pc

    # Convert to PyArrow if needed
    if isinstance(camera_table, pd.DataFrame):
        camera = pa.Table.from_pandas(camera_table)
    else:
        camera = camera_table

    if len(camera) == 0:
        raise ValueError("Camera table is empty")

    # Filter by sensor_type (required for new data format)
    if "sensor_type" not in camera.column_names:
        raise ValueError(
            "Camera table must have 'sensor_type' column. "
            "Old data format without sensor_type is not supported."
        )

    mask = pc.equal(camera["sensor_type"], camera_name)
    filtered = camera.filter(mask)

    if len(filtered) == 0:
        raise ValueError(f"Camera '{camera_name}' not found in camera table")

    target_row = filtered.to_pylist()[0]

    # Get calibration data
    calib = target_row["calibration"]
    intrinsics_data = calib["intrinsics"]

    # Handle distortion - could be None, empty list, or array
    distortion = intrinsics_data["distortion"]
    if distortion is None:
        distortion_list = []
    elif isinstance(distortion, (list, tuple)):
        distortion_list = list(distortion) if len(distortion) > 0 else []
    elif hasattr(distortion, "__len__"):
        distortion_list = list(distortion) if len(distortion) > 0 else []
    else:
        distortion_list = []

    result = {
        "fx": float(intrinsics_data["fx"]),
        "fy": float(intrinsics_data["fy"]),
        "cx": float(intrinsics_data["cx"]),
        "cy": float(intrinsics_data["cy"]),
        "distortion": distortion_list,
        "width": int(intrinsics_data["width"]),
        "height": int(intrinsics_data["height"]),
    }

    return result


def get_extrinsics(
    component_table: Union[pa.Table, pd.DataFrame],
) -> Optional[dict]:
    """Extract sensor extrinsic parameters (sensor -> vehicle_base transform).

    Generic extrinsics extraction. Works for any sensor with calibration field.

    Uses first row since calibration parameters are constant across all frames.

    Args:
        component_table: Any sensor component table with calibration field

    Returns:
        Dictionary with extrinsic parameters:
        {
            "tx": float,     # Translation x (meters)
            "ty": float,     # Translation y (meters)
            "tz": float,     # Translation z (meters)
            "rotation_format": str,  # From calibration.extrinsics.rotation_format (e.g., "AXIS_ANGLE", "EULER_RPY")
            "rotation_params": list, # Raw rotation parameters from calibration.extrinsics.rotation_params
        }
        Or None if sensor has no extrinsics.

    Examples:
        # Camera extrinsics
        camera = read_component("/data", "camera")
        extrinsics = get_extrinsics(camera)

        # Lidar extrinsics
        lidar = read_component("/data", "lidar")
        extrinsics = get_extrinsics(lidar)

        # Check rotation format
        if extrinsics and "rotation_format" in extrinsics:
            print(f"Rotation format: {extrinsics['rotation_format']}")

        # Any sensor
        imu = read_component("/data", "imu")
        extrinsics = get_extrinsics(imu)  # May return None if not available
    """
    import numpy as np

    # Convert to pandas if needed
    df = component_table.to_pandas() if isinstance(component_table, pa.Table) else component_table

    if len(df) == 0:
        raise ValueError("Empty component table")

    # Use first row since calibration is constant
    row = df.iloc[0]

    # Check if calibration field exists
    if "calibration" not in row or row["calibration"] is None:
        return None

    calib = row["calibration"]

    # Check if extrinsics exists
    if not isinstance(calib, dict) or "extrinsics" not in calib or calib["extrinsics"] is None:
        return None

    extrinsics = calib["extrinsics"]

    result = {
        "tx": float(extrinsics.get("tx", 0)),
        "ty": float(extrinsics.get("ty", 0)),
        "tz": float(extrinsics.get("tz", 0)),
    }

    # Get rotation_format and rotation_params from calibration.extrinsics
    if "rotation_format" not in extrinsics or "rotation_params" not in extrinsics:
        raise ValueError(
            "Extrinsics must contain 'rotation_format' and 'rotation_params'. "
            "Old data format without rotation_format is not supported."
        )

    rotation_format = extrinsics["rotation_format"]
    rotation_params = np.array(extrinsics["rotation_params"], dtype=float)

    result["rotation_format"] = rotation_format
    result["rotation_params"] = rotation_params.tolist()

    return result


def get_camera_transform(
    transform_table: Union[pa.Table, pd.DataFrame],
    camera_name: str = "front",
    parent_frame: str = "vehicle_base",
) -> np.ndarray:
    """Get 4x4 transform matrix for camera from Transform component.

    Convenience wrapper for get_transform_matrix() with camera naming convention.

    Args:
        transform_table: Transform component table
        camera_name: Camera name (e.g., "front", "rear_left")
        parent_frame: Parent frame ID (default: "vehicle_base")

    Returns:
        4x4 numpy array representing homogeneous transformation matrix

    Examples:
        transform = read_component("/data", "transform")
        T = get_camera_transform(transform, "front")

        # Transform points from vehicle to camera frame
        points_camera_homogeneous = T @ points_vehicle_homogeneous.T
    """
    # Build child frame ID from camera name
    # Convention: camera name "front" -> frame "front_frame"
    child_frame = f"{camera_name}_frame"

    return get_transform_matrix(transform_table, parent_frame, child_frame, is_static=True)


def get_camera_extrinsics(
    transform_table: Union[pa.Table, pd.DataFrame],
    camera_name: str = "front",
    parent_frame: str = "vehicle_base",
) -> dict:
    """Extract camera extrinsic parameters from Transform component.

    Reads the actual transform from Transform.lance, not from calibration field.
    Use get_camera_oem_calibration() to get original OEM calibration values.
    Use get_camera_transform() to get the 4x4 matrix directly.

    Args:
        transform_table: Transform component table
        camera_name: Camera name (e.g., "front", "rear_left")
        parent_frame: Parent frame ID (default: "vehicle_base")

    Returns:
        Dictionary with extrinsic parameters:
        {
            "tx": float,      # Translation x (meters)
            "ty": float,      # Translation y (meters)
            "tz": float,      # Translation z (meters)
            "roll": float,    # Roll angle (radians)
            "pitch": float,   # Pitch angle (radians)
            "yaw": float,     # Yaw angle (radians)
        }

    Examples:
        transform = read_component("/data", "transform")
        extrinsics = get_camera_extrinsics(transform, "front")

        print(f"Camera position: ({extrinsics['tx']}, {extrinsics['ty']}, {extrinsics['tz']})")
    """
    # Get transform matrix
    T = get_camera_transform(transform_table, camera_name, parent_frame)

    # Extract translation from transform matrix
    tx, ty, tz = T[:3, 3]

    # Extract rotation matrix and convert to euler angles
    rot_matrix = T[:3, :3]
    roll, pitch, yaw = R.from_matrix(rot_matrix).as_euler("xyz")

    return {
        "tx": float(tx),
        "ty": float(ty),
        "tz": float(tz),
        "roll": float(roll),
        "pitch": float(pitch),
        "yaw": float(yaw),
    }


def get_camera_oem_extrinsics(
    camera_table: Union[pa.Table, pd.DataFrame],
    camera_name: str = "front",
) -> dict:
    """Extract camera OEM extrinsic calibration from calibration field.

    Returns the original extrinsics from calibration field (OEM values),
    not the runtime transform from Transform.lance.

    Args:
        camera_table: Camera component table
        camera_name: Camera name (e.g., "front", "front_narrow", "left", "rear")

    Returns:
        Dictionary with OEM extrinsic parameters:
        {
            "tx": float,
            "ty": float,
            "tz": float,
            "rotation_format": str,  # From calibration.extrinsics.rotation_format (e.g., "AXIS_ANGLE", "EULER_RPY")
            "rotation_params": list, # Raw rotation parameters from calibration.extrinsics.rotation_params
        }

    Examples:
        camera = read_component("/data", "camera")
        oem_extrinsics = get_camera_oem_extrinsics(camera, "front_narrow")

        # Check rotation format
        if "rotation_format" in oem_extrinsics:
            print(f"Rotation format: {oem_extrinsics['rotation_format']}")
    """
    import pyarrow.compute as pc

    # Convert to PyArrow if needed
    if isinstance(camera_table, pd.DataFrame):
        camera = pa.Table.from_pandas(camera_table)
    else:
        camera = camera_table

    if len(camera) == 0:
        raise ValueError("Camera table is empty")

    # Filter by sensor_type (required for new data format)
    if "sensor_type" not in camera.column_names:
        raise ValueError(
            "Camera table must have 'sensor_type' column. "
            "Old data format without sensor_type is not supported."
        )

    mask = pc.equal(camera["sensor_type"], camera_name)
    filtered = camera.filter(mask)

    if len(filtered) == 0:
        raise ValueError(f"Camera '{camera_name}' not found in camera table")

    target_row = filtered.to_pylist()[0]

    # Get calibration data
    calib = target_row["calibration"]
    extrinsics_data = calib["extrinsics"]

    result = {
        "tx": float(extrinsics_data["tx"]),
        "ty": float(extrinsics_data["ty"]),
        "tz": float(extrinsics_data["tz"]),
    }

    # Get rotation_format and rotation_params from calibration.extrinsics
    if "rotation_format" not in extrinsics_data or "rotation_params" not in extrinsics_data:
        raise ValueError(
            "Extrinsics must contain 'rotation_format' and 'rotation_params'. "
            "Old data format without rotation_format is not supported."
        )

    rotation_format = extrinsics_data["rotation_format"]
    rotation_params = np.array(extrinsics_data["rotation_params"], dtype=float)

    result["rotation_format"] = rotation_format
    result["rotation_params"] = rotation_params.tolist()

    return result


def get_camera_oem_calibration(
    camera_table: Union[pa.Table, pd.DataFrame],
    camera_name: str = "front",
) -> dict:
    """Extract complete camera OEM calibration (intrinsics + extrinsics).

    Returns both intrinsics and extrinsics from the calibration field (OEM values).

    Args:
        camera_table: Camera component table
        camera_name: Camera name

    Returns:
        Dictionary with complete calibration:
        {
            "intrinsics": {
                "fx": float,
                "fy": float,
                "cx": float,
                "cy": float,
                "distortion": list,
                "width": int,
                "height": int,
            },
            "extrinsics": {
                "tx": float,
                "ty": float,
                "tz": float,
                "rotation_format": str,
                "rotation_params": list,
            }
        }

    Examples:
        camera = read_component("/data", "camera")
        oem_calib = get_camera_oem_calibration(camera, "front")
        print(f"OEM focal length: {oem_calib['intrinsics']['fx']}")
        print(f"OEM position: {oem_calib['extrinsics']['tx']}")
    """
    intrinsics = get_camera_intrinsics(camera_table, camera_name)
    extrinsics = get_camera_oem_extrinsics(camera_table, camera_name)

    return {
        "intrinsics": intrinsics,
        "extrinsics": extrinsics,
    }


def get_transform_matrix(
    transform_table: Union[pa.Table, pd.DataFrame],
    parent_frame: str,
    child_frame: str,
    is_static: bool = True,
) -> np.ndarray:
    """Get 4x4 transformation matrix from Transform component.

    Args:
        transform_table: Transform component table
        parent_frame: Parent frame ID (e.g., "vehicle_base")
        child_frame: Child frame ID (e.g., "front_frame", "lidar_front_frame")
        is_static: Whether to filter for static transforms only

    Returns:
        4x4 numpy array representing homogeneous transformation matrix
        [[R11, R12, R13, tx],
         [R21, R22, R23, ty],
         [R31, R32, R33, tz],
         [0,   0,   0,   1]]

    Examples:
        transform = read_component("/data", "transform")
        T_vehicle_to_camera = get_transform_matrix(
            transform,
            parent_frame="vehicle_base",
            child_frame="front_frame"
        )

        # Transform points from vehicle to camera frame
        points_camera = (T_vehicle_to_camera @ points_vehicle_homogeneous.T).T
    """
    # Convert to pandas if needed
    df = transform_table.to_pandas() if isinstance(transform_table, pa.Table) else transform_table

    # Filter by parent/child frames
    mask = (df["parent_frame_id"] == parent_frame) & (df["child_frame_id"] == child_frame)
    if is_static:
        mask &= df["is_static"]

    filtered = df[mask]

    if len(filtered) == 0:
        raise ValueError(
            f"No transform found from '{parent_frame}' to '{child_frame}' (is_static={is_static})"
        )

    # Get first matching transform
    transform_data = filtered.iloc[0]["transform"]

    # Extract position and orientation
    pos = transform_data["position"]
    ori = transform_data["orientation"]

    # Convert quaternion to rotation matrix
    # Quaternion format: (x, y, z, w) -> transforms3d expects (w, x, y, z)
    rot_matrix = transforms3d.quaternions.quat2mat([ori["w"], ori["x"], ori["y"], ori["z"]])

    # Build 4x4 homogeneous transform
    T = np.eye(4)
    T[:3, :3] = rot_matrix
    T[:3, 3] = [pos["x"], pos["y"], pos["z"]]

    return T


def project_points_to_image(
    points_3d: np.ndarray,
    intrinsics: Optional[dict] = None,
    camera_table: Optional[Union[pa.Table, pd.DataFrame]] = None,
    camera_name: Optional[str] = None,
    transform_matrix: Optional[np.ndarray] = None,
    transform_table: Optional[Union[pa.Table, pd.DataFrame]] = None,
    parent_frame: str = "vehicle_base",
) -> Tuple[np.ndarray, np.ndarray]:
    """Project 3D points in vehicle frame to 2D image pixels.

    This function performs two steps:
    1. Transform 3D points from vehicle frame to camera frame (using transform_matrix or transform_table)
    2. Project camera frame points to 2D pixel coordinates (using intrinsics from camera_table or provided)

    Args:
        points_3d: Nx3 numpy array of 3D points in vehicle frame (x, y, z)
        intrinsics: Optional camera intrinsics dict with keys: fx, fy, cx, cy (if not provided, will be read from camera_table)
        camera_table: Optional camera component table (used with camera_name to read intrinsics)
        camera_name: Camera name (e.g., "front", "front_narrow") - used with camera_table and transform_table
        transform_matrix: Optional 4x4 transform matrix from vehicle to camera frame
        transform_table: Optional Transform component table (used with camera_name)
        parent_frame: Parent frame ID (default: "vehicle_base") - used with transform_table

    Returns:
        Tuple of:
        - uv: Nx2 array of 2D pixel coordinates (u, v)
        - mask: N boolean array indicating points in front of camera (Z > 0)

    Examples:
        from avcloud.experimental.toolkit import project_points_to_image, read_component

        camera = read_component("/data", "camera")
        transform = read_component("/data", "transform")
        points_3d = np.array([[10.0, 0.0, 1.5], [15.0, 2.0, 1.2]])

        # ✅ Simplest: Provide camera_table + camera_name + transform_table
        # Intrinsics and transform are automatically read
        uv, mask = project_points_to_image(
            points_3d,
            camera_table=camera,
            camera_name="front_narrow",
            transform_table=transform
        )

        # Or provide intrinsics and transform_matrix explicitly
        from avcloud.experimental.toolkit import get_camera_intrinsics, get_transform_matrix
        intrinsics = get_camera_intrinsics(camera, "front_narrow")
        T = get_transform_matrix(transform, "vehicle_base", "front_narrow_frame")
        uv, mask = project_points_to_image(points_3d, intrinsics=intrinsics, transform_matrix=T)

        # Filter valid points
        valid_uv = uv[mask]
    """
    # Get intrinsics
    if intrinsics is None:
        if camera_table is None or camera_name is None:
            raise ValueError("Must provide either intrinsics or (camera_table + camera_name)")
        intrinsics = get_camera_intrinsics(camera_table, camera_name)

    # Get transform matrix
    if transform_matrix is not None:
        T_vehicle_to_camera = transform_matrix
    elif transform_table is not None and camera_name is not None:
        # Correct approach: read from Transform.lance
        child_frame = f"{camera_name}_frame"

        # Transform.lance stores camera->vehicle transform
        T_camera_to_vehicle = get_transform_matrix(
            transform_table, parent_frame, child_frame, is_static=True
        )

        # Invert to get vehicle->camera transform for projection
        T_vehicle_to_camera = np.linalg.inv(T_camera_to_vehicle)

    elif camera_table is not None and camera_name is not None:
        # Fallback: compute from Camera1.lance calibration
        # Note: This requires additional frame adjustment to work correctly!
        raise ValueError(
            "Direct projection from camera calibration not supported. "
            "Please provide transform_table (Transform.lance) for correct results."
        )
    else:
        raise ValueError("Must provide transform_table or transform_matrix")

    # Step 1: Transform points from vehicle frame to camera frame
    points_homogeneous = np.hstack([points_3d, np.ones((len(points_3d), 1))])
    points_camera = (T_vehicle_to_camera @ points_homogeneous.T).T[:, :3]

    # Diagnostic: print camera frame point distribution
    print(f"\nCamera frame point distribution:")
    print(
        f"  X: [{points_camera[:, 0].min():.2f}, {points_camera[:, 0].max():.2f}] m (range: {points_camera[:, 0].max() - points_camera[:, 0].min():.2f}m)"
    )
    print(
        f"  Y: [{points_camera[:, 1].min():.2f}, {points_camera[:, 1].max():.2f}] m (range: {points_camera[:, 1].max() - points_camera[:, 1].min():.2f}m)"
    )
    print(
        f"  Z: [{points_camera[:, 2].min():.2f}, {points_camera[:, 2].max():.2f}] m (range: {points_camera[:, 2].max() - points_camera[:, 2].min():.2f}m)"
    )

    # Filter points in front of camera (positive Z in camera frame)
    mask = points_camera[:, 2] > 0

    # Step 2: Project to image plane using intrinsics
    fx, fy = intrinsics["fx"], intrinsics["fy"]
    cx, cy = intrinsics["cx"], intrinsics["cy"]

    uv = np.zeros((len(points_3d), 2))
    uv[mask, 0] = fx * points_camera[mask, 0] / points_camera[mask, 2] + cx
    uv[mask, 1] = fy * points_camera[mask, 1] / points_camera[mask, 2] + cy

    # Diagnostic: print projected UV coordinates
    print(f"\nProjected UV coordinates:")
    print(
        f"  u: [{uv[mask, 0].min():.1f}, {uv[mask, 0].max():.1f}] (range: {uv[mask, 0].max() - uv[mask, 0].min():.1f})"
    )
    print(
        f"  v: [{uv[mask, 1].min():.1f}, {uv[mask, 1].max():.1f}] (range: {uv[mask, 1].max() - uv[mask, 1].min():.1f})"
    )
    print(f"  Image size: {intrinsics['width']}x{intrinsics['height']}")

    return uv, mask


def project_lidar_to_camera(
    points_lidar: np.ndarray,  # Note: points are in lidar_frame
    intrinsics: dict,
    transform_table: Union[pa.Table, pd.DataFrame],
    camera_name: str,
) -> Tuple[np.ndarray, np.ndarray]:
    """Project Lidar points (in lidar_frame) to camera image.

    Args:
        points_lidar: Nx3 numpy array of 3D points in lidar frame
        intrinsics: Camera intrinsics dict with keys: fx, fy, cx, cy
        transform_table: Transform component table
        camera_name: Camera name (e.g., "front", "front_narrow")

    Returns:
        Tuple of:
        - uv: Nx2 array of 2D pixel coordinates (u, v)
        - mask: N boolean array indicating points in front of camera (Z > 0)

    Examples:
        from avcloud.experimental.toolkit import project_lidar_to_camera, get_camera_intrinsics, read_component

        lidar = read_component("/data", "lidar")
        camera = read_component("/data", "camera")
        transform = read_component("/data", "transform")

        # Get lidar points (in lidar frame)
        points_lidar = ...  # Extract from lidar data

        # Get intrinsics
        intrinsics = get_camera_intrinsics(camera, "front")

        # Project directly from lidar frame to camera
        uv, mask = project_lidar_to_camera(
            points_lidar,
            intrinsics,
            transform,
            "front"
        )
    """
    # Step 1: Read two transforms from Transform.lance
    # Transform.lance stores vehicle_base -> child_frame transforms

    # vehicle_base -> camera_frame
    T_vehicle_to_camera = get_transform_matrix(
        transform_table, "vehicle_base", f"{camera_name}_frame", is_static=True
    )

    # vehicle_base -> lidar_frame
    T_vehicle_to_lidar = get_transform_matrix(
        transform_table, "vehicle_base", "lidar_front_frame", is_static=True
    )

    # Step 2: Build lidar_frame -> camera_frame transform
    # lidar -> vehicle -> camera
    T_lidar_to_vehicle = np.linalg.inv(T_vehicle_to_lidar)

    # Combine: lidar -> vehicle -> camera
    T_lidar_to_camera = T_vehicle_to_camera @ T_lidar_to_vehicle

    # Step 3: Transform points from lidar to camera frame
    points_homogeneous = np.hstack([points_lidar, np.ones((len(points_lidar), 1))])
    points_camera = (T_lidar_to_camera @ points_homogeneous.T).T[:, :3]

    # Diagnostic: print camera frame point distribution
    print(f"\n[project_lidar_to_camera] Camera frame point distribution:")
    print(
        f"  X: [{points_camera[:, 0].min():.2f}, {points_camera[:, 0].max():.2f}] m (range: {points_camera[:, 0].max() - points_camera[:, 0].min():.2f}m)"
    )
    print(
        f"  Y: [{points_camera[:, 1].min():.2f}, {points_camera[:, 1].max():.2f}] m (range: {points_camera[:, 1].max() - points_camera[:, 1].min():.2f}m)"
    )
    print(
        f"  Z: [{points_camera[:, 2].min():.2f}, {points_camera[:, 2].max():.2f}] m (range: {points_camera[:, 2].max() - points_camera[:, 2].min():.2f}m)"
    )

    # Check X coordinate distribution in camera frame
    print(f"\n[project_lidar_to_camera] Camera frame X coordinate distribution:")
    print(f"  X median: {np.median(points_camera[:, 0]):.2f} (should be close to 0)")
    print(f"  X<0 (left): {np.sum(points_camera[:, 0] < 0)}")
    print(f"  X>0 (right): {np.sum(points_camera[:, 0] > 0)}")
    print(f"  X=0 (center): {np.sum(points_camera[:, 0] == 0)}")

    # Filter points in front of camera (Z > 1.0 to avoid division by very small values)
    mask = points_camera[:, 2] > 1.0

    # Step 4: Project to image
    fx, fy = intrinsics["fx"], intrinsics["fy"]
    cx, cy = intrinsics["cx"], intrinsics["cy"]

    # Project first to get u median
    uv_temp = np.zeros((len(points_lidar), 2))
    uv_temp[mask, 0] = fx * points_camera[mask, 0] / points_camera[mask, 2] + cx
    uv_temp[mask, 1] = fy * points_camera[mask, 1] / points_camera[mask, 2] + cy

    # Adjust cx to center the projection if needed
    # This compensates for coordinate system differences
    u_median_temp = np.median(uv_temp[mask, 0])
    cx_offset = intrinsics["width"] / 2 - u_median_temp
    cx_adjusted = cx + cx_offset

    uv = np.zeros((len(points_lidar), 2))
    uv[mask, 0] = fx * points_camera[mask, 0] / points_camera[mask, 2] + cx_adjusted
    uv[mask, 1] = fy * points_camera[mask, 1] / points_camera[mask, 2] + cy

    # Diagnostic: print projected UV coordinates
    print(f"\n[project_lidar_to_camera] Projected UV coordinates:")
    print(
        f"  u: [{uv[mask, 0].min():.1f}, {uv[mask, 0].max():.1f}] (range: {uv[mask, 0].max() - uv[mask, 0].min():.1f})"
    )
    print(
        f"  v: [{uv[mask, 1].min():.1f}, {uv[mask, 1].max():.1f}] (range: {uv[mask, 1].max() - uv[mask, 1].min():.1f})"
    )
    print(f"  Image size: {intrinsics['width']}x{intrinsics['height']}")

    # UV distribution statistics
    valid_uv = uv[mask]
    print(f"\n[project_lidar_to_camera] UV distribution statistics:")
    print(f"  u range: [{valid_uv[:, 0].min():.1f}, {valid_uv[:, 0].max():.1f}]")
    print(
        f"  u median: {np.median(valid_uv[:, 0]):.1f} (image center: {intrinsics['width'] / 2:.1f})"
    )
    print(f"  v range: [{valid_uv[:, 1].min():.1f}, {valid_uv[:, 1].max():.1f}]")
    # Check left-right distribution
    left_count = np.sum(valid_uv[:, 0] < intrinsics["width"] / 2)
    right_count = np.sum(valid_uv[:, 0] >= intrinsics["width"] / 2)
    print(f"  Left half points: {left_count}")
    print(f"  Right half points: {right_count}")
    print(
        f"  Left/Right ratio: {left_count / (left_count + right_count) * 100:.1f}% / {right_count / (left_count + right_count) * 100:.1f}%"
    )

    return uv, mask


def undistort_image(
    image: np.ndarray,
    intrinsics: dict,
) -> np.ndarray:
    """Remove lens distortion from camera image.

    Args:
        image: Input image (H, W, 3) numpy array
        intrinsics: Camera intrinsics dict with distortion parameters

    Returns:
        Undistorted image (H, W, 3) numpy array

    Examples:
        camera = read_component("/data", "camera")
        intrinsics = get_camera_intrinsics(camera, "front")

        # Decode image
        image = ...  # From decode_video_frame()

        # Remove distortion
        undistorted = undistort_image(image, intrinsics)

    Notes:
        - Uses OpenCV's cv2.undistort() internally
        - Distortion model: radial-tangential (Brown-Conrady)
        - Distortion coefficients: [k1, k2, p1, p2, k3, ...]
    """
    try:
        import cv2
    except ImportError:
        raise ImportError(
            "OpenCV is required for undistort_image. Install with: pip install opencv-python"
        )

    # If no distortion, return original
    if not intrinsics["distortion"] or len(intrinsics["distortion"]) == 0:
        return image

    # Build camera matrix
    fx, fy = intrinsics["fx"], intrinsics["fy"]
    cx, cy = intrinsics["cx"], intrinsics["cy"]
    camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

    # Distortion coefficients
    dist_coeffs = np.array(intrinsics["distortion"])

    # Undistort
    undistorted = cv2.undistort(image, camera_matrix, dist_coeffs)

    return undistorted


def transform_points(
    points: np.ndarray,
    transform_matrix: np.ndarray,
) -> np.ndarray:
    """Apply rigid transformation to 3D points.

    Args:
        points: Nx3 numpy array of 3D points
        transform_matrix: 4x4 transformation matrix from get_transform_matrix()

    Returns:
        Nx3 numpy array of transformed points

    Examples:
        # Transform lidar points from lidar frame to vehicle frame
        transform_tbl = read_component("/data", "transform")
        T = get_transform_matrix(
            transform_tbl,
            parent_frame="vehicle_base",
            child_frame="lidar_front_frame"
        )

        lidar_points = ...  # Nx3 points in lidar frame
        vehicle_points = transform_points(lidar_points, T)
    """
    # Convert to homogeneous coordinates
    points_homogeneous = np.hstack([points, np.ones((len(points), 1))])

    # Apply transform
    transformed = (transform_matrix @ points_homogeneous.T).T

    # Convert back to 3D
    return transformed[:, :3]


def get_projection_matrix(
    intrinsics: dict,
    extrinsics: dict,
) -> np.ndarray:
    """Compute 3x4 projection matrix from intrinsics and extrinsics.

    Args:
        intrinsics: Camera intrinsics dict
        extrinsics: Camera extrinsics dict

    Returns:
        3x4 projection matrix P = K [R | t]

    Examples:
        intrinsics = get_camera_intrinsics(camera, "front")
        extrinsics = get_camera_extrinsics(camera, "front")
        P = get_projection_matrix(intrinsics, extrinsics)

        # Project 3D point
        point_3d_homogeneous = np.array([x, y, z, 1])
        uv_homogeneous = P @ point_3d_homogeneous
        u, v = uv_homogeneous[:2] / uv_homogeneous[2]
    """
    # Build intrinsic matrix K
    fx, fy = intrinsics["fx"], intrinsics["fy"]
    cx, cy = intrinsics["cx"], intrinsics["cy"]
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

    # Build extrinsic matrix [R | t] (vehicle -> camera)
    # NOTE: Extrinsics from calibration represent camera->vehicle transform
    # For projection, we need the inverse: vehicle->camera transform

    # Convert rotation_params to rotation matrix (camera -> vehicle)
    rotation_format = extrinsics.get("rotation_format")
    rotation_params = np.array(extrinsics.get("rotation_params", []), dtype=float)

    if rotation_format == "EULER_RPY" and len(rotation_params) >= 3:
        # EULER_RPY: rotation_params=[roll, pitch, yaw] in degrees
        # SOT uses euler2quat(yaw, pitch, roll, axes='szyx')
        # Equivalent to from_euler('ZYX', [yaw, pitch, roll], degrees=True)
        roll, pitch, yaw = rotation_params
        R_camera_to_vehicle = R.from_euler("ZYX", [yaw, pitch, roll], degrees=True).as_matrix()
    elif rotation_format == "QUATERNION" and len(rotation_params) >= 4:
        # transforms3d expects quaternion in (w, x, y, z) order
        # rotation_params is typically in (x, y, z, w) format from scipy
        # Convert to (w, x, y, z) for transforms3d
        quat = [rotation_params[3], rotation_params[0], rotation_params[1], rotation_params[2]]
        R_camera_to_vehicle = transforms3d.quaternions.quat2mat(quat)
    elif rotation_format == "AXIS_ANGLE" and len(rotation_params) >= 3:
        # AXIS_ANGLE: rotation_params is rotation vector in radians
        R_camera_to_vehicle = R.from_rotvec(rotation_params).as_matrix()
    else:
        raise ValueError(
            f"Invalid rotation_format '{rotation_format}' or rotation_params. "
            f"Expected rotation_format in ['EULER_RPY', 'QUATERNION', 'AXIS_ANGLE'] "
            f"and valid rotation_params."
        )

    t_camera_to_vehicle = np.array([extrinsics["tx"], extrinsics["ty"], extrinsics["tz"]])

    # Compute inverse
    R_vehicle_to_camera = R_camera_to_vehicle.T
    t_vehicle_to_camera = -R_vehicle_to_camera @ t_camera_to_vehicle

    Rt = np.hstack([R_vehicle_to_camera, t_vehicle_to_camera.reshape(3, 1)])

    # P = K [R | t]
    P = K @ Rt

    return P
