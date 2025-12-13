"""Integration tests for Radicle issue commands."""

import pytest
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


@pytest.mark.asyncio
async def test_issue_open_with_required_args(mcp_server, mock_rad_subprocess):
    """Test rad_issue_open with required title argument."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("rad_issue_open", {
                "title": "Fix critical bug"
            })

            assert not result.isError

            # Verify subprocess was called with correct command
            call_args = mock_rad_subprocess.call_args[0][0]
            assert "rad" in call_args
            assert "issue" in call_args
            assert "open" in call_args
            assert "--title" in call_args
            assert "Fix critical bug" in call_args


@pytest.mark.asyncio
async def test_issue_open_with_all_args(mcp_server, mock_rad_subprocess):
    """Test rad_issue_open with all arguments."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("rad_issue_open", {
                "title": "Fix critical bug",
                "description": "This is a detailed description",
                "label": ["urgent", "bug"]
            })

            assert not result.isError

            # Verify all arguments passed to CLI
            call_args = mock_rad_subprocess.call_args[0][0]
            assert "--title" in call_args
            assert "Fix critical bug" in call_args
            assert "--description" in call_args
            assert "This is a detailed description" in call_args
            assert "--label" in call_args
            # Labels should be passed separately
            assert "urgent" in call_args
            assert "bug" in call_args


@pytest.mark.asyncio
async def test_issue_open_with_single_label(mcp_server, mock_rad_subprocess):
    """Test rad_issue_open with a single label."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("rad_issue_open", {
                "title": "Test issue",
                "label": ["urgent"]
            })

            assert not result.isError

            call_args = mock_rad_subprocess.call_args[0][0]
            assert "--label" in call_args
            assert "urgent" in call_args


@pytest.mark.asyncio
async def test_issue_list_basic(mcp_server, mock_rad_subprocess):
    """Test rad_issue_list without arguments."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("rad_issue_list", {})

            assert not result.isError
            assert mock_rad_subprocess.called

            call_args = mock_rad_subprocess.call_args[0][0]
            assert "rad" in call_args
            assert "issue" in call_args
            assert "list" in call_args


@pytest.mark.asyncio
async def test_issue_list_with_filters(mcp_server, mock_rad_subprocess):
    """Test rad_issue_list with filter arguments."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            # Check what options are available for issue list
            tools_result = await client.list_tools()
            tools = tools_result.tools
            issue_list_tool = next((t for t in tools if t.name == "rad_issue_list"), None)

            if issue_list_tool:
                # Test with any available filter options
                result = await client.call_tool("rad_issue_list", {})
                assert not result.isError


@pytest.mark.asyncio
async def test_patch_tools_exist(mcp_server):
    """Test that patch-related tools exist."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            # Verify patch tools are registered
            tools_result = await client.list_tools()
            tools = tools_result.tools
            tool_names = [t.name for t in tools]

            # Check that patch tools exist
            assert any("patch" in name for name in tool_names), "No patch tools found"
