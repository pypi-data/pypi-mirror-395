from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from .client import RecursorClient

# Initialize the MCP server
mcp = FastMCP("Recursor")

# Initialize API Client (lazy load to allow env vars to be set)
_client = None

def get_client() -> RecursorClient:
    global _client
    if not _client:
        _client = RecursorClient()
    return _client

def main():
    """Run the MCP server using stdio transport"""
    mcp.run()

