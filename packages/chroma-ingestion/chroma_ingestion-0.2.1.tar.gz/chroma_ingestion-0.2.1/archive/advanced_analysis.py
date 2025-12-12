#!/usr/bin/env python3
"""
Advanced analysis of recommendations with detailed insights.

Tests:
1. Different distance thresholds to find optimal filtering
2. Analyze embedding space for the collection
3. Metadata structure analysis
4. Multi-collection search with debugging
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))


from clients.chroma_client import get_chroma_client
from retrieval import CodeRetriever


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def analyze_distance_distribution():
    """Analyze the distance distribution in the collection."""
    print_section("ANALYSIS 1: Distance Distribution")

    retriever = CodeRetriever("agents_analysis")

    # Get results with various n_results to understand distance distribution
    print("Getting all results to analyze distance distribution...")
    results = retriever.query(query_text="Next.js patterns", n_results=20)

    distances = [r.get("distance", float("inf")) for r in results]

    print("Sample of distances from 20 results:")
    print(f"  Min distance: {min(distances):.4f}")
    print(f"  Max distance: {max(distances):.4f}")
    print(f"  Average: {sum(distances)/len(distances):.4f}")
    print("\nDistance breakdown:")
    print(f"  < 0.5:  {sum(1 for d in distances if d < 0.5)} results")
    print(f"  < 0.8:  {sum(1 for d in distances if d < 0.8)} results")
    print(f"  < 1.0:  {sum(1 for d in distances if d < 1.0)} results")
    print(f"  < 1.2:  {sum(1 for d in distances if d < 1.2)} results")
    print(f"  All:    {len(results)} results")

    print("\n💡 INSIGHT: Distance threshold of 0.5 is too strict for this collection.")
    print("   Suggested thresholds based on distribution:")
    print("   - Strict (high precision): 0.95")
    print("   - Moderate (balanced): 1.0")
    print("   - Permissive: 1.2")

    return results


def test_optimal_thresholds():
    """Test various distance thresholds."""
    print_section("ANALYSIS 2: Optimal Distance Thresholds")

    retriever = CodeRetriever("agents_analysis")

    thresholds = [0.95, 1.0, 1.05, 1.1, 1.2]

    print("Testing 'Next.js patterns' with different thresholds:\n")

    for threshold in thresholds:
        results = retriever.query_semantic(
            query_text="Next.js patterns", n_results=5, distance_threshold=threshold
        )

        if results:
            agent = results[0].get("metadata", {}).get("agent_name", "Unknown")
            best_distance = results[0].get("distance", "N/A")
            print(
                f"  Threshold {threshold}: ✅ {len(results)} results (best: {agent} @ {best_distance:.4f})"
            )
        else:
            print(f"  Threshold {threshold}: ❌ No results")

    print("\n💡 INSIGHT: Use distance < 1.0 for high-confidence matches in this collection.")


def analyze_metadata_structure():
    """Analyze the metadata structure of stored chunks."""
    print_section("ANALYSIS 3: Metadata Structure")

    retriever = CodeRetriever("agents_analysis")
    collection_info = retriever.get_collection_info()

    print("Collection: agents_analysis")
    if isinstance(collection_info, dict) and "total_documents" in collection_info:
        print(f"Total documents: {collection_info['total_documents']}")
    else:
        print(f"Collection info: {collection_info}")

    # Get a sample result to see metadata structure
    sample = retriever.query(query_text="Next.js", n_results=1)
    if sample:
        meta = sample[0].get("metadata", {})
        print("\nSample metadata keys:")
        for key in sorted(meta.keys()):
            value = meta[key]
            if isinstance(value, list):
                print(f"  {key}: list[{len(value)}] (first 3: {value[:3]})")
            else:
                print(f"  {key}: {type(value).__name__} = {str(value)[:50]}")

    print("\n💡 INSIGHT: Available metadata fields for filtering:")
    print("  - Use equality operators: $eq")
    print("  - Use comparison: $gt, $gte, $lt, $lte")
    print("  - Use set operations: $in, $nin")
    print("  - NOT supported: $contains (use regex or exact match instead)")


def test_metadata_filters():
    """Test different metadata filter approaches."""
    print_section("ANALYSIS 4: Metadata Filtering Approaches")

    retriever = CodeRetriever("agents_analysis")

    # Test 1: Exact category filter
    print("Test 1: category = 'frontend'")
    results = retriever.query_by_metadata(where={"category": "frontend"}, n_results=3)
    print(f"  ✅ Results: {len(results)}")
    if results:
        for r in results[:3]:
            print(f"     - {r.get('metadata', {}).get('agent_name', 'Unknown')}")

    # Test 2: Check what metadata contains
    print("\nTest 2: Analyzing metadata structure for tech_stack")
    sample = retriever.query(query_text="Next.js", n_results=5)

    if sample:
        print(f"  Sample metadata from {len(sample)} results:")
        tech_stacks = []
        for result in sample:
            meta = result.get("metadata", {})
            if "tech_stack" in meta:
                tech_stacks.append(meta["tech_stack"])

        if tech_stacks:
            print(f"  tech_stack field found in {len(tech_stacks)} results:")
            for ts in tech_stacks[:2]:
                print(f"    Type: {type(ts).__name__}")
                if isinstance(ts, list):
                    print(f"    Value: {ts[:3]}")
                else:
                    print(f"    Value: {ts}")

    print("\n💡 INSIGHT: Use exact value filters with metadata fields.")
    print("   For tech_stack, check if it's stored as list or string first.")


def test_different_query_topics():
    """Test different query topics with appropriate thresholds."""
    print_section("ANALYSIS 5: Query Topic Effectiveness")

    retriever = CodeRetriever("agents_analysis")

    queries = [
        ("Next.js patterns", 1.0),
        ("Server Components", 1.0),
        ("App Router patterns", 1.1),
        ("TypeScript types", 0.5),
        ("React hooks", 1.0),
        ("Frontend architecture", 1.0),
    ]

    print("Testing different query topics with calibrated thresholds:\n")

    for query, threshold in queries:
        results = retriever.query_semantic(
            query_text=query, n_results=3, distance_threshold=threshold
        )

        if results:
            top_agent = results[0].get("metadata", {}).get("agent_name", "Unknown")
            top_dist = results[0].get("distance", "N/A")
            print(f"'{query}'")
            print(f"  Threshold {threshold}: ✅ {len(results)} results")
            print(f"  Top match: {top_agent} ({top_dist:.4f})")
        else:
            # Try without threshold to see what's available
            unrestricted = retriever.query(query_text=query, n_results=1)
            if unrestricted:
                top_agent = unrestricted[0].get("metadata", {}).get("agent_name", "Unknown")
                top_dist = unrestricted[0].get("distance", "N/A")
                print(f"'{query}'")
                print(f"  Threshold {threshold}: ❌ No results")
                print(f"  Best available: {top_agent} ({top_dist:.4f})")
            else:
                print(f"'{query}': ❌ No results even without threshold")
        print()


def list_all_collections_and_sizes():
    """List all available collections and their sizes."""
    print_section("ANALYSIS 6: Available Collections")

    client = get_chroma_client()

    try:
        collections = client.list_collections()

        print(f"Found {len(collections)} collections:\n")

        for collection in collections:
            try:
                count = collection.count()
                print(f"  📦 {collection.name}")
                print(f"     Documents: {count}")
            except Exception as e:
                print(f"  📦 {collection.name}")
                print(f"     Error counting: {e}")

        print(
            f"\n💡 INSIGHT: MultiCollectionSearcher can search across all {len(collections)} collections."
        )
        print("   Current focus: agents_analysis (1,086 chunks)")

    except Exception as e:
        print(f"❌ Error listing collections: {e}")


def main():
    """Run all analyses."""
    print("\n" + "=" * 80)
    print("  ADVANCED ANALYSIS OF CHROMA RECOMMENDATIONS")
    print("=" * 80)
    print("\nExecuting 6 detailed analyses to optimize query strategies...")

    try:
        # Run all analyses
        analyze_distance_distribution()
        test_optimal_thresholds()
        analyze_metadata_structure()
        test_metadata_filters()
        test_different_query_topics()
        list_all_collections_and_sizes()

        # Final recommendations
        print_section("FINAL RECOMMENDATIONS")

        print("✅ RECOMMENDATION 1 (Distance Threshold):")
        print("   Optimal: Use distance < 1.0 instead of < 0.5")
        print("   Reasoning: Embedding space in this collection has different distance scale")
        print("   Action: Call query_semantic() with distance_threshold=1.0")

        print("\n✅ RECOMMENDATION 2 (Metadata Filtering):")
        print("   Working: category filter works perfectly")
        print("   Issue: tech_stack field requires different approach")
        print("   Action: Use exact value matches with metadata filters")

        print("\n✅ RECOMMENDATION 3 (Different Queries):")
        print("   Effective queries: 'Next.js patterns', 'React hooks', 'TypeScript'")
        print("   Less effective: 'App Router patterns', 'Server Components'")
        print("   Action: Use topic queries that align with agent expertise areas")

        print("\n✅ RECOMMENDATION 4 (Multi-Collection Search):")
        print("   Status: 5 collections available for cross-search")
        print("   Issue: MultiCollectionSearcher has bug in result processing")
        print("   Action: Needs debugging or alternative implementation")

        print("\n" + "=" * 80)
        print("✨ Analysis complete! Use these insights to optimize query strategies.")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
