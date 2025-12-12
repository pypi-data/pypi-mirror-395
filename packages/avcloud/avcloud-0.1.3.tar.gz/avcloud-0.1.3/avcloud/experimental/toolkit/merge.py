"""Merge utilities for combining Lance component tables."""

from typing import List, Set, Union

import pandas as pd
import pyarrow as pa


def _select_key_columns(df: pd.DataFrame, key_prefix: str = "") -> Set[str]:
    """Select key columns for merging.

    If key_prefix is provided, select columns starting with that prefix.
    Otherwise, use common key column names.
    """
    if key_prefix:
        return set([c for c in df.columns if c.startswith(key_prefix)])

    # Common key columns in our schema
    common_keys = {
        "scene_id",
        "run_id",
        "frame_timestamp",
        "frame_id",
        "sensor_timestamp",
        "sensor_frame_id",
    }
    return set(df.columns) & common_keys


def _how(left_nullable: bool = False, right_nullable: bool = False) -> str:
    """Determine join type from nullable flags."""
    if left_nullable and right_nullable:
        return "outer"
    elif left_nullable and not right_nullable:
        return "right"
    elif not left_nullable and right_nullable:
        return "left"
    else:
        return "inner"


def _cast_keys(src: pd.DataFrame, dst: pd.DataFrame, keys: Set[str]):
    """Cast key columns in dst to match src dtypes."""
    for key in keys:
        if key in dst.columns and key in src.columns:
            if dst[key].dtype != src[key].dtype:
                dst[key] = dst[key].astype(src[key].dtype)


def _group_by(src: pd.DataFrame, keys: Set[str]) -> pd.DataFrame:
    """Group DataFrame by keys, aggregating other columns into lists."""
    dst = src.groupby(list(keys)).agg(list).reset_index()
    # Fix key types automatically created from the MultiIndex
    _cast_keys(src, dst, keys)
    return dst


def merge(
    left: Union[pa.Table, pd.DataFrame],
    right: Union[pa.Table, pd.DataFrame],
    left_nullable: bool = False,
    right_nullable: bool = False,
    left_group: bool = False,
    right_group: bool = False,
    keys: List[str] = None,
    key_prefix: str = "",
) -> pa.Table:
    """Merge two component tables using pandas DataFrame.merge().

    Like Waymo's v2.merge() - converts to pandas, merges, converts back.
    This handles struct columns naturally since pandas treats them as objects.

    Args:
        left: Left PyArrow table or pandas DataFrame
        right: Right PyArrow table or pandas DataFrame
        left_nullable: If True, output may contain rows where only right columns
                      are present (LEFT join)
        right_nullable: If True, output may contain rows where only left columns
                       are present (RIGHT join)
        left_group: If True, group left table by common keys
        right_group: If True, group right table by common keys
        keys: Explicit list of key columns (auto-detected if None)
        key_prefix: String prefix for auto-detecting key columns (e.g. 'key.')

    Returns:
        Merged PyArrow table

    Examples:
        # Simple merge - auto-detects keys
        camera_table = read_component('/data', 'camera')
        imu_table = read_component('/data', 'imu')
        merged = merge(camera_table, imu_table)

        # Group right side - all IMU measurements per camera frame
        merged = merge(camera_table, imu_table, right_group=True)

        # Explicit keys
        merged = merge(camera_table, imu_table, keys=['scene_id', 'run_id'])

        # Left outer join
        merged = merge(camera_table, imu_table, right_nullable=True)
    """
    # Convert to pandas if needed
    left_df = left.to_pandas() if isinstance(left, pa.Table) else left
    right_df = right.to_pandas() if isinstance(right, pa.Table) else right

    # Determine keys
    # Always detect what keys each table has (for grouping logic)
    left_keys = _select_key_columns(left_df, key_prefix)
    right_keys = _select_key_columns(right_df, key_prefix)

    if keys is not None:
        # Use explicitly provided keys
        common_keys = set(keys)
    else:
        # Auto-detect common keys
        common_keys = left_keys.intersection(right_keys)

        if not common_keys:
            raise ValueError(
                f"No common key columns found. "
                f"Left keys: {sorted(left_keys)}, "
                f"Right keys: {sorted(right_keys)}"
            )

    # Group if requested (like Waymo)
    # Group when table has MORE keys than the keys we're merging on
    # E.g., if left has [scene_id, run_id, camera_id] but we merge on [scene_id, run_id],
    # group by [scene_id, run_id] to aggregate multiple camera_id values
    if left_group and left_keys != common_keys:
        left_df = _group_by(left_df, common_keys)
    if right_group and right_keys != common_keys:
        right_df = _group_by(right_df, common_keys)

    # Perform pandas merge (handles struct columns naturally!)
    merged_df = left_df.merge(
        right_df, on=list(common_keys), how=_how(left_nullable, right_nullable)
    )

    # Convert back to PyArrow
    return pa.Table.from_pandas(merged_df)


def merge_temporal(
    left: Union[pa.Table, pd.DataFrame],
    right: Union[pa.Table, pd.DataFrame],
    on: List[str] = None,
    timestamp_column: str = "frame_timestamp",
    tolerance: pd.Timedelta = None,
    direction: str = "nearest",
) -> pa.Table:
    """Merge tables by temporal alignment (time-based nearest neighbor).

    For multi-rate sensors (e.g., camera 10Hz, IMU 100Hz), this does temporal
    alignment instead of Cartesian product. Each left row gets matched to the
    closest right row by timestamp.

    Uses pandas merge_asof() which is designed for time-series data.

    Args:
        left: Left table (typically lower frequency, e.g., camera)
        right: Right table (typically higher frequency, e.g., IMU)
        on: Columns to match exactly (e.g., ['scene_id', 'run_id'])
        timestamp_column: Column name for timestamps (default: 'frame_timestamp')
        tolerance: Maximum time difference allowed (default: None = no limit)
        direction: 'backward', 'forward', or 'nearest' (default: 'nearest')

    Returns:
        Merged table with 1-1 correspondence (one right row per left row)

    Examples:
        # Match each camera frame to nearest IMU reading
        camera = read_component('/data', 'camera')
        imu = read_component('/data', 'imu')
        merged = merge_temporal(
            camera, imu,
            on=['scene_id', 'run_id'],
            tolerance=pd.Timedelta('100ms')
        )

        # Result: same number of rows as camera (1-1 matching)
    """
    # Convert to pandas
    left_df = left.to_pandas() if isinstance(left, pa.Table) else left.copy()
    right_df = right.to_pandas() if isinstance(right, pa.Table) else right.copy()

    # Ensure timestamp columns are sorted
    left_df = left_df.sort_values(timestamp_column)
    right_df = right_df.sort_values(timestamp_column)

    # Use merge_asof for temporal alignment
    if on is None:
        # No grouping columns, just match by time
        merged_df = pd.merge_asof(
            left_df,
            right_df,
            on=timestamp_column,
            direction=direction,
            tolerance=tolerance,
        )
    else:
        # Match by exact keys AND closest time
        merged_df = pd.merge_asof(
            left_df,
            right_df,
            on=timestamp_column,
            by=on,
            direction=direction,
            tolerance=tolerance,
        )

    # Convert back to PyArrow
    return pa.Table.from_pandas(merged_df)


def merge_temporal_window(
    left: Union[pa.Table, pd.DataFrame],
    right: Union[pa.Table, pd.DataFrame],
    on: List[str] = None,
    left_timestamp: str = "frame_timestamp",
    right_timestamp: str = None,
    window: pd.Timedelta = None,
    window_start: pd.Timedelta = None,
    window_end: pd.Timedelta = None,
) -> pa.Table:
    """Merge tables by aggregating all right rows within a time window.

    Unlike merge_temporal() which does 1-1 matching, this function collects ALL
    right table rows within a time window around each left row timestamp.

    This is useful for:
    - Collecting all high-frequency sensor readings (IMU 100Hz) for each
      low-frequency event (Camera 10Hz)
    - Preparing training samples with temporal context
    - Analyzing sensor behavior during specific events

    Args:
        left: Left table (typically lower frequency, e.g., camera)
        right: Right table (typically higher frequency, e.g., IMU)
        on: Columns to match exactly (e.g., ['scene_id', 'run_id'])
        left_timestamp: Timestamp column in left table (default: 'frame_timestamp')
        right_timestamp: Timestamp column in right table (default: same as left_timestamp)
        window: Symmetric time window (e.g., pd.Timedelta('50ms') means ±50ms)
        window_start: Start of time window relative to left timestamp (e.g., '-100ms')
        window_end: End of time window relative to left timestamp (e.g., '+100ms')

    Returns:
        Merged table where right columns become lists containing all values
        within the time window. Same number of rows as left table.

    Examples:
        # Collect all IMU readings within ±50ms of each camera frame
        camera = read_component('/data', 'camera')
        imu = read_component('/data', 'imu')
        merged = merge_temporal_window(
            camera, imu,
            on=['scene_id', 'run_id'],
            left_timestamp='frame_timestamp',
            right_timestamp='sensor_timestamp',
            window=pd.Timedelta('50ms')
        )

        # Result: same rows as camera, but IMU columns are lists
        df = merged.to_pandas()
        print(df.iloc[0]['frame_id'])  # [[...], [...], ...] (lists of lists)

        # Asymmetric window: look back 100ms, no look ahead
        merged = merge_temporal_window(
            camera, imu,
            on=['scene_id'],
            left_timestamp='frame_timestamp',
            right_timestamp='sensor_timestamp',
            window_start=pd.Timedelta('-100ms'),
            window_end=pd.Timedelta('0ms')
        )
    """
    # Convert to pandas
    left_df = left.to_pandas() if isinstance(left, pa.Table) else left.copy()
    right_df = right.to_pandas() if isinstance(right, pa.Table) else right.copy()

    # Default right_timestamp to left_timestamp if not specified
    if right_timestamp is None:
        right_timestamp = left_timestamp

    # Determine time window
    if window is not None:
        # Symmetric window
        window_start = -abs(window)
        window_end = abs(window)
    elif window_start is None or window_end is None:
        raise ValueError(
            "Must specify either 'window' (symmetric) or both "
            "'window_start' and 'window_end' (asymmetric)"
        )

    # Sort by timestamp for efficiency
    left_df = left_df.sort_values(left_timestamp).reset_index(drop=True)
    right_df = right_df.sort_values(right_timestamp).reset_index(drop=True)

    # Get columns to aggregate from right table
    # Exclude: 'on' keys (already in left), but INCLUDE right_timestamp (as list)
    exclude_cols = set()
    if on:
        exclude_cols.update(on)

    right_agg_cols = [col for col in right_df.columns if col not in exclude_cols]

    # Prepare result DataFrame starting with left
    result_df = left_df.copy()

    # Initialize aggregated columns as empty lists
    for col in right_agg_cols:
        result_df[col] = [[] for _ in range(len(result_df))]

    # For each left row, find matching right rows in time window
    if on:
        # Group by 'on' keys for efficiency
        for keys, left_group in left_df.groupby(on):
            # Filter right table to same keys
            if isinstance(keys, tuple):
                mask = True
                for i, key_col in enumerate(on):
                    mask &= right_df[key_col] == keys[i]
            else:
                mask = right_df[on[0]] == keys

            right_filtered = right_df[mask]

            # For each row in this group
            for left_idx in left_group.index:
                left_time = left_df.loc[left_idx, left_timestamp]

                # Find right rows in time window
                time_mask = (right_filtered[right_timestamp] >= left_time + window_start) & (
                    right_filtered[right_timestamp] <= left_time + window_end
                )
                matched_right = right_filtered[time_mask]

                # Aggregate matched rows into lists
                for col in right_agg_cols:
                    result_df.at[left_idx, col] = matched_right[col].tolist()
    else:
        # No grouping, check all right rows for each left row
        for left_idx in range(len(left_df)):
            left_time = left_df.loc[left_idx, left_timestamp]

            # Find right rows in time window
            time_mask = (right_df[right_timestamp] >= left_time + window_start) & (
                right_df[right_timestamp] <= left_time + window_end
            )
            matched_right = right_df[time_mask]

            # Aggregate matched rows into lists
            for col in right_agg_cols:
                result_df.at[left_idx, col] = matched_right[col].tolist()

    # Convert back to PyArrow
    return pa.Table.from_pandas(result_df)
