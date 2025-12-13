"""IO utilities for reading Lance components."""

from pathlib import Path
from typing import Dict, List, Optional

import lance
import pyarrow as pa

# Component tags mapping to Lance folder names
COMPONENT_TAGS = {
    "camera": "Camera.lance",
    "lidar": "Lidar.lance",
    "imu": "Imu.lance",
    "gnss": "Gnss.lance",
    "vehicle_state": "VehicleState.lance",
    "transform": "Transform.lance",
    "wheel_odometry": "WheelOdometry.lance",
    "summary": "Summary.lance",
}


def _lance_filter_in(column: str, values: List[str]) -> str:
    """Build a Lance filter for IN operation."""
    if not values:
        return f"{column} IN ()"
    # Escape single quotes
    escaped = [v.replace("'", "''") for v in values]
    quoted = ", ".join([f"'{v}'" for v in escaped])
    return f"{column} IN ({quoted})"


def get_schema(
    base_path: str,
    component_tag: str,
) -> pa.Schema:
    """Get the PyArrow schema for a component.

    Args:
        base_path: Path to downloaded dataset directory
        component_tag: Component tag ('camera', 'lidar', 'imu', 'gnss', etc.)

    Returns:
        PyArrow Schema with field names and types

    Examples:
        # Get camera schema
        schema = get_schema('/data', 'camera')
        print(schema)

        # List all field names
        field_names = [field.name for field in schema]
        print(f"Available fields: {field_names}")

        # Get field types
        for field in schema:
            print(f"{field.name}: {field.type}")
    """
    # Get folder name for component
    folder_name = COMPONENT_TAGS.get(component_tag)
    if not folder_name:
        raise ValueError(
            f"Unknown component tag: {component_tag}. Available: {list(COMPONENT_TAGS.keys())}"
        )

    # Build URI
    uri = str((Path(base_path) / folder_name).as_posix())

    # Open dataset
    try:
        ds = lance.dataset(uri)
    except Exception as e:
        raise FileNotFoundError(
            f"Could not open component '{component_tag}' at {uri}. "
            f"Make sure data is downloaded. Error: {e}"
        )

    return ds.schema


def read_component(
    base_path: str,
    component_tag: str,
    scene_ids: Optional[List[str]] = None,
    columns: Optional[List[str]] = None,
    filter: Optional[str] = None,
) -> pa.Table:
    """Read a Lance component as PyArrow Table.

    Like Waymo's read() function, but for Lance datasets.

    Args:
        base_path: Path to downloaded dataset directory
        component_tag: Component tag ('camera', 'lidar', 'imu', 'gnss', etc.)
        scene_ids: Optional list of scene_ids to filter
        columns: Optional list of columns to read (reads all if None)
        filter: Optional Lance SQL filter expression. Applied at scanner level for efficiency.
                Examples:
                - "camera.front IS NOT NULL"
                - "LENGTH(camera.front) > 0"
                - "sensor_type = 'front_narrow'"
                - "scene_id = 'scene_001' AND camera.front IS NOT NULL"

    Returns:
        PyArrow Table with component data

    Examples:
        # Read all camera data
        camera_table = read_component('/data', 'camera')

        # Read specific scenes
        camera_table = read_component(
            '/data', 'camera',
            scene_ids=['scene_001', 'scene_002']
        )

        # Read specific columns only
        camera_table = read_component(
            '/data', 'camera',
            columns=['scene_id', 'frame_timestamp', 'camera.front']
        )

        # Filter by sensor_type at scanner level (recommended for sparse data)
        camera_table = read_component(
            '/data', 'camera',
            columns=['camera.front_narrow', 'sensor_type'],
            filter="sensor_type = 'front_narrow'"  # Filter at scanner level
        )

        # Combine scene_ids and sensor_type filter
        camera_table = read_component(
            '/data', 'camera',
            scene_ids=['scene_001'],
            columns=['camera.front_narrow', 'sensor_type'],
            filter="sensor_type = 'front_narrow'"
        )
    """
    # Get folder name for component
    folder_name = COMPONENT_TAGS.get(component_tag)
    if not folder_name:
        raise ValueError(
            f"Unknown component tag: {component_tag}. Available: {list(COMPONENT_TAGS.keys())}"
        )

    # Build URI
    uri = str((Path(base_path) / folder_name).as_posix())

    # Open dataset
    try:
        ds = lance.dataset(uri)
    except Exception as e:
        raise FileNotFoundError(
            f"Could not open component '{component_tag}' at {uri}. "
            f"Make sure data is downloaded. Error: {e}"
        )

    # Build scanner with optional filters
    scanner_kwargs = {}
    if columns:
        scanner_kwargs["columns"] = columns

    # Combine scene_ids filter and custom filter
    filter_parts = []
    if scene_ids:
        filter_parts.append(_lance_filter_in("scene_id", scene_ids))
    if filter:
        filter_parts.append(filter)

    if filter_parts:
        scanner_kwargs["filter"] = " AND ".join(filter_parts)

    scanner = ds.scanner(**scanner_kwargs)
    return scanner.to_table()


def read_components(
    base_path: str,
    component_tags: List[str],
    scene_ids: Optional[List[str]] = None,
    columns: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, pa.Table]:
    """Read multiple components at once.

    Args:
        base_path: Path to downloaded dataset
        component_tags: List of component tags to read
        scene_ids: Optional scene_ids to filter (applied to all components)
        columns: Optional dict mapping component_tag to list of columns
                 e.g., {'camera': ['scene_id', 'camera.front'], 'lidar': ['scene_id']}

    Returns:
        Dict mapping component_tag to PyArrow Table

    Example:
        tables = read_components(
            '/data',
            ['camera', 'lidar', 'imu'],
            scene_ids=['scene_001']
        )
        camera_table = tables['camera']
        lidar_table = tables['lidar']
    """
    result = {}
    for tag in component_tags:
        cols = columns.get(tag) if columns else None
        result[tag] = read_component(base_path, tag, scene_ids, cols)
    return result
