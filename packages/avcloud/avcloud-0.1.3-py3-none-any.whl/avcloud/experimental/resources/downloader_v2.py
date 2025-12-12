from __future__ import annotations

"""
Downloader V2

STRICT POLICY (Scene-level atomicity):
- A scene is only COMPLETE if ALL components downloaded successfully
- If any component fails, the entire scene is marked FAILED and partial data is cleaned up
- Failed scenes can be retried with on_exist="replace"

PARALLEL DOWNLOADS:
- Uses max_workers threads for concurrent batch downloads
- Significantly improves performance when downloading many scene_ids
- Default max_workers=5, increase to 20+ for faster downloads on high-bandwidth connections

MINI-BATCH COMMIT:
- Sensor components: commits every 500 scenes to reduce commit overhead (~27% faster)
- Summary component: commits all scenes at once (small metadata)
- On interrupt: max 500 uncommitted scenes lost, all committed scenes are safe
- Failed batch commits trigger scene-level cleanup (maintains atomicity)

INDEX CREATION:
- Automatically creates BTREE indices on run_id, scene_id, sensor_timestamp, frame_id, frame_timestamp after download
- Index creation is parallelized across components using max_workers threads
- Indices can be created separately using create_indices() method
- Skips index creation if index already exists

Quick Start:
------------
from avcloud.experimental.client import AvCloudClient
from avcloud.experimental.resources.downloader_v2 import (
    SummaryItem,
    aggregate_results_by_run,
    get_failed_run_ids,
    get_complete_run_ids
)

# Create client and get downloader with parallel downloads
client = AvCloudClient(access_token="your_token")
downloader = client.downloader_v2(max_workers=5, live_logs=True)

# Prepare scenes to download
summary_items = [
    SummaryItem(scene_id="scene_001", run_id="run_001", country="US"),
    SummaryItem(scene_id="scene_002", run_id="run_001", country="US"),
]

# Download (indices are created automatically at the end)
results = downloader.download(
    dataset_base_path="/path/to/local/output",
    summary_items=summary_items,
    on_exist="skip"  # or "replace"
)

# Check results - only COMPLETE or FAILED (no PARTIAL)
complete = [r for r in results if r.overall_status == "COMPLETE"]
failed = [r for r in results if r.overall_status == "FAILED"]

# Get run-level summary
run_summary = aggregate_results_by_run(results)
for run_result in run_summary:
    print(f"Run {run_result.run_id}: {run_result.complete_scenes}/{run_result.total_scenes} scenes")

# Retry failed scenes
if failed:
    failed_items = [item for item in summary_items if item.scene_id in [r.scene_id for r in failed]]
    downloader.download(
        dataset_base_path="/path/to/local/output",
        summary_items=failed_items,
        on_exist="replace"
    )

# Create indices separately (e.g., if indices were not created during download)
# With verification (checks that datasets have data before creating indices)
downloader.create_indices(
    dataset_base_path="/path/to/local/output",
    verify_completeness=True
)

# Or create indices without verification (faster, but may create indices on empty datasets)
downloader.create_indices(
    dataset_base_path="/path/to/local/output",
    verify_completeness=False
)

Requirements:
- Lance version 0.37.0 (required for compatibility with remote data)
- OCI_ACCESS_KEY and OCI_SECRET_KEY environment variables (for direct LanceClient access)
"""

import json
import os
import re
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple

import lance
import pyarrow as pa
from lance import LanceOperation
from lance.fragment import write_fragments

from avcloud.experimental.http_client import HTTPClient
from avcloud.experimental.lance_client.client import LanceClient, _component_to_folder_name
from avcloud.experimental.resources.entity import SummaryItem
from avcloud.experimental.resources.stats_collector import StatsCollector
from avcloud.experimental.utils import s3_keys_utils

# Metadata component for run_id/scene_id lookups
SUMMARY_COMPONENT = "summary"


@dataclass
class ComponentDownloadResult:
    """Outcome for a single component (e.g., camera) for one scene_id."""

    component_name: str
    status: Literal["DOWNLOADED", "SKIPPED", "FAILED"]
    error_message: Optional[str] = None


@dataclass
class DownloadResult:
    """Overall outcome for a single scene_id across all components.

    STRICT POLICY:
    - COMPLETE: All components successfully downloaded (scene is usable)
    - FAILED: One or more components failed (incomplete data cleaned up)

    Note: No PARTIAL state - scenes are either fully complete or failed.
    """

    scene_id: str
    overall_status: Literal["COMPLETE", "FAILED"]
    base_path: str
    components: List[ComponentDownloadResult]
    # Verification after download: whether all requested components exist locally
    verified: bool = False
    missing_components: List[str] = None
    # Run ID this scene belongs to (if download was initiated with run_id)
    run_id: Optional[str] = None


@dataclass
class RunDownloadResult:
    """Aggregated result for a run_id (which contains multiple scenes).

    A run is COMPLETE only if ALL its scenes are COMPLETE.
    """

    run_id: str
    overall_status: Literal["COMPLETE", "FAILED"]
    total_scenes: int
    complete_scenes: int
    failed_scenes: int
    scene_results: List[DownloadResult]


# Convenience alias for return type
DownloadResults = List[DownloadResult]

# ----------------------------- Utilities ----------------------------- #


def _chunked(items: List[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _distinct_column_values(table: pa.Table, column: str) -> List[str]:
    if column not in table.column_names:
        return []
    arr = table[column]
    uniques = arr.unique()
    return [str(v.as_py()) for v in uniques if v is not None]


def _lance_filter_in(column: str, values: List[str]) -> str:
    if not values:
        return f"{column} IN ()"  # empty filter
    # Escape single quotes in values
    escaped = [v.replace("'", "''") for v in values]
    quoted = ", ".join([f"'{v}'" for v in escaped])
    return f"{column} IN ({quoted})"


def _log(live: bool, msg: str):
    if live:
        print(msg, flush=True)


def _ensure_local_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def _delete_local_rows_by_scene(local_ds, scene_ids: List[str]):
    if not scene_ids:
        return
    predicate = _lance_filter_in("scene_id", scene_ids)
    local_ds.delete(predicate)


def _scanner_with_stats(
    dataset,
    filter: Optional[str] = None,
    columns: Optional[List[str]] = None,
    batch_size: Optional[int] = None,
    fragment_readahead: Optional[int] = None,
    batch_readahead: Optional[int] = None,
    io_buffer_size: Optional[int] = None,
    use_scalar_index: Optional[bool] = None,
    **kwargs,
):
    """Create a scanner with statistics callback.

    Args:
      dataset: Lance dataset to scan
      filter: Optional filter expression
      columns: Optional list of columns to select
      batch_size: Optional batch size for scanning
      fragment_readahead: Optional fragment readahead limit
      batch_readahead: Optional batch readahead limit
      io_buffer_size: Optional IO buffer size in bytes (limits memory usage)
      use_scalar_index: Optional flag to use scalar index if available (more memory efficient)
      **kwargs: Additional scanner arguments

    Returns:
      Scanner object with statistics callback attached
    """
    scanner = None  # Will be set before callback is called

    def scan_stats_callback(stats: lance.ScanStatistics):
        scanner._scan_stats = stats  # Update scanner attribute directly

    # Build scanner kwargs
    scanner_kwargs = {"scan_stats_callback": scan_stats_callback}
    scanner_kwargs.update(kwargs)  # Add any additional kwargs first
    if filter is not None:
        scanner_kwargs["filter"] = filter
    if columns is not None:
        scanner_kwargs["columns"] = columns
    if batch_size is not None:
        scanner_kwargs["batch_size"] = batch_size
    if fragment_readahead is not None:
        scanner_kwargs["fragment_readahead"] = fragment_readahead
    if batch_readahead is not None:
        scanner_kwargs["batch_readahead"] = batch_readahead
    if io_buffer_size is not None:
        scanner_kwargs["io_buffer_size"] = io_buffer_size
    if use_scalar_index is not None:
        scanner_kwargs["use_scalar_index"] = use_scalar_index

    scanner = dataset.scanner(**scanner_kwargs)
    scanner._scan_stats = None

    return scanner


def _has_index(local_ds, column: str) -> bool:
    """Check if an index exists on the specified column.

    Args:
        local_ds: Local lance dataset
        column: Column name to check for index

    Returns:
        True if index exists, False otherwise
    """
    try:
        indices = local_ds.list_indices()
        for index in indices:
            # Lance returns indices as dictionaries with 'fields' key
            if isinstance(index, dict):
                fields = index.get("fields", [])
                if column in fields:
                    return True
                # Also check index name
                name = index.get("name", "")
                if column in name:
                    return True
            # Fallback for other formats
            elif hasattr(index, "columns") and column in index.columns:
                return True
            elif hasattr(index, "name") and column in str(index.name):
                return True
        return False
    except Exception:
        return False


def _build_indices(local_ds, component: str, live_logs: bool):
    """Build indices on local dataset after download.

    Creates indices for efficient querying:
    - BTREE indices on run_id and scene_id (for range queries and sorting)
    - BTREE indices on sensor_timestamp, frame_id, frame_timestamp (for temporal queries)

    Note: Indices are always rebuilt after new data is appended, as Lance indices
    only cover data that existed at index creation time. Appended data requires
    index rebuild to be included in the index.

    Args:
      local_ds: Local lance dataset
      component: Component name (e.g., 'camera', 'lidar')
      live_logs: Whether to print logs
    """

    def _create_index_if_exists(column: str, index_type: str, description: str = ""):
        """Helper to create index if column exists."""
        try:
            if column not in local_ds.schema.names:
                if live_logs and description:
                    _log(
                        live_logs,
                        f"[{component}] Skipping {column} index ({description}): column not found",
                    )
                return False

            # Drop existing index if present
            if _has_index(local_ds, column):
                try:
                    indices = local_ds.list_indices()
                    for index in indices:
                        if isinstance(index, dict):
                            fields = index.get("fields", [])
                            name = index.get("name", "")
                            if column in fields or column in name:
                                index_name = name if name else f"{column}_idx"
                                local_ds.drop_index(index_name)
                                if live_logs:
                                    _log(
                                        live_logs, f"[{component}] Dropped existing {column} index"
                                    )
                                break
                except Exception as e:
                    if live_logs:
                        _log(live_logs, f"[{component}] ⚠️ Failed to drop index on {column}: {e}")

            # Create index
            if live_logs:
                desc = f" ({description})" if description else ""
                _log(live_logs, f"[{component}] Creating {index_type} index on {column}{desc}...")
            local_ds.create_scalar_index(column=column, index_type=index_type)
            if live_logs:
                _log(
                    live_logs,
                    f"[{component}] ✅ Successfully created {index_type} index on {column}",
                )
            return True
        except Exception as e:
            if live_logs:
                _log(live_logs, f"[{component}] ⚠️ Failed to create index on {column}: {e}")
            return False

    # BITMAP indices for run_id and scene_id (for range queries and sorting)
    _create_index_if_exists("run_id", "BITMAP", "range queries")
    _create_index_if_exists("scene_id", "BITMAP", "range queries")

    # BTREE indices for temporal columns (exist across sensor datasets)
    _create_index_if_exists("sensor_timestamp", "BTREE", "temporal queries")
    _create_index_if_exists("frame_id", "BITMAP", "frame lookups")
    _create_index_if_exists("frame_timestamp", "BTREE", "temporal queries")


class DownloaderV2(HTTPClient):
    def __init__(
        self,
        http_client: HTTPClient,
        max_workers: int = 5,
        live_logs: bool = False,
    ):
        """
        Initialize DownloaderV2.

        Args:
            http_client: HTTP client for making requests
            max_workers: Number of parallel workers for downloads
            live_logs: Whether to print live logs
        """
        super().__init__()  # Initialize HTTPClient
        self._http_client = http_client
        self._client = LanceClient(http_client)
        self.max_workers = max_workers
        self.live_logs = live_logs
        # Generate unique session ID for this downloader instance
        self.session_id = "downloader_v2_" + str(uuid.uuid4())

    def _collect_scanner_stats(
        self,
        stats_collector: StatsCollector,
        component: str,
        scanner,
        scenes_count: int = 0,
        batch_count: int = 0,
        operation_type: str = "UNSPECIFIED",
    ) -> None:
        """Collect scanner statistics from a Lance scanner.

        This helper is called throughout the download process to collect stats from Lance operations.
        It extracts statistics from the scanner and submits them to the stats collector.

        STATS LIFECYCLE: This is where add_scan() is called (step 2 of lifecycle)
        - Called during preflight checks (LOCAL operations on summary.lance)
        - Called during component downloads (REMOTE operations)
        - Called during post-download verification (LOCAL operations)

        Args:
            stats_collector: StatsCollector instance to collect stats into
            component: Component name
            scanner: Lance scanner with stats attached via scan_stats_callback
            scenes_count: Number of scenes
            batch_count: Number of batches
            operation_type: "LOCAL" for local operations, "REMOTE" for remote/download operations
        """
        scan_stats = getattr(scanner, "_scan_stats", None)
        # Submit stats to collector (non-blocking, returns immediately)
        stats_collector.add_scan(
            component_name=component,
            scan_stats=scan_stats,
            scenes_count=scenes_count,
            batch_count=batch_count,
            operation_type=operation_type,
            http_client=self._http_client,
        )

    def _write_scene_as_fragment(
        self,
        local_uri: str,
        remote_ds,
        table: pa.Table,
        storage_options: Optional[Dict] = None,
        collect_fragments: bool = False,
    ) -> Optional[List]:
        """Write a single scene's data as one fragment.

        Args:
            local_uri: Local dataset URI
            remote_ds: Remote dataset for schema
            table: Data table to write
            storage_options: Storage options for remote datasets
            collect_fragments: If True, return fragments for batch commit instead of immediate commit

        Returns:
            List of fragments if collect_fragments=True and appending, None otherwise
        """
        schema = remote_ds.schema
        try:
            # Dataset exists - check if we should batch commit
            _ = lance.dataset(local_uri, storage_options=storage_options)
            if collect_fragments:
                # Return fragments for batch commit
                fragments = write_fragments(
                    table, local_uri, mode="append", storage_options=storage_options
                )
                return fragments
            else:
                # Immediate commit (original behavior)
                lance.write_dataset(
                    table,
                    local_uri,
                    schema=schema,
                    mode="append",
                    data_storage_version="2.1",
                    storage_options=storage_options,
                )
                return None
        except Exception:
            # Create new dataset - always immediate commit
            lance.write_dataset(
                table,
                local_uri,
                schema=schema,
                mode="create",
                data_storage_version="2.1",
                storage_options=storage_options,
            )
            return None

    def _get_existing_scene_ids(
        self,
        stats_collector: StatsCollector,
        local_ds,
        scene_ids: List[str],
        dataset_name: Optional[str] = None,
    ) -> List[str]:
        """Get existing scene IDs from local dataset.

        Args:
            stats_collector: StatsCollector instance to collect stats into
            local_ds: Local Lance dataset
            scene_ids: List of scene IDs to check
            dataset_name: Name of the dataset/component for logging and stats

        Returns:
            List of scene IDs that exist in the local dataset
        """
        if not scene_ids:
            return []
        where = _lance_filter_in("scene_id", scene_ids)
        scanner = _scanner_with_stats(local_ds, filter=where, columns=["scene_id"])
        tbl = scanner.to_table()
        _log(
            self.live_logs,
            f"[_get_existing_scene_ids:{dataset_name}] scanner._scan_stats = {scanner._scan_stats}",
        )
        self._collect_scanner_stats(
            stats_collector,
            dataset_name,
            scanner,
            scenes_count=len(scene_ids),
            operation_type="LOCAL",
        )

        return _distinct_column_values(tbl, "scene_id")

    def _compute_target_scene_ids_for_component(
        self,
        stats_collector: StatsCollector,
        component: str,
        local_base: Path,
        scene_ids: List[str],
        on_exist: Literal["replace", "skip"],
    ) -> List[str]:
        """Return the scene_ids that should be downloaded for this component considering on_exist policy.

        Also handles deletion of existing data when on_exist="replace".
        """
        if not scene_ids:
            return []

        # Map component to local folder name
        local_folder_name = _component_to_folder_name(component)
        local_uri = str((local_base / local_folder_name).as_posix())

        try:
            local_ds = lance.dataset(local_uri)
            existing = set(
                self._get_existing_scene_ids(
                    stats_collector, local_ds, scene_ids, dataset_name=component
                )
            )
        except Exception:
            existing = set()

        if on_exist == "replace":
            # Delete existing scenes before downloading
            if existing:
                try:
                    _delete_local_rows_by_scene(local_ds, list(existing))
                    _log(
                        self.live_logs,
                        f"Preflight: [{component}] deleted {len(existing)} existing scene rows",
                    )
                except Exception as e:
                    _log(
                        self.live_logs,
                        f"Preflight: [{component}] failed deleting existing rows: {e}",
                    )
            return list(scene_ids)

        # on_exist == "skip" -> exclude already present locally
        return [sid for sid in scene_ids if sid not in existing]

    def _preflight_plan(
        self,
        stats_collector: StatsCollector,
        local_base: Path,
        scene_ids: List[str],
        on_exist: Literal["replace", "skip"],
        region: Optional[str] = None,
    ) -> Dict[str, List[str]]:
        """Build a download plan by checking summary.lance for scene_id presence.

        Returns a mapping: component -> target scene_ids to download (after on_exist filtering).
        Note: We only check summary.lance during preflight. If actual component data is missing,
        we'll catch it during download and record in the error state.
        """
        # Default to US region if not specified (for backward compatibility)
        if region is None:
            region = self._client.get_us_region()

        plan: Dict[str, List[str]] = {}

        # First, verify all requested scene_ids exist in summary.lance
        _log(self.live_logs, "Preflight: Checking scene_ids in summary.lance...")
        summary_ds = self._client.open_component(SUMMARY_COMPONENT, region)
        found_in_summary: set = set()
        # For metadata queries, batch 100 at a time (much faster than data queries)
        for chunk in _chunked(scene_ids, 100):
            where = _lance_filter_in("scene_id", chunk)
            scanner = _scanner_with_stats(summary_ds, filter=where, columns=["scene_id"])
            tbl = scanner.to_table()
            _log(
                self.live_logs,
                f"[_preflight_plan:summary] scanner._scan_stats = {scanner._scan_stats}",
            )
            # Collect remote stats for preflight check, but don't advance the progress bar
            # (set scenes_count=0 to avoid counting metadata checks as downloads)
            self._collect_scanner_stats(
                stats_collector,
                SUMMARY_COMPONENT,
                scanner,
                scenes_count=0,
                operation_type="REMOTE",
            )
            found_in_summary.update(_distinct_column_values(tbl, "scene_id"))

        missing_in_summary = [sid for sid in scene_ids if sid not in found_in_summary]
        if missing_in_summary:
            raise RuntimeError(
                f"Preflight failed: scene_ids not found in summary.lance: {missing_in_summary}"
            )

        _log(self.live_logs, f"Preflight: All {len(scene_ids)} scene_ids found in summary.lance ✅")

        # Build plan for each component
        components = self._client.get_components()
        # Reorder components: put Lidar first for faster testing
        if "lidar" in components:
            components = ["lidar"] + [c for c in components if c != "lidar"]
        for component in components:
            # Determine target scene_ids for this component based on on_exist policy
            target = self._compute_target_scene_ids_for_component(
                stats_collector, component, local_base, scene_ids, on_exist
            )
            plan[component] = target
            if target:
                _log(
                    self.live_logs,
                    f"Preflight: [{component}] planned {len(target)} scene_ids to download",
                )
            else:
                _log(
                    self.live_logs,
                    f"Preflight: [{component}] nothing to download (all present or skipped)",
                )

        return plan

    def _verify_component_presence(
        self,
        stats_collector: StatsCollector,
        component: str,
        local_base: Path,
        scene_ids: List[str],
    ) -> List[str]:
        """Return scene_ids missing in local component dataset."""
        # Map component to local folder name
        local_folder_name = _component_to_folder_name(component)
        local_uri = str((local_base / local_folder_name).as_posix())
        missing: List[str] = list(scene_ids)
        try:
            ds = lance.dataset(local_uri)
            where = _lance_filter_in("scene_id", scene_ids)
            scanner = _scanner_with_stats(ds, filter=where, columns=["scene_id"])
            tbl = scanner.to_table()
            _log(
                self.live_logs,
                f"[_verify_component_presence:{component}] scanner._scan_stats = {scanner._scan_stats}",
            )
            # Collect local verification stats
            self._collect_scanner_stats(
                stats_collector,
                component,
                scanner,
                scenes_count=len(scene_ids),
                operation_type="LOCAL",
            )
            present = set(_distinct_column_values(tbl, "scene_id"))
            missing = [sid for sid in scene_ids if sid not in present]
        except Exception:
            # If dataset doesn't exist locally, all are missing
            pass
        return missing

    def _verify_presence(
        self, stats_collector: StatsCollector, local_base: Path, scene_ids: List[str]
    ) -> Dict[str, List[str]]:
        """Map scene_id -> missing component names after download."""
        result: Dict[str, List[str]] = {sid: [] for sid in scene_ids}
        for comp in self._client.get_components():
            missing_for_comp = set(
                self._verify_component_presence(stats_collector, comp, local_base, scene_ids)
            )
            if missing_for_comp:
                for sid in scene_ids:
                    if sid in missing_for_comp:
                        result[sid].append(comp)
        return result

    def _download_component_for_scenes(
        self,
        stats_collector: StatsCollector,
        component: str,
        local_base: Path,
        scene_ids: List[str],
        on_exist: Literal["replace", "skip"],
        region: Optional[str] = None,
        retry: int = 3,
        retry_backoff_sec: float = 1.0,
        executor: Optional[ThreadPoolExecutor] = None,
        write_locks: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[str], Dict[str, ComponentDownloadResult]]:
        """Download component data for given scene_ids."""
        # Default to US region if not specified (for backward compatibility)
        if region is None:
            region = self._client.get_us_region()
        results: Dict[str, ComponentDownloadResult] = {
            sid: ComponentDownloadResult(component, "FAILED") for sid in scene_ids
        }

        # Map component to local folder name
        local_folder_name = _component_to_folder_name(component)
        local_uri = str((local_base / local_folder_name).as_posix())

        # Open remote dataset (already validated in preflight check and cached)
        remote_ds = self._client.open_component(component, region)

        # Ensure local directory
        _ensure_local_dir(local_base)

        # scene_ids is already filtered by preflight plan (and deletions already handled)
        target_sids = list(scene_ids)

        # Process in batches
        # Summary: process all scenes in one batch (small metadata)
        # Sensors: process in batches of 500 scene_ids for efficiency (mini-batch commit)
        if not target_sids:
            # Nothing to download, all results already set above
            return scene_ids, results

        batch_size = len(target_sids) if component == SUMMARY_COMPONENT else 500
        batches = list(_chunked(target_sids, batch_size))

        # Get write lock for this component
        write_lock = write_locks.get(component) if write_locks else None

        def process_batch(batch):
            """Process a single batch of scene_ids with retry logic.

            Uses mini-batch commit: collects fragments for all scenes in batch,
            then commits them all at once. This reduces commit overhead (~27% faster)
            while maintaining reasonable recovery granularity (max 500 scenes lost on interrupt).
            """
            if not batch:
                return {}

            batch_results = {}
            attempt = 0
            last_error = None

            while attempt < retry:
                # Reset fragments for each retry attempt to avoid committing stale fragments
                batch_fragments = []  # Collect fragments for batch commit

                def write_and_collect(table_to_write):
                    """Helper to write fragment and collect for batch commit."""
                    if write_lock:
                        with write_lock:
                            frags = self._write_scene_as_fragment(
                                local_uri, remote_ds, table_to_write, collect_fragments=True
                            )
                    else:
                        frags = self._write_scene_as_fragment(
                            local_uri, remote_ds, table_to_write, collect_fragments=True
                        )
                    if frags:
                        batch_fragments.extend(frags)

                try:
                    where = _lance_filter_in("scene_id", batch)
                    scene_id = batch[0] if len(batch) == 1 else None
                    scene_ids = batch

                    _log(self.live_logs, f"[{component}] Downloading {len(batch)} scene(s)...")

                    # Configure scanner optimization parameters for faster downloads
                    # Aggressive settings: large batches, high readahead, optimized IO buffer
                    if component.lower() == "lidar":
                        scanner_batch_size = 1024  # Large batches for lidar (was 64)
                        scanner_fragment_readahead = 8  # Parallel fragment reading (was 4)
                        scanner_batch_readahead = 8  # Parallel batch reading (was 4)
                        scanner_io_buffer_size = 256 * 1024 * 1024  # 256MB IO buffer for lidar
                        scanner_use_scalar_index = True
                    elif component.lower() == "camera":
                        scanner_batch_size = 1024  # Very large batches for camera (was 128)
                        scanner_fragment_readahead = 8  # Parallel fragment reading (was 4)
                        scanner_batch_readahead = 8  # Parallel batch reading (was 4)
                        scanner_io_buffer_size = 128 * 1024 * 1024  # 128MB IO buffer for camera
                        scanner_use_scalar_index = None
                    else:
                        scanner_batch_size = (
                            1024  # Large batches for all other components (was 128)
                        )
                        scanner_fragment_readahead = 8  # Parallel fragment reading (was 4)
                        scanner_batch_readahead = 8  # Parallel batch reading (was 4)
                        scanner_io_buffer_size = 64 * 1024 * 1024  # 64MB IO buffer for others
                        scanner_use_scalar_index = None

                    scanner_kwargs = {"filter": where}
                    if scanner_batch_size:
                        scanner_kwargs["batch_size"] = scanner_batch_size
                    if scanner_fragment_readahead:
                        scanner_kwargs["fragment_readahead"] = scanner_fragment_readahead
                    if scanner_batch_readahead:
                        scanner_kwargs["batch_readahead"] = scanner_batch_readahead
                    if scanner_io_buffer_size:
                        scanner_kwargs["io_buffer_size"] = scanner_io_buffer_size
                    if scanner_use_scalar_index:
                        scanner_kwargs["use_scalar_index"] = scanner_use_scalar_index

                    # Use to_table() for single scene - faster than accumulating batches
                    # With optimized batch_size and readahead, this should be fast and memory-efficient
                    scanner = _scanner_with_stats(remote_ds, **scanner_kwargs)
                    _log(self.live_logs, f"[{component}] Scanner created, loading table...")

                    try:
                        # Direct to_table() for all components - simpler and faster
                        # The optimized scanner parameters (batch_size, readahead, io_buffer) handle performance
                        table = scanner.to_table()

                        if table.num_rows == 0:
                            raise RuntimeError(f"No data returned for scene(s) {batch}")

                        _log(
                            self.live_logs,
                            f"[{component}] Loaded {table.num_rows:,} rows ({table.nbytes / 1024 / 1024:.1f} MB)",
                        )

                    except Exception as e:
                        _log(self.live_logs, f"[{component}] ❌ Error loading table: {e}")
                        raise

                    # Write directly - simple and fast, one fragment per scene
                    self._write_scene_as_fragment(
                        local_uri,
                        remote_ds,
                        table,
                        collect_fragments=False,  # Immediate commit
                    )

                    if scene_id:
                        _log(
                            self.live_logs,
                            f"[{component}] ✅ Downloaded and wrote scene {scene_id} [Session: {self.session_id}]",
                        )
                    else:
                        _log(
                            self.live_logs,
                            f"[{component}] ✅ Downloaded and wrote {len(batch)} scenes [Session: {self.session_id}]",
                        )

                    # Collect stats
                    # Note: batch_count is not available when using to_table()
                    self._collect_scanner_stats(
                        stats_collector,
                        component,
                        scanner,
                        scenes_count=len(batch),
                        batch_count=0,
                        operation_type="REMOTE",
                    )

                    for sid in batch:
                        batch_results[sid] = ComponentDownloadResult(component, "DOWNLOADED")
                    break  # Success, exit retry loop

                except Exception as e:
                    last_error = str(e)
                    extracted_error = extract_error(e)

                    # Check if this is a key expiration error that needs credential refresh
                    if extracted_error["code"] == "SignatureDoesNotMatch":
                        raise Exception(f"SignatureDoesNotMatch: {extracted_error['message']}")

                    attempt += 1
                    if attempt >= retry:
                        # After all retries failed, mark all scenes in this batch as failed
                        error_msg = f"Download failed after {retry} retries: {last_error}"
                        _log(self.live_logs, f"[{component}] ❌ Batch failed: {error_msg}")
                        for sid in batch:
                            if (
                                sid not in batch_results
                                or batch_results[sid].status != "DOWNLOADED"
                            ):
                                batch_results[sid] = ComponentDownloadResult(
                                    component, "FAILED", error_message=error_msg
                                )
                    else:
                        # Backoff and retry
                        backoff_time = retry_backoff_sec * (2 ** (attempt - 1))
                        _log(
                            self.live_logs,
                            f"[{component}] Retry {attempt}/{retry} after {backoff_time}s...",
                        )
                        time.sleep(backoff_time)

            # Mini-batch commit: commit all fragments collected in this batch
            if batch_fragments:
                try:
                    if write_lock:
                        with write_lock:
                            operation = LanceOperation.Append(batch_fragments)
                            dataset = lance.dataset(local_uri)
                            lance.LanceDataset.commit(
                                local_uri, operation, read_version=dataset.version
                            )
                    else:
                        operation = LanceOperation.Append(batch_fragments)
                        dataset = lance.dataset(local_uri)
                        lance.LanceDataset.commit(
                            local_uri, operation, read_version=dataset.version
                        )
                    _log(
                        self.live_logs,
                        f"[{component}] ✅ Batch committed {len(batch_fragments)} fragments for {len(batch)} scenes",
                    )
                except Exception as e:
                    _log(self.live_logs, f"[{component}] ❌ Batch commit failed: {e}")

                    # Cleanup orphan fragments (data written but not committed)
                    # These fragments are already written to storage but not in manifest
                    # TODO: Lance doesn't currently provide API to delete uncommitted fragments
                    # Orphan fragments will occupy storage but are not visible in dataset
                    # Potential solutions:
                    # 1. Use dataset.cleanup_old_versions() after fixing (may not work for uncommitted)
                    # 2. Implement custom S3 deletion of fragment files using fragment.data_file path
                    # 3. Run periodic storage cleanup jobs
                    _log(
                        self.live_logs,
                        f"[{component}] ⚠️ {len(batch_fragments)} orphan fragments in storage (commit failed, manual cleanup may be needed)",
                    )

                    # Mark all downloaded scenes in this batch as failed if commit fails
                    for sid in batch:
                        if (
                            batch_results.get(
                                sid, ComponentDownloadResult(component, "FAILED")
                            ).status
                            == "DOWNLOADED"
                        ):
                            batch_results[sid] = ComponentDownloadResult(
                                component, "FAILED", error_message=f"Batch commit failed: {e}"
                            )

            return batch_results

        # If executor provided, use it for parallel batch processing
        if executor:
            batch_futures = {executor.submit(process_batch, batch): batch for batch in batches}

            for future in as_completed(batch_futures):
                try:
                    batch_results = future.result()
                    # Merge batch results into main results
                    results.update(batch_results)
                except Exception as e:
                    # Check if this is a key expiration error that needs to bubble up
                    if "SignatureDoesNotMatch" in str(e):
                        # Cancel all remaining futures to avoid wasted work with expired credentials
                        _log(
                            self.live_logs,
                            f"[{component}] 🛑 Cancelling remaining batches due to credential expiration...",
                        )
                        cancelled_count = 0
                        for remaining_future in batch_futures:
                            if remaining_future != future and not remaining_future.done():
                                remaining_future.cancel()
                                cancelled_count += 1
                        _log(
                            self.live_logs,
                            f"[{component}] Cancelled {cancelled_count} pending batch(es)",
                        )
                        # Re-raise to trigger credential refresh in outer handler
                        raise

                    # Handle unexpected thread execution errors
                    batch = batch_futures[future]
                    error_msg = f"Thread execution error: {e}"
                    _log(self.live_logs, f"[{component}] ❌ Batch thread failure: {error_msg}")
                    for sid in batch:
                        if results[sid].status != "DOWNLOADED":
                            results[sid] = ComponentDownloadResult(
                                component, "FAILED", error_message=error_msg
                            )
        else:
            # Sequential processing (backward compatibility)
            for batch in batches:
                batch_results = process_batch(batch)
                results.update(batch_results)

        # Build indices after download (placeholder)
        try:
            local_ds_post = lance.dataset(local_uri)
            _build_indices(local_ds_post, component, self.live_logs)
        except Exception:
            pass

        return scene_ids, results

    def _group_summary_items_by_region(
        self, summary_items: List[SummaryItem]
    ) -> Dict[str, List[SummaryItem]]:
        """Group summary items by region based on country.

        Default behavior: scenes with missing/None country are treated as US.
        """
        us_region = self._client.get_us_region()
        eu_region = self._client.get_eu_region()

        us_items = []
        eu_items = []

        for item in summary_items:
            # Treat missing/None country as US (default region)
            if not item.country or item.country == "US":
                us_items.append(item)
            else:
                eu_items.append(item)

        return {
            us_region: us_items,
            eu_region: eu_items,
        }

    def download(
        self,
        dataset_base_path: str,
        summary_items: List[SummaryItem],
        on_exist: Literal["replace", "skip"] = "replace",
    ) -> DownloadResults:
        """Download Lance datasets from OCI to a local base path."""
        grouped_by_region = self._group_summary_items_by_region(summary_items)
        results = []
        for region, region_items in grouped_by_region.items():
            if not region_items:  # Skip empty regions
                continue
            region_results = self.download_single_region(
                dataset_base_path, region_items, region, on_exist
            )
            results.extend(region_results)
        return results

    def download_single_region(
        self,
        dataset_base_path: str,
        summary_items: List[SummaryItem],
        region: str,
        on_exist: Literal["replace", "skip"] = "replace",
    ) -> DownloadResults:
        """Download Lance datasets from OCI to a local base path for a specific region.

        Strategy:
        - Scene-level atomicity: A scene is only considered COMPLETE if ALL components downloaded successfully.
          If any component fails, the entire scene is marked FAILED and incomplete data is cleaned up.
        - Job-level best-effort: If some scenes fail, continue downloading other scenes.
          Provides detailed error reporting for failed scenes.
        - Parallel downloads: Uses max_workers threads to download batches concurrently.
          Increase max_workers (e.g., 20) for faster downloads on high-bandwidth connections.

        Parameters:
        - dataset_base_path: Local directory path where datasets will be stored
        - summary_items: List of SummaryItem objects containing scene_id, run_id, and metadata
        - region: OCI region to download from (obtained from config, e.g., US or EU region)
        - on_exist: "replace" = re-download existing scenes, "skip" = skip existing scenes

        Returns:
        - DownloadResults: List of DownloadResult with per-scene status (COMPLETE/FAILED) and detailed error info
        """
        # STATS LIFECYCLE STEP 1: Initialize stats collector for this download session
        # - Creates local StatsCollector instance (scoped to this download)
        # - Starts background thread pools for non-blocking stats collection
        # - Stats will be collected throughout download and finalized at the end
        stats_collector = StatsCollector(
            session_id=self.session_id,
            dataset_path=dataset_base_path,
            region=region,
            on_exist_policy=on_exist,
            live_logs=self.live_logs,
        )

        components = self._client.get_components()
        # Reorder components: put Lidar first for faster testing
        if "lidar" in components:
            components = ["lidar"] + [c for c in components if c != "lidar"]
        self._client.ensure_components_available(components, region)

        local_base = Path(dataset_base_path)
        _ensure_local_dir(local_base)

        # Extract scene_ids and build scene_to_run_map from summary_items
        scene_to_run_map: Dict[str, str] = {}  # scene_id -> run_id mapping
        all_scene_ids: List[str] = []
        requested_run_ids_set: set = set()

        for item in summary_items:
            if item.scene_id:
                all_scene_ids.append(item.scene_id)
                if item.run_id:
                    scene_to_run_map[item.scene_id] = item.run_id
                    requested_run_ids_set.add(item.run_id)

        # Remove duplicates and sort for consistency
        all_scene_ids = sorted(list(set(all_scene_ids)))
        requested_run_ids = sorted(list(requested_run_ids_set)) if requested_run_ids_set else None

        # Always print session ID for users to track their download
        print(f"Download Session ID: {self.session_id}")

        _log(
            self.live_logs,
            f"Processing {len(all_scene_ids)} scene(s) from {len(summary_items)} summary item(s)",
        )
        if requested_run_ids:
            _log(self.live_logs, f"Spanning {len(requested_run_ids)} run(s)")
        _log(self.live_logs, f"Using {self.max_workers} worker(s) for parallel downloads")

        # Nothing to do
        if not all_scene_ids:
            _log(self.live_logs, "⚠️ No valid scene_ids found in summary_items")
            return []

        # STATS LIFECYCLE STEP 2a: Collect stats during preflight checks
        # Preflight: plan and verify remote presence for all targets before any write
        plan = self._preflight_plan(stats_collector, local_base, all_scene_ids, on_exist, region)

        # Calculate total download operations from the plan
        # Each scene-component pair is one download operation
        total_download_operations = sum(len(target_scenes) for target_scenes in plan.values())

        # Register total for progress tracking (scenes × components)
        stats_collector.set_total_scenes(total_download_operations)

        # Process per component; we accumulate per-scene results
        per_scene_components: Dict[str, List[ComponentDownloadResult]] = {
            sid: [] for sid in all_scene_ids
        }

        from threading import Lock

        # STATS LIFECYCLE STEP 2b: Collect stats during component downloads
        # Stats are collected via add_scan() calls within _download_component_for_scenes()
        for component in components:
            target_for_component = plan.get(component, [])
            if not target_for_component:
                # Nothing to download for this component under on_exist policy; still mark SKIPPED
                for sid in all_scene_ids:
                    per_scene_components[sid].append(ComponentDownloadResult(component, "SKIPPED"))
                continue

            retried = False
            while True:
                try:
                    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                        _, comp_results = self._download_component_for_scenes(
                            stats_collector=stats_collector,
                            component=component,
                            local_base=local_base,
                            scene_ids=target_for_component,
                            on_exist=on_exist,
                            region=region,
                            executor=executor,
                            write_locks={component: Lock()},
                        )
                    # Fill in SKIPPED status for scenes not targeted
                    for sid in all_scene_ids:
                        if sid not in comp_results:
                            per_scene_components[sid].append(
                                ComponentDownloadResult(component, "SKIPPED")
                            )
                        else:
                            per_scene_components[sid].append(comp_results[sid])

                    break

                except Exception as e:
                    if not retried and "SignatureDoesNotMatch" in str(e):
                        retried = True
                        _log(
                            self.live_logs,
                            f"[{component}] 🔄 API key expired, refreshing credentials...",
                        )
                        _log(
                            self.live_logs,
                            f"[{component}] ⏳ Waiting for remaining threads to complete...",
                        )
                        # Note: When we exit this except block and continue, the ThreadPoolExecutor
                        # context manager will automatically wait for all running threads to finish
                        # (cancelled futures won't run, but already-running threads will complete)

                        try:
                            self._client._setup_s3_compatible_keys()
                            self._client.reset_cache()
                            # Verify credentials work by checking all components
                            components = self._client.get_components()
                            self._client.ensure_components_available(components, region)
                            _log(
                                self.live_logs,
                                f"[{component}] ✅ Credentials refreshed successfully, retrying ALL batches...",
                            )
                            continue
                        except Exception as refresh_error:
                            # Credential refresh failed - mark all scenes as failed
                            error_msg = f"Failed to refresh credentials: {refresh_error}"
                            _log(
                                self.live_logs,
                                f"[{component}] ❌ Credential refresh failed: {error_msg}",
                            )
                            for sid in all_scene_ids:
                                per_scene_components[sid].append(
                                    ComponentDownloadResult(
                                        component, "FAILED", error_message=error_msg
                                    )
                                )
                            break
                    else:
                        # Unexpected exception - mark all target scenes as failed for this component
                        error_msg = f"Unexpected error: {e}"
                        _log(self.live_logs, f"[{component}] ❌ Catastrophic failure: {error_msg}")
                        for sid in all_scene_ids:
                            per_scene_components[sid].append(
                                ComponentDownloadResult(
                                    component, "FAILED", error_message=error_msg
                                )
                            )
                        break

        # STRICT POLICY: Cleanup incomplete scenes
        # A scene is only valid if ALL components are DOWNLOADED or SKIPPED
        _log(self.live_logs, "\nEnforcing scene-level atomicity (strict policy)...")
        incomplete_scenes = []

        for sid, comp_list in per_scene_components.items():
            statuses = {c.status for c in comp_list}
            # Valid states: all DOWNLOADED, all SKIPPED, or mix of DOWNLOADED and SKIPPED
            is_complete = statuses.issubset({"DOWNLOADED", "SKIPPED"})

            if not is_complete:
                incomplete_scenes.append(sid)
                _log(self.live_logs, f"  ⚠️ Scene {sid} incomplete - cleaning up partial data...")

                # Delete this scene from all components where it was written
                for component in components:
                    # Map component to local folder name
                    local_folder_name = _component_to_folder_name(component)
                    local_uri = str((local_base / local_folder_name).as_posix())
                    try:
                        local_ds = lance.dataset(local_uri)
                        _delete_local_rows_by_scene(local_ds, [sid])
                        _log(self.live_logs, f"    Cleaned {component} for scene {sid}")
                    except Exception as e:
                        # Dataset might not exist or scene might not be present - that's ok
                        pass

        if incomplete_scenes:
            _log(
                self.live_logs,
                f"Cleaned up {len(incomplete_scenes)} incomplete scene(s) to maintain data integrity",
            )
        else:
            _log(self.live_logs, f"✅ All scenes are complete - no cleanup needed")

        # Build final results per scene
        results: DownloadResults = []
        # STATS LIFECYCLE STEP 2c: Collect stats during post-download verification
        # Post-verify local presence to surface resumable status to users
        verify_missing = self._verify_presence(stats_collector, local_base, all_scene_ids)
        for sid, comp_list in per_scene_components.items():
            if not comp_list:
                overall = "FAILED"
            else:
                statuses = {r.status for r in comp_list}
                # STRICT: Only COMPLETE if all components are DOWNLOADED or SKIPPED (no FAILED)
                if statuses.issubset({"DOWNLOADED", "SKIPPED"}):
                    overall = "COMPLETE"
                else:
                    # Any FAILED component means the whole scene is FAILED
                    overall = "FAILED"

            missing_components = verify_missing.get(sid, [])
            verified = len(missing_components) == 0

            # Add run_id if this was a run_id-based download
            associated_run_id = scene_to_run_map.get(sid) if scene_to_run_map else None

            results.append(
                DownloadResult(
                    scene_id=sid,
                    overall_status=overall,
                    base_path=str(local_base),
                    components=comp_list,
                    verified=verified,
                    missing_components=missing_components,
                    run_id=associated_run_id,
                )
            )

        # Optional: write a download summary
        try:
            manifest_path = local_base / "download_summary.json"
            with manifest_path.open("w", encoding="utf-8") as f:
                json.dump(
                    [
                        {
                            "scene_id": r.scene_id,
                            "run_id": r.run_id,
                            "overall_status": r.overall_status,
                            "verified": r.verified,
                            "missing_components": r.missing_components,
                            "components": [
                                {
                                    "component": c.component_name,
                                    "status": c.status,
                                    "error": c.error_message,
                                }
                                for c in r.components
                            ],
                        }
                        for r in results
                    ],
                    f,
                    indent=2,
                )
            _log(self.live_logs, f"Download summary written to: {manifest_path}")
        except Exception:
            pass

        # Print summary
        if self.live_logs:
            print("\n" + "=" * 70)
            print("DOWNLOAD SUMMARY (STRICT POLICY)")
            print(f"Session ID: {self.session_id}")
            print("=" * 70)

            complete_count = sum(
                1 for r in results if r.overall_status == "COMPLETE" and r.verified
            )
            failed_count = sum(1 for r in results if r.overall_status == "FAILED")

            # Scene-level summary
            print(f"\n📦 Scene-level Summary:")
            print(f"  Total scenes: {len(results)}")
            print(f"    ✅ Complete: {complete_count}")
            print(f"    ❌ Failed: {failed_count}")

            # Run-level summary (if downloaded by run_id)
            if requested_run_ids:
                run_summary = aggregate_results_by_run(results)
                complete_runs = [r for r in run_summary if r.overall_status == "COMPLETE"]
                failed_runs = [r for r in run_summary if r.overall_status == "FAILED"]

                print(f"\nRun-level Summary:")
                print(f"  Total runs: {len(run_summary)}")
                print(f"    ✅ Complete runs: {len(complete_runs)}")
                print(f"    ❌ Failed runs: {len(failed_runs)}")

                # Show which runs are complete/failed
                if complete_runs:
                    print(f"\n  Complete runs (all scenes downloaded):")
                    for run_result in complete_runs:
                        print(f"    • {run_result.run_id} ({run_result.total_scenes} scenes)")

                if failed_runs:
                    print(f"\n  ❌ Failed runs (some scenes missing):")
                    for run_result in failed_runs:
                        print(
                            f"    • {run_result.run_id}: {run_result.complete_scenes}/{run_result.total_scenes} scenes complete"
                        )
                        # Show failed scenes
                        failed_scene_ids = [
                            s.scene_id
                            for s in run_result.scene_results
                            if s.overall_status == "FAILED"
                        ]
                        if failed_scene_ids:
                            print(
                                f"      Failed scenes: {', '.join(failed_scene_ids[:5])}"
                                + (
                                    f" ... and {len(failed_scene_ids) - 5} more"
                                    if len(failed_scene_ids) > 5
                                    else ""
                                )
                            )

            # Show failures details
            if failed_count > 0:
                print(f"\n⚠️ Failed scenes details (can be retried):")
                for r in results[:5]:  # Show first 5 failures
                    if r.overall_status == "FAILED":
                        run_info = f" [run: {r.run_id}]" if r.run_id else ""
                        print(f"\n  Scene: {r.scene_id}{run_info}")
                        failed_components = [c for c in r.components if c.status == "FAILED"]
                        if failed_components:
                            print(f"    Missing components:")
                            for c in failed_components:
                                print(
                                    f"      ✗ {c.component_name}: {c.error_message or 'Unknown error'}"
                                )

                if failed_count > 5:
                    print(f"\n  ... and {failed_count - 5} more failed scenes")

            print("\n" + "=" * 70)
            print(
                f"Tip: Retry failed {'runs' if requested_run_ids else 'scenes'} with on_exist='replace'"
            )
            print("=" * 70)

        # STATS LIFECYCLE STEP 3: Finalize stats collection
        # - Signals shutdown (no new stats accepted after this point)
        # - Waits for all pending stats processing to complete (BLOCKING)
        # - Computes final summary statistics from download results
        # - Sends aggregated stats to server via HTTP POST
        stats_collector.finalize(
            results,
            http_client=self._http_client,
        )

        # Create indices after successful download
        _log(self.live_logs, "\nCreating indices on downloaded datasets...")
        try:
            self.create_indices(
                dataset_base_path=dataset_base_path,
                verify_completeness=False,  # Already verified during download
            )
        except Exception as e:
            _log(self.live_logs, f"⚠️ Index creation failed (non-fatal): {e}")

        return results

    def create_indices(
        self,
        dataset_base_path: str,
        verify_completeness: bool = True,
    ) -> Dict[str, bool]:
        """Create indices on run_id, scene_id, sensor_timestamp, frame_id, frame_timestamp for all datasets.

        This method can be run separately to create indices after download,
        or to rebuild indices if they were not created during download.
        Both run_id and scene_id columns exist across all datasets.

        Index creation is parallelized across components using max_workers threads
        for improved performance.

        Args:
            dataset_base_path: Local directory path where datasets are stored
            verify_completeness: If True, verifies that datasets are complete before creating indices.
                               If False, creates indices on all existing datasets.

        Returns:
            Dictionary mapping component name to success status (True/False)

        Example:
            # Create indices on all datasets with verification
            downloader.create_indices("/path/to/dataset", verify_completeness=True)

            # Create indices without verification (faster)
            downloader.create_indices("/path/to/dataset", verify_completeness=False)
        """
        local_base = Path(dataset_base_path)

        if not local_base.exists():
            raise RuntimeError(f"Dataset path does not exist: {dataset_base_path}")

        components = self._client.get_components()
        results = {}

        _log(self.live_logs, f"Creating indices for {len(components)} component(s) in parallel...")

        def create_index_for_component(component: str) -> tuple[str, bool]:
            """Create indices for a single component. Returns (component_name, success)."""
            # Map component to local folder name
            local_folder_name = _component_to_folder_name(component)
            local_uri = str((local_base / local_folder_name).as_posix())

            try:
                # Check if dataset exists
                local_ds = lance.dataset(local_uri)

                # Optional: Verify completeness by checking for any data
                if verify_completeness:
                    count = local_ds.count_rows()
                    if count == 0:
                        _log(self.live_logs, f"[{component}] ⚠️ Skipping - dataset is empty")
                        return (component, False)
                    _log(self.live_logs, f"[{component}] Verified: {count} rows")

                # Create index
                _build_indices(local_ds, component, self.live_logs)
                return (component, True)

            except FileNotFoundError:
                _log(self.live_logs, f"[{component}] ⚠️ Dataset not found at {local_uri}")
                return (component, False)
            except Exception as e:
                _log(self.live_logs, f"[{component}] ❌ Error: {e}")
                return (component, False)

        # Create indices in parallel using thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(create_index_for_component, comp): comp for comp in components
            }

            for future in as_completed(futures):
                component, success = future.result()
                results[component] = success

        # Summary
        successful = sum(1 for v in results.values() if v)
        total = len(results)
        _log(
            self.live_logs,
            f"\n✅ Index creation complete: {successful}/{total} components successful",
        )

        return results


# ----------------------------- Helper Functions ----------------------------- #


def aggregate_results_by_run(scene_results: DownloadResults) -> List[RunDownloadResult]:
    """Aggregate scene-level results to run-level results.

    A run is COMPLETE only if ALL its scenes are COMPLETE.
    """
    from collections import defaultdict

    run_to_scenes: Dict[str, List[DownloadResult]] = defaultdict(list)

    for scene_result in scene_results:
        if scene_result.run_id:
            run_to_scenes[scene_result.run_id].append(scene_result)

    run_results: List[RunDownloadResult] = []

    for run_id, scenes in sorted(run_to_scenes.items()):
        complete_scenes = [s for s in scenes if s.overall_status == "COMPLETE"]
        failed_scenes = [s for s in scenes if s.overall_status == "FAILED"]

        # STRICT: Run is only COMPLETE if ALL scenes are COMPLETE
        overall_status = "COMPLETE" if len(failed_scenes) == 0 else "FAILED"

        run_results.append(
            RunDownloadResult(
                run_id=run_id,
                overall_status=overall_status,
                total_scenes=len(scenes),
                complete_scenes=len(complete_scenes),
                failed_scenes=len(failed_scenes),
                scene_results=scenes,
            )
        )

    return run_results


def get_failed_run_ids(scene_results: DownloadResults) -> List[str]:
    """Get list of run_ids that have at least one failed scene."""
    run_summary = aggregate_results_by_run(scene_results)
    return [r.run_id for r in run_summary if r.overall_status == "FAILED"]


def get_complete_run_ids(scene_results: DownloadResults) -> List[str]:
    """Get list of run_ids that have all scenes successfully downloaded."""
    run_summary = aggregate_results_by_run(scene_results)
    return [r.run_id for r in run_summary if r.overall_status == "COMPLETE"]


def extract_error(exc: Exception):
    msg = str(exc)
    code = re.search(r"<Code>(.*?)</Code>", msg)
    message = re.search(r"<Message>(.*?)</Message>", msg)
    return {
        "code": code.group(1) if code else None,
        "message": message.group(1) if message else None,
    }
