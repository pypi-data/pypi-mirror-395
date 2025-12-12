#!/usr/bin/env python3
"""
Verification script: Demonstrate all working recommendations with optimal configurations.

This script shows the correct way to use each recommendation after analysis.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from retrieval import CodeRetriever


def print_header(title: str):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def verify_recommendation_1():
    """Verify: Distance threshold filtering with optimal threshold."""
    print_header("VERIFICATION 1: Distance Threshold (< 1.0)")

    retriever = CodeRetriever("agents_analysis")

    print("Using optimal distance threshold: 1.0")
    results = retriever.query_semantic(
        query_text="Next.js patterns", n_results=5, distance_threshold=1.0
    )

    if results:
        print(f"✅ SUCCESS: Found {len(results)} high-confidence results\n")
        for i, r in enumerate(results, 1):
            agent = r.get("metadata", {}).get("agent_name", "Unknown")
            distance = r.get("distance", "N/A")
            print(f"  {i}. {agent} (distance: {distance:.4f})")
        return True
    else:
        print("❌ FAILED: No results found")
        return False


def verify_recommendation_2():
    """Verify: Metadata filtering with category field."""
    print_header("VERIFICATION 2: Metadata Filtering (Category)")

    retriever = CodeRetriever("agents_analysis")

    print("Filtering by category='frontend'")
    results = retriever.query_by_metadata(where={"category": "frontend"}, n_results=5)

    if results:
        print(f"✅ SUCCESS: Found {len(results)} frontend results\n")
        for i, r in enumerate(results[:5], 1):
            agent = r.get("metadata", {}).get("agent_name", "Unknown")
            category = r.get("metadata", {}).get("category", "Unknown")
            print(f"  {i}. {agent} (category: {category})")
        return True
    else:
        print("❌ FAILED: No results found")
        return False


def verify_recommendation_3():
    """Verify: Different semantic queries with calibrated thresholds."""
    print_header("VERIFICATION 3: Different Semantic Queries")

    retriever = CodeRetriever("agents_analysis")

    queries = [
        ("React hooks", 1.0),
        ("TypeScript types", 0.5),
        ("Frontend architecture", 1.0),
    ]

    all_passed = True

    for query, threshold in queries:
        results = retriever.query_semantic(
            query_text=query, n_results=3, distance_threshold=threshold
        )

        if results:
            agent = results[0].get("metadata", {}).get("agent_name", "Unknown")
            distance = results[0].get("distance", "N/A")
            print(f"✅ '{query}' (threshold={threshold}): Found {len(results)}")
            print(f"   Top: {agent} ({distance:.4f})\n")
        else:
            print(f"❌ '{query}' (threshold={threshold}): No results\n")
            all_passed = False

    return all_passed


def verify_recommendation_4():
    """Verify: Multi-collection search (workaround)."""
    print_header("VERIFICATION 4: Multi-Collection Search (Workaround)")

    collections = ["ghc_agents", "agents_analysis", "superclaude_agents", "vibe_agents"]

    print(f"Searching across {len(collections)} collections for 'Next.js patterns'\n")

    all_results = []

    for collection_name in collections:
        try:
            retriever = CodeRetriever(collection_name)
            results = retriever.query("Next.js patterns", n_results=2)

            for result in results:
                result["collection"] = collection_name
                all_results.append(result)

            if results:
                print(f"✅ {collection_name}: Found {len(results)} results")
            else:
                print(f"⚠️  {collection_name}: No results")
        except Exception as e:
            print(f"❌ {collection_name}: Error - {e}")

    if all_results:
        print(f"\n✅ SUCCESS: Found {len(all_results)} total results across collections\n")

        # Sort by distance and show top results
        all_results.sort(key=lambda r: r.get("distance", float("inf")))

        print("Top matches across all collections:")
        for i, r in enumerate(all_results[:5], 1):
            agent = r.get("metadata", {}).get("agent_name", "Unknown")
            collection = r.get("collection", "Unknown")
            distance = r.get("distance", "N/A")
            print(f"  {i}. [{collection}] {agent} ({distance:.4f})")

        return True
    else:
        print("❌ FAILED: No results found across any collection")
        return False


def main():
    """Run all verifications."""
    print("\n" + "=" * 80)
    print("  VERIFICATION: Query Recommendations Implementation")
    print("=" * 80)
    print("\nThis script verifies all 4 recommendations with optimal configurations.")

    try:
        results = []

        results.append(("Recommendation 1 (Distance Threshold)", verify_recommendation_1()))
        results.append(("Recommendation 2 (Metadata Filtering)", verify_recommendation_2()))
        results.append(("Recommendation 3 (Different Queries)", verify_recommendation_3()))
        results.append(("Recommendation 4 (Multi-Collection)", verify_recommendation_4()))

        # Summary
        print_header("VERIFICATION SUMMARY")

        all_passed = all(result[1] for result in results)

        for name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status}: {name}")

        print("\n" + "=" * 80)

        if all_passed:
            print("\n✨ ALL RECOMMENDATIONS VERIFIED AND WORKING!")
            print("\nRecommended Query Pattern:")
            print(
                """
    from src.retrieval import CodeRetriever

    retriever = CodeRetriever("agents_analysis")

    # Use optimal distance threshold
    results = retriever.query_semantic(
        query_text="React hooks",
        n_results=5,
        distance_threshold=1.0
    )

    # Or filter by metadata
    results = retriever.query_by_metadata(
        where={"category": "frontend"},
        n_results=5
    )
            """
            )
        else:
            print("\n⚠️ Some recommendations need adjustment")

        print("\n")
        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
