"""Test doubles for dependency injection testing."""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock

from src.protocols import VersionManagerProtocol, CommandExecutorProtocol
from src.command_executor import CommandResult
from src.definitions.schema import Command, RadicleVersion


class MockVersionManager:
    """Test double for VersionManager."""

    def __init__(self, command_definitions: dict[str, Command] | None = None):
        self.command_definitions = command_definitions or {}
        self._installed_version = "1.5.0"

    def get_installed_version(self) -> str:
        return self._installed_version

    def get_current_definition(self) -> RadicleVersion:
        from src.definitions.schema import RadicleVersionMetadata

        return RadicleVersion(
            metadata=RadicleVersionMetadata(
                version=self._installed_version,
                release_date="2024-01-01",
                description="Test version",
            ),
            commands=self.command_definitions,
        )

    def get_command_definition(
        self, command: str, version: str | None = None
    ) -> Command:
        if command not in self.command_definitions:
            from src.exceptions import CommandNotFoundError

            raise CommandNotFoundError(f"Command '{command}' not found")
        return self.command_definitions[command]

    def get_supported_versions(self) -> list[str]:
        return [self._installed_version]

    def is_version_supported(self, version: str) -> bool:
        return version == self._installed_version

    def load_version_definition(self, version: str) -> RadicleVersion:
        return self.get_current_definition()

    def clear_cache(self) -> None:
        pass


class MockCommandExecutor:
    """Test double for CommandExecutor."""

    def __init__(self, results: dict[str, CommandResult] | None = None):
        self.results = results or {}
        self.executed_commands = []

    def execute_command(
        self,
        command: str,
        subcommand: str | None = None,
        args: dict[str, Any] | None = None,
        cwd: str | None = None,
        timeout: int = 30,
    ) -> CommandResult:
        command_key = f"{command}_{subcommand or 'main'}"
        self.executed_commands.append((command, subcommand, args))

        if command_key in self.results:
            return self.results[command_key]

        # Default success result
        return CommandResult(
            success=True,
            returncode=0,
            stdout=f"Mock output for {command}",
            stderr="",
            command=f"rad {command}",
            parsed_output=None,
        )
