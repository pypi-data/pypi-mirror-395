from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from avcloud.experimental.http_client.client import HTTPClient


class Search:
    def __init__(self, client: HTTPClient):
        """
        Initialize the Search resource.

        Args:
            client: HTTPClient instance for making synchronous requests
        """
        self._client = client

    def search_data(
        self,
        time_range: Tuple[datetime, datetime],
        country: Optional[str] = "",
        city: Optional[str] = "",
        device_type: Optional[str] = "DEVICE_TYPE_INVALID",
        device_id: Optional[str] = "",
        limit: Optional[int] = 20,
        page_token: Optional[str] = "",
    ) -> List[Dict[str, str]]:
        request = {
            "time_range": {
                "start": time_range[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end": time_range[1].strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            "country": country,
            "city": city,
            "device_type": device_type,
            "device_id": device_id,
            "limit": limit,
            "page_token": page_token,
        }

        resp = self._client.post("/avcloud/api/v1/searchdata", json=request)
        return resp.json()
