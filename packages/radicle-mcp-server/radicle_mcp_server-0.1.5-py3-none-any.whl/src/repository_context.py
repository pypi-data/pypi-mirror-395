"""Repository context management for Radicle MCP server."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from .exceptions import CommandExecutionError


class RepositoryContext:
    """Manages repository detection and RID storage for MCP server session."""

    rid: Optional[str]
    path: Optional[Path]
    description: Optional[str]
    confirmed_rid: Optional[str]

    def __init__(self, rid: Optional[str] = None) -> None:
        """Initialize repository context by detecting current repository.

        Args:
            rid: Optional RID to set directly (bypasses auto-detection)
        """
        self.rid = None
        self.path = None
        self.description = None
        self.confirmed_rid = None

        if rid:
            if self._validate_rid_format(rid):
                self.rid = rid
                self.confirmed_rid = rid
                self.path = Path.cwd().resolve()
                self.description = "Repository set via RID parameter"
            else:
                print(f"Warning: Invalid RID format: {rid}")
        else:
            self._detect_repository()

    def _detect_repository(self) -> None:
        """Detect current Radicle repository and extract RID and description.

        Does NOT raise exceptions - sets None values if detection fails.
        """
        try:
            result = subprocess.run(
                ["rad", "inspect", "."],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                return

            rid_result = subprocess.run(
                ["rad", "inspect", "--rid"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if rid_result.returncode == 0:
                self.rid = rid_result.stdout.strip()
                self.path = Path.cwd().resolve()

                desc_result = subprocess.run(
                    ["rad", "inspect"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if desc_result.returncode == 0:
                    self.description = self._extract_description(desc_result.stdout)
                else:
                    self.description = "No description available"

        except subprocess.TimeoutExpired:
            print("Warning: Repository detection timed out")
        except FileNotFoundError:
            print("Warning: Radicle CLI not found in PATH")
        except Exception as e:
            print(f"Warning: Failed to detect repository: {str(e)}")

    def _extract_description(self, inspect_output: str) -> str:
        """Extract repository description from rad inspect output."""
        for line in inspect_output.strip().split("\n"):
            if line.strip() and not line.startswith(" ") and ":" not in line:
                # First non-indented line without colon is likely the description
                return line.strip()
        return "No description available"

    def is_valid(self) -> bool:
        """Check if repository context is valid."""
        return (
            self.confirmed_rid is not None or self.rid is not None
        ) and self.path is not None

    def get_error_message(self) -> str:
        """Get formatted informational message for repository context."""
        if self.rid is None:
            return (
                "ℹ️  No Radicle repository detected in current directory\n\n"
                "You can:\n"
                "1. Use the select_repository tool to set a repository RID\n"
                "2. Navigate to a Radicle repository and restart the server\n"
                "3. Use --rid parameter when starting the server"
            )
        return "ℹ️  Repository context available"

    def set_repository(self, rid: str) -> tuple[bool, str]:
        """Set or change the active repository at runtime.

        Args:
            rid: Repository ID to set

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self._validate_rid_format(rid):
            return (
                False,
                f"Invalid RID format: {rid}. Expected format: rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5",
            )

        try:
            result = subprocess.run(
                ["rad", "inspect", rid],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                return (
                    False,
                    f"Repository {rid} not found or not accessible: {result.stderr}",
                )

            description = self._extract_description(result.stdout)

            self.rid = rid
            self.confirmed_rid = rid
            self.description = description

            return (True, f"Repository set to {rid}: {description}")

        except subprocess.TimeoutExpired:
            self.rid = rid
            self.confirmed_rid = rid
            self.description = "Repository set (validation timed out)"
            return (True, f"Repository set to {rid} (validation timed out)")
        except Exception as e:
            return (False, f"Failed to validate repository: {str(e)}")

    def get_repository_info(self) -> dict[str, Any]:
        """Get current repository context information.

        Returns:
            Dictionary with repository details
        """
        return {
            "detected_rid": self.rid,
            "confirmed_rid": self.confirmed_rid,
            "active_rid": self.confirmed_rid or self.rid,
            "path": str(self.path) if self.path else None,
            "description": self.description,
            "is_valid": self.is_valid(),
        }

    def _validate_rid_format(self, rid: str) -> bool:
        """Validate RID format."""
        if not rid.startswith("rad:"):
            return False
        # Basic validation - should be more thorough if needed
        parts = rid.split(":")
        return len(parts) == 2 and len(parts[1]) > 10

    def __str__(self) -> str:
        """String representation of repository context."""
        if self.is_valid():
            return f"Repository: {self.confirmed_rid or self.rid} at {self.path}"
        return "No repository context"
