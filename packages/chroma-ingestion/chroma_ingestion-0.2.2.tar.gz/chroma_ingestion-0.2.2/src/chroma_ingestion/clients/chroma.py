"""Chroma HttpClient wrapper and initialization.

This module provides initialization and utility functions for the Chroma
HttpClient, following best practices for client management and configuration.
"""

import chromadb

from chroma_ingestion.config import get_chroma_config

# Global client instance (singleton pattern)
_client: chromadb.HttpClient | None = None


def get_chroma_client() -> chromadb.HttpClient:
    """Get or initialize the Chroma HttpClient.

    Uses a singleton pattern to ensure a single client instance is reused
    across the application. Connects to a local ChromaDB HTTP server.
    Configuration is loaded from environment variables.

    Returns:
        chromadb.HttpClient: Initialized Chroma HttpClient

    Raises:
        ValueError: If required configuration is missing or invalid
    """
    global _client

    if _client is None:
        config = get_chroma_config()
        _client = chromadb.HttpClient(
            host=config["host"],
            port=config["port"],
        )

    return _client


def reset_client() -> None:
    """Reset the global client instance.

    Useful for testing or when you need to reinitialize with new configuration.
    """
    global _client
    _client = None
