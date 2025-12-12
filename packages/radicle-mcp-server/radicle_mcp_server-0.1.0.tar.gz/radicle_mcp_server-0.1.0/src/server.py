"""Main FastMCP server for Radicle CLI integration."""

from __future__ import annotations

import sys
from pathlib import Path


try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: fastmcp is required. Install with: pip install fastmcp")
    sys.exit(1)

from .container import Container
from .protocols import VersionManagerProtocol, ToolGeneratorProtocol


class RadicleMCPServer:
    """Main MCP server for Radicle CLI."""

    version_manager: VersionManagerProtocol
    tool_generator: ToolGeneratorProtocol
    mcp: FastMCP

    def __init__(
        self,
        version_manager: VersionManagerProtocol,
        tool_generator: ToolGeneratorProtocol,
        mcp: FastMCP,
    ):
        """Initialize the MCP server.

        Args:
            version_manager: Version manager instance
            tool_generator: Tool generator instance
            mcp: FastMCP instance
        """
        self.version_manager = version_manager
        self.tool_generator = tool_generator
        self.mcp = mcp

    @classmethod
    def create(cls, definitions_dir: Path | None = None) -> "RadicleMCPServer":
        """Create server with default dependencies.

        Args:
            definitions_dir: Path to YAML definitions directory

        Returns:
            Configured RadicleMCPServer instance
        """
        container = Container()
        version_manager, tool_generator, mcp = container.create_mcp_server_components(
            definitions_dir
        )
        return cls(version_manager, tool_generator, mcp)

    def _register_tools(self):
        """Register all available tools with the MCP server."""
        try:
            tools = self.tool_generator.generate_all_tools()

            for tool_name, tool_function in tools.items():
                # Register the tool with FastMCP
                _ = self.mcp.tool(tool_name)(tool_function)

        except Exception as e:
            # Register fallback tools if there's an error
            print(f"Error loading dynamic tools: {e}")
            import traceback

            traceback.print_exc()
            print(f"Warning: Could not load full tool definitions: {e}")

    def run(self, host: str = "localhost", port: int = 8000, transport: str = "stdio"):
        """Run the MCP server.

        Args:
            host: Host for HTTP transport
            port: Port for HTTP transport
            transport: Transport type ('stdio' or 'http')
        """
        try:
            print("Radicle MCP Server starting...")
            print(f"Transport: {transport}")

            # Register all available tools with the MCP server
            self._register_tools()

            if transport == "http":
                print(f"Listening on http://{host}:{port}")
                self.mcp.run(host=host, port=port, transport="http")
            else:
                print("Using stdio transport")
                self.mcp.run()

        except KeyboardInterrupt:
            print("\nShutting down Radicle MCP Server...")
            raise
        except Exception as e:
            print(f"Server error: {e}")
            sys.exit(1)


def main():
    """Main entry point for the MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="Radicle MCP Server")
    _ = parser.add_argument(
        "--host",
        default="localhost",
        help="Host for HTTP transport (default: localhost)",
    )
    _ = parser.add_argument(
        "--port", type=int, default=8000, help="Port for HTTP transport (default: 8000)"
    )
    _ = parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    _ = parser.add_argument(
        "--definitions-dir", type=str, help="Path to YAML definitions directory"
    )

    args = parser.parse_args()

    definitions_dir = (
        Path(args.definitions_dir) if args.definitions_dir else None
    )  # CLI argument
    server = RadicleMCPServer.create(definitions_dir)

    server.run(
        host=args.host, port=args.port, transport=args.transport
    )  # CLI arguments


if __name__ == "__main__":
    main()
