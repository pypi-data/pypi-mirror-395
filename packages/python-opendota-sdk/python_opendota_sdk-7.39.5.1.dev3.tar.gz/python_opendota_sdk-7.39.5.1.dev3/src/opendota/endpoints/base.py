"""Base endpoint class for OpenDota API endpoints."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import OpenDota


class BaseEndpoint:
    """Base class for API endpoints."""

    def __init__(self, client: "OpenDota"):
        self.client = client
