"""YAML definition loader and version manager for Radicle MCP Server."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .definitions.schema import (
    Command,
    RadicleVersion,
    YAMLDefinitionError,
    validate_yaml_schema,
)
from .exceptions import (
    CommandNotFoundError,
    RadicleNotInstalledError,
    VersionNotSupportedError,
)


class VersionManager:
    """Manages Radicle version detection and YAML definition loading."""

    definitions_dir: Path
    _version_cache: str | None
    _definition_cache: dict[str, RadicleVersion]

    def __init__(self, definitions_dir: Path | None = None):
        """Initialize version manager with definitions directory and caches.

        Args:
            definitions_dir: Path to YAML definitions directory, defaults to
                package definitions/ folder if None
        """
        if definitions_dir is None:
            definitions_dir = Path(__file__).parent / "definitions"

        self.definitions_dir = Path(definitions_dir)
        self._version_cache = None
        self._definition_cache = {}

    def get_installed_version(self) -> str:
        """Get installed Radicle version via 'rad --version' with caching.

        Executes 'rad --version' subprocess and parses output using regex.
        Results cached in _version_cache to avoid repeated subprocess calls.

        Returns:
            Version string (e.g., "1.4.0")

        Raises:
            RadicleNotInstalledError: If rad CLI not found in PATH, command
                times out, or version output cannot be parsed
        """
        if self._version_cache:
            return self._version_cache

        try:
            result = subprocess.run(
                ["rad", "--version"], capture_output=True, text=True, timeout=10
            )

            if result.returncode != 0:
                raise RadicleNotInstalledError("Radicle CLI not found")

            version_match = re.search(r"rad (\d+\.\d+\.\d+)", result.stdout)
            if not version_match:
                raise RadicleNotInstalledError("Could not parse Radicle version")

            version = version_match.group(1)
            self._version_cache = version
            return version

        except FileNotFoundError:
            raise RadicleNotInstalledError("Radicle CLI not found in PATH")
        except subprocess.TimeoutExpired:
            raise RadicleNotInstalledError("Radicle CLI command timed out")

    def load_version_definition(self, version: str) -> RadicleVersion:
        """Load YAML definition for a specific version.

        Args:
            version: Version string (e.g., "1.4.0")

        Returns:
            RadicleVersion object

        Raises:
            VersionNotSupportedError: If version definition is not found
            YAMLDefinitionError: If YAML definition is invalid
        """
        if version in self._definition_cache:
            return self._definition_cache[version]

        yaml_file = self.definitions_dir / f"radicle-{version}.yaml"
        if not yaml_file.exists():
            # Try to find closest supported version
            closest_version = self._find_closest_supported_version(version)
            if closest_version:
                yaml_file = self.definitions_dir / f"radicle-{closest_version}.yaml"
            else:
                raise VersionNotSupportedError(
                    f"No definition found for version {version}"
                )

        try:
            import yaml

            with open(yaml_file, "r") as f:
                yaml_data = yaml.safe_load(f)

            definition = validate_yaml_schema(yaml_data)
            self._definition_cache[version] = definition
            return definition

        except FileNotFoundError:
            raise VersionNotSupportedError(f"Definition file not found: {yaml_file}")
        except Exception as e:
            raise YAMLDefinitionError(f"Failed to load definition: {e}")

    def get_current_definition(self) -> RadicleVersion:
        """Get definition for currently installed Radicle version.

        Returns:
            RadicleVersion object for current version

        Raises:
            RadicleNotInstalledError: If rad CLI is not installed
            VersionNotSupportedError: If current version is not supported
        """
        version = self.get_installed_version()
        print(f"[DEBUG] Loading definition for version: {version}")
        definition = self.load_version_definition(version)
        issue_cmd = definition.commands.get("issue")
        if issue_cmd:
            issue_options = list(issue_cmd.options.keys())
            print(f"[DEBUG] Loaded definition with issue options: {issue_options}")
        else:
            print(f"[DEBUG] No issue command found in definition")
        return definition
        return definition

    def get_supported_versions(self) -> list[str]:
        """Get list of supported Radicle versions.

        Returns:
            List of version strings
        """
        versions: list[str] = []
        for yaml_file in self.definitions_dir.glob("radicle-*.yaml"):
            # Extract version from filename like "radicle-1.4.0.yaml"
            version_match = re.search(r"radicle-(\d+\.\d+\.\d+)\.yaml", yaml_file.name)
            if version_match:
                versions.append(version_match.group(1))

        return sorted(versions, key=self._version_key, reverse=True)

    def is_version_supported(self, version: str) -> bool:
        """Check if a version is supported.

        Args:
            version: Version string to check

        Returns:
            True if version is supported, False otherwise
        """
        yaml_file = self.definitions_dir / f"radicle-{version}.yaml"
        return yaml_file.exists()

    def get_command_definition(
        self, command: str, version: str | None = None
    ) -> Command:
        """Get command definition for a specific command.

        Args:
            command: Command name (e.g., "issue", "patch")
            version: Optional version override

        Returns:
            Command object

        Raises:
            CommandNotFoundError: If command is not found
            VersionNotSupportedError: If version is not supported
        """
        if version is None:
            definition = self.get_current_definition()
        else:
            definition = self.load_version_definition(version)

        if command not in definition.commands:
            raise CommandNotFoundError(
                f"Command '{command}' not found in version {definition.metadata.version}"
            )

        return definition.commands[command]

    def _find_closest_supported_version(self, target_version: str) -> str | None:
        """Find closest supported version using semantic version comparison.

        Compares target version against supported versions list, finding the
        highest supported version that is <= target. Uses tuple comparison
        on (major, minor, patch) version components.

        Args:
            target_version: Version to find match for (e.g., "1.4.2")

        Returns:
            Closest supported version string, or None if target is below
            minimum supported version
        """
        supported = self.get_supported_versions()
        if not supported:
            return None

        target_parts = [int(x) for x in target_version.split(".")]

        best_match = None
        best_score = -1

        for version in supported:
            version_parts = [int(x) for x in version.split(".")]

            score = 0
            for i in range(min(3, len(target_parts), len(version_parts))):
                if target_parts[i] == version_parts[i]:
                    score += 1
                else:
                    break

            if score > best_score:
                best_score = score
                best_match = version

        return best_match

    @staticmethod
    def _version_key(version: str) -> tuple[int, ...]:
        """Convert version string to sortable tuple.

        Args:
            version: Version string like "1.4.0"

        Returns:
            Tuple like (1, 4, 0) for sorting
        """
        parts = version.split(".")
        return tuple(int(x) for x in parts)

    def clear_cache(self):
        """Clear internal caches."""
        self._version_cache = None
        self._definition_cache.clear()
