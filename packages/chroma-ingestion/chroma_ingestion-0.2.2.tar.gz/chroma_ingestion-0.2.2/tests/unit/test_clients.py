"""Unit tests for chroma_ingestion.clients module.

Tests for ChromaDB client initialization and singleton pattern covering:
- Singleton pattern enforcement
- Client initialization
- Configuration handling
- Connection management
- Client reset functionality
"""

from unittest.mock import MagicMock, patch

import pytest

from chroma_ingestion.clients.chroma import get_chroma_client, reset_client


class TestGetChromaClientSingleton:
    """Test singleton pattern of get_chroma_client."""

    def test_get_chroma_client_returns_client(self) -> None:
        """Test that get_chroma_client returns a ChromaDB client."""
        with patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http:
            reset_client()  # Start fresh
            mock_client_instance = MagicMock()
            mock_http.return_value = mock_client_instance

            client = get_chroma_client()

            assert client is not None
            assert client == mock_client_instance

    def test_get_chroma_client_singleton_reuses_instance(self) -> None:
        """Test that get_chroma_client returns same instance on multiple calls."""
        with patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http:
            reset_client()  # Start fresh
            mock_client_instance = MagicMock()
            mock_http.return_value = mock_client_instance

            client1 = get_chroma_client()
            client2 = get_chroma_client()
            client3 = get_chroma_client()

            # All should be same instance
            assert client1 is client2
            assert client2 is client3

            # Constructor should only be called once
            assert mock_http.call_count == 1

    def test_get_chroma_client_loads_config(self) -> None:
        """Test that get_chroma_client loads configuration."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            reset_client()
            mock_config.return_value = {
                "host": "localhost",
                "port": 9500,
            }
            mock_client_instance = MagicMock()
            mock_http.return_value = mock_client_instance

            client = get_chroma_client()

            # Verify config was loaded
            mock_config.assert_called_once()

            # Verify HttpClient was called with config values
            mock_http.assert_called_once_with(
                host="localhost",
                port=9500,
            )

    def test_get_chroma_client_uses_custom_config(self) -> None:
        """Test get_chroma_client with custom configuration."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            reset_client()
            custom_config = {
                "host": "custom-host.example.com",
                "port": 8000,
            }
            mock_config.return_value = custom_config
            mock_client_instance = MagicMock()
            mock_http.return_value = mock_client_instance

            client = get_chroma_client()

            # Verify custom config was used
            mock_http.assert_called_once_with(
                host="custom-host.example.com",
                port=8000,
            )


class TestResetClient:
    """Test reset_client functionality."""

    def test_reset_client_clears_singleton(self) -> None:
        """Test that reset_client clears the singleton instance."""
        with patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http:
            # Create first instance
            reset_client()
            mock_http.return_value = MagicMock()
            client1 = get_chroma_client()

            # Reset
            reset_client()

            # Create second instance - should call constructor again
            mock_http.return_value = MagicMock()
            client2 = get_chroma_client()

            # Should have been called twice (once per cycle)
            assert mock_http.call_count == 2

    def test_reset_client_multiple_times(self) -> None:
        """Test resetting client multiple times."""
        with patch("chroma_ingestion.clients.chroma.chromadb.HttpClient"):
            # Multiple resets should not error
            reset_client()
            reset_client()
            reset_client()
            # Should complete without error

    def test_reset_client_allows_new_config(self) -> None:
        """Test that reset allows picking up new configuration."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            # First initialization with host1
            reset_client()
            mock_config.return_value = {"host": "host1", "port": 9500}
            mock_http.return_value = MagicMock()
            client1 = get_chroma_client()
            mock_http.assert_called_with(host="host1", port=9500)

            # Reset and change config
            reset_client()
            mock_config.return_value = {"host": "host2", "port": 8000}
            mock_http.reset_mock()
            mock_http.return_value = MagicMock()
            client2 = get_chroma_client()

            # Should use new config
            mock_http.assert_called_with(host="host2", port=8000)


class TestClientInitialization:
    """Test ChromaDB client initialization details."""

    def test_client_config_types(self) -> None:
        """Test that client receives correct configuration types."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            reset_client()
            mock_config.return_value = {
                "host": "localhost",
                "port": 9500,
            }
            mock_http.return_value = MagicMock()

            get_chroma_client()

            # Verify types of arguments
            call_kwargs = mock_http.call_args[1]
            assert isinstance(call_kwargs["host"], str)
            assert isinstance(call_kwargs["port"], int)

    def test_client_config_with_env_variables(self) -> None:
        """Test client initialization respects environment variables."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
            patch.dict("os.environ", {"CHROMA_HOST": "env-host"}),
        ):
            reset_client()
            mock_config.return_value = {
                "host": "env-host",
                "port": 9500,
            }
            mock_http.return_value = MagicMock()

            get_chroma_client()

            # Should use env-based config
            assert mock_http.call_args[1]["host"] == "env-host"

    def test_client_initialization_failure_handling(self) -> None:
        """Test handling of client initialization failures."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            reset_client()
            mock_config.return_value = {
                "host": "invalid-host",
                "port": 99999,
            }
            mock_http.side_effect = Exception("Connection failed")

            # Should raise the exception
            with pytest.raises(Exception):
                get_chroma_client()


class TestClientConnectionManagement:
    """Test client connection management."""

    def test_client_reuses_connection(self) -> None:
        """Test that singleton reuses connection instead of creating new ones."""
        with patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http:
            reset_client()
            mock_client = MagicMock()
            mock_http.return_value = mock_client

            # Get client multiple times
            for _ in range(5):
                client = get_chroma_client()
                # Use client (simulate operations)
                client.get_or_create_collection("test")

            # HttpClient constructor should only be called once
            assert mock_http.call_count == 1
            # But collection get should be called multiple times
            assert mock_client.get_or_create_collection.call_count == 5

    def test_client_not_created_until_first_call(self) -> None:
        """Test lazy initialization - client not created until get_chroma_client called."""
        with patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http:
            reset_client()
            # Client not created yet
            assert mock_http.call_count == 0

            # First call creates it
            get_chroma_client()
            assert mock_http.call_count == 1

            # Subsequent calls don't create new ones
            get_chroma_client()
            get_chroma_client()
            assert mock_http.call_count == 1


class TestClientModuleExports:
    """Test module exports and public API."""

    def test_get_chroma_client_is_callable(self) -> None:
        """Test that get_chroma_client is callable."""
        from chroma_ingestion.clients.chroma import get_chroma_client as gcc

        assert callable(gcc)

    def test_reset_client_is_callable(self) -> None:
        """Test that reset_client is callable."""
        from chroma_ingestion.clients.chroma import reset_client as rc

        assert callable(rc)

    def test_client_module_docstring(self) -> None:
        """Test that module has docstring."""
        import chroma_ingestion.clients.chroma

        assert chroma_ingestion.clients.chroma.__doc__ is not None


class TestClientErrorScenarios:
    """Test client error scenarios."""

    def test_config_loading_failure(self) -> None:
        """Test handling when config loading fails."""
        with patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config:
            reset_client()
            mock_config.side_effect = ValueError("Invalid config")

            with pytest.raises(ValueError):
                get_chroma_client()

    def test_invalid_config_parameters(self) -> None:
        """Test with invalid configuration parameters."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            reset_client()
            # Missing required keys
            mock_config.return_value = {"host": "localhost"}
            mock_http.return_value = MagicMock()

            # Should still work (port may have default)
            try:
                client = get_chroma_client()
                assert client is not None
            except KeyError:
                # Or it may raise if port is required
                pass

    def test_network_connection_error(self) -> None:
        """Test handling of network connection errors."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            reset_client()
            mock_config.return_value = {
                "host": "unreachable-host.invalid",
                "port": 9500,
            }
            # Simulate network error
            mock_http.side_effect = ConnectionError("Unable to connect")

            with pytest.raises(ConnectionError):
                get_chroma_client()


class TestClientThreadSafety:
    """Test client thread safety (basic)."""

    def test_singleton_consistency(self) -> None:
        """Test that singleton pattern maintains consistency."""
        with patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http:
            reset_client()
            mock_instance = MagicMock()
            mock_http.return_value = mock_instance

            # Get client multiple times rapidly
            clients = [get_chroma_client() for _ in range(10)]

            # All should be same instance
            assert all(c is clients[0] for c in clients)
            # Constructor should only be called once
            assert mock_http.call_count == 1


class TestClientIntegration:
    """Integration tests for client module."""

    def test_client_full_lifecycle(self) -> None:
        """Test full client lifecycle."""
        with (
            patch("chroma_ingestion.clients.chroma.chromadb.HttpClient") as mock_http,
            patch("chroma_ingestion.clients.chroma.get_chroma_config") as mock_config,
        ):
            # Setup
            reset_client()
            mock_config.return_value = {
                "host": "localhost",
                "port": 9500,
            }
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_http.return_value = mock_client

            # Get client and use it
            client = get_chroma_client()
            collection = client.get_or_create_collection("test_collection")

            # Verify
            assert client == mock_client
            assert collection == mock_collection
            mock_client.get_or_create_collection.assert_called_with("test_collection")

            # Reset
            reset_client()

            # Verify reset worked
            mock_http.reset_mock()
            mock_http.return_value = MagicMock()
            new_client = get_chroma_client()

            # Should be different instance
            assert new_client is not client
            assert mock_http.call_count == 1
