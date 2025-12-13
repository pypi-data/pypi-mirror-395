"""
Statistics Collector for Download Operations

Collects, aggregates, and reports download statistics using Python dataclasses.
Provides JSON serialization and HTTP POST capabilities for sending stats to a server.
"""

from __future__ import annotations

import json
import logging
import queue
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional

import lance
from tqdm import tqdm

from avcloud.experimental.resources.entity import (
    ComponentStats,
    DownloadSummaryStats,
    EmitScanOperationRequest,
    LanceScanStats,
    OperationType,
)

logger = logging.getLogger(__name__)

# API Endpoints
API_EMIT_SCAN_OPERATION = "/avcloud/api/v2/emitscanoperation"
API_EMIT_DOWNLOAD_SUMMARY = "/avcloud/api/v2/emitdownloadsummary"

# Worker thread configuration
MAX_WORKERS = 2
HTTP_WORKER_THREADS = 2


def lance_stats_to_lance_scan_stats(stats: Optional[lance.ScanStatistics]) -> LanceScanStats:
    """Convert Lance ScanStatistics to LanceScanStats dataclass."""
    if stats is None:
        return LanceScanStats()

    # Extract counts from all_counts dict
    all_counts = stats.all_counts if hasattr(stats, "all_counts") else {}
    ranges_scanned = all_counts.get("ranges_scanned", 0)
    rows_scanned = all_counts.get("rows_scanned", 0)
    fragments_scanned = all_counts.get("fragments_scanned", 0)

    # Get other known counts and store extras in additional_counts
    known_keys = {"ranges_scanned", "rows_scanned", "fragments_scanned"}
    additional = {k: v for k, v in all_counts.items() if k not in known_keys}

    # Extract latency metric (in microseconds for precision)
    # Lance may provide this as attribute or in all_counts
    total_latency_us = getattr(stats, "total_latency_us", 0)

    # Also check all_counts for latency metric
    if not total_latency_us and "total_latency_us" in all_counts:
        total_latency_us = all_counts["total_latency_us"]

    scan_stats = LanceScanStats(
        iops=stats.iops if hasattr(stats, "iops") else 0,
        requests=stats.requests if hasattr(stats, "requests") else 0,
        bytes_read=stats.bytes_read if hasattr(stats, "bytes_read") else 0,
        indices_loaded=stats.indices_loaded if hasattr(stats, "indices_loaded") else 0,
        parts_loaded=stats.parts_loaded if hasattr(stats, "parts_loaded") else 0,
        index_comparisons=stats.index_comparisons if hasattr(stats, "index_comparisons") else 0,
        ranges_scanned=ranges_scanned,
        rows_scanned=rows_scanned,
        fragments_scanned=fragments_scanned,
        total_latency_us=total_latency_us,
        additional_counts=additional,
    )

    return scan_stats


class StatsCollector:
    """Collects download statistics using dataclasses."""

    def __init__(
        self,
        session_id: str,
        dataset_path: str,
        region: str,
        on_exist_policy: str,
        stats_workers: int = 1,
        live_logs: bool = False,
    ):
        """
        Initialize stats collector.

        Args:
            session_id: Unique session identifier
            dataset_path: Local dataset path
            region: OCI region
            on_exist_policy: "skip" or "replace"
            stats_workers: Number of worker threads for processing stats updates (default: 1,
                          since updates are serialized by lock anyway)
            live_logs: Whether to print live logs (default: False)
        """
        self.session_stats = DownloadSummaryStats(
            session_id=session_id,
            dataset_path=dataset_path,
            region=region,
            on_exist_policy=on_exist_policy,
            max_workers=MAX_WORKERS,
        )
        self.start_time = datetime.now()
        self.component_stats_map = {}  # component_name -> ComponentStats
        self._lock = threading.Lock()  # Protects component_stats_map modifications
        self.live_logs = live_logs

        self._stats_executor = ThreadPoolExecutor(
            max_workers=stats_workers, thread_name_prefix="stats-worker"
        )
        self._http_executor = ThreadPoolExecutor(
            max_workers=HTTP_WORKER_THREADS, thread_name_prefix="http-worker"
        )
        self._shutdown = False

        # Progress tracking
        self.completed_scenes_count = 0
        self.total_scenes_expected = 0
        self.progress_bar = None

    def _log(self, msg: str):
        """Log message if live_logs is enabled."""
        if self.live_logs:
            print(msg, flush=True)

    def set_total_scenes(self, total: int):
        """Set total expected scenes and start progress bar.

        Args:
            total: Total number of scenes to download
        """
        with self._lock:
            self.total_scenes_expected = total

        if total > 0:
            self.progress_bar = tqdm(total=total, desc="Downloading", unit="scene")

    def add_scan(
        self,
        component_name: str,
        scan_stats: Optional[lance.ScanStatistics],
        scenes_count: int = 0,
        batch_count: int = 0,
        operation_type: str = "UNSPECIFIED",
        http_client=None,
    ):
        """Add scanner statistics for a component.

        Non-blocking method that submits stats processing to a background thread pool.
        Can be called concurrently from multiple threads without blocking.

        Args:
            component_name: Name of the component (e.g., "camera", "lidar")
            scan_stats: Lance ScanStatistics object (extracted from scanner._scan_stats)
            scenes_count: Number of scenes processed
            batch_count: Number of batches processed
            operation_type: "LOCAL" or "REMOTE" to categorize the operation
            http_client: Optional HTTP client to send scan operation stats to server
        """
        # Convert stats to dataclass outside the critical section (non-blocking)
        try:
            lance_scan_stats = lance_stats_to_lance_scan_stats(scan_stats)
        except Exception as e:
            logging.warning(
                f"Failed to convert scan_stats to LanceScanStats: {e}. Skipping stats collection."
            )
            return

        # Determine component key and operation type
        if operation_type == "LOCAL":
            component_key = f"{component_name}_LOCAL"
            comp_operation_type = OperationType.LOCAL
        elif operation_type == "REMOTE":
            component_key = f"{component_name}_REMOTE"
            comp_operation_type = OperationType.REMOTE
        else:
            component_key = component_name
            comp_operation_type = OperationType.UNSPECIFIED

        with self._lock:
            if self._shutdown:
                logger.warning("Cannot add scan stats - collector is shutting down")
                return

            # Track completed scenes for progress bar (only for REMOTE/download operations)
            if comp_operation_type == OperationType.REMOTE and scenes_count > 0:
                self.completed_scenes_count += scenes_count
                # Update progress bar immediately (tqdm is thread-safe)
                if self.progress_bar:
                    self.progress_bar.update(scenes_count)

            # Submit HTTP request if remote operation
            if comp_operation_type == OperationType.REMOTE:
                self._http_executor.submit(
                    self._send_scan_operation,
                    http_client,
                    component_key,
                    comp_operation_type,
                    lance_scan_stats,
                    scenes_count,
                    batch_count,
                )

            # Submit to thread pool for async stats processing (non-blocking)
            self._stats_executor.submit(
                self._process_scan_update,
                component_key,
                comp_operation_type,
                lance_scan_stats,
                scenes_count,
                batch_count,
            )

    def _process_scan_update(
        self,
        component_key: str,
        comp_operation_type: OperationType,
        lance_scan_stats: LanceScanStats,
        scenes_count: int,
        batch_count: int,
    ):
        """Process a single scan update (runs in background thread pool)."""
        try:
            with self._lock:
                # Get or create component stats
                if component_key not in self.component_stats_map:
                    comp_stats = ComponentStats(
                        component_name=component_key,
                        operation_type=comp_operation_type,
                    )
                    self.component_stats_map[component_key] = comp_stats
                else:
                    comp_stats = self.component_stats_map[component_key]

                # Increment counts
                if scenes_count > 0:
                    comp_stats.scenes_downloaded += scenes_count
                if batch_count > 0:
                    comp_stats.batches_processed += batch_count

                # Aggregate stats incrementally
                agg = comp_stats.aggregated_stats
                agg.iops += lance_scan_stats.iops
                agg.requests += lance_scan_stats.requests
                agg.bytes_read += lance_scan_stats.bytes_read
                agg.indices_loaded += lance_scan_stats.indices_loaded
                agg.parts_loaded += lance_scan_stats.parts_loaded
                agg.index_comparisons += lance_scan_stats.index_comparisons
                agg.ranges_scanned += lance_scan_stats.ranges_scanned
                agg.rows_scanned += lance_scan_stats.rows_scanned
                agg.fragments_scanned += lance_scan_stats.fragments_scanned
                agg.total_latency_us += lance_scan_stats.total_latency_us

                # Merge additional_counts
                for key, value in lance_scan_stats.additional_counts.items():
                    agg.additional_counts[key] = agg.additional_counts.get(key, 0) + value

        except Exception as e:
            logger.error(f"Error processing scan update: {e}", exc_info=True)

    def _send_scan_operation(
        self,
        http_client,
        component_key: str,
        comp_operation_type: OperationType,
        lance_scan_stats: LanceScanStats,
        scenes_count: int,
        batch_count: int,
    ):
        """Send scan operation to server via HTTP POST."""
        try:
            # Create EmitScanOperationRequest dataclass
            request = EmitScanOperationRequest(
                session_id=self.session_stats.session_id,
                component_name=component_key,
                operation_type=comp_operation_type,
                scan_stats=lance_scan_stats,
                scene_id="",  # Can be populated if scene_id is tracked
                start_timestamp=None,
                end_timestamp=None,
            )

            # Log if live_logs is enabled
            json_data = request.to_dict()
            response = http_client.post(API_EMIT_SCAN_OPERATION, json=json_data)
            if response.status_code != 200:
                logger.warning(
                    f"Unexpected response when sending scan operation. Response: {response.status_code}"
                )
                logger.warning(f"Request: {json_data}")
        except Exception as e:
            logger.error(f"Failed to send scan operation: {e}")

    def finalize(self, results, http_client=None):
        """Finalize the session stats with results and optionally send via HTTP.

        Waits for all pending stats updates to complete before finalizing.
        If http_client is provided, sends the stats to the server.

        Args:
            results: Download results to compute summary statistics
            http_client: Optional HTTP client to send stats to server
        """
        # Signal shutdown and wait for all pending stats updates to complete
        self._shutdown = True
        self._stats_executor.shutdown(wait=True)
        self._http_executor.shutdown(wait=True)

        # Close progress bar
        if self.progress_bar:
            self.progress_bar.close()

        end_time = datetime.now()

        # Set timestamps on the dataclass
        self.session_stats.start_time = self.start_time
        self.session_stats.end_time = end_time

        # Set duration
        duration = (end_time - self.start_time).total_seconds()
        self.session_stats.total_duration_seconds = duration

        # Set scene counts from results
        self.session_stats.total_scenes_requested = len(results)
        self.session_stats.total_scenes_completed = sum(
            1 for r in results if r.overall_status == "COMPLETE"
        )
        self.session_stats.total_scenes_failed = sum(
            1 for r in results if r.overall_status == "FAILED"
        )

        # Add component stats to session (aggregated stats already computed incrementally)
        self.session_stats.component_stats = list(self.component_stats_map.values())

        # Extract run IDs
        run_ids = sorted(set(r.run_id for r in results if r.run_id))
        self.session_stats.run_ids = run_ids
        self.send_stats_via_http(http_client)

    def send_stats_via_http(self, http_client) -> bool:
        """Send the finalized stats to the server via HTTP POST.

        Args:
            http_client: Instance of HTTPClient to use for sending

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert dataclass to JSON dict
            json_data = self.session_stats.to_dict()

            self._log(f"\n📊 Sending download metrics to server...")
            self._log(f"   Session ID: {self.session_stats.session_id}")
            self._log(f"   Total scenes: {self.session_stats.total_scenes_requested}")
            self._log(f"   Components: {len(self.session_stats.component_stats)}")

            # Send via HTTP POST
            response = http_client.post(API_EMIT_DOWNLOAD_SUMMARY, json=json_data)
            if response.status_code != 200:
                logger.warning(
                    f"Unexpected response when sending statistics. Response: {response.status_code}"
                )
                logger.warning(f"Request: {json_data}")
                self._log(f"⚠️  Metrics sent but unexpected response: {response.status_code}")
            else:
                self._log(f"✅ Download metrics sent successfully to server")
            return True

        except Exception as e:
            logger.error(f"Failed to send statistics: {e}")
            self._log(f"❌ Failed to send metrics: {e}")
            return False
