"""Test YAML definitions for Radicle versions."""

import pytest
import yaml
from pathlib import Path

from src.definitions.schema import validate_yaml_schema


class TestYAMLDefinitions:
    """Test that YAML definition files are valid."""

    def test_radicle_1_1_0_definition(self):
        """Test radicle-1.1.0.yaml definition is valid."""
        definitions_dir = Path(__file__).parent.parent / "src" / "definitions"
        yaml_file = definitions_dir / "radicle-1.1.0.yaml"

        assert yaml_file.exists(), f"YAML file {yaml_file} should exist"

        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)

        # Should validate without errors
        result = validate_yaml_schema(yaml_data)
        assert result.metadata.version == "1.1.0"
        assert result.metadata.breaking_changes
        assert result.metadata.migration_required

        # Check for key commands
        assert "issue" in result.commands
        assert "patch" in result.commands
        assert "node" in result.commands
        assert "cob" in result.commands

        # Check for 1.1.0 specific features
        cob_cmd = result.commands["cob"]
        assert "migrate" in cob_cmd.subcommands
        assert cob_cmd.subcommands["migrate"].added_in == "1.1.0"

        id_cmd = result.commands["id"]
        assert "update" in id_cmd.subcommands
        assert id_cmd.subcommands["update"].options["edit"].added_in == "1.1.0"

    def test_radicle_1_2_0_definition(self):
        """Test radicle-1.2.0.yaml definition is valid."""
        definitions_dir = Path(__file__).parent.parent / "src" / "definitions"
        yaml_file = definitions_dir / "radicle-1.2.0.yaml"

        assert yaml_file.exists(), f"YAML file {yaml_file} should exist"

        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)

        result = validate_yaml_schema(yaml_data)
        assert result.metadata.version == "1.2.0"
        assert not result.metadata.breaking_changes

        # Check for 1.2.0 specific features
        config_cmd = result.commands["config"]
        assert "schema" in config_cmd.subcommands
        assert config_cmd.subcommands["schema"].added_in == "1.2.0"

        issue_cmd = result.commands["issue"]
        assert issue_cmd.options["json"].added_in == "1.2.0"
        assert issue_cmd.options["status"].added_in == "1.2.0"

        patch_cmd = result.commands["patch"]
        assert patch_cmd.options["json"].added_in == "1.2.0"
        assert "edit" in patch_cmd.subcommands
        assert patch_cmd.subcommands["edit"].added_in == "1.2.0"

        node_cmd = result.commands["node"]
        assert "inventory" in node_cmd.subcommands
        assert node_cmd.subcommands["inventory"].added_in == "1.2.0"

        cob_cmd = result.commands["cob"]
        assert "show" in cob_cmd.subcommands
        assert cob_cmd.subcommands["show"].options["json"].added_in == "1.2.0"
        assert "create" in cob_cmd.subcommands
        assert "update" in cob_cmd.subcommands

    def test_radicle_1_3_0_definition(self):
        """Test radicle-1.3.0.yaml definition is valid."""
        definitions_dir = Path(__file__).parent.parent / "src" / "definitions"
        yaml_file = definitions_dir / "radicle-1.3.0.yaml"

        assert yaml_file.exists(), f"YAML file {yaml_file} should exist"

        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)

        result = validate_yaml_schema(yaml_data)
        assert result.metadata.version == "1.3.0"
        assert not result.metadata.breaking_changes

        # Check for 1.3.0 specific features
        cob_cmd = result.commands["cob"]
        assert "log" in cob_cmd.subcommands
        log_cmd = cob_cmd.subcommands["log"]
        assert log_cmd.options["from"].added_in == "1.3.0"
        assert log_cmd.options["to"].added_in == "1.3.0"

    def test_radicle_1_4_0_definition(self):
        """Test radicle-1.4.0.yaml definition is valid."""
        definitions_dir = Path(__file__).parent.parent / "src" / "definitions"
        yaml_file = definitions_dir / "radicle-1.4.0.yaml"

        assert yaml_file.exists(), f"YAML file {yaml_file} should exist"

        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)

        result = validate_yaml_schema(yaml_data)
        assert result.metadata.version == "1.4.0"
        assert not result.metadata.breaking_changes

        # Check for 1.4.0 specific features
        cob_cmd = result.commands["cob"]
        log_cmd = cob_cmd.subcommands["log"]
        # 1.4.0 should have the same log options as 1.3.0
        assert log_cmd.options["from"].added_in == "1.4.0"
        assert log_cmd.options["to"].added_in == "1.4.0"

    def test_radicle_1_5_0_definition(self):
        """Test radicle-1.5.0.yaml definition is valid."""
        definitions_dir = Path(__file__).parent.parent / "src" / "definitions"
        yaml_file = definitions_dir / "radicle-1.5.0.yaml"

        assert yaml_file.exists(), f"YAML file {yaml_file} should exist"

        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)

        result = validate_yaml_schema(yaml_data)
        assert result.metadata.version == "1.5.0"
        assert not result.metadata.breaking_changes

        # Check for 1.5.0 specific features (should be same as 1.4.0 for now)
        # This test will need to be updated when 1.5.0 has new features

    def test_all_definitions_have_required_fields(self):
        """Test that all definitions have required metadata fields."""
        definitions_dir = Path(__file__).parent.parent / "src" / "definitions"

        for yaml_file in definitions_dir.glob("radicle-*.yaml"):
            with open(yaml_file, "r") as f:
                yaml_data = yaml.safe_load(f)

            result = validate_yaml_schema(yaml_data)

            # Check required metadata fields
            assert result.metadata.version is not None
            assert result.metadata.release_date is not None
            assert "commands" in yaml_data

            # Check that commands have required fields
            for cmd_name, cmd_def in result.commands.items():
                assert cmd_def.name is not None
                assert cmd_def.help is not None
                assert isinstance(cmd_def.options, dict)
                assert isinstance(cmd_def.subcommands, dict)

    def test_version_progression(self):
        """Test that version progression makes sense."""
        definitions_dir = Path(__file__).parent.parent / "src" / "definitions"

        versions = []
        for yaml_file in definitions_dir.glob("radicle-*.yaml"):
            with open(yaml_file, "r") as f:
                yaml_data = yaml.safe_load(f)
            versions.append(yaml_data["metadata"]["version"])

        # Sort versions
        versions.sort()

        # Check that we have the expected versions
        expected_versions = ["1.1.0", "1.2.0", "1.3.0", "1.4.0", "1.5.0"]
        for expected in expected_versions:
            assert expected in versions, f"Version {expected} should be defined"

        # Check that breaking changes are properly marked
        for version in versions:
            yaml_file = definitions_dir / f"radicle-{version}.yaml"
            with open(yaml_file, "r") as f:
                yaml_data = yaml.safe_load(f)

            if version == "1.1.0":
                assert yaml_data["metadata"]["breaking_changes"]
            else:
                assert not yaml_data["metadata"]["breaking_changes"]


if __name__ == "__main__":
    pytest.main([__file__])
