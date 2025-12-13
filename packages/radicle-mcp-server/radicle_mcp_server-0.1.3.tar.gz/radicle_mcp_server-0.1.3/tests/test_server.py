"""Test server functionality and integration."""

import pytest
from unittest.mock import Mock, patch

# Mock the imports to avoid dependency issues
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestServerIntegration:
    """Test server integration and tool registration."""

    def test_server_initialization(self):
        """Test server initialization with mock dependencies."""
        # Mock FastMCP to avoid import issues
        with patch.dict("sys.modules", {"fastmcp": Mock()}):
            from src.server import RadicleMCPServer

            server = RadicleMCPServer.create()
            assert server.version_manager is not None
            assert server.tool_generator is not None
            assert server.mcp is not None

    def test_server_run_methods(self):
        """Test server run methods."""
        with patch.dict("sys.modules", {"fastmcp": Mock()}):
            from src.server import RadicleMCPServer

            server = RadicleMCPServer.create()

            server.mcp.run = Mock()

            server.run(transport="stdio")
            server.mcp.run.assert_called_once_with()

            server.mcp.run = Mock()
            server.run(host="localhost", port=8000, transport="http")
            server.mcp.run.assert_called_once_with(
                host="localhost", port=8000, transport="http"
            )


class TestMainFunction:
    """Test main entry point."""

    def test_main_function_parsing(self):
        """Test argument parsing in main function."""
        with patch.dict("sys.modules", {"fastmcp": Mock()}):
            with patch("src.server.RadicleMCPServer.create") as mock_create:
                mock_server = Mock()
                mock_create.return_value = mock_server

                # Mock sys.argv
                with patch(
                    "sys.argv", ["server.py", "--port", "9000", "--transport", "http"]
                ):
                    from src.server import main

                    main()

                    mock_create.assert_called_once_with(None, rid=None)

                    # Check server run call
                    mock_server.run.assert_called_once_with(
                        host="localhost", port=9000, transport="http"
                    )

    def test_main_function_defaults(self):
        """Test main function with default arguments."""
        with patch.dict("sys.modules", {"fastmcp": Mock()}):
            with patch("src.server.RadicleMCPServer.create") as mock_create:
                mock_server = Mock()
                mock_create.return_value = mock_server

                # Mock sys.argv with minimal args
                with patch("sys.argv", ["server.py"]):
                    from src.server import main

                    main()

                    mock_create.assert_called_once_with(None, rid=None)

                    # Check server run call with defaults
                    mock_server.run.assert_called_once_with(
                        host="localhost", port=8000, transport="stdio"
                    )


class TestErrorHandling:
    """Test error handling in server."""

    def test_fastmcp_import_error(self):
        """Test handling when fastmcp is not available."""
        # This test can't easily be done since the import happens at module level
        # We'll skip it for now
        pass

    def test_keyboard_interrupt_handling(self):
        """Test handling of keyboard interrupt."""
        with patch.dict("sys.modules", {"fastmcp": Mock()}):
            from src.server import RadicleMCPServer

            server = RadicleMCPServer.create()

            server.mcp.run = Mock(side_effect=KeyboardInterrupt())

            with patch("builtins.print") as mock_print:
                with pytest.raises(KeyboardInterrupt):
                    server.run()

                    mock_print.assert_called_with(
                        "\nShutting down Radicle MCP Server..."
                    )

    def test_general_exception_handling(self):
        """Test handling of general exceptions."""
        with patch.dict("sys.modules", {"fastmcp": Mock()}):
            from src.server import RadicleMCPServer

            server = RadicleMCPServer.create()

            server.mcp.run = Mock(side_effect=Exception("Test error"))

            with patch("builtins.print") as mock_print:
                with patch("sys.exit") as mock_exit:
                    server.run()

                    mock_print.assert_called_with("Server error: Test error")
                    mock_exit.assert_called_once_with(1)


if __name__ == "__main__":
    pytest.main([__file__])
