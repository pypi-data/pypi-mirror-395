#!/usr/bin/env python3
"""
Test Collection Queries - Execute all 4 practical examples from USAGE_GUIDE
Tests the original_agents collection with proven query patterns
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from chroma_ingestion.retrieval import CodeRetriever


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def test_frontend_query():
    """Test Example 1: Frontend Question"""
    print_header("TEST 1: Frontend Question ✅")

    query = "React hooks patterns"
    print(f"📝 Query: {query}")
    print("❓ Expected: frontend-architect.prompt.md")
    print("⚠️  Note: May get performance-engineer.prompt.md (distance 0.78)\n")

    retriever = CodeRetriever("original_agents")
    results = retriever.query(query, n_results=3)

    results_data = {"query": query, "expected": "frontend-architect.prompt.md", "results": []}

    for i, result in enumerate(results, 1):
        distance = result["distance"]
        source = result["metadata"]["filename"]
        rating = (
            "🟢 Great"
            if distance < 0.5
            else "🟡 Good"
            if distance < 0.7
            else "🟠 Okay"
            if distance < 0.9
            else "🔴 Poor"
        )

        print(f"Result {i}: {source}")
        print(f"  Distance: {distance:.4f} ({rating})")
        print(f"  Content preview: {result['document'][:100]}...")
        print()

        results_data["results"].append(
            {"rank": i, "filename": source, "distance": distance, "rating": rating}
        )

    return results_data


def test_devops_query():
    """Test Example 2: DevOps Question"""
    print_header("TEST 2: DevOps Question ✅")

    query = "CI/CD pipeline"
    print(f"📝 Query: {query}")
    print("❓ Expected: devops-architect.prompt.md")
    print("📊 Likely Distance: 0.65-0.75\n")

    retriever = CodeRetriever("original_agents")
    results = retriever.query(query, n_results=3)

    results_data = {"query": query, "expected": "devops-architect.prompt.md", "results": []}

    for i, result in enumerate(results, 1):
        distance = result["distance"]
        source = result["metadata"]["filename"]
        rating = (
            "🟢 Great"
            if distance < 0.5
            else "🟡 Good"
            if distance < 0.7
            else "🟠 Okay"
            if distance < 0.9
            else "🔴 Poor"
        )

        print(f"Result {i}: {source}")
        print(f"  Distance: {distance:.4f} ({rating})")
        print(f"  Content preview: {result['document'][:100]}...")
        print()

        results_data["results"].append(
            {"rank": i, "filename": source, "distance": distance, "rating": rating}
        )

    return results_data


def test_missing_specialist_query():
    """Test Example 3: Missing Specialist Query"""
    print_header("TEST 3: Missing Specialist Query ❌")

    query = "database optimization strategies"
    print(f"📝 Query: {query}")
    print("❓ Expected: database-architect.md (NOT IN COLLECTION)")
    print("🔴 Will get: backend-architect.prompt.md (distance 1.0+)\n")

    retriever = CodeRetriever("original_agents")
    results = retriever.query(query, n_results=3)

    results_data = {
        "query": query,
        "expected": "database-architect.md (NOT IN COLLECTION)",
        "actual_available": "backend-architect.prompt.md (fallback)",
        "results": [],
    }

    for i, result in enumerate(results, 1):
        distance = result["distance"]
        source = result["metadata"]["filename"]
        rating = (
            "🟢 Great"
            if distance < 0.5
            else "🟡 Good"
            if distance < 0.7
            else "🟠 Okay"
            if distance < 0.9
            else "🔴 Poor"
        )

        print(f"Result {i}: {source}")
        print(f"  Distance: {distance:.4f} ({rating})")
        print(f"  Content preview: {result['document'][:100]}...")
        print()

        results_data["results"].append(
            {"rank": i, "filename": source, "distance": distance, "rating": rating}
        )

    return results_data


def test_multiconceptpoor_query():
    """Test Example 4: Multi-Concept Query (Usually Fails)"""
    print_header("TEST 4: Multi-Concept Query (Usually Fails) ❌")

    query = "How do I design a secure backend system with proper error handling and monitoring?"
    print(f"📝 Query (Multi-concept): {query}")
    print("⚠️  Expected Distance: > 0.9 (Poor match due to multiple concepts)\n")
    print("💡 Better Approach:")
    print("   1. 'backend architecture' (for design)")
    print("   2. 'security patterns' (for security)")
    print("   3. 'monitoring and observability' (for monitoring)\n")

    retriever = CodeRetriever("original_agents")
    results = retriever.query(query, n_results=3)

    results_data = {
        "query": query,
        "note": "Multi-concept queries perform poorly",
        "better_approach": [
            "backend architecture",
            "security patterns",
            "monitoring and observability",
        ],
        "results": [],
    }

    for i, result in enumerate(results, 1):
        distance = result["distance"]
        source = result["metadata"]["filename"]
        rating = (
            "🟢 Great"
            if distance < 0.5
            else "🟡 Good"
            if distance < 0.7
            else "🟠 Okay"
            if distance < 0.9
            else "🔴 Poor"
        )

        print(f"Result {i}: {source}")
        print(f"  Distance: {distance:.4f} ({rating})")
        print(f"  Content preview: {result['document'][:100]}...")
        print()

        results_data["results"].append(
            {"rank": i, "filename": source, "distance": distance, "rating": rating}
        )

    return results_data


def verify_distance_thresholds():
    """Verify distance threshold calibration"""
    print_header("VERIFICATION: Distance Threshold Calibration")

    print("Testing calibrated thresholds from optimizations phase:\n")

    test_queries = [
        ("JWT authentication", "Good single-concept query"),
        ("Docker containers", "Good single-concept query"),
        ("circuit breaker pattern", "Good single-concept query"),
        ("backend architecture system design", "Original USAGE_GUIDE example"),
    ]

    retriever = CodeRetriever("original_agents")
    threshold_results = []

    for query, description in test_queries:
        results = retriever.query(query, n_results=1)
        if results:
            distance = results[0]["distance"]
            source = results[0]["metadata"]["filename"]

            if distance < 0.5:
                threshold = "🟢 Great (< 0.5)"
            elif distance < 0.7:
                threshold = "🟡 Good (0.5-0.7)"
            elif distance < 0.9:
                threshold = "🟠 Okay (0.7-0.9)"
            else:
                threshold = "🔴 Poor (> 0.9)"

            print(f"✓ '{query}'")
            print(f"  Result: {source} ({distance:.4f}) {threshold}")
            print(f"  Note: {description}\n")

            threshold_results.append(
                {
                    "query": query,
                    "description": description,
                    "result_filename": source,
                    "distance": distance,
                    "threshold": threshold,
                }
            )

    return threshold_results


def main():
    """Execute all tests and generate report"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  CHROMA COLLECTION TASK EXECUTION - Test all 4 Query Patterns".center(78) + "║")
    print(
        "║"
        + f"  Collection: original_agents | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(
            78
        )
        + "║"
    )
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    all_results = {
        "execution_date": datetime.now().isoformat(),
        "collection": "original_agents",
        "tests": [],
        "threshold_verification": [],
    }

    try:
        # Execute all 4 tests
        print("\n📋 EXECUTING TEST SUITE\n")

        test1 = test_frontend_query()
        all_results["tests"].append(
            {"test_number": 1, "name": "Frontend Question", "status": "✅ Complete", **test1}
        )

        test2 = test_devops_query()
        all_results["tests"].append(
            {"test_number": 2, "name": "DevOps Question", "status": "✅ Complete", **test2}
        )

        test3 = test_missing_specialist_query()
        all_results["tests"].append(
            {
                "test_number": 3,
                "name": "Missing Specialist Query",
                "status": "✅ Complete (Expected Failure)",
                **test3,
            }
        )

        test4 = test_multiconceptpoor_query()
        all_results["tests"].append(
            {
                "test_number": 4,
                "name": "Multi-Concept Query",
                "status": "✅ Complete (Expected Failure)",
                **test4,
            }
        )

        # Verify thresholds
        thresholds = verify_distance_thresholds()
        all_results["threshold_verification"] = thresholds

        # Print summary
        print_header("EXECUTION SUMMARY")
        print("✅ All 4 tests completed successfully\n")
        print("📊 Results Summary:")
        print("   - Test 1 (Frontend): Complete")
        print("   - Test 2 (DevOps): Complete")
        print("   - Test 3 (Missing Specialist): Complete (Expected pattern)")
        print("   - Test 4 (Multi-Concept): Complete (Expected poor results)")
        print(f"   - Threshold Verification: {len(thresholds)} calibration queries tested\n")

        # Save results to JSON
        results_file = Path(__file__).parent / "test_collection_results.json"
        with open(results_file, "w") as f:
            json.dump(all_results, f, indent=2)

        print(f"💾 Results saved to: {results_file}\n")

        return True

    except Exception as e:
        print(f"\n❌ Error during test execution: {e}\n")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
