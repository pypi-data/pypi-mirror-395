import os
from functools import cache, cached_property

from avcloud.experimental.http_client.client import HTTPClient
from avcloud.experimental.resources.downloader import Downloader
from avcloud.experimental.resources.downloader_v2 import DownloaderV2
from avcloud.experimental.resources.search import Search
from avcloud.experimental.resources.search_v2 import SearchV2
from avcloud.experimental.utils import s3_keys_utils


class AvCloudClient(HTTPClient):
    def __init__(self, *, access_token: str | None = None) -> None:
        if access_token is None:
            access_token = os.environ.get("AVCLOUD_ACCESS_TOKEN")
        if access_token is None or access_token == "":
            raise Exception(
                "The access_token option must be set either by passing access_token to the client or by setting the AVCLOUD_ACCESS_TOKEN environment variable"
            )

        super().__init__(
            base_url="https://api.uber.com",
            timeout=30.0,
            headers={"Authorization": f"Bearer {access_token}"},
            follow_redirects=True,
        )

    @cached_property
    def search(self) -> Search:
        return Search(self)

    @cache
    def downloader(self, max_workers: int | None = None, live_logs: bool = False) -> Downloader:
        if max_workers is None:
            max_workers = os.cpu_count() - 1

        return Downloader(self, max_workers, live_logs)

    @cached_property
    def search_v2(self) -> SearchV2:
        return SearchV2(self)

    @cache
    def downloader_v2(
        self, max_workers: int | None = None, live_logs: bool = False
    ) -> DownloaderV2:
        if max_workers is None:
            max_workers = os.cpu_count() - 1

        return DownloaderV2(self, max_workers, live_logs)
