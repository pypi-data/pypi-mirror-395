"""Test configuration functionality."""

import pytest
import tempfile
import yaml
from pathlib import Path

# Mock imports to avoid dependency issues
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestConfig:
    """Test configuration management."""

    def test_default_config_loading(self):
        """Test loading of default configuration."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"
            config = Config(config_file)

            # Test default values
            assert config.get("server.host") == "localhost"
            assert config.get("server.port") == 8000
            assert config.get("server.transport") == "stdio"
            assert config.get("radicle.timeout") == 30

    def test_config_merging(self):
        """Test configuration merging."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"

            # Create custom config
            custom_config = {
                "server": {"port": 9000, "transport": "http"},
                "radicle": {"timeout": 60},
            }

            with open(config_file, "w") as f:
                yaml.dump(custom_config, f)

            config = Config(config_file)

            # Test merged values
            assert config.get("server.host") == "localhost"  # Default
            assert config.get("server.port") == 9000  # Custom
            assert config.get("server.transport") == "http"  # Custom
            assert config.get("radicle.timeout") == 60  # Custom

    def test_config_dot_notation(self):
        """Test configuration access with dot notation."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"
            config = Config(config_file)

            # Test dot notation
            assert config.get("server.host") == "localhost"
            assert config.get("radicle.timeout") == 30

            # Test setting with dot notation
            config.set("server.host", "example.com")
            assert config.get("server.host") == "example.com"

            config.set("new.nested.key", "value")
            assert config.get("new.nested.key") == "value"

    def test_config_save_and_load(self):
        """Test saving and loading configuration."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"
            config = Config(config_file)

            # Modify configuration
            config.set("test.key", "test_value")
            config.save()

            # Load fresh instance
            config2 = Config(config_file)
            assert config2.get("test.key") == "test_value"

    def test_config_get_with_default(self):
        """Test getting configuration with default values."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.yaml"
            config = Config(config_file)

            # Test getting existing key
            assert config.get("server.host", "default") == "localhost"

            # Test getting missing key with default
            assert config.get("missing.key", "default_value") == "default_value"

            # Test getting missing key without default
            assert config.get("missing.key") is None

    def test_config_error_handling(self):
        """Test error handling in configuration."""
        from src.config import Config

        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "invalid.yaml"

            # Create invalid YAML file
            with open(config_file, "w") as f:
                f.write("invalid: yaml: content: [")

            # Should handle invalid YAML gracefully
            config = Config(config_file)
            # Should still have default values
            assert config.get("server.host") == "localhost"


if __name__ == "__main__":
    pytest.main([__file__])
