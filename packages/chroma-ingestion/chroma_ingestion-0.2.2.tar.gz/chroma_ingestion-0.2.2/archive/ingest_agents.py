#!/usr/bin/env python3
"""CLI for ingesting agent definitions into Chroma.

Ingests agents from multiple source folders, parses metadata,
and stores in Chroma vector database for semantic analysis.

Usage:
    python ingest_agents.py
"""

import argparse
import sys
from pathlib import Path

from chroma_ingestion.ingestion import AgentIngester

# Exclusion list - agents not relevant to our tech stack
EXCLUSIONS = [
    # Language-specific (not in our stack)
    "CSharpExpert.agent.md",
    "WinFormsExpert.agent.md",
    "swift-macos-expert.md",
    "golang-pro.md",
    "electron-pro.md",
    "mobile-developer.md",
    "c-pro.md",
    "cpp-pro.md",
    # Framework-specific (Svelte not in stack)
    "svelte-development.md",
    "svelte-storybook.md",
    "svelte-testing.md",
    # Enterprise tools (not in stack)
    "azure-devops-specialist.md",
    "octopus-deploy-release-notes-mcp.agent.md",
    "dynatrace-expert.agent.md",
    "amplitude-experiment-implementation.agent.md",
    "arm-migration.agent.md",
    "jfrog-sec.agent.md",
    "launchdarkly-flag-cleanup.agent.md",
    "pagerduty-incident-responder.agent.md",
    "stackhawk-security-onboarding.agent.md",
    "terraform.agent.md",
]


def get_source_folders() -> list:
    """Get list of source folders for agent files.

    Returns:
        List of absolute paths to agent source folders
    """
    base_path = Path("/home/ob/Development/Tools/vibe-tools")

    return [
        str(base_path / ".github" / "agents"),
        str(base_path / "ccs" / ".claude" / "agents"),
        str(base_path / "ghc_tools" / "agents"),
        str(base_path / "scf" / "src" / "superclaude" / "agents"),
    ]


def main():
    """Main ingestion workflow."""
    parser = argparse.ArgumentParser(
        description="Ingest agent definitions into Chroma for semantic analysis"
    )
    parser.add_argument(
        "--collection",
        default="agents_analysis",
        help="Chroma collection name (default: agents_analysis)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1500,
        help="Tokens per chunk (default: 1500 for agents)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=300,
        help="Token overlap (default: 300)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Chunks per batch upsert (default: 50)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="Additional files to exclude (can repeat)",
    )

    args = parser.parse_args()

    # Combine default and custom exclusions
    exclusions = EXCLUSIONS.copy()
    if args.exclude:
        exclusions.extend(args.exclude)

    print("=" * 70)
    print("AGENT INGESTION - Multi-folder Analysis")
    print("=" * 70)

    source_folders = get_source_folders()
    print("\n📂 Source Folders:")
    for folder in source_folders:
        print(f"   - {folder}")

    print(f"\n🚫 Excluded Files: {len(exclusions)} patterns")

    # Initialize ingester
    ingester = AgentIngester(
        source_folders=source_folders,
        collection_name=args.collection,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        exclusions=exclusions,
    )

    # Run ingestion
    print("\n⏳ Starting ingestion...\n")
    files_processed, chunks_ingested = ingester.ingest_agents(batch_size=args.batch_size)

    # Print summary
    print("\n" + "=" * 70)
    print("INGESTION COMPLETE")
    print("=" * 70)
    print(f"✅ Files processed: {files_processed}")
    print(f"✅ Chunks ingested: {chunks_ingested}")

    if chunks_ingested > 0:
        print(f"✅ Avg chunks per file: {chunks_ingested / files_processed:.1f}")

    # Print collection stats
    stats = ingester.get_collection_stats()
    print("\n📊 Collection Stats:")
    print(f"   Collection: {stats['collection_name']}")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Chunk size: {stats['chunk_size']} tokens")
    print(f"   Chunk overlap: {stats['chunk_overlap']} tokens")

    print("\n✨ Ready for analysis! Run: python analyze_agents.py\n")

    return 0 if chunks_ingested > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
