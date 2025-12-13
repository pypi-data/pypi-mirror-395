"""Contract tests for issue command - validates YAML against actual rad CLI."""

import pytest

from .cli_parser import CLIHelpParser


@pytest.mark.cli_contract
@pytest.mark.requires_rad
class TestIssueListContract:
    """Test issue list command contract."""

    def test_issue_list_options_exist(self, rad_version, yaml_command_def):
        """Verify all YAML-defined options exist in CLI."""
        # Get YAML definition
        yaml_spec = yaml_command_def("issue", "list")

        # Get actual CLI specification
        cli_spec = CLIHelpParser.parse_command_help("issue", "list")

        # Check that all YAML options exist in CLI
        yaml_options = set(yaml_spec.options.keys())
        cli_options = set(cli_spec.options.keys())

        missing_in_cli = yaml_options - cli_options
        assert not missing_in_cli, (
            f"YAML defines options not found in CLI help: {missing_in_cli}\n"
            f"YAML options: {sorted(yaml_options)}\n"
            f"CLI options: {sorted(cli_options)}"
        )

    def test_issue_list_uses_flag_types(self, rad_version, yaml_command_def):
        """Verify status filtering uses flags, not string parameters."""
        # Get YAML definition
        yaml_spec = yaml_command_def("issue", "list")

        # These should all be flags, not string parameters
        status_flags = ["all", "closed", "open", "solved"]

        for flag_name in status_flags:
            assert flag_name in yaml_spec.options, (
                f"Missing status flag '{flag_name}' in YAML definition.\n"
                f"Available options: {list(yaml_spec.options.keys())}"
            )

            yaml_opt = yaml_spec.options[flag_name]
            assert yaml_opt.type == "flag", (
                f"Option '{flag_name}' should be type 'flag' but is '{yaml_opt.type}'.\n"
                f"The CLI uses mutually exclusive flags: --all | --closed | --open | --solved\n"
                f"\n"
                f"Fix in radicle-1.5.0.yaml:\n"
                f"  list:\n"
                f"    options:\n"
                f"      {flag_name}:\n"
                f"        type: flag\n"
                f"        description: Show only {flag_name} issues\n"
                f"        required: false"
            )

    def test_issue_list_mutually_exclusive_documented(
        self, rad_version, yaml_command_def
    ):
        """Verify mutually exclusive flags are documented correctly."""
        # Get actual CLI specification
        cli_spec = CLIHelpParser.parse_command_help("issue", "list")

        # CLI should show mutually exclusive group
        assert len(cli_spec.mutually_exclusive_groups) > 0, (
            "CLI should have mutually exclusive flags but none were detected"
        )

        # Should include the status flags
        status_group = None
        for group in cli_spec.mutually_exclusive_groups:
            if "open" in group and "closed" in group:
                status_group = group
                break

        assert status_group is not None, (
            f"Could not find status flag group in mutually exclusive groups: "
            f"{cli_spec.mutually_exclusive_groups}"
        )

        # The group should include our main status flags
        expected_flags = {"all", "closed", "open", "solved"}
        found_flags = set(status_group)

        assert expected_flags.issubset(found_flags), (
            f"Status flag group is incomplete.\n"
            f"Expected at least: {expected_flags}\n"
            f"Found: {found_flags}"
        )


@pytest.mark.cli_contract
@pytest.mark.requires_rad
class TestIssueOpenContract:
    """Test issue open command contract."""

    def test_issue_open_has_required_title(self, rad_version, yaml_command_def):
        """Verify title parameter is required."""
        yaml_spec = yaml_command_def("issue", "open")

        assert "title" in yaml_spec.options, (
            "Missing required 'title' option in issue open command"
        )

        title_opt = yaml_spec.options["title"]
        assert title_opt.required, (
            "The 'title' option should be marked as required=true"
        )
        assert title_opt.type == "string", (
            f"The 'title' option should be type 'string', not '{title_opt.type}'"
        )

    def test_issue_open_optional_params(self, rad_version, yaml_command_def):
        """Verify optional parameters are correctly defined."""
        yaml_spec = yaml_command_def("issue", "open")

        # Description should be optional string
        if "description" in yaml_spec.options:
            desc_opt = yaml_spec.options["description"]
            assert desc_opt.type == "string"
            assert not desc_opt.required

        # Label should be optional list
        if "label" in yaml_spec.options:
            label_opt = yaml_spec.options["label"]
            assert label_opt.type == "list"
            assert not label_opt.required


@pytest.mark.cli_contract
@pytest.mark.requires_rad
class TestIssueStateContract:
    """Test issue state command contract."""

    def test_issue_state_mutually_exclusive_flags(self, rad_version, yaml_command_def):
        """Verify state options are mutually exclusive flags."""
        yaml_spec = yaml_command_def("issue", "state")

        # These should all be present and be flag/boolean type
        state_flags = ["closed", "open", "solved"]

        for flag_name in state_flags:
            assert flag_name in yaml_spec.options, (
                f"Missing state flag '{flag_name}' in YAML definition"
            )

            yaml_opt = yaml_spec.options[flag_name]
            # Can be either 'flag' or 'boolean' - both work
            assert yaml_opt.type in ["flag", "boolean"], (
                f"Option '{flag_name}' should be type 'flag' or 'boolean' "
                f"but is '{yaml_opt.type}'"
            )
