from __future__ import annotations

import os
import pathlib
from dataclasses import dataclass
from typing import Dict, List, Optional

import pyarrow as pa

from .av_schema_to_arrow import (
    camera_labels_schema,
    camera_schema,
    gnss_schema,
    imu_schema,
    laser_map_schema,
    lidar_labels_schema,
    lidar_schema,
    misc_data_schema,
    odd_schema,
    path_point_schema,
    pose_schema,
    radar_schema,
    summary_schema,
    transform_schema,
    vehicle_state_schema,
    wheel_odometry_schema,
)

DEFAULT_REGISTRY_PATH = pathlib.Path(
    os.environ.get("PEARL_SCHEMA_REGISTRY", "./schema_registry.pb")
)


@dataclass
class SchemaIdentity:
    name: str
    version: str
    revision: int


from . import registry_meta_pb2 as pb


class SchemaRegistry:
    def __init__(self) -> None:
        self._name_to_versions: Dict[str, List[SchemaIdentity]] = {}

    def register(
        self, name: str, schema: pa.Schema, version: str = "1.0.0", revision: int = 0
    ) -> SchemaIdentity:
        ident = SchemaIdentity(name=name, version=version, revision=revision)
        self._name_to_versions.setdefault(name, [])
        replaced = False
        for i, existing in enumerate(self._name_to_versions[name]):
            if existing.version == version and existing.revision == revision:
                self._name_to_versions[name][i] = ident
                replaced = True
                break
        if not replaced:
            self._name_to_versions[name].append(ident)
        return ident

    def _resolve_schema(self, name: str) -> pa.Schema:
        if name == "Camera":
            return camera_schema()
        if name == "Lidar":
            return lidar_schema()
        if name == "Imu":
            return imu_schema()
        if name == "Gnss":
            return gnss_schema()
        if name == "WheelOdometry":
            return wheel_odometry_schema()
        if name == "VehicleState":
            return vehicle_state_schema()
        if name == "Pose":
            return pose_schema()
        if name == "Odd":
            return odd_schema()
        if name == "Summary":
            return summary_schema()
        if name == "CameraLabels":
            return camera_labels_schema()
        if name == "LidarLabels":
            return lidar_labels_schema()
        if name == "LaserMap":
            return laser_map_schema()
        if name == "PathPoint":
            return path_point_schema()
        if name == "Transform":
            return transform_schema()
        if name == "Radar":
            return radar_schema()
        if name == "MiscData":
            return misc_data_schema()
        raise KeyError(f"Unknown schema name: {name}")

    def get(
        self, name: str, version: Optional[str] = None, revision: Optional[int] = None
    ) -> pa.Schema:
        versions = self._name_to_versions.get(name, [])
        if not versions:
            raise KeyError(f"Schema not found: {name}")
        if version is not None:
            versions = [v for v in versions if v.version == version]
            if not versions:
                raise KeyError(f"Schema not found: {name} version={version}")
        if revision is None:
            chosen = max(versions, key=lambda x: x.revision)
        else:
            matches = [v for v in versions if v.revision == revision]
            if not matches:
                raise KeyError(f"Schema not found: {name} version={version} revision={revision}")
            chosen = matches[0]
        return self._resolve_schema(chosen.name)

    def list_identities(self) -> List[SchemaIdentity]:
        out: List[SchemaIdentity] = []
        for items in self._name_to_versions.values():
            out.extend(items)
        return out

    def save(self, path: os.PathLike[str] | str = DEFAULT_REGISTRY_PATH) -> None:
        module = pb
        reg = module.SchemaRegistry()
        for name, versions in self._name_to_versions.items():
            for v in versions:
                reg.records.add(name=name, version=v.version, revision=v.revision)
        pathlib.Path(path).write_bytes(reg.SerializeToString())

    @classmethod
    def load(cls, path: os.PathLike[str] | str = DEFAULT_REGISTRY_PATH) -> "SchemaRegistry":
        module = pb
        reg = module.SchemaRegistry()
        reg.ParseFromString(pathlib.Path(path).read_bytes())
        inst = cls()
        for rec in reg.records:
            inst.register(
                name=rec.name,
                schema=inst._resolve_schema(rec.name),
                version=rec.version,
                revision=rec.revision,
            )
        return inst
