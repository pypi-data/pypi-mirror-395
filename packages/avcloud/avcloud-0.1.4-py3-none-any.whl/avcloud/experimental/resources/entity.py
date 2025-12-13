"""
Shared entity definitions for AVCloud resources.

This module contains common data models used across different resources
like SearchV2, DownloaderV2, and statistics collection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


@dataclass
class SummaryItem:
    """A summary item describing a scene.

    This entity represents a scene with its metadata including timestamps,
    identifiers, location, and operational design domain (ODD) attributes.

    Attributes:
        create_timestamp: When the record was created
        update_timestamp: When the record was last updated
        delete_timestamp: When the record was deleted (if applicable)
        scene_start_timestamp: When the scene started
        scene_end_timestamp: When the scene ended
        scene_id: Unique identifier for the scene
        run_id: Identifier for the run
        device_type: Type of device (e.g., "LUCID_AIR")
        device_id: Unique identifier for the device
        city: City where the scene was captured
        country: Country where the scene was captured
        odds: Operational Design Domain attributes (flexible dict)
    """

    create_timestamp: Optional[datetime] = None
    update_timestamp: Optional[datetime] = None
    delete_timestamp: Optional[datetime] = None

    scene_start_timestamp: Optional[datetime] = None
    scene_end_timestamp: Optional[datetime] = None

    scene_id: Optional[str] = None
    run_id: Optional[str] = None
    device_type: Optional[str] = None
    device_id: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    odds: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SummaryItem:
        """Create SummaryItem from API response dict.

        Handles timestamp conversion from ISO strings or epoch milliseconds
        to datetime objects.

        Args:
            data: Dictionary from API response

        Returns:
            SummaryItem with parsed timestamps
        """

        def parse_timestamp(value: Any) -> Optional[datetime]:
            """Parse timestamp from various formats."""
            if value is None:
                return None

            # If it's already a datetime, return it
            if isinstance(value, datetime):
                return value

            # If it's an epoch timestamp (milliseconds)
            if isinstance(value, (int, float)):
                return datetime.fromtimestamp(value / 1000)

            # If it's a string, try to parse it
            if isinstance(value, str):
                # Try ISO format
                try:
                    # Remove 'Z' suffix if present
                    ts = value.replace("Z", "+00:00")
                    return datetime.fromisoformat(ts)
                except ValueError:
                    pass

                # Try other common formats
                for fmt in [
                    "%Y-%m-%dT%H:%M:%S.%f",
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                ]:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue

            return None

        return cls(
            create_timestamp=parse_timestamp(data.get("createTimestamp")),
            update_timestamp=parse_timestamp(data.get("updateTimestamp")),
            delete_timestamp=parse_timestamp(data.get("deleteTimestamp")),
            scene_start_timestamp=parse_timestamp(data.get("sceneStartTimestamp")),
            scene_end_timestamp=parse_timestamp(data.get("sceneEndTimestamp")),
            scene_id=data.get("sceneId"),
            run_id=data.get("runId"),
            device_type=data.get("deviceType"),
            device_id=data.get("deviceId"),
            city=data.get("city"),
            country=data.get("country"),
            odds=data.get("odds", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert SummaryItem to dictionary.

        Timestamps are converted to ISO format strings.

        Returns:
            Dictionary representation
        """

        def format_timestamp(dt: Optional[datetime]) -> Optional[str]:
            """Format datetime to ISO string."""
            return dt.isoformat() if dt else None

        return {
            "create_timestamp": format_timestamp(self.create_timestamp),
            "update_timestamp": format_timestamp(self.update_timestamp),
            "delete_timestamp": format_timestamp(self.delete_timestamp),
            "scene_start_timestamp": format_timestamp(self.scene_start_timestamp),
            "scene_end_timestamp": format_timestamp(self.scene_end_timestamp),
            "scene_id": self.scene_id,
            "run_id": self.run_id,
            "device_type": self.device_type,
            "device_id": self.device_id,
            "city": self.city,
            "country": self.country,
            "odds": self.odds,
        }


class OperationType(Enum):
    """Type of operation (local disk vs remote download)."""

    UNSPECIFIED = "OPERATION_TYPE_UNSPECIFIED_INVALID"
    LOCAL = "OPERATION_TYPE_LOCAL"
    REMOTE = "OPERATION_TYPE_REMOTE"


@dataclass
class LanceScanStats:
    """Statistics from a single Lance scan operation."""

    iops: int = 0
    requests: int = 0
    bytes_read: int = 0
    indices_loaded: int = 0
    parts_loaded: int = 0
    index_comparisons: int = 0
    ranges_scanned: int = 0
    rows_scanned: int = 0
    fragments_scanned: int = 0
    total_latency_us: int = 0
    additional_counts: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "iops": self.iops,
            "requests": self.requests,
            "bytes_read": self.bytes_read,
            "indices_loaded": self.indices_loaded,
            "parts_loaded": self.parts_loaded,
            "index_comparisons": self.index_comparisons,
            "ranges_scanned": self.ranges_scanned,
            "rows_scanned": self.rows_scanned,
            "fragments_scanned": self.fragments_scanned,
            "total_latency_us": self.total_latency_us,
            "additional_counts": self.additional_counts,
        }


@dataclass
class ComponentStats:
    """Aggregated statistics for a component (e.g., camera, lidar)."""

    component_name: str
    operation_type: OperationType = OperationType.UNSPECIFIED
    aggregated_stats: LanceScanStats = field(default_factory=LanceScanStats)
    scenes_downloaded: int = 0
    batches_processed: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""

        def format_timestamp(dt: Optional[datetime]) -> Optional[str]:
            """Format datetime to RFC3339 string with Z suffix."""
            if dt is None:
                return None
            # Convert naive datetime to UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            # Convert to UTC and format with Z suffix
            return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

        return {
            "component_name": self.component_name,
            "operation_type": self.operation_type.value,
            "aggregated_stats": self.aggregated_stats.to_dict(),
            "scenes_downloaded": self.scenes_downloaded,
            "batches_processed": self.batches_processed,
            "start_time": format_timestamp(self.start_time),
            "end_time": format_timestamp(self.end_time),
        }


@dataclass
class EmitScanOperationRequest:
    """Request for emitting a scan operation to the server."""

    session_id: str
    component_name: str
    operation_type: OperationType
    scan_stats: LanceScanStats
    scene_id: str = ""
    start_timestamp: Optional[datetime] = None
    end_timestamp: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""

        def format_timestamp(dt: Optional[datetime]) -> Optional[str]:
            """Format datetime to RFC3339 string with Z suffix."""
            if dt is None:
                return None
            # Convert naive datetime to UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            # Convert to UTC and format with Z suffix
            return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

        return {
            "session_id": self.session_id,
            "component_name": self.component_name,
            "operation_type": self.operation_type.value,
            "scan_stats": self.scan_stats.to_dict(),
            "scene_id": self.scene_id,
            "start_timestamp": format_timestamp(self.start_timestamp),
            "end_timestamp": format_timestamp(self.end_timestamp),
        }


@dataclass
class DownloadSummaryStats:
    """Complete download session statistics."""

    session_id: str
    dataset_path: str
    region: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_scenes_requested: int = 0
    total_scenes_completed: int = 0
    total_scenes_failed: int = 0
    on_exist_policy: str = "skip"
    component_stats: List[ComponentStats] = field(default_factory=list)
    run_ids: List[str] = field(default_factory=list)
    max_workers: int = 1
    total_duration_seconds: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization.

        Timestamps are converted to RFC3339 format with 'Z' suffix for UTC.
        """

        def format_timestamp(dt: Optional[datetime]) -> Optional[str]:
            """Format datetime to RFC3339 string with Z suffix."""
            if dt is None:
                return None
            # Convert naive datetime to UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            # Convert to UTC and format with Z suffix
            return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

        return {
            "session_id": self.session_id,
            "dataset_path": self.dataset_path,
            "region": self.region,
            "start_time": format_timestamp(self.start_time),
            "end_time": format_timestamp(self.end_time),
            "total_scenes_requested": self.total_scenes_requested,
            "total_scenes_completed": self.total_scenes_completed,
            "total_scenes_failed": self.total_scenes_failed,
            "on_exist_policy": self.on_exist_policy,
            "component_stats": [comp.to_dict() for comp in self.component_stats],
            "run_ids": self.run_ids,
            "max_workers": self.max_workers,
            "total_duration_seconds": self.total_duration_seconds,
        }
