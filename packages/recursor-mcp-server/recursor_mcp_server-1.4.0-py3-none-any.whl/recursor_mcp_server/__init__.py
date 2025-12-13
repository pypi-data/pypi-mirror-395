"""
Recursor MCP Server - Model Context Protocol server for AI assistants
"""

__version__ = "1.4.0"

from .server import mcp, get_client
from .client import RecursorClient

# Import tools and resources to register them with the MCP server
from . import tools
from . import resources

__all__ = ["mcp", "get_client", "RecursorClient", "__version__"]

