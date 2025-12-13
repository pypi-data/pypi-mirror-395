"""Python wrapper for the OpenDota API."""

from .client import OpenDota
from .constants import DotaConstants, dota_constants
from .fantasy import FANTASY

__version__ = "7.39.5.1.dev1"
__all__ = ["OpenDota", "DotaConstants", "dota_constants", "FANTASY"]
