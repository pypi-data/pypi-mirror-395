"""Configuration module for Chroma SDK.

Loads configuration from environment variables. For local development,
use a .env file (which is loaded automatically via python-dotenv).
"""

import os


def get_chroma_config() -> dict[str, str | int]:
    """Load Chroma HttpClient configuration from environment variables.

    Configuration for connecting to a local ChromaDB HTTP server.

    Environment variables:
    - CHROMA_HOST: Host of the ChromaDB server (default: 'localhost')
    - CHROMA_PORT: Port of the ChromaDB server (default: 9500)

    Returns:
        dict: Configuration dictionary for HttpClient

    Raises:
        ValueError: If invalid port configuration
    """
    host: str = os.getenv("CHROMA_HOST", "localhost")
    port_str: str | None = os.getenv("CHROMA_PORT", "9500")

    try:
        port: int = int(port_str)
    except (ValueError, TypeError) as err:
        raise ValueError(
            f"Invalid CHROMA_PORT: {port_str}. Must be a valid integer. Default is 9500."
        ) from err

    return {
        "host": host,
        "port": port,
    }
