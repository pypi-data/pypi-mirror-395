"""Generic command executor for Radicle CLI."""

from __future__ import annotations

import subprocess
import json
import re
from typing import Any, TypedDict
from pathlib import Path

from .exceptions import CommandExecutionError, InvalidArgumentError
from .protocols import VersionManagerProtocol
from .definitions.schema import Command


class CommandResult(TypedDict):
    """Result of executing a Radicle command."""

    success: bool
    returncode: int
    stdout: str
    stderr: str
    command: str
    parsed_output: dict[str, str] | list[dict[str, str]] | None  # Parsed CLI output


class CommandExecutor:
    """Executes Radicle commands with proper argument handling."""

    version_manager: VersionManagerProtocol
    repository_context: Any  # RepositoryContext instance

    # Commands that support --repo option based on CLI investigation
    _repo_supported_commands = {"issue", "patch", "cob"}

    # Commands that accept RID as positional argument
    _positional_rid_commands = {"inspect", "sync", "checkout"}

    def _validate_string_arg(self, name: str, value: Any) -> str:  # pyright: ignore[reportExplicitAny]  # External input validation
        """Validate and convert argument to string."""
        if not isinstance(value, str):
            raise InvalidArgumentError(
                f"Argument '{name}' must be a string, got {type(value)}"
            )
        return value

    def _validate_bool_arg(self, name: str, value: Any) -> bool:  # pyright: ignore[reportExplicitAny]  # External input
        """Validate and convert argument to boolean."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        raise InvalidArgumentError(
            f"Argument '{name}' must be a boolean, got {type(value)}"
        )

    def __init__(
        self, version_manager: VersionManagerProtocol, repository_context: Any = None
    ):
        """Initialize command executor with version manager for command validation."""
        self.version_manager = version_manager
        self.repository_context = repository_context

    def _detect_working_directory(self) -> Path | None:
        from pathlib import Path
        import subprocess

        search_path = Path.cwd()
        while search_path != search_path.parent:
            try:
                result = subprocess.run(
                    ["rad", "inspect", "."],
                    cwd=search_path,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    return search_path.resolve()

            except (
                subprocess.TimeoutExpired,
                subprocess.SubprocessError,
                FileNotFoundError,
            ):
                pass

            search_path = search_path.parent

        return None

    def execute_command(
        self,
        command: str,
        subcommand: str | None = None,
        args: dict[str, Any] | None = None,  # pyright: ignore[reportExplicitAny]  # External CLI interface
        cwd: Path | None = None,
        repository: str | None = None,
        timeout: int = 30,
    ) -> CommandResult:
        """Execute a Radicle command with validation.

        Args:
            command: Main command (e.g., "issue", "patch")
            subcommand: Optional subcommand (e.g., "open", "list")
            args: Command arguments and options
            cwd: Working directory for command execution
            repository: Repository ID to operate on (overrides detected repo)
            timeout: Command timeout in seconds

        Returns:
            Dictionary with command result

        Raises:
            CommandExecutionError: If command execution fails
            InvalidArgumentError: If arguments are invalid
        """
        if args is None:
            args = {}

        # Auto-detect working directory if not explicitly provided
        if cwd is None:
            cwd = self._detect_working_directory()
            if cwd is None:
                raise CommandExecutionError(
                    "Not in a Radicle repository. Please navigate to a Radicle repository "
                    "or specify a working directory."
                )

        # Determine repository to use
        target_repository = self._determine_target_repository(repository, command, args)

        try:
            cmd_def = self.version_manager.get_command_definition(command)
        except Exception as e:
            raise CommandExecutionError(f"Failed to get command definition: {e}")

        cmd_list = ["rad", command]
        if subcommand:
            cmd_list.append(subcommand)
            if subcommand not in cmd_def.subcommands:
                raise InvalidArgumentError(
                    f"Subcommand '{subcommand}' not found for command '{command}'"
                )
            # Save parent command options before switching to subcommand definition
            parent_options = cmd_def.options.copy()
            cmd_def = cmd_def.subcommands[subcommand]
            # Merge parent command options with subcommand options
            # Subcommand options override parent options if there's a conflict
            cmd_def.options = {**parent_options, **cmd_def.options}

        # Add --repo parameter for supported commands
        if target_repository and command in self._repo_supported_commands:
            args["repo"] = target_repository

        # Add RID as positional argument for commands that support it
        if target_repository and command in self._positional_rid_commands:
            # For positional RID commands, we need to handle the RID differently
            if command == "inspect":
                # rad inspect <rid> - RID is positional
                pass  # Will be added as positional arg below
            elif command == "sync":
                # rad sync <rid> - RID is positional
                pass  # Will be added as positional arg below
            elif command == "checkout":
                # rad checkout <rid> - RID is positional
                pass  # Will be added as positional arg below

        validated_args = self._validate_arguments(cmd_def, args)
        cmd_list.extend(validated_args)

        positional_args = self._get_positional_args(cmd_def, args)

        # Add RID as positional argument if needed
        if target_repository and command in self._positional_rid_commands:
            positional_args.insert(
                0, target_repository
            )  # Add RID as first positional arg

        cmd_list.extend(positional_args)

        try:
            result = subprocess.run(
                cmd_list, cwd=cwd, capture_output=True, text=True, timeout=timeout
            )

            return CommandResult(
                success=result.returncode == 0,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                command=" ".join(cmd_list),
                parsed_output=self._parse_output(result.stdout, cmd_def, args),
            )

        except subprocess.TimeoutExpired:
            raise CommandExecutionError(f"Command timed out after {timeout} seconds")
        except Exception as e:
            raise CommandExecutionError(f"Command execution failed: {e}")

    def _determine_target_repository(
        self, explicit_repository: str | None, command: str, args: dict[str, Any]
    ) -> str | None:
        """Determine which repository ID to use for command execution."""
        # If explicit repository provided, use it
        if explicit_repository:
            return explicit_repository

        # If repository context available, use detected repository
        if (
            self.repository_context
            and hasattr(self.repository_context, "rid")
            and self.repository_context.rid
        ):
            return self.repository_context.rid

        # Check if command requires repository context
        if command in ["issue", "patch", "cob"]:
            # These commands typically need a repository context
            return None

        # For commands that work without repository context
        return None

    def _validate_arguments(
        self,
        command_def: Command,
        args: dict[str, Any],  # pyright: ignore[reportExplicitAny]  # External input
    ) -> list[str]:
        """Validate and convert arguments to command line format.

        Args:
            command_def: Command definition with options
            args: Arguments from external input

        Returns:
            List of validated command line arguments
        """
        validated: list[str] = []

        for opt_name, opt_def in command_def.options.items():
            opt_value = args.get(opt_name)

            if opt_def.required and opt_value is None:
                raise InvalidArgumentError(f"Required option '--{opt_name}' is missing")

            if opt_value is None:
                continue

            if opt_def.type == "flag":
                if opt_value:  # True flag
                    validated.append(f"--{opt_name}")
            elif opt_def.type == "list":
                if isinstance(opt_value, str):
                    opt_value = [opt_value]
                for item in opt_value:
                    validated.extend(
                        [f"--{opt_name}", str(item)]
                    )  # String list extend, CLI arg conversion
            else:
                validated.extend([f"--{opt_name}", str(opt_value)])

        return validated

    def _get_positional_args(
        self,
        command_def: Command,
        args: dict[str, Any],  # pyright: ignore[reportExplicitAny]  # External input
    ) -> list[str]:
        """Extract positional arguments from args.

        Args:
            command_def: Command definition
            args: Provided arguments

        Returns:
            List of positional arguments
        """
        positional: list[str] = []

        for pos_arg in command_def.positional_args or []:
            if pos_arg.name in args:
                value = args[pos_arg.name]
                if isinstance(value, list):
                    positional.extend(str(x) for x in value)  # CLI list processing
                else:
                    positional.append(
                        str(value)
                    )  # String list append, CLI arg conversion

        return positional

    def _parse_output(
        self,
        output: str,
        command_def: Command,
        args: dict[str, Any],  # pyright: ignore[reportExplicitAny]  # External input
    ) -> dict[str, Any] | list[dict[str, str]] | None:  # pyright: ignore[reportExplicitAny]  # Parsed output
        """Parse command output into structured data based on command type.

        Attempts JSON parsing first if --json flag detected. Falls back to
        command-specific parsers for issue/patch lists, node status, sync status.

        Args:
            output: Raw command output string
            command_def: Command definition for parsing hints
            args: Command arguments to determine output format

        Returns:
            dict: For JSON output, node status, single responses
            list[dict]: For issue lists, patch lists, sync status
            None: If output empty or all parsing attempts fail
        """
        if not output.strip():
            return None

        if args.get("json") or command_def.name == "cob" and args.get("json"):
            try:
                parsed = json.loads(output)
                # Type narrowing: json.loads returns Any, but we know it's a JSON value
                return parsed
            except json.JSONDecodeError:
                pass

        if command_def.name == "issue" and not args.get("subcommand"):
            return self._parse_issue_list(output)
        elif command_def.name == "patch" and not args.get("subcommand"):
            return self._parse_patch_list(output)
        elif command_def.name == "node" and args.get("subcommand") == "status":
            return self._parse_node_status(output)
        elif command_def.name == "sync" and args.get("subcommand") == "status":
            return self._parse_sync_status(output)

        return None

    def _parse_issue_list(self, output: str) -> list[dict[str, str]]:
        """Parse 'rad issue list' output into structured issue data.

        Extracts issue information using regex on lines like "#123 Fix bug open".
        Handles empty lines and malformed entries gracefully.

        Args:
            output: Raw stdout from 'rad issue list' command
        Returns:
            List of issue dictionaries, each containing:
            - 'id': Issue number as string
            - 'title': Issue title with whitespace trimmed
            - 'status': Issue status (e.g., 'open', 'closed')
            Empty list if no issues found or parsing fails
        """
        issues: list[dict[str, str]] = []
        lines = output.strip().split("\n")

        for line in lines:
            if not line.strip():
                continue

            issue_match = re.search(r"#(\d+)\s+(.+)\s+(\w+)$", line)
            if issue_match:
                issues.append(
                    {
                        "id": issue_match.group(1),
                        "title": issue_match.group(2).strip(),
                        "status": issue_match.group(3),
                    }
                )

        return issues

    def _parse_patch_list(self, output: str) -> list[dict[str, str]]:
        """Parse patch list output.

        Args:
            output: Raw command output

        Returns:
            List of patch dictionaries
        """
        patches: list[dict[str, str]] = []
        lines = output.strip().split("\n")

        for line in lines:
            if not line.strip():
                continue

            patch_match = re.search(r"(\w+)\s+(.+?)\s+(\w+)", line)
            if patch_match:
                patches.append(
                    {
                        "id": patch_match.group(1),
                        "title": patch_match.group(2).strip(),
                        "status": patch_match.group(3),
                    }
                )

        return patches

    def _parse_node_status(self, output: str) -> dict[str, str]:
        """Parse node status output.

        Args:
            output: Raw command output

        Returns:
            Node status dictionary
        """
        status: dict[str, str] = {}
        lines = output.strip().split("\n")

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                status[key.strip().lower()] = value.strip()

        return status

    def _parse_sync_status(self, output: str) -> list[dict[str, str]]:
        """Parse sync status output.

        Args:
            output: Raw command output

        Returns:
            List of sync status dictionaries
        """
        repos: list[dict[str, str]] = []
        lines = output.strip().split("\n")

        for line in lines:
            if not line.strip():
                continue

            repo_match = re.search(r"([✓✗!•])\s+(.+?)\s+(\w+)", line)
            if repo_match:
                repos.append(
                    {
                        "status": repo_match.group(1),
                        "repository": repo_match.group(2).strip(),
                        "sync_state": repo_match.group(3),
                    }
                )

        return repos
