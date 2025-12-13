"""Shared fixtures for CLI contract tests."""

import pytest
import subprocess
import re
from pathlib import Path

from src.yaml_loader import VersionManager


@pytest.fixture
def rad_cli_available():
    """Check if rad CLI is installed and accessible.

    Skips test if rad CLI is not available.

    Returns:
        str: Version string from rad --version
    """
    try:
        result = subprocess.run(
            ["rad", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            pytest.skip("rad CLI not installed or not accessible")
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pytest.skip("rad CLI not installed or not accessible")


@pytest.fixture
def rad_version(rad_cli_available):
    """Get installed rad version and verify compatibility.

    Args:
        rad_cli_available: Version string from rad --version

    Returns:
        tuple: Version tuple (major, minor, patch)
    """
    # Parse version from "rad 1.5.0 (commit_hash)"
    match = re.search(r"rad (\d+)\.(\d+)\.(\d+)", rad_cli_available)
    if not match:
        pytest.skip(f"Could not parse rad version from: {rad_cli_available}")

    version = (int(match.group(1)), int(match.group(2)), int(match.group(3)))

    # Verify we have 1.5.0 or later
    if version < (1, 5, 0):
        pytest.skip(
            f"rad version {'.'.join(map(str, version))} < 1.5.0, skipping contract tests"
        )

    return version


@pytest.fixture
def yaml_definitions():
    """Load YAML definitions for version 1.5.0.

    Returns:
        VersionManager: Loaded definitions
    """
    return VersionManager()


@pytest.fixture
def yaml_command_def(yaml_definitions):
    """Get a specific command definition from YAML.

    Returns:
        function: Helper to get command definition
    """

    def _get_command(command_name: str, subcommand_name: str = None):
        """Get command definition from YAML.

        Args:
            command_name: Main command (e.g., 'issue', 'patch')
            subcommand_name: Subcommand (e.g., 'list', 'open')

        Returns:
            Command or Subcommand object
        """
        cmd = yaml_definitions.get_command_definition(command_name)
        if subcommand_name:
            return cmd.subcommands[subcommand_name]
        return cmd

    return _get_command
