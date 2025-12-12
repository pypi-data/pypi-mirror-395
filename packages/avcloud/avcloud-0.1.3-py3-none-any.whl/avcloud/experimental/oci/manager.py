import asyncio
import logging
import os
from typing import List

import httpx

from avcloud.experimental.oci._logger import AsyncMultiProcessLogger

logger = logging.getLogger(__name__)


class OCIManager:
    """A class to handle downloading data from OCI using rclone."""

    def __init__(self, max_workers: int = 10, live_logs: bool = False):
        """
        Initialize the DataDownloader.

        Args:
            max_workers: Maximum number of concurrent download threads
        """
        self.max_workers = max_workers
        self.async_logger = AsyncMultiProcessLogger(live_logs=live_logs)
        self._download_semaphore = asyncio.Semaphore(max_workers)

    async def _list_objects(self, par: str, prefix: str) -> List[str]:
        """
        List all objects with the given prefix using async HTTP client.

        Args:
            par: OCI Pre-authenticated request string https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingpreauthenticatedrequests_topic-Working_with_PreAuthenticated_Requests.htm
            prefix: Object prefix to filter by

        Returns:
            List of object paths
        """
        # Use new HTTP client for each listing operation
        url = f"{par}?prefix={prefix}"

        async with httpx.AsyncClient(
            verify=False,  # Disable SSL verification for OCI PARs
        ) as client:
            response = await client.get(url)
            if response.status_code != 200:
                error_text = response.text
                raise Exception(
                    f"Failed to list objects: HTTP {response.status_code} - {error_text}"
                )

            data = response.json()
            objects = data.get("objects", [])
            return [obj["name"] for obj in objects if obj and obj.get("name")]

    async def _download_object(self, par: str, object_path: str, output_dir: str) -> str:
        """
        Download a single object using rclone.

        Args:
            par: OCI Pre-authenticated request string https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingpreauthenticatedrequests_topic-Working_with_PreAuthenticated_Requests.htm
            object_path: Full path of the object to download
            output_dir: Directory to save the downloaded file

        Returns:
            Path of the downloaded file
        """

        try:
            # Construct the full source and destination paths
            source = f"{par}{object_path}"
            dest = os.path.join(output_dir, object_path)

            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest), exist_ok=True)

            # Build rclone command with multi-threaded streams
            cmd = [
                "rclone",
                "copyurl",
                source,
                dest,
                "--progress",
            ]

            # Execute the command
            async with self._download_semaphore:
                # Register this process with the logger
                process_id = self.async_logger.register_process(f"Download-{object_path}")
                proc = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )

                self.async_logger.add_log(process_id, f"Starting download: {object_path}")

                # Monitor stdout and stderr in real-time with improved buffering
                async def read_stream(stream, prefix, process_id):
                    buffer = ""
                    while True:
                        chunk = await stream.read(1024)  # Read in chunks
                        if not chunk:
                            break
                        buffer += chunk.decode("utf-8", errors="ignore")

                        # Process complete lines
                        while "\n" in buffer:
                            line, buffer = buffer.split("\n", 1)
                            line = line.strip()
                            if line:
                                self.async_logger.add_log(process_id, f"{prefix}: {line}")

                # Start reading both stdout and stderr concurrently
                stdout_task = asyncio.create_task(read_stream(proc.stdout, "STDOUT", process_id))
                stderr_task = asyncio.create_task(read_stream(proc.stderr, "STDERR", process_id))

                # Wait for both streams to finish
                await asyncio.gather(stdout_task, stderr_task)

                # Wait for process to complete
                return_code = await proc.wait()

                if return_code != 0:
                    self.async_logger.add_log(
                        process_id, f"FAILED: Process exited with code {return_code}"
                    )
                    logger.error(f"Failed to download {object_path}: {return_code}")
                    self.async_logger.deregister_process(process_id, "failed")
                    raise Exception(f"Failed to download {object_path}: {return_code}")
                else:
                    self.async_logger.add_log(process_id, f"SUCCESS: Downloaded {object_path}")
                    logger.info(f"Downloaded: {object_path}")
                    self.async_logger.deregister_process(process_id, "completed")

                return dest

        except Exception as e:
            self.async_logger.add_log(process_id, f"ERROR: {e}")
            logger.error(f"Failed to download {object_path}: {e}")
            self.async_logger.deregister_process(process_id, "failed")
            raise

    async def download_with_par_async(self, par: str, prefix: str, output_dir: str) -> List[str]:
        """
        Download all objects with the given pre-authenticated request using ThreadPoolExecutor in a non-blocking async way.

        Args:
            par: OCI Pre-authenticated request string
            prefix: Object prefix to filter by
            output_dir: Directory to save downloaded files

        Returns:
            List of paths to downloaded files
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # List all objects to download
        objects = await self._list_objects(par, prefix)
        if not objects:
            logger.warning(f"No objects found with prefix: {prefix}")
            return []

        logger.info(f"Found {len(objects)} objects to download")

        downloaded_files = []
        successfully_downloads = 0
        failed_downloads = 0

        results = await asyncio.gather(
            *[self._download_object(par, obj, output_dir) for obj in objects],
            return_exceptions=True,
        )

        for obj, result in zip(objects, results):
            if isinstance(result, Exception):
                logger.error(f"Failed to download {obj}: {result}")
                failed_downloads += 1
            else:
                downloaded_files.append(result)
                successfully_downloads += 1

        logger.info(
            f"Successfully downloaded {successfully_downloads} files, failed to download {failed_downloads} files"
        )
        print(
            f"✅ Successfully downloaded {successfully_downloads} files \n❌ failed to download {failed_downloads} files"
        )

        return downloaded_files
