import asyncio
from datetime import datetime
from typing import Tuple

from avcloud.experimental.http_client import HTTPClient
from avcloud.experimental.oci.manager import OCIManager
from avcloud.experimental.resources.search import Search


class Downloader(HTTPClient):
    def __init__(self, client: HTTPClient, max_workers: int = 10, live_logs: bool = False):
        self._client = client

        self._search = Search(self._client)
        self._oci_manager = OCIManager(max_workers, live_logs)

    async def download_av_logs_async(
        self, item_ids: list[str], output_dir: str, bucket_size: int = 1000
    ):
        try:
            for i in range(0, len(item_ids), bucket_size):
                bucket_item_ids = item_ids[i : min(i + bucket_size, len(item_ids))]
                await self._batch_download_av_logs_async(bucket_item_ids, output_dir)
        finally:
            self._oci_manager.async_logger.stop()

    async def _batch_download_av_logs_async(self, item_ids: list[str], output_dir: str):
        request = {
            "item_ids": item_ids,
        }
        resp = self._client.post("/avcloud/api/v1/createdownloadurls", json=request)
        download_urls = resp.json().get("downloadUrls", [])

        print(f"Downloading {len(download_urls)} items ...")

        futures = []
        for item in download_urls:
            download_url_base = item.get("downloadUrlBase")
            path = item.get("path")
            futures.append(
                self._oci_manager.download_with_par_async(download_url_base, path, output_dir)
            )

        await gather_with_concurrency(self.max_workers, *futures)

    @property
    def max_workers(self) -> int:
        return self._oci_manager.max_workers

    @max_workers.setter
    def max_workers(self, value: int):
        self._oci_manager.max_workers = value


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))
