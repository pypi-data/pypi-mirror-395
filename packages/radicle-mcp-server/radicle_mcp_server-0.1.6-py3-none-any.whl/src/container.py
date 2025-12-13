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
from .repository_context import RepositoryContext


class Container:
    """Simple dependency injection container."""

    def create_version_manager(
        self, definitions_dir: Path | None = None
    ) -> VersionManagerProtocol:
        """Create version manager instance."""
        return VersionManager(definitions_dir)

    def create_command_executor(
        self,
        version_manager: VersionManagerProtocol,
        repository_context: RepositoryContext,
    ) -> CommandExecutorProtocol:
        """Create command executor instance."""
        return CommandExecutor(version_manager, repository_context)

    def create_tool_generator(
        self, version_manager: VersionManagerProtocol, executor: CommandExecutorProtocol
    ) -> ToolGeneratorProtocol:
        """Create tool generator instance."""
        return ToolGenerator(version_manager, executor)

    def create_repository_context(self, rid: str | None = None) -> RepositoryContext:
        """Create repository context instance.

        Args:
            rid: Optional repository ID to set directly

        Returns:
            RepositoryContext instance
        """
        return RepositoryContext(rid=rid)

    def create_mcp_server_components(
        self, definitions_dir: Path | None = None, rid: str | None = None
    ):
        """Create components for MCP server assembly.

        Args:
            definitions_dir: Optional path to YAML definitions directory
            rid: Optional repository ID to set directly

        Returns:
            Tuple of (version_manager, tool_generator, repository_context, mcp)
        """
        version_manager = self.create_version_manager(definitions_dir)
        repository_context = self.create_repository_context(rid)
        executor = self.create_command_executor(version_manager, repository_context)
        tool_generator = self.create_tool_generator(version_manager, executor)
        mcp = FastMCP("radicle-mcp-server")

        return version_manager, tool_generator, repository_context, mcp
