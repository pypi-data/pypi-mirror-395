"""Unit tests for chroma_ingestion.config module.

Tests the configuration loading and management functionality,
including environment variable handling and default values.
"""

from __future__ import annotations

import os
from unittest.mock import patch

from chroma_ingestion.config import get_chroma_config


class TestGetChromaConfig:
    """Test suite for get_chroma_config function."""

    def test_get_chroma_config_defaults(self) -> None:
        """Test that default configuration values are returned correctly.

        Verifies that the function returns a dictionary with expected keys
        and reasonable default values when no environment variables are set.
        """
        with patch.dict(os.environ, {}, clear=False):
            config = get_chroma_config()

            # Check required keys are present
            assert isinstance(config, dict)
            assert "host" in config
            assert "port" in config

    def test_get_chroma_config_returns_dict(self) -> None:
        """Test that get_chroma_config returns a dictionary.

        Ensures the function always returns a dict type for consistency.
        """
        config = get_chroma_config()
        assert isinstance(config, dict)

    def test_get_chroma_config_from_env_host(self) -> None:
        """Test configuration loading from CHROMA_HOST environment variable.

        Verifies that custom host values set via environment variables
        are properly reflected in the returned configuration.
        """
        custom_host = "custom-chroma-host.example.com"
        with patch.dict(os.environ, {"CHROMA_HOST": custom_host}):
            config = get_chroma_config()
            assert config.get("host") == custom_host

    def test_get_chroma_config_from_env_port(self) -> None:
        """Test configuration loading from CHROMA_PORT environment variable.

        Verifies that custom port values set via environment variables
        are properly reflected in the returned configuration.
        """
        with patch.dict(os.environ, {"CHROMA_PORT": "8000"}):
            config = get_chroma_config()
            # Port may be stored as string or int depending on implementation
            assert config.get("port") in [8000, "8000"]

    def test_get_chroma_config_localhost_default(self) -> None:
        """Test that localhost is used as default host.

        Verifies that the default host is localhost when no environment
        variable is set.
        """
        with patch.dict(os.environ, {}, clear=False):
            # Remove CHROMA_HOST if it exists
            os.environ.pop("CHROMA_HOST", None)
            config = get_chroma_config()

            # Default should be localhost or 127.0.0.1
            assert config.get("host") in ["localhost", "127.0.0.1"]

    def test_get_chroma_config_port_type(self) -> None:
        """Test that port configuration is returned as expected type.

        Verifies that port is returned in the correct format (int or str)
        for proper connection handling.
        """
        config = get_chroma_config()
        port = config.get("port")

        # Port should be either int or string representation of int
        if isinstance(port, str):
            assert port.isdigit()
        else:
            assert isinstance(port, int)

    def test_get_chroma_config_multiple_calls(self) -> None:
        """Test that multiple calls return consistent configuration.

        Ensures that calling get_chroma_config multiple times returns
        the same configuration values.
        """
        config1 = get_chroma_config()
        config2 = get_chroma_config()

        assert config1 == config2

    def test_get_chroma_config_with_multiple_env_vars(self) -> None:
        """Test configuration with multiple environment variables set.

        Verifies that multiple environment variables are processed correctly
        and all custom values are reflected in the returned configuration.
        """
        custom_vars = {
            "CHROMA_HOST": "api.chroma.example.com",
            "CHROMA_PORT": "443",
        }
        with patch.dict(os.environ, custom_vars):
            config = get_chroma_config()

            assert config.get("host") == "api.chroma.example.com"
            assert config.get("port") in [443, "443"]

    def test_get_chroma_config_immutability(self) -> None:
        """Test that returned config doesn't affect future calls.

        Verifies that modifications to the returned config dictionary
        don't affect subsequent calls to get_chroma_config.
        """
        config1 = get_chroma_config()
        config1["host"] = "modified-host"

        config2 = get_chroma_config()

        # config2 should have original values
        assert config2.get("host") != "modified-host"
