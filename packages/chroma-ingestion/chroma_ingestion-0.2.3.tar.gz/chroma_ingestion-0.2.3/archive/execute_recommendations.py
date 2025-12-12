#!/usr/bin/env python3
"""
Execute all recommendations from query_nextjs_patterns analysis.

Runs 4 types of queries:
1. Distance threshold filtering (< 0.5)
2. Metadata filtering (category, tech_stack)
3. Different semantic queries (Server Components, App Router, TypeScript)
4. Multi-collection search
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from clients.chroma_client import get_chroma_client
from retrieval import CodeRetriever, MultiCollectionSearcher


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def format_result(result: dict, index: int) -> str:
    """Format a single result for display."""
    distance = result.get("distance", "N/A")
    metadata = result.get("metadata", {})
    agent_name = metadata.get("agent_name", "Unknown")
    category = metadata.get("category", "Unknown")
    tech_stack = ", ".join(metadata.get("tech_stack", [])[:3]) or "N/A"
    doc_preview = result.get("document", "")[:100] + "..." if result.get("document") else "N/A"

    return f"""{index + 1}. [{agent_name}] Category: {category}
   Distance: {distance:.4f} | Tech: {tech_stack}
   Preview: {doc_preview}"""


def recommendation_1_distance_threshold():
    """1. Lower distance thresholds: filter results with distance < 0.5"""
    print_section("RECOMMENDATION 1: Distance Threshold Filtering (< 0.5)")

    retriever = CodeRetriever("agents_analysis")

    print("Query: 'Next.js patterns' with distance_threshold=0.5")
    print("-" * 80)

    # Execute with strict distance threshold
    results = retriever.query_semantic(
        query_text="Next.js patterns", n_results=5, distance_threshold=0.5
    )

    if results:
        print(f"✅ Found {len(results)} results with distance < 0.5:\n")
        for i, result in enumerate(results):
            print(format_result(result, i))
        print(f"\n📊 Summary: {len(results)} high-confidence matches")
    else:
        print("❌ No results found with distance < 0.5 (threshold too strict)")

    return results


def recommendation_2_metadata_filtering():
    """2. Metadata filtering: use where clause for category/tech_stack"""
    print_section("RECOMMENDATION 2: Metadata Filtering")

    retriever = CodeRetriever("agents_analysis")

    print("Query 1: Filter by category='frontend'\n")
    print("-" * 80)

    results_frontend = retriever.query_by_metadata(where={"category": "frontend"}, n_results=5)

    if results_frontend:
        print(f"✅ Found {len(results_frontend)} frontend results:\n")
        for i, result in enumerate(results_frontend[:5]):
            meta = result.get("metadata", {})
            agent_name = meta.get("agent_name", "Unknown")
            print(f"{i + 1}. {agent_name}")
    else:
        print("❌ No results found")

    print("\n" + "=" * 80)
    print("Query 2: Filter by tech_stack containing 'next.js'\n")
    print("-" * 80)

    # Try metadata filter with tech_stack (if it contains 'next.js')
    results_nextjs = retriever.query_by_metadata(
        where={"tech_stack": {"$contains": "next.js"}}, n_results=5
    )

    if results_nextjs:
        print(f"✅ Found {len(results_nextjs)} Next.js results:\n")
        for i, result in enumerate(results_nextjs[:5]):
            meta = result.get("metadata", {})
            agent_name = meta.get("agent_name", "Unknown")
            tech = ", ".join(meta.get("tech_stack", [])[:3])
            print(f"{i + 1}. {agent_name} - Tech: {tech}")
    else:
        print("❌ No results found (metadata may use different structure)")

    return results_frontend, results_nextjs


def recommendation_3_different_queries():
    """3. Different queries: Server Components, App Router patterns, TypeScript types"""
    print_section("RECOMMENDATION 3: Different Semantic Queries")

    retriever = CodeRetriever("agents_analysis")

    queries = ["Server Components", "App Router patterns", "TypeScript types"]

    all_results = {}

    for query in queries:
        print(f"\nQuery: '{query}' (distance_threshold=0.5)")
        print("-" * 80)

        results = retriever.query_semantic(query_text=query, n_results=3, distance_threshold=0.5)

        all_results[query] = results

        if results:
            print(f"✅ Found {len(results)} results:\n")
            for i, result in enumerate(results):
                print(format_result(result, i))
        else:
            print("⚠️  No results with distance < 0.5")
            # Show what we get without threshold
            unrestricted = retriever.query(query_text=query, n_results=3)
            print(f"   Without threshold: {len(unrestricted)} results available")
            if unrestricted:
                best = unrestricted[0]
                print(
                    f"   Best match: {best.get('metadata', {}).get('agent_name', 'Unknown')} (distance: {best.get('distance', 'N/A'):.4f})"
                )

    return all_results


def recommendation_4_multi_collection_search():
    """4. Multi-collection search: use MultiCollectionSearcher"""
    print_section("RECOMMENDATION 4: Multi-Collection Search")

    client = get_chroma_client()

    # List available collections
    try:
        collections = client.list_collections()
        collection_names = [c.name for c in collections]
        print(f"📦 Available collections: {len(collection_names)}")
        for name in collection_names:
            print(f"   - {name}")
    except Exception as e:
        print(f"❌ Failed to list collections: {e}")
        return {}

    print("\n" + "-" * 80)

    if len(collection_names) > 1:
        print(f"\n🔍 Searching across {len(collection_names)} collections for 'Next.js patterns'\n")

        try:
            searcher = MultiCollectionSearcher(collection_names)

            # Search all collections
            results = searcher.search_all(query_text="Next.js patterns", n_results=3)

            print(f"✅ Found {len(results)} results across all collections:\n")
            for i, result in enumerate(results):
                collection = result.get("collection", "Unknown")
                agent = result.get("metadata", {}).get("agent_name", "Unknown")
                distance = result.get("distance", "N/A")
                print(f"{i + 1}. [{collection}] {agent} (distance: {distance:.4f})")

            print("\n" + "-" * 80)
            print("\n🔍 Ranked search across collections\n")

            ranked = searcher.search_ranked(query_text="Next.js patterns", n_results=3)

            print("✅ Ranked results (best match first):\n")
            for i, result in enumerate(ranked):
                collection = result.get("collection", "Unknown")
                agent = result.get("metadata", {}).get("agent_name", "Unknown")
                distance = result.get("distance", "N/A")
                rank_score = result.get("rank_score", "N/A")
                print(
                    f"{i + 1}. [{collection}] {agent} (distance: {distance:.4f}, rank: {rank_score})"
                )

            return results

        except Exception as e:
            print(f"❌ MultiCollectionSearcher failed: {e}")
            return {}
    else:
        print(f"⚠️  Only {len(collection_names)} collection available")
        print("   MultiCollectionSearcher requires multiple collections")
        return {}


def main():
    """Execute all recommendations."""
    print("\n" + "=" * 80)
    print("  EXECUTING CHROMA QUERY RECOMMENDATIONS")
    print("=" * 80)
    print("\nThis script tests all 4 recommendations from the query analysis:")
    print("  1. Lower distance thresholds (< 0.5)")
    print("  2. Metadata filtering (category, tech_stack)")
    print("  3. Different semantic queries")
    print("  4. Multi-collection search")

    try:
        # Execute all recommendations
        results_1 = recommendation_1_distance_threshold()
        results_2 = recommendation_2_metadata_filtering()
        results_3 = recommendation_3_different_queries()
        results_4 = recommendation_4_multi_collection_search()

        # Final summary
        print_section("SUMMARY OF FINDINGS")

        print("✅ RECOMMENDATION 1 (Distance Threshold)")
        print(f"   Status: {'PASSED' if results_1 else 'INCONCLUSIVE - Threshold too strict'}")
        if results_1:
            print(f"   Results: {len(results_1)} matches with distance < 0.5")

        print("\n✅ RECOMMENDATION 2 (Metadata Filtering)")
        frontend_count = len(results_2[0]) if results_2 and results_2[0] else 0
        nextjs_count = len(results_2[1]) if results_2 and results_2[1] else 0
        print(f"   Frontend category: {frontend_count} results")
        print(f"   Next.js tech_stack: {nextjs_count} results")

        print("\n✅ RECOMMENDATION 3 (Different Queries)")
        for query, results in results_3.items():
            print(f"   '{query}': {len(results)} high-confidence matches")

        print("\n✅ RECOMMENDATION 4 (Multi-Collection Search)")
        print(
            f"   Status: {'PASSED' if results_4 else 'INCONCLUSIVE - Requires multiple collections'}"
        )
        if results_4:
            print(f"   Results: {len(results_4)} matches across collections")

        print("\n" + "=" * 80)
        print("\n✨ All recommendations have been executed!")
        print("   See detailed results above for insights.")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
