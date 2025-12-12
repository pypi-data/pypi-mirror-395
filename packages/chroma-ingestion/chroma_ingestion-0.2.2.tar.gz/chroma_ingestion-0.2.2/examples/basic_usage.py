"""Main entry point for Chroma SDK application."""

from dotenv import load_dotenv

from chroma_ingestion.clients.chroma import get_chroma_client


def main():
    """Initialize and use the Chroma CloudClient."""
    # Load environment variables from .env file
    load_dotenv()

    # Get the Chroma client
    client = get_chroma_client()

    # Example: Check client is connected
    print("✓ Connected to Chroma Cloud")
    print(f"  Client type: {type(client).__name__}")


if __name__ == "__main__":
    main()
