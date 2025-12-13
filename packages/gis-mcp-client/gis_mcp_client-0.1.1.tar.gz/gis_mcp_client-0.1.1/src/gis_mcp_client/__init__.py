"""GIS MCP Client - Lightweight client for connecting to GIS MCP servers."""

__version__ = "0.1.1"

from .client import GISMCPClient
from .storage import RemoteStorage

__all__ = ["GISMCPClient", "RemoteStorage"]

