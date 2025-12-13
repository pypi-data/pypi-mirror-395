"""Integration tests for MCP tool invocation."""

import pytest
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


@pytest.mark.asyncio
async def test_tool_discovery(mcp_server):
    """Verify all dynamic tools are registered."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            tools_result = await client.list_tools()
            tool_names = [t.name for t in tools_result.tools]

            # Verify essential tools exist
            assert "select_repository" in tool_names
            assert "rad_issue_open" in tool_names
            assert "rad_issue_list" in tool_names
            assert "rad_patch_open" in tool_names


@pytest.mark.asyncio
async def test_select_repository_tool(mcp_server):
    """Test select_repository tool invocation."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("select_repository", {})

            assert not result.isError
            assert len(result.content) > 0
            # Should contain repository information
            content_text = str(result.content[0].text)
            assert "Repository" in content_text or "repository" in content_text


@pytest.mark.asyncio
async def test_tool_with_arguments(mcp_server, mock_rad_subprocess):
    """Test tool invocation with arguments."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("rad_issue_list", {})

            assert not result.isError
            # Verify subprocess was called
            assert mock_rad_subprocess.called

            # Verify the final command includes 'rad' and 'issue'
            # Last call should be the actual command (first may be 'rad inspect')
            call_args = mock_rad_subprocess.call_args[0][0]
            assert "rad" in call_args
            assert "issue" in call_args
            assert "list" in call_args


@pytest.mark.asyncio
async def test_tool_with_repo_option(mcp_server, mock_rad_subprocess):
    """Test tool invocation with command-level repo option."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("rad_issue_list", {
                "repo": "rad:z2XdTQ5C8wJC6RK8WkLmMtcDANZs4"
            })

            assert not result.isError
            assert mock_rad_subprocess.called

            # Check all calls for the --repo argument (may be in any call)
            all_calls = [str(call) for call in mock_rad_subprocess.call_args_list]
            repo_found = any("--repo" in str(call) and "rad:z2XdTQ5C8wJC6RK8WkLmMtcDANZs4" in str(call)
                           for call in mock_rad_subprocess.call_args_list)
            assert repo_found, f"--repo argument not found in any call: {all_calls}"


@pytest.mark.asyncio
async def test_tool_error_handling(mcp_server, mock_rad_subprocess_with_error):
    """Test tool handles subprocess errors correctly."""
    async with streamablehttp_client(mcp_server) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            result = await client.call_tool("rad_issue_list", {})

            # The tool should return the error but wrapped in result
            # Error should be in the content
            content_text = str(result.content[0].text)
            assert "Command failed" in content_text or "Error" in content_text
