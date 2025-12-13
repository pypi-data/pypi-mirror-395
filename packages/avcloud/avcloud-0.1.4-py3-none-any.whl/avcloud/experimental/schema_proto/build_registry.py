from __future__ import annotations

import argparse
import pathlib

from .av_schema_to_arrow import (
    camera_labels_schema,
    camera_schema,
    gnss_schema,
    imu_schema,
    laser_map_schema,
    lidar_labels_schema,
    lidar_schema,
    misc_data_schema,
    path_point_schema,
    pose_schema,
    radar_schema,
    summary_schema,
    transform_schema,
    vehicle_state_schema,
    wheel_odometry_schema,
)
from .registry import DEFAULT_REGISTRY_PATH, SchemaRegistry


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and persist AV schema registry")
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=DEFAULT_REGISTRY_PATH,
        help="Output path for schema_registry.pb",
    )
    parser.add_argument(
        "--version",
        type=str,
        default="1.0.0",
        help="Semantic version for these schemas",
    )
    parser.add_argument("--revision", type=int, default=1, help="Monotonic revision number")
    args = parser.parse_args()

    reg = SchemaRegistry()
    reg.register("Camera", camera_schema(), version=args.version, revision=args.revision)
    reg.register("Lidar", lidar_schema(), version=args.version, revision=args.revision)
    reg.register("Imu", imu_schema(), version=args.version, revision=args.revision)
    reg.register("Gnss", gnss_schema(), version=args.version, revision=args.revision)
    reg.register(
        "WheelOdometry",
        wheel_odometry_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "VehicleState",
        vehicle_state_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "Pose",
        pose_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "Summary",
        summary_schema(),
        version=args.version,
        revision=args.revision,
    )

    # Detached label datasets
    reg.register(
        "CameraLabels",
        camera_labels_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "LidarLabels",
        lidar_labels_schema(),
        version=args.version,
        revision=args.revision,
    )

    reg.register(
        "LaserMap",
        laser_map_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "PathPoint",
        path_point_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "Transform",
        transform_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "Radar",
        radar_schema(),
        version=args.version,
        revision=args.revision,
    )
    reg.register(
        "MiscData",
        misc_data_schema(),
        version=args.version,
        revision=args.revision,
    )

    reg.save(args.out)
    print(f"Saved schema registry with {len(reg.list_identities())} records to {args.out}")


if __name__ == "__main__":
    main()
