"""Main entry point for code ingestion into Chroma.

This script discovers Python files in a target folder, intelligently chunks
them using code-aware splitting, and stores them in Chroma Cloud with metadata.

Usage:
    Basic: python ingest.py
    Custom folder: python ingest.py --folder /path/to/folder --collection my_collection
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from chroma_ingestion.ingestion import CodeIngester
from chroma_ingestion.retrieval import verify_ingestion


def main():
    """Main entry point for ingestion pipeline."""
    # Load environment variables
    load_dotenv()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Intelligently ingest Python code into Chroma Cloud"
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="/home/ob/Development/Tools/vibe-tools/ghc_tools/agents",
        help="Target folder to ingest (default: vibe-tools/ghc_tools/agents)",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="agents_context",
        help="Chroma collection name (default: agents_context)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Approximate tokens per chunk (default: 1000)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Token overlap between chunks (default: 200)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run verification queries after ingestion",
    )

    args = parser.parse_args()

    # Validate target folder
    if not Path(args.folder).exists():
        print(f"❌ Target folder does not exist: {args.folder}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("🚀 CHROMA CODE INGESTION")
    print("=" * 70)
    print(f"Target folder: {args.folder}")
    print(f"Collection: {args.collection}")
    print(f"Chunk size: {args.chunk_size} tokens")
    print(f"Chunk overlap: {args.chunk_overlap} tokens")
    print("=" * 70 + "\n")

    try:
        # Initialize ingester
        ingester = CodeIngester(
            target_folder=args.folder,
            collection_name=args.collection,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )

        # Run ingestion
        files_processed, chunks_ingested = ingester.ingest_files()

        # Print summary
        print("\n" + "-" * 70)
        print("📋 INGESTION SUMMARY")
        print("-" * 70)
        stats = ingester.get_collection_stats()
        print(f"Files processed: {files_processed}")
        print(f"Chunks ingested: {chunks_ingested}")
        print(f"Collection size: {stats['total_chunks']}")
        print("-" * 70 + "\n")

        # Run verification if requested
        if args.verify:
            verify_ingestion(args.collection)

        print("✅ Ingestion completed successfully!\n")
        return 0

    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
