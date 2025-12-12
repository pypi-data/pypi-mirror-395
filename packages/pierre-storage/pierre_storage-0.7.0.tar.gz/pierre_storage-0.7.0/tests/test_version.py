"""Tests for version module."""

from pierre_storage.version import PACKAGE_NAME, PACKAGE_VERSION, get_user_agent


class TestVersion:
    """Tests for version constants and functions."""

    def test_package_name(self) -> None:
        """Test PACKAGE_NAME constant."""
        assert PACKAGE_NAME == "code-storage-py-sdk"

    def test_package_version(self) -> None:
        """Test PACKAGE_VERSION constant."""
        assert PACKAGE_VERSION == "0.7.0"

    def test_package_version_format(self) -> None:
        """Test that version follows semantic versioning."""
        import re

        semver_pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$"
        assert re.match(semver_pattern, PACKAGE_VERSION)

    def test_get_user_agent(self) -> None:
        """Test get_user_agent function."""
        user_agent = get_user_agent()
        assert user_agent == f"{PACKAGE_NAME}/{PACKAGE_VERSION}"
        assert user_agent == "code-storage-py-sdk/0.7.0"

    def test_get_user_agent_consistency(self) -> None:
        """Test that get_user_agent returns consistent value."""
        user_agent1 = get_user_agent()
        user_agent2 = get_user_agent()
        assert user_agent1 == user_agent2

    def test_user_agent_format(self) -> None:
        """Test that user agent follows expected format."""
        import re

        user_agent = get_user_agent()
        # Pattern: name/version
        pattern = r"^[\w-]+/\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$"
        assert re.match(pattern, user_agent)
