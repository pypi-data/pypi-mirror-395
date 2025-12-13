"""Shared fixtures for integration tests."""

import pytest
import pytest_asyncio
from unittest.mock import Mock, patch
from fastmcp.utilities.tests import run_server_async
from mcp.client.streamable_http import StreamableHTTPTransport

from src.server import RadicleMCPServer


@pytest_asyncio.fixture
async def mcp_server():
    """Create and start MCP server for testing.

    Yields:
        str: Server URL for HTTP transport
    """
    server = RadicleMCPServer.create()
    # Register tools before starting server
    server._register_tools()

    async with run_server_async(server.mcp) as url:
        yield url


@pytest.fixture
def mock_rad_subprocess():
    """Mock subprocess.run for Radicle CLI commands.

    Yields:
        Mock: Mocked subprocess.run callable
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"id": "abc123", "title": "Test Issue"}',
            stderr=""
        )
        yield mock_run


@pytest.fixture
def mock_rad_subprocess_with_error():
    """Mock subprocess.run that returns an error.

    Yields:
        Mock: Mocked subprocess.run callable that fails
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: Command failed"
        )
        yield mock_run
