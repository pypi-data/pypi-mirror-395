from importlib import metadata

from .oc_client import (
    GraphQLError,
    HTTPRequestError,
    OpenCollectiveClient,
    PROD_URL,
    STAGING_URL,
    TransportError,
)
from .operations import UpsertResult, load_items, upsert_collective, upsert_host, upsert_project

try:
    __version__ = metadata.version("oc-opsdevnz")
except metadata.PackageNotFoundError:  # Local/editable installs without metadata
    __version__ = "0.0.0+local"

__all__ = [
    "GraphQLError",
    "HTTPRequestError",
    "OpenCollectiveClient",
    "PROD_URL",
    "STAGING_URL",
    "TransportError",
    "UpsertResult",
    "load_items",
    "__version__",
    "upsert_collective",
    "upsert_host",
    "upsert_project",
]
