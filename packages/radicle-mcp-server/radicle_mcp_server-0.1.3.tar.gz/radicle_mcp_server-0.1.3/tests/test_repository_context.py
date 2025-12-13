"""Test repository context functionality."""

import pytest
from unittest.mock import Mock, patch

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.repository_context import RepositoryContext


class TestRepositoryContext:
    """Test RepositoryContext class."""

    def test_init_without_rad_installed(self):
        """Test initialization when rad CLI not installed."""
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            context = RepositoryContext()

            assert context.rid is None
            assert context.path is None
            assert context.confirmed_rid is None
            assert not context.is_valid()

    def test_init_outside_repository(self):
        """Test initialization outside a Radicle repository."""
        mock_result = Mock(returncode=1, stdout="", stderr="Not in repository")

        with patch("subprocess.run", return_value=mock_result):
            context = RepositoryContext()

            assert context.rid is None
            assert context.path is None
            assert not context.is_valid()

    def test_init_with_explicit_rid(self):
        """Test initialization with explicit RID parameter."""
        test_rid = "rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5"

        context = RepositoryContext(rid=test_rid)

        assert context.rid == test_rid
        assert context.confirmed_rid == test_rid
        assert context.is_valid()

    def test_init_inside_repository(self):
        """Test successful repository detection."""
        mock_inspect = Mock(returncode=0, stdout="Repository info", stderr="")
        mock_rid = Mock(
            returncode=0, stdout="rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5\n", stderr=""
        )

        with patch(
            "subprocess.run", side_effect=[mock_inspect, mock_rid, mock_inspect]
        ):
            context = RepositoryContext()

            assert context.rid == "rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5"
            assert context.path is not None
            assert context.is_valid()

    def test_set_repository_valid(self):
        """Test setting repository with valid RID."""
        context = RepositoryContext()
        test_rid = "rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5"

        mock_result = Mock(
            returncode=0, stdout="Test Repository\n\nDetails...", stderr=""
        )

        with patch("subprocess.run", return_value=mock_result):
            success, message = context.set_repository(test_rid)

            assert success
            assert test_rid in message
            assert context.rid == test_rid
            assert context.confirmed_rid == test_rid

    def test_set_repository_invalid_format(self):
        """Test setting repository with invalid RID format."""
        context = RepositoryContext()

        success, message = context.set_repository("invalid-rid")

        assert not success
        assert "Invalid RID format" in message

    def test_set_repository_not_found(self):
        """Test setting repository that doesn't exist."""
        context = RepositoryContext()
        test_rid = "rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5"

        mock_result = Mock(returncode=1, stdout="", stderr="Repository not found")

        with patch("subprocess.run", return_value=mock_result):
            success, message = context.set_repository(test_rid)

            assert not success
            assert "not found" in message.lower()

    def test_get_repository_info_valid(self):
        """Test getting repository info when valid."""
        test_rid = "rad:z3gqcJUoA1n9HaHKufZs5FCSGazv5"
        context = RepositoryContext(rid=test_rid)

        info = context.get_repository_info()

        assert info["detected_rid"] == test_rid
        assert info["confirmed_rid"] == test_rid
        assert info["active_rid"] == test_rid
        assert info["is_valid"]

    def test_get_repository_info_none(self):
        """Test getting repository info when no repository set."""
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            context = RepositoryContext()

        info = context.get_repository_info()

        assert info["detected_rid"] is None
        assert info["confirmed_rid"] is None
        assert info["active_rid"] is None
        assert not info["is_valid"]


if __name__ == "__main__":
    pytest.main([__file__])
