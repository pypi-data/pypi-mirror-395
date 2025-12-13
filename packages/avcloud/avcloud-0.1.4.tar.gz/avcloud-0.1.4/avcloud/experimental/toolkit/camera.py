"""
Camera video encoding/decoding utilities.

This module provides functions for working with camera data in Lance datasets,
including video encoding/decoding and frame extraction.
"""

import io
from typing import Optional, Union

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc


def stitch_camera_to_video(
    camera_table: Union[pa.Table, pd.DataFrame, str],
    scene_id: Optional[str] = None,
    camera_name: str = "front",
    output_path: str = "output.mp4",
    fps: float = 30.0,
    container_format: str = "mp4",
) -> dict:
    """Stitch compressed camera frames directly into video (fast, lossless muxing).

    Directly **muxes** (封装) already-compressed H.264/H.265 frames into a video
    container WITHOUT decoding/re-encoding. Much faster and preserves original quality.

    This is the RECOMMENDED method for exporting camera data to video.

    Args:
        camera_table: PyArrow Table, pandas DataFrame, or path string.
                     If string, treated as base_path and scene_id is required.
        scene_id: Scene ID to export (required if camera_table is a path string)
        camera_name: Camera name (e.g., "front", "left", "right")
        output_path: Output video file path (e.g., "/output/front.mp4")
        fps: Playback frame rate (default: 30.0)
        container_format: Container format - "mp4", "mkv" (default: "mp4")

    Returns:
        dict with statistics:
        {
            "output_path": str,
            "frames_written": int,
            "duration_sec": float,
            "codec": str,  # Detected codec (h264/hevc)
        }

    Examples:
        from avcloud.experimental.toolkit import stitch_camera_to_video, read_component

        # Option 1: Use with path (backward compatible)
        result = stitch_camera_to_video(
            "/data",
            scene_id="scene_001",
            camera_name="front",
            output_path="/output/front.mp4"
        )

        # Option 2: Use with already-loaded table (more efficient!)
        camera = read_component("/data", "camera", scene_ids=["scene_001"])
        result = stitch_camera_to_video(
            camera,
            camera_name="front",
            output_path="/output/front.mp4"
        )

    Notes:
        - NO transcoding: directly muxes compressed frames (10-100× faster)
        - Preserves original quality (lossless)
        - Output codec matches input (H.264 or H.265)
        - Recommended over encode_camera_to_video() unless you need transcoding
    """
    from .io import read_component

    # Handle path string (backward compatibility)
    if isinstance(camera_table, str):
        if scene_id is None:
            raise ValueError("scene_id is required when camera_table is a path string")
        base_path = camera_table
        # Read camera data (need sensor_timestamp and sensor_type for filtering)
        camera = read_component(
            base_path,
            "camera",
            columns=["scene_id", "sensor_timestamp", "is_keyframe", "camera", "sensor_type"],
            scene_ids=[scene_id],
        )
    else:
        # Already loaded table
        camera = camera_table
        if isinstance(camera, pd.DataFrame):
            camera = pa.Table.from_pandas(camera)

        # Filter by scene_id if provided
        if scene_id is not None:
            mask = pc.equal(camera["scene_id"], scene_id)
            camera = camera.filter(mask)

    if len(camera) == 0:
        raise ValueError(
            f"No camera data found" + (f" for scene_id={scene_id}" if scene_id else "")
        )

    try:
        import av
    except ImportError:
        raise ImportError("PyAV is required for video muxing. Install with: pip install av")

    # Filter by sensor_type using PyArrow compute (no pandas conversion needed!)
    if "sensor_type" in camera.column_names:
        # Use PyArrow compute to filter
        mask = pc.equal(camera["sensor_type"], camera_name)
        camera_filtered = camera.filter(mask)

        # Check if filtering by sensor_type worked (might be None/null values in old data)
        if len(camera_filtered) == 0:
            # Fallback: filter by checking camera dict (for old data without sensor_type values)
            df = camera.to_pandas()

            def has_camera_data(camera_dict):
                if not isinstance(camera_dict, dict):
                    return False
                cam_data = camera_dict.get(camera_name)
                return cam_data is not None and len(cam_data) > 0

            df_filtered = df[df["camera"].apply(has_camera_data)].copy()
            camera_filtered = pa.Table.from_pandas(df_filtered)
    else:
        # Fallback: convert to pandas if sensor_type column doesn't exist
        df = camera.to_pandas()

        def has_camera_data(camera_dict):
            if not isinstance(camera_dict, dict):
                return False
            cam_data = camera_dict.get(camera_name)
            return cam_data is not None and len(cam_data) > 0

        df_filtered = df[df["camera"].apply(has_camera_data)].copy()
        camera_filtered = pa.Table.from_pandas(df_filtered)

    if len(camera_filtered) == 0:
        raise ValueError(f"No frames found for camera '{camera_name}'")

    # Convert to list for iteration (more efficient than pandas)
    camera_list = camera_filtered.to_pylist()

    # Collect frames with valid data
    frames_data = []
    first_timestamp = None

    for row in camera_list:
        video_data = row.get("camera")
        # With sensor_type filtering, we can directly access the camera_name in the dict
        if isinstance(video_data, dict) and camera_name in video_data:
            chunk = video_data[camera_name]
            if chunk is not None and len(chunk) > 0:
                # Parse timestamp (PyArrow returns as int64 nanoseconds or string)
                timestamp_raw = row["sensor_timestamp"]
                if isinstance(timestamp_raw, (int, np.integer)):
                    timestamp = pd.Timestamp(timestamp_raw, unit="ns")
                elif isinstance(timestamp_raw, str):
                    timestamp = pd.Timestamp(timestamp_raw)
                else:
                    timestamp = pd.Timestamp(timestamp_raw)

                if first_timestamp is None:
                    first_timestamp = timestamp

                # Calculate relative time in seconds
                relative_time_sec = (timestamp - first_timestamp).total_seconds()

                is_keyframe = row.get("is_keyframe", False)
                frames_data.append(
                    {
                        "data": chunk,
                        "is_keyframe": is_keyframe,
                        "timestamp": relative_time_sec,
                    }
                )

    if not frames_data:
        raise ValueError(f"No valid frames found for camera '{camera_name}'")

    # Detect codec from first frame
    first_frame_bytes = frames_data[0]["data"]
    codec_detected = _detect_codec(first_frame_bytes)

    # Open output container
    output = av.open(output_path, mode="w", format=container_format)

    # Create video stream (copy mode - no transcoding)
    from fractions import Fraction

    # Convert fps to Fraction for PyAV
    if isinstance(fps, (int, float)):
        fps_fraction = Fraction(int(fps * 1000), 1000).limit_denominator(10000)
    else:
        fps_fraction = fps
    stream = output.add_stream(codec_detected, rate=fps_fraction)

    # Get resolution from first frame
    temp_container = av.open(io.BytesIO(first_frame_bytes))
    temp_stream = temp_container.streams.video[0]
    stream.width = temp_stream.width
    stream.height = temp_stream.height
    temp_container.close()

    # Use high-precision time_base (90kHz is standard for video)
    # This allows accurate representation of any timestamp
    TIME_BASE_HZ = 90000
    stream.time_base = Fraction(1, TIME_BASE_HZ)

    # Write frames with actual timestamps
    frames_written = 0
    for frame_info in frames_data:
        # Create packet from raw compressed data
        packet = av.Packet(frame_info["data"])

        # Set keyframe flag
        if frame_info["is_keyframe"]:
            packet.is_keyframe = True

        # Set presentation timestamp from actual sensor_timestamp
        # Convert seconds to time_base units
        timestamp_sec = frame_info["timestamp"]
        pts_value = int(timestamp_sec * TIME_BASE_HZ)

        packet.pts = pts_value
        packet.dts = pts_value
        packet.time_base = stream.time_base

        # Mux packet to container
        output.mux(packet)
        frames_written += 1

    # Close output
    output.close()

    return {
        "output_path": output_path,
        "frames_written": frames_written,
        "duration_sec": frames_written / fps,
        "codec": codec_detected,
    }


def _detect_codec(video_bytes: bytes) -> str:
    """Detect H.264 or H.265 codec from compressed video data."""
    try:
        import av

        container = av.open(io.BytesIO(video_bytes))
        stream = container.streams.video[0]
        codec_name = stream.codec_context.codec.name
        container.close()

        if "hevc" in codec_name.lower() or "h265" in codec_name.lower():
            return "hevc"
        elif "h264" in codec_name.lower() or "avc" in codec_name.lower():
            return "h264"
        else:
            return "hevc"  # Default
    except:
        return "hevc"  # Fallback


def encode_camera_to_video(
    base_path: str,
    scene_id: str,
    camera_name: str,
    output_path: str,
    codec: str = "h265",
    fps: float = 30.0,
    bitrate: str = "5M",
    resolution: Optional[tuple] = None,
    gop_size: Optional[int] = None,
) -> dict:
    """Transcode camera frames to video with custom encoding parameters.

    This function **transcodes** (转码): decodes frames and re-encodes with custom
    parameters. Slower than stitch_camera_to_video() but allows changing codec,
    resolution, bitrate, etc.

    **Recommendation:** Use stitch_camera_to_video() unless you need to change
    encoding parameters. It's much faster and preserves quality.

    Args:
        base_path: Path to downloaded Lance dataset directory
        scene_id: Scene ID to export (e.g., "scene_001")
        camera_name: Camera name (e.g., "front", "left", "right")
        output_path: Output video file path (e.g., "/output/front.mp4")
        codec: Output codec - "h264", "h265", "vp9" (default: "h265")
        fps: Output frame rate (default: 10.0)
        bitrate: Target bitrate (e.g., "5M", "10M", default: "5M")
        resolution: Optional (width, height) to resize (default: keep original)
        gop_size: GOP (Group of Pictures) size - keyframe interval (default: None, uses encoder default)

    Returns:
        dict with statistics:
        {
            "output_path": str,
            "frames_written": int,
            "duration_sec": float,
            "codec": str,
            "resolution": tuple,
            "bitrate": str,
            "gop_size": int or None,
        }

    Examples:
        from avcloud.experimental.toolkit import encode_camera_to_video

        # Transcode to H.264 (for compatibility)
        result = encode_camera_to_video(
            "/data",
            "scene_001",
            "front",
            "/output/front_h264.mp4",
            codec="h264",
            bitrate="10M"
        )

        # Resize to lower resolution
        result = encode_camera_to_video(
            "/data",
            "scene_001",
            "front",
            "/output/front_720p.mp4",
            resolution=(1280, 720)
        )

        # Set custom GOP size (keyframe every 30 frames)
        result = encode_camera_to_video(
            "/data",
            "scene_001",
            "front",
            "/output/front_gop30.mp4",
            codec="h264",
            gop_size=30
        )

    Notes:
        - Slower than stitch_camera_to_video() (requires decode+encode)
        - May have quality loss due to re-encoding
        - Use when you need to change codec, resolution, or bitrate
    """
    from .io import read_component

    # Read camera data
    camera = read_component(
        base_path, "camera", columns=["scene_id", "is_keyframe", "camera"], scene_ids=[scene_id]
    )

    if len(camera) == 0:
        raise ValueError(f"No camera data found for scene_id={scene_id}")

    try:
        import av
    except ImportError:
        raise ImportError("PyAV is required for video encoding. Install with: pip install av")

    # Decode all frames first (using optimized batch decoder)
    decoded_table = decode_video_column(camera, camera_name=camera_name, format="raw")
    decoded_df = decoded_table.to_pandas()

    # Filter valid frames
    valid_frames = [f for f in decoded_df["decoded_frame"] if f is not None]

    if not valid_frames:
        raise ValueError(f"No valid frames to encode for camera '{camera_name}'")

    # Get original resolution
    orig_height, orig_width = valid_frames[0].shape[:2]

    # Use original resolution if not specified
    if resolution is None:
        resolution = (orig_width, orig_height)

    # Open output container
    output = av.open(output_path, mode="w")

    # Map codec names
    codec_map = {
        "h264": "h264",
        "h265": "hevc",
        "hevc": "hevc",
        "vp9": "vp9",
    }
    codec_name = codec_map.get(codec.lower(), "hevc")

    # Create video stream
    from fractions import Fraction

    stream = output.add_stream(codec_name, rate=Fraction(int(fps * 1000), 1000))
    stream.width = resolution[0]
    stream.height = resolution[1]
    stream.pix_fmt = "yuv420p"

    # Set bitrate
    if bitrate:
        # Parse bitrate (e.g., "5M" -> 5000000)
        if isinstance(bitrate, str):
            if bitrate.endswith("M") or bitrate.endswith("m"):
                bitrate_int = int(float(bitrate[:-1]) * 1_000_000)
            elif bitrate.endswith("K") or bitrate.endswith("k"):
                bitrate_int = int(float(bitrate[:-1]) * 1_000)
            else:
                bitrate_int = int(bitrate)
        else:
            bitrate_int = bitrate
        stream.bit_rate = bitrate_int

    # Set GOP size
    if gop_size is not None:
        stream.gop_size = gop_size

    # Encode frames
    frames_written = 0
    for frame_array in valid_frames:
        # Resize if needed
        if resolution != (orig_width, orig_height):
            try:
                import cv2

                frame_array = cv2.resize(frame_array, resolution)
            except ImportError:
                from PIL import Image

                img = Image.fromarray(frame_array)
                img = img.resize(resolution, Image.Resampling.LANCZOS)
                frame_array = np.array(img)

        # Create VideoFrame
        frame = av.VideoFrame.from_ndarray(frame_array, format="rgb24")

        # Encode
        for packet in stream.encode(frame):
            output.mux(packet)

        frames_written += 1

    # Flush encoder
    for packet in stream.encode():
        output.mux(packet)

    # Close output
    output.close()

    return {
        "output_path": output_path,
        "frames_written": frames_written,
        "duration_sec": frames_written / fps,
        "codec": codec,
        "resolution": resolution,
        "bitrate": bitrate,
        "gop_size": gop_size,
    }


def decode_video_column(
    camera_table: Union[pa.Table, pd.DataFrame],
    video_column: str = "camera",
    camera_name: str = "front",
    output_column: str = "decoded_frame",
    format: str = "jpeg",
) -> pa.Table:
    """Decode video column into individual camera frames (optimized batch decoding).

    Efficiently decodes all frames by processing each GOP (Group of Pictures) once,
    avoiding redundant decoding. Much faster than calling decode_video_frame() per row.

    Args:
        camera_table: PyArrow Table or Pandas DataFrame with video column
        video_column: Name of video column to decode (default: "camera")
        camera_name: Camera name to decode (default: "front")
        output_column: Name of output decoded image column (default: "decoded_frame")
        format: Output image format ("jpeg", "png", "raw", default: "jpeg")

    Returns:
        PyArrow Table with decoded frame column added.

    Examples:
        # Read camera data
        camera = read_component("/data", "camera")

        # Decode front camera frames to JPEG (optimized batch processing)
        decoded = decode_video_column(camera, camera_name="front", format="jpeg")

        # Access decoded frames
        df = decoded.to_pandas()
        img_bytes = df.iloc[0]['decoded_frame']  # JPEG bytes for row 0

        # Decode to raw numpy arrays for processing
        decoded_raw = decode_video_column(camera, camera_name="front", format="raw")
        df_raw = decoded_raw.to_pandas()
        img_array = df_raw.iloc[0]['decoded_frame']  # numpy array (H, W, 3)

    Notes:
        - Optimized for batch decoding (O(N) instead of O(N²))
        - Processes each GOP only once
        - Much faster than sequential decode_video_frame() calls
        - "jpeg": Returns compressed JPEG bytes (smaller memory footprint)
        - "png": Returns compressed PNG bytes (lossless)
        - "raw": Returns numpy arrays (H, W, 3) uint8 (larger memory usage)
    """
    try:
        import av
    except ImportError:
        raise ImportError("PyAV is required for video decoding. Install with: pip install av")

    # Convert to pandas if needed
    df = camera_table.to_pandas() if isinstance(camera_table, pa.Table) else camera_table.copy()

    # Filter by sensor_type column if available (much simpler!)
    if "sensor_type" in df.columns:
        df = df[df["sensor_type"] == camera_name].copy()
    else:
        # Fallback: filter by checking camera dict
        def has_camera_data(camera_dict):
            if not isinstance(camera_dict, dict):
                return False
            cam_data = camera_dict.get(camera_name)
            return cam_data is not None and len(cam_data) > 0

        df = df[df[video_column].apply(has_camera_data)].copy()

    if len(df) == 0:
        raise ValueError(f"No frames found for camera '{camera_name}'")

    # Initialize result array
    decoded_frames = [None] * len(df)

    # Group by scene_id for efficient processing
    for scene_id, scene_group in df.groupby("scene_id", sort=False):
        # Note: scene_id is already in temporal order, no need to sort

        # Find all keyframes with valid camera data
        keyframe_indices = []

        for idx in scene_group.index:
            row = scene_group.loc[idx]
            # Only consider rows marked as keyframes
            if not row.get("is_keyframe", False):
                continue

            video_data = row[video_column]
            if isinstance(video_data, dict) and camera_name in video_data:
                chunk = video_data[camera_name]
                if chunk is not None and len(chunk) > 0:
                    keyframe_indices.append(idx)

        # If no keyframes found, we cannot decode this scene_group
        # (P/B-frames require a preceding I-frame to decode)
        if not keyframe_indices:
            continue

        # Process each GOP (from keyframe to next keyframe)
        for i, keyframe_idx in enumerate(keyframe_indices):
            # Determine GOP range
            next_keyframe_idx = keyframe_indices[i + 1] if i + 1 < len(keyframe_indices) else None

            # Collect video chunks for this GOP
            video_chunks = []
            gop_indices = []

            # Iterate through sorted indices in scene_group
            for idx in scene_group.index:
                # Skip frames before this keyframe
                if idx < keyframe_idx:
                    continue

                # Stop at next keyframe (belongs to next GOP)
                if next_keyframe_idx is not None and idx >= next_keyframe_idx:
                    break

                row = scene_group.loc[idx]
                video_data = row[video_column]
                if isinstance(video_data, dict) and camera_name in video_data:
                    chunk = video_data[camera_name]
                    if chunk is not None and len(chunk) > 0:
                        video_chunks.append(chunk)
                        gop_indices.append(idx)

            if not video_chunks:
                continue

            # Decode entire GOP at once
            combined_video = b"".join(video_chunks)
            try:
                container = av.open(io.BytesIO(combined_video))
                stream = container.streams.video[0]

                # Decode all frames in GOP
                gop_frames = []
                for frame in container.decode(stream):
                    img = frame.to_ndarray(format="rgb24")

                    # Encode to requested format
                    if format == "raw":
                        gop_frames.append(img)
                    elif format == "jpeg":
                        try:
                            import cv2

                            _, encoded = cv2.imencode(".jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                            gop_frames.append(encoded.tobytes())
                        except ImportError:
                            from PIL import Image

                            buf = io.BytesIO()
                            Image.fromarray(img).save(buf, format="JPEG")
                            gop_frames.append(buf.getvalue())
                    elif format == "png":
                        try:
                            import cv2

                            _, encoded = cv2.imencode(".png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                            gop_frames.append(encoded.tobytes())
                        except ImportError:
                            from PIL import Image

                            buf = io.BytesIO()
                            Image.fromarray(img).save(buf, format="PNG")
                            gop_frames.append(buf.getvalue())

                container.close()

                # Assign decoded frames to result
                for idx, frame in zip(gop_indices, gop_frames):
                    decoded_frames[df.index.get_loc(idx)] = frame

            except Exception as e:
                print(f"Warning: Failed to decode GOP starting at {gop_start}: {e}")

    # Add decoded column
    df[output_column] = decoded_frames

    # Convert back to PyArrow
    return pa.Table.from_pandas(df)


def decode_video_frame(
    camera_table: Union[pa.Table, pd.DataFrame],
    timestamp: Union[pd.Timestamp, str, int, None] = None,
    camera_name: str = "front",
    format: str = "jpeg",
    scene_id: Optional[str] = None,
    timestamp_column: str = "sensor_timestamp",
    frame_id: Optional[str] = None,
) -> Union[bytes, np.ndarray]:
    """Decode a single frame with proper keyframe pre-roll.

    Correctly decodes video frames by finding the frame by timestamp or frame_id,
    then finding the previous keyframe and decoding sequentially (pre-roll).
    This is necessary because most frames are P-frames or B-frames that depend on
    previous frames.

    Args:
        camera_table: PyArrow Table or Pandas DataFrame with camera data
        timestamp: Target timestamp to decode (sensor_timestamp or frame_timestamp).
                   Can be pd.Timestamp, ISO string, or Unix nanoseconds.
                   If None, must provide frame_id.
        camera_name: Camera name (e.g., "front", "left", default: "front")
        format: Output format ("jpeg", "png", "raw", default: "jpeg")
        scene_id: Scene ID (required for timestamp or frame_id lookup)
        timestamp_column: Column to use for timestamp matching
                          ("sensor_timestamp" or "frame_timestamp", default: "sensor_timestamp")
        frame_id: Frame ID within the scene (e.g., "00", "01", "42").
                  Must provide scene_id when using frame_id.

    Returns:
        Decoded frame as bytes (JPEG/PNG) or numpy array (raw).

    Examples:
        # Read camera table
        camera = read_component("/data", "camera",
                                columns=["scene_id", "frame_id", "sensor_timestamp",
                                         "is_keyframe", "camera"])

        # Decode frame by timestamp (recommended)
        target_ts = pd.Timestamp("2024-01-01 12:00:00.123456")
        frame = decode_video_frame(camera, timestamp=target_ts,
                                    camera_name="front", scene_id="scene_001")

        # Decode by frame_id
        frame = decode_video_frame(camera, frame_id="42",
                                    camera_name="front", scene_id="scene_001")

        # Decode as raw numpy array
        frame_array = decode_video_frame(camera, frame_id="00",
                                          camera_name="front", scene_id="scene_001",
                                          format="raw")
        print(frame_array.shape)  # (height, width, 3)

    Notes:
        - Automatically handles keyframe detection and pre-roll
        - P-frames and B-frames are decoded correctly by pre-rolling from keyframe
        - For "raw" format, returns numpy array (H, W, 3) uint8 RGB
        - For "jpeg"/"png", returns compressed image bytes
        - Keyframe handling is automatic - you don't need to worry about frame types
    """
    try:
        import av
    except ImportError:
        raise ImportError("PyAV is required for video decoding. Install with: pip install av")

    # Convert to pandas if needed
    df = camera_table.to_pandas() if isinstance(camera_table, pa.Table) else camera_table

    # Filter by sensor_type column if available (much simpler!)
    if "sensor_type" in df.columns:
        df = df[df["sensor_type"] == camera_name].copy()
    else:
        # Fallback: filter by checking camera dict
        def has_camera_data(camera_dict):
            if not isinstance(camera_dict, dict):
                return False
            cam_data = camera_dict.get(camera_name)
            return cam_data is not None and len(cam_data) > 0

        df = df[df["camera"].apply(has_camera_data)].copy()

    if len(df) == 0:
        raise ValueError(f"No frames found for camera '{camera_name}'")

    # Validate: must provide exactly one of timestamp or frame_id
    if timestamp is not None and frame_id is not None:
        raise ValueError("Provide either 'timestamp' or 'frame_id', not both")
    if timestamp is None and frame_id is None:
        raise ValueError("Must provide either 'timestamp' or 'frame_id'")

    # Ensure timestamp column is datetime
    if timestamp_column in df.columns:
        df[timestamp_column] = pd.to_datetime(df[timestamp_column])

    # Determine target row_index from timestamp or frame_id
    if timestamp is not None:
        # Timestamp-based lookup
        if scene_id is None:
            raise ValueError("scene_id is required when using timestamp-based lookup")

        # Parse timestamp
        if isinstance(timestamp, (int, np.integer)):
            # Unix nanoseconds
            target_ts = pd.Timestamp(timestamp, unit="ns")
        elif isinstance(timestamp, str):
            # ISO string
            target_ts = pd.Timestamp(timestamp)
        else:
            # Already a Timestamp
            target_ts = pd.Timestamp(timestamp)

        # Filter by scene_id (already filtered by sensor_type above)
        scene_df = df[df["scene_id"] == scene_id].copy()
        if len(scene_df) == 0:
            raise ValueError(f"No data found for camera '{camera_name}' in scene_id={scene_id}")

        # Find frame closest to target timestamp (all rows already have this camera)
        valid_df = scene_df.copy()

        if len(valid_df) == 0:
            raise ValueError(
                f"No valid frames found for camera '{camera_name}' in scene {scene_id}"
            )

        # Find closest timestamp
        time_diffs = (valid_df[timestamp_column] - target_ts).abs()
        closest_idx = time_diffs.idxmin()
        target_row_index = df.index.get_loc(closest_idx)

    elif frame_id is not None:
        # Frame ID-based lookup
        if scene_id is None:
            raise ValueError("scene_id is required when using frame_id lookup")

        # Filter by scene_id and frame_id (already filtered by sensor_type above)
        mask = (df["scene_id"] == scene_id) & (df["frame_id"] == frame_id)
        matching_rows = df[mask]

        if len(matching_rows) == 0:
            raise ValueError(
                f"No data found for camera '{camera_name}' in scene_id={scene_id}, frame_id={frame_id}"
            )

        # Get first matching row (all rows already have this camera due to sensor_type filter)
        target_row_index = df.index.get_loc(matching_rows.index[0])

    # Get target row info
    target_row = df.iloc[target_row_index]
    target_scene_id = target_row["scene_id"]
    is_keyframe = target_row.get("is_keyframe", True)

    # Find keyframe to start from
    # With sensor_type filtering, all rows already have this camera, so just check is_keyframe
    if is_keyframe:
        keyframe_index = target_row_index
    else:
        keyframe_index = None

    # Search backwards for keyframe if not found
    if keyframe_index is None:
        for i in range(target_row_index - 1, -1, -1):
            row = df.iloc[i]
            # Must match: same scene and is_keyframe=True
            # (all rows already have this camera due to sensor_type filter)
            if row["scene_id"] != target_scene_id:
                continue
            if row.get("is_keyframe", False):
                keyframe_index = i
                break

        if keyframe_index is None:
            raise ValueError(
                f"No keyframe found before row {target_row_index} for camera '{camera_name}' in scene {target_scene_id}. "
                f"Cannot decode P/B-frame without keyframe."
            )

    # Collect all video data from keyframe to target (pre-roll)
    # With sensor_type filtering, all rows already have this camera
    video_chunks = []
    for i in range(keyframe_index, target_row_index + 1):
        row = df.iloc[i]
        if row["scene_id"] != target_scene_id:
            break  # Stop if scene changes

        video_data = row["camera"]
        if isinstance(video_data, dict) and camera_name in video_data:
            chunk = video_data[camera_name]
            if chunk is not None and len(chunk) > 0:
                video_chunks.append(chunk)

    if not video_chunks:
        raise ValueError(f"No valid video data found from keyframe to row {target_row_index}")

    # Concatenate video chunks (H.264/H.265 AnnexB format can be concatenated)
    combined_video = b"".join(video_chunks)

    # Decode video stream
    container = av.open(io.BytesIO(combined_video))

    try:
        stream = container.streams.video[0]

        # Decode all frames and get the last one (target frame)
        target_frame = None
        for frame in container.decode(stream):
            target_frame = frame

        if target_frame is None:
            raise RuntimeError(f"Failed to decode frame at row {target_row_index}")

        # Convert to numpy array (RGB)
        img = target_frame.to_ndarray(format="rgb24")
    finally:
        container.close()

    # Return in requested format
    if format == "raw":
        return img
    elif format == "jpeg":
        try:
            import cv2

            _, encoded = cv2.imencode(".jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            return encoded.tobytes()
        except ImportError:
            from PIL import Image

            buf = io.BytesIO()
            Image.fromarray(img).save(buf, format="JPEG")
            return buf.getvalue()
    elif format == "png":
        try:
            import cv2

            _, encoded = cv2.imencode(".png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            return encoded.tobytes()
        except ImportError:
            from PIL import Image

            buf = io.BytesIO()
            Image.fromarray(img).save(buf, format="PNG")
            return buf.getvalue()
    else:
        raise ValueError(f"Unknown format: {format}. Use 'jpeg', 'png', or 'raw'.")


def get_video_info(video_data: bytes) -> dict:
    """Get metadata information from video data.

    Extract video metadata without decoding frames.

    Args:
        video_data: Compressed video data (H.265/H.264 bytes)

    Returns:
        Dictionary with video metadata:
        {
            "codec": "h265" or "h264",
            "width": int,
            "height": int,
            "num_frames": int,
            "fps": float,
            "duration_ms": float
        }

    Examples:
        camera = read_component("/data", "camera")
        df = camera.to_pandas()

        info = get_video_info(df.iloc[0]['camera']['front'])
        print(f"Video: {info['width']}x{info['height']}, {info['num_frames']} frames")
    """
    try:
        import av
    except ImportError:
        raise ImportError(
            "PyAV is required for video info extraction. Install with: pip install av"
        )

    # Open video container
    container = av.open(io.BytesIO(video_data))
    stream = container.streams.video[0]

    # Extract codec name
    codec_name = stream.codec_context.name
    if "hevc" in codec_name or "h265" in codec_name:
        codec = "h265"
    elif "h264" in codec_name or "avc" in codec_name:
        codec = "h264"
    else:
        codec = codec_name

    # Get dimensions
    width = stream.width
    height = stream.height

    # Get frame rate
    fps = float(stream.average_rate) if stream.average_rate else 0.0

    # Count frames (need to decode to get accurate count)
    num_frames = stream.frames if stream.frames > 0 else sum(1 for _ in container.decode(stream))

    # Calculate duration
    duration_ms = (num_frames / fps * 1000) if fps > 0 else 0.0

    container.close()

    return {
        "codec": codec,
        "width": width,
        "height": height,
        "num_frames": num_frames,
        "fps": fps,
        "duration_ms": duration_ms,
    }
