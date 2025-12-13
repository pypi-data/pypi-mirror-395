import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple

import lance
import pyarrow as pa

from avcloud.experimental.http_client import HTTPClient
from avcloud.experimental.utils import s3_keys_utils


def _component_to_folder_name(component: str) -> str:
    """Convert component name to folder name following the pattern: 'camera' -> 'Camera.lance'."""
    # Handle special cases with underscores
    if "_" in component:
        # Convert snake_case to PascalCase: vehicle_state -> VehicleState
        words = component.split("_")
        folder_name = "".join(word.capitalize() for word in words)
    else:
        # Simple capitalize: camera -> Camera
        folder_name = component.capitalize()
    return f"{folder_name}.lance"


class LanceClient:
    def __init__(self, client: HTTPClient):
        self._client = client
        self._remote_root_us = None
        self._remote_root_eu = None
        self._storage_options_us = None
        self._storage_options_eu = None
        self._config_cache: Optional[Dict[str, Any]] = None
        # Region names - will be populated from config
        self._us_region: Optional[str] = None
        self._eu_region: Optional[str] = None
        self._cache: Dict[str, Dict[str, Any]] = {}
        # Only setup S3 keys if not already set (to avoid redundant API calls)
        if not (os.environ.get("OCI_ACCESS_KEY") and os.environ.get("OCI_SECRET_KEY")):
            try:
                self._setup_s3_compatible_keys()
            except Exception as e:
                raise Exception(f"Failed to setup S3 compatible keys: {e}. Please contact support.")

    def _setup_s3_compatible_keys(self) -> None:
        private_key, public_key = s3_keys_utils.generate_key_pair()
        request_body = {"public_key": public_key}

        try:
            response = self._client.post("/avcloud/api/v2/gets3compatiblekeys", json=request_body)

            encrypted_access_key = response.json()["encryptedAccessKey"]
            encrypted_secret_key = response.json()["encryptedSecretKey"]
        except Exception as e:
            raise Exception(f"Failed to get S3 compatible keys from API: {e}")

        try:
            access_key = s3_keys_utils.decrypt_with_private_key(encrypted_access_key, private_key)
            secret_key = s3_keys_utils.decrypt_with_private_key(encrypted_secret_key, private_key)
        except Exception as e:
            raise Exception(f"Failed to decrypt S3 compatible keys: {e}")

        os.environ["OCI_ACCESS_KEY"] = access_key
        os.environ["OCI_SECRET_KEY"] = secret_key

    def _fetch_datalake_config(self) -> Dict[str, Any]:
        """Fetch data lake configuration from the API."""
        if self._config_cache is not None:
            return self._config_cache

        try:
            response = self._client.get("/avcloud/api/v2/getdatalakeconfig")
            config = response.json()
            self._config_cache = config

            # Cache region names for quick access
            self._us_region = config.get("usRegion")
            self._eu_region = config.get("euRegion")

            # Initialize cache dict with actual region names
            if self._us_region:
                self._cache[self._us_region] = {}
            if self._eu_region:
                self._cache[self._eu_region] = {}

            return config
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data lake config: {e}")

    def get_components(self) -> List[str]:
        """Get the list of available components from config.

        Components are stored in extra_config["components"] as a comma-separated string.
        Falls back to a default list if not specified in config.
        """
        config = self._fetch_datalake_config()
        extra_config = config.get("extraConfig", {})
        components_str = extra_config.get("components", "")

        if components_str:
            # Parse comma-separated string and strip whitespace
            components = [c.strip() for c in components_str.split(",") if c.strip()]
            return components

        # Fallback to default components if not specified
        return [
            "camera",
            "imu",
            "lidar",
            "gnss",
            "vehicle_state",
            "transform",
            "wheel_odometry",
            "radar",
            "misc_data",
            "summary",
        ]

    def _is_us_region(self, region: str) -> bool:
        """Check if the given region is the US region."""
        # Ensure config is fetched so we have region names
        if self._us_region is None:
            self._fetch_datalake_config()
        return region == self._us_region

    def _ensure_config(self, region: str) -> None:
        """Ensure connection config has been set before use."""
        is_us = self._is_us_region(region)
        storage_options = self._storage_options_us if is_us else self._storage_options_eu
        if not storage_options:
            # Auto-fetch config if not already set
            if is_us:
                self._set_connection_us()
            else:
                self._set_connection_eu()

    def _set_connection_us(self) -> None:
        """Configure storage options using API config and environment credentials."""
        config = self._fetch_datalake_config()

        # Use bucket URL from API response (e.g., "s3://prod-pearl-test/lance_example_oct")
        self._remote_root_us = config["usBucketUrl"]

        self._storage_options_us = {
            "endpoint_url": config["usEndpointUrl"],
            "aws_access_key_id": os.environ.get("OCI_ACCESS_KEY"),
            "aws_secret_access_key": os.environ.get("OCI_SECRET_KEY"),
            "region": config["usRegion"],
            "aws_s3_addressing_style": "path",
        }

    def _set_connection_eu(self) -> None:
        """Configure storage options using API config and environment credentials."""
        config = self._fetch_datalake_config()

        # Use bucket URL from API response (e.g., "s3://prod-pearl-test/lance_example_oct")
        self._remote_root_eu = config["euBucketUrl"]

        self._storage_options_eu = {
            "endpoint_url": config["euEndpointUrl"],
            "aws_access_key_id": os.environ.get("OCI_ACCESS_KEY"),
            "aws_secret_access_key": os.environ.get("OCI_SECRET_KEY"),
            "region": config["euRegion"],
            "aws_s3_addressing_style": "path",
        }

    def remote_uri_for_component(self, component: str, region: str) -> str:
        self._ensure_config(region)
        folder_name = _component_to_folder_name(component)
        is_us = self._is_us_region(region)
        remote_root = self._remote_root_us if is_us else self._remote_root_eu
        return f"{remote_root}/{folder_name}"

    def open_component(self, component: str, region: str):
        if region in self._cache and component in self._cache[region]:
            return self._cache[region][component]
        self._ensure_config(region)
        is_us = self._is_us_region(region)
        storage_options = self._storage_options_us if is_us else self._storage_options_eu
        ds = lance.dataset(
            self.remote_uri_for_component(component, region), storage_options=storage_options
        )
        # Ensure region key exists in cache
        if region not in self._cache:
            self._cache[region] = {}
        self._cache[region][component] = ds
        return ds

    def ensure_components_available(self, components: List[str], region: str) -> None:
        """Ensure all components can be accessed (connection must be set first)."""
        for c in components:
            _ = self.open_component(c, region)

    def reset_cache(self) -> None:
        """Reset dataset cache and storage options to force re-reading credentials from environment."""
        self._cache = {}
        # Clear storage options so they get re-initialized with fresh credentials
        self._storage_options_us = None
        self._storage_options_eu = None

    def get_us_region(self) -> str:
        """Get the US region name from config."""
        if self._us_region is None:
            self._fetch_datalake_config()
        return self._us_region

    def get_eu_region(self) -> str:
        """Get the EU region name from config."""
        if self._eu_region is None:
            self._fetch_datalake_config()
        return self._eu_region
