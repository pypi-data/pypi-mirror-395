"""Parser for rad CLI help output to extract command specifications."""

import re
import subprocess
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OptionSpec:
    """Specification for a command-line option."""

    name: str
    type: str  # 'flag', 'string', 'integer', 'list'
    required: bool = False
    takes_value: bool = False
    short_form: Optional[str] = None
    description: str = ""


@dataclass
class ParsedCommand:
    """Parsed command specification from CLI help output."""

    command: str
    subcommand: Optional[str] = None
    options: dict[str, OptionSpec] = field(default_factory=dict)
    positional_args: list[str] = field(default_factory=list)
    mutually_exclusive_groups: list[list[str]] = field(default_factory=list)


class CLIHelpParser:
    """Parser for rad CLI --help output."""

    @staticmethod
    def get_help_text(command: str, subcommand: Optional[str] = None) -> str:
        """Execute rad command --help and return output.

        Args:
            command: Main command (e.g., 'issue', 'patch')
            subcommand: Optional subcommand (e.g., 'list', 'open')

        Returns:
            Help text output

        Raises:
            subprocess.SubprocessError: If command fails
        """
        cmd_parts = ["rad", command]
        if subcommand:
            cmd_parts.append(subcommand)
        cmd_parts.append("--help")

        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            raise subprocess.SubprocessError(
                f"Command failed: {' '.join(cmd_parts)}\nstderr: {result.stderr}"
            )

        return result.stdout + result.stderr  # Some help goes to stderr

    @classmethod
    def parse_command_help(
        cls, command: str, subcommand: Optional[str] = None
    ) -> ParsedCommand:
        """Parse rad command help output into structured data.

        Args:
            command: Main command (e.g., 'issue', 'patch')
            subcommand: Optional subcommand (e.g., 'list', 'open')

        Returns:
            ParsedCommand object with extracted specifications
        """
        help_text = cls.get_help_text(command, subcommand)

        parsed = ParsedCommand(command=command, subcommand=subcommand)
        parsed.options = cls.extract_options(help_text)
        parsed.positional_args = cls.extract_positional_args(help_text)
        parsed.mutually_exclusive_groups = cls.extract_mutually_exclusive_groups(
            help_text
        )

        return parsed

    @staticmethod
    def extract_options(help_text: str) -> dict[str, OptionSpec]:
        """Extract option definitions from help text.

        Parses patterns like:
        - `--flag` → boolean flag
        - `--option <value>` → string parameter
        - `-a, --add <did>` → option with short form
        - Options from Usage line: `rad issue list [--all | --closed | --open | --solved]`

        Args:
            help_text: Raw help output

        Returns:
            Dictionary mapping option names to OptionSpec objects
        """
        options: dict[str, OptionSpec] = {}

        # First, extract options from the detailed Options section
        # Pattern to match option definitions
        # Matches: --option-name, --option <value>, -s, --short <val>
        option_pattern = re.compile(
            r"^\s*(?:-([a-z]), )?--([a-z][-a-z]*)"  # -s, --long-name
            r"(?:\s+<([^>]+)>)?"  # Optional <value>
            r"\s+(.+)?$",  # Description
            re.MULTILINE,
        )

        for match in option_pattern.finditer(help_text):
            short_form = match.group(1)  # May be None
            long_name = match.group(2)
            value_placeholder = match.group(3)  # May be None
            description = match.group(4) or ""

            # Determine option type
            takes_value = value_placeholder is not None
            if takes_value:
                opt_type = "string"  # Default for options with values
            else:
                opt_type = "flag"

            options[long_name] = OptionSpec(
                name=long_name,
                type=opt_type,
                takes_value=takes_value,
                short_form=short_form,
                description=description.strip(),
            )

        # Then, extract additional options from Usage line that might not be in detailed section
        usage_match = re.search(
            r"Usage\s*\n(.+?)(?:\n\n|\n[A-Z])", help_text, re.DOTALL
        )
        if usage_match:
            usage_text = usage_match.group(1)

            # Find the specific subcommand line we're interested in
            # Look for patterns like: rad issue list [--assigned <did>] [--all | --closed | --open | --solved]
            subcommand_pattern = re.compile(
                r"rad\s+\w+\s+(\w+)(.+?)(?:\n|$)", re.MULTILINE
            )

            for match in subcommand_pattern.finditer(usage_text):
                subcommand = match.group(1)
                subcommand_line = match.group(2)

                # Extract options from this subcommand's usage line
                # Pattern matches: --option, --option <value>
                usage_option_pattern = re.compile(r"--([a-z][-a-z]*)(?:\s+<([^>]+)>)?")

                for opt_match in usage_option_pattern.finditer(subcommand_line):
                    option_name = opt_match.group(1)
                    value_placeholder = opt_match.group(2)

                    # Skip if we already have this option from detailed section
                    if option_name not in options:
                        takes_value = value_placeholder is not None
                        if takes_value:
                            opt_type = "string"
                        else:
                            opt_type = "flag"

                        options[option_name] = OptionSpec(
                            name=option_name,
                            type=opt_type,
                            takes_value=takes_value,
                            short_form=None,
                            description=f"Option from usage line for {subcommand}",
                        )

        return options

    @staticmethod
    def extract_mutually_exclusive_groups(help_text: str) -> list[list[str]]:
        """Extract mutually exclusive option groups from help text.

        Parses patterns like:
        - `[--all | --closed | --open | --solved]`
        - `[--closed | --open | --solved]`

        Args:
            help_text: Raw help output

        Returns:
            List of groups, where each group is a list of option names
        """
        groups: list[list[str]] = []

        # Pattern to match [--opt1 | --opt2 | --opt3]
        mutex_pattern = re.compile(r"\[--([a-z][-a-z]*)(?:\s*\|\s*--([a-z][-a-z]*))+\]")

        for match in mutex_pattern.finditer(help_text):
            # Extract all options from the match
            # match.group(0) is the full match like "[--all | --closed | --open]"
            full_match = match.group(0)
            # Extract individual option names
            options = re.findall(r"--([a-z][-a-z]*)", full_match)
            if options:
                groups.append(options)

        return groups

    @staticmethod
    def extract_positional_args(help_text: str) -> list[str]:
        """Extract positional argument names from help text.

        Parses patterns like:
        - `<issue-id>`
        - `<patch-id>`
        - `<did>`

        Args:
            help_text: Raw help output

        Returns:
            List of positional argument names
        """
        positional: list[str] = []

        # Look in Usage section for <arg> patterns
        usage_match = re.search(
            r"Usage\s*\n(.+?)(?:\n\n|\n[A-Z])", help_text, re.DOTALL
        )
        if not usage_match:
            return positional

        usage_text = usage_match.group(1)

        # Extract <arg-name> patterns
        arg_pattern = re.compile(r"<([^>]+)>")
        for match in arg_pattern.finditer(usage_text):
            arg_name = match.group(1)
            # Filter out option value placeholders (they appear after --)
            # We only want standalone positional args
            if arg_name not in positional:
                positional.append(arg_name)

        return positional
