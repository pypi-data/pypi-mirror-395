"""
AVCloud SDK

A Python SDK for interfacing with AVCloud services.
"""

# Version - must be defined before importing client to avoid circular import
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("avcloud")
except PackageNotFoundError:
    from pathlib import Path

    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:
        import tomli as tomllib  # Python 3.10
    with open(Path(__file__).parent.parent.parent / "pyproject.toml", "rb") as f:
        __version__ = tomllib.load(f)["project"]["version"]

# Import main components
from .experimental.client import AvCloudClient

__all__ = [
    "__version__",
    "AvCloudClient",
]
