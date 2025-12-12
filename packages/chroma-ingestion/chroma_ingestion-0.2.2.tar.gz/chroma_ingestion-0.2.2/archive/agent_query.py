#!/usr/bin/env python3
"""Example: Query agent definitions and inject context into prompts.

This script demonstrates how to use ChromaDB to retrieve agent definitions
and inject them into system prompts for AI tools.

Usage:
    python agent_query.py "agent name or task"
    python agent_query.py "what are the best practices for backend architecture?"
"""

import sys

from chroma_ingestion.retrieval import CodeRetriever, MultiCollectionSearcher


def query_single_collection(query: str, collection: str = "vibe_agents") -> None:
    """Query a single collection and display results.

    Args:
        query: Search query text
        collection: Collection name to search
    """
    print(f"\n🔍 Searching '{collection}' for: {query}\n")

    retriever = CodeRetriever(collection)

    # Get semantic results with good relevance
    results = retriever.query_semantic(query, n_results=3, distance_threshold=0.6)

    if not results:
        print(f"❌ No results found in '{collection}'")
        return

    print(f"📊 Found {len(results)} relevant chunk(s):\n")

    for i, result in enumerate(results, 1):
        meta = result["metadata"]
        doc = result["document"]
        distance = result["distance"]

        print(f"Result {i}:")
        print(f"  📄 Source: {meta.get('source', 'unknown')}")
        print(f"  📏 Relevance: {(1 - distance):.1%}")
        print("  ✂️  Preview:\n")
        print(f"     {doc[:300]}...")
        print()


def query_all_collections(query: str) -> None:
    """Search across all agent collections and show ranked results.

    Args:
        query: Search query text
    """
    print(f"\n🔍 Searching all collections for: {query}\n")

    collections = ["vibe_agents", "ghc_agents", "superclaude_agents"]
    searcher = MultiCollectionSearcher(collections)

    # Get ranked results across all collections
    results = searcher.search_ranked(query, n_results=5)

    if not results:
        print("❌ No results found across any collection")
        return

    print(f"📊 Found {len(results)} relevant chunk(s) (ranked by relevance):\n")

    for i, result in enumerate(results, 1):
        meta = result["metadata"]
        doc = result["document"]
        distance = result["distance"]
        collection = result.get("collection", "unknown")

        print(f"Result {i} ({collection}):")
        print(f"  📄 Source: {meta.get('source', 'unknown')}")
        print(f"  📏 Relevance: {(1 - distance):.1%}")
        print("  ✂️  Preview:\n")
        print(f"     {doc[:300]}...")
        print()


def get_injection_context(query: str) -> str:
    """Get formatted context ready for prompt injection.

    Args:
        query: Search query text

    Returns:
        Formatted context string
    """
    collections = ["vibe_agents", "ghc_agents", "superclaude_agents"]
    searcher = MultiCollectionSearcher(collections)

    return searcher.get_context_multiway(query, n_results=2)


def example_agent_prompt_injection(agent_task: str) -> None:
    """Example of injecting agent context into a system prompt.

    Args:
        agent_task: Description of the agent task to find relevant agents for
    """
    print(f"\n💡 EXAMPLE: Prompt injection for task: '{agent_task}'\n")

    # Get relevant context
    context = get_injection_context(agent_task)

    # Build a system prompt
    system_prompt = f"""You are an AI assistant helping to design or select agents.

Use the following relevant agent definitions and patterns as reference:

{context}

Based on the above context, respond to the user's request."""

    print("📝 Generated System Prompt:\n")
    print("=" * 70)
    print(system_prompt)
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent_query.py <query>")
        print("\nExamples:")
        print("  python agent_query.py 'backend architect'")
        print("  python agent_query.py 'error handling in agents'")
        print("  python agent_query.py 'how to validate user input'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # Show results from all collections
    query_all_collections(query)

    # Show example prompt injection
    example_agent_prompt_injection(query)
