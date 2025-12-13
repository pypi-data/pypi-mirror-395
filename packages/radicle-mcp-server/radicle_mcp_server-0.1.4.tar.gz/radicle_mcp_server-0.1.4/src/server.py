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
from .repository_context import RepositoryContext


class RadicleMCPServer:
    """Main MCP server for Radicle CLI."""

    version_manager: VersionManagerProtocol
    tool_generator: ToolGeneratorProtocol
    repository_context: RepositoryContext
    mcp: FastMCP

    def __init__(
        self,
        version_manager: VersionManagerProtocol,
        tool_generator: ToolGeneratorProtocol,
        repository_context: RepositoryContext,
        mcp: FastMCP,
    ):
        """Initialize MCP server.

        Args:
            version_manager: Version manager instance
            tool_generator: Tool generator instance
            repository_context: Repository context instance
            mcp: FastMCP instance
        """
        self.version_manager = version_manager
        self.tool_generator = tool_generator
        self.repository_context = repository_context
        self.mcp = mcp

    @classmethod
    def create(
        cls, definitions_dir: Path | None = None, rid: str | None = None
    ) -> "RadicleMCPServer":
        """Create server with default dependencies.

        Args:
            definitions_dir: Path to YAML definitions directory
            rid: Optional repository ID to set directly

        Returns:
            Configured RadicleMCPServer instance
        """
        container = Container()
        version_manager, tool_generator, repository_context, mcp = (
            container.create_mcp_server_components(definitions_dir, rid)
        )
        return cls(version_manager, tool_generator, repository_context, mcp)

    def _register_tools(self):
        """Register all available tools with MCP server."""
        try:
            @self.mcp.tool()
            def select_repository(rid: str | None = None) -> str:
                """Query or change the active Radicle repository.

                Args:
                    rid: Repository ID to set (format: rad:z...). If None, returns current repository info.

                Returns:
                    Repository information or confirmation message

                Examples:
                    - select_repository() - Get current repository info
                    - select_repository("rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5") - Set repository
                """
                if rid is None:
                    info = self.repository_context.get_repository_info()
                    if info["active_rid"]:
                        return (
                            f"Active Repository:\n"
                            f"  RID: {info['active_rid']}\n"
                            f"  Path: {info['path'] or 'Not detected'}\n"
                            f"  Description: {info['description'] or 'None'}\n"
                            f"  Valid: {info['is_valid']}"
                        )
                    else:
                        return (
                            "No repository currently set.\n\n"
                            "To set a repository, call select_repository with a RID:\n"
                            "  select_repository('rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5')"
                        )
                else:
                    success, message = self.repository_context.set_repository(rid)
                    if success:
                        return f"✅ {message}"
                    else:
                        return f"❌ {message}"

            tools = self.tool_generator.generate_all_tools()

            for tool_name, tool_function in tools.items():
                _ = self.mcp.tool(tool_name)(tool_function)

        except Exception as e:
            print(f"Error loading dynamic tools: {e}")
            import traceback

            traceback.print_exc()
            print(f"Warning: Could not load full tool definitions: {e}")

    def run(self, host: str = "localhost", port: int = 8000, transport: str = "stdio"):
        """Run MCP server.

        Args:
            host: Host for HTTP transport
            port: Port for HTTP transport
            transport: Transport type ('stdio' or 'http')
        """
        try:
            repo_info = self.repository_context.get_repository_info()

            print("\n🚀 Starting Radicle MCP Server...")
            print(f"Transport: {transport}")

            if repo_info["active_rid"]:
                print(f"✅ Repository detected:")
                print(f"   RID: {repo_info['active_rid']}")
                if repo_info["path"]:
                    print(f"   Path: {repo_info['path']}")
                if repo_info["description"]:
                    print(f"   Description: {repo_info['description']}")
            else:
                print(
                    "ℹ️  No repository detected - server will start without repository context"
                )
                print("   Use select_repository tool to set a repository at runtime")

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
    """Main entry point for MCP server."""
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
    _ = parser.add_argument(
        "--rid",
        type=str,
        help="Repository ID to use (bypasses auto-detection)",
    )

    args = parser.parse_args()

    definitions_dir = Path(args.definitions_dir) if args.definitions_dir else None
    server = RadicleMCPServer.create(definitions_dir, rid=args.rid)

    server.run(host=args.host, port=args.port, transport=args.transport)


if __name__ == "__main__":
    main()
