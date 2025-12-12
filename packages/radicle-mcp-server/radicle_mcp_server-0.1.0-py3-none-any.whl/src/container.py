"""Dependency injection container for wiring dependencies."""

from __future__ import annotations

from pathlib import Path

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: fastmcp is required. Install with: pip install fastmcp")
    raise

from .command_executor import CommandExecutor
from .protocols import (
    VersionManagerProtocol,
    CommandExecutorProtocol,
    ToolGeneratorProtocol,
)
from .tool_generator import ToolGenerator
from .yaml_loader import VersionManager


class Container:
    """Simple dependency injection container."""

    def create_version_manager(
        self, definitions_dir: Path | None = None
    ) -> VersionManagerProtocol:
        """Create version manager instance."""
        return VersionManager(definitions_dir)

    def create_command_executor(
        self, version_manager: VersionManagerProtocol
    ) -> CommandExecutorProtocol:
        """Create command executor instance."""
        return CommandExecutor(version_manager)

    def create_tool_generator(
        self, version_manager: VersionManagerProtocol, executor: CommandExecutorProtocol
    ) -> ToolGeneratorProtocol:
        """Create tool generator instance."""
        return ToolGenerator(version_manager, executor)

    def create_mcp_server_components(self, definitions_dir: Path | None = None):
        """Create components for MCP server assembly."""
        version_manager = self.create_version_manager(definitions_dir)
        executor = self.create_command_executor(version_manager)
        tool_generator = self.create_tool_generator(version_manager, executor)
        mcp = FastMCP("radicle-mcp-server")

        return version_manager, tool_generator, mcp
