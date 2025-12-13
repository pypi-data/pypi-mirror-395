"""Protocol interfaces for dependency injection."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol, TypedDict, runtime_checkable

from .definitions.schema import Command, RadicleVersion


class CommandResult(TypedDict):
    """Result of executing a Radicle command."""

    success: bool
    returncode: int
    stdout: str
    stderr: str
    command: str
    parsed_output: dict[str, str] | list[dict[str, str]] | None  # Parsed CLI output


@runtime_checkable
class VersionManagerProtocol(Protocol):
    """Protocol for version management operations."""

    def get_installed_version(self) -> str:
        """Get installed Radicle version."""
        ...

    def get_current_definition(self) -> RadicleVersion:
        """Get definition for currently installed version."""
        ...

    def get_command_definition(
        self, command: str, version: str | None = None
    ) -> Command:
        """Get command definition for specific command."""
        ...

    def get_supported_versions(self) -> list[str]:
        """Get list of supported versions."""
        ...

    def is_version_supported(self, version: str) -> bool:
        """Check if version is supported."""
        ...

    def load_version_definition(self, version: str) -> RadicleVersion:
        """Load YAML definition for specific version."""
        ...

    def clear_cache(self) -> None:
        """Clear internal caches."""
        ...


@runtime_checkable
class CommandExecutorProtocol(Protocol):
    """Protocol for command execution operations."""


def execute_command(
    self,
    command: str,
    subcommand: str | None = None,
    args: dict[str, Any] | None = None,  # pyright: ignore[reportExplicitAny]  # External CLI interface
    cwd: Path | None = None,
    repository: str | None = None,
    timeout: int = 30,
) -> CommandResult:
    """Execute a Radicle command."""
    ...


@runtime_checkable
class ToolGeneratorProtocol(Protocol):
    """Protocol for tool generation operations."""

    def generate_all_tools(self) -> dict[str, Callable[..., str]]:
        """Generate all MCP tools."""
        ...

    def get_tool_schemas(self) -> dict[str, dict[str, Any]]:  # pyright: ignore[reportExplicitAny]
        """Generate JSON schemas for all tools."""
        ...
