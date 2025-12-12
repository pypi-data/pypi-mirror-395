#!/usr/bin/env python3
"""
Extended Test Collection Queries - Phase 1.2 Comprehensive Test Suite
Tests the original_agents collection with 12 comprehensive query patterns
Tests all 6 agent types with edge cases, multi-concept, and ambiguous queries
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from chroma_ingestion.retrieval import CodeRetriever


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def test_query(test_num, name, query, expected_agent, expected_distance_range, query_type):
    """
    Generic test runner for any query

    Args:
        test_num: Test number (1-12)
        name: Test name
        query: Query text
        expected_agent: Expected agent filename
        expected_distance_range: Tuple (min, max) expected distance
        query_type: Classification (multi-concept, ambiguous, etc.)

    Returns:
        Dictionary with test results
    """
    print(f"\nTEST {test_num}: {name}")
    print(f"  Query Type: {query_type}")
    print(f'  Query: "{query}"')
    print(f"  Expected Agent: {expected_agent}")
    print(
        f"  Expected Distance: {expected_distance_range[0]:.1f}-{expected_distance_range[1]:.1f}\n"
    )

    retriever = CodeRetriever("original_agents")
    results = retriever.query(query, n_results=3)

    results_data = {
        "test_number": test_num,
        "name": name,
        "query": query,
        "query_type": query_type,
        "expected_agent": expected_agent,
        "expected_distance_range": {
            "min": expected_distance_range[0],
            "max": expected_distance_range[1],
        },
        "results": [],
        "pass": False,
    }

    for i, result in enumerate(results, 1):
        distance = result["distance"]
        source = result["metadata"]["filename"]

        # Rate based on NEW thresholds (< 0.8 excellent, 0.8-1.0 good, 1.0-1.2 okay, > 1.2 poor)
        rating = (
            "🟢 Excellent"
            if distance < 0.8
            else "🟡 Good"
            if distance < 1.0
            else "🟠 Okay"
            if distance < 1.2
            else "🔴 Poor"
        )

        print(f"  Result {i}: {source}")
        print(f"    Distance: {distance:.4f} {rating}")
        print(f"    Preview: {result['document'][:80]}...\n")

        # Check if this is the expected agent
        if i == 1 and source == expected_agent:
            within_range = expected_distance_range[0] <= distance <= expected_distance_range[1]
            if within_range:
                results_data["pass"] = True
                print("  ✅ PASS: Correct agent found with distance in expected range!\n")
            else:
                print("  ⚠️  PARTIAL: Correct agent but distance slightly outside expected range\n")

        results_data["results"].append(
            {
                "rank": i,
                "filename": source,
                "distance": distance,
                "rating": rating,
                "is_expected": source == expected_agent,
            }
        )

    return results_data


def main():
    """Execute all 12 extended tests and generate comprehensive report"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  PHASE 1.2: EXTENDED TEST SUITE - 12 Comprehensive Tests".center(78) + "║")
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
        "total_tests": 12,
        "tests": [],
        "statistics": {},
    }

    try:
        print("\n📋 EXECUTING EXTENDED TEST SUITE (12 Tests)\n")

        # Test 1: Frontend Architecture - Multi-concept
        test1 = test_query(
            1,
            "Frontend Architecture - React Hooks",
            "How do I use React hooks and compose them effectively?",
            "frontend-architect.prompt.md",
            (1.0, 1.3),
            "multi-concept",
        )
        all_results["tests"].append(test1)

        # Test 2: Frontend Edge Case - Ambiguous
        test2 = test_query(
            2,
            "Frontend Edge Case - State Management",
            "state management",
            "frontend-architect.prompt.md",
            (1.1, 1.4),
            "ambiguous",
        )
        all_results["tests"].append(test2)

        # Test 3: Backend Architecture - Multi-concept
        test3 = test_query(
            3,
            "Backend Architecture - Secure System Design",
            "How do I design a secure backend system with proper error handling and monitoring?",
            "backend-architect.prompt.md",
            (0.7, 1.0),
            "multi-concept",
        )
        all_results["tests"].append(test3)

        # Test 4: Backend Edge Case - Simple
        test4 = test_query(
            4,
            "Backend Edge Case - API Design",
            "API design",
            "backend-architect.prompt.md",
            (0.9, 1.3),
            "simple",
        )
        all_results["tests"].append(test4)

        # Test 5: DevOps/Infrastructure - Multi-concept
        test5 = test_query(
            5,
            "DevOps Infrastructure - CI/CD Pipeline",
            "CI/CD pipeline setup and best practices",
            "devops-architect.prompt.md",
            (1.0, 1.3),
            "multi-concept",
        )
        all_results["tests"].append(test5)

        # Test 6: DevOps Edge Case - Technology-specific
        test6 = test_query(
            6,
            "DevOps Edge Case - Docker & Kubernetes",
            "Docker containers and Kubernetes orchestration",
            "devops-architect.prompt.md",
            (1.0, 1.4),
            "technology-specific",
        )
        all_results["tests"].append(test6)

        # Test 7: Security Engineering - Multi-concept
        test7 = test_query(
            7,
            "Security Engineering - Authentication & Authorization",
            "How do I implement authentication and authorization securely?",
            "security-engineer.prompt.md",
            (0.8, 1.2),
            "multi-concept",
        )
        all_results["tests"].append(test7)

        # Test 8: Security Edge Case - Threat Modeling
        test8 = test_query(
            8,
            "Security Edge Case - Threat Assessment",
            "threat assessment vulnerability testing",
            "security-engineer.prompt.md",
            (1.1, 1.5),
            "technical",
        )
        all_results["tests"].append(test8)

        # Test 9: Performance Engineering - Multi-concept
        test9 = test_query(
            9,
            "Performance Engineering - Database Optimization",
            "database optimization and query performance tuning",
            "performance-engineer.prompt.md",
            (0.9, 1.3),
            "multi-concept",
        )
        all_results["tests"].append(test9)

        # Test 10: Quality Engineering - Multi-concept
        test10 = test_query(
            10,
            "Quality Engineering - Testing Strategies",
            "testing strategies test automation and quality assurance",
            "quality-engineer.prompt.md",
            (0.9, 1.3),
            "multi-concept",
        )
        all_results["tests"].append(test10)

        # Test 11: Architecture Pattern - Pattern-specific
        test11 = test_query(
            11,
            "Architecture Pattern - Circuit Breaker",
            "circuit breaker pattern microservices architecture",
            "backend-architect.prompt.md",
            (1.0, 1.4),
            "pattern-specific",
        )
        all_results["tests"].append(test11)

        # Test 12: Cross-cutting Concern - Multi-domain
        test12 = test_query(
            12,
            "Cross-cutting Concern - Observability",
            "How do I implement observability, logging, and monitoring across my system?",
            "devops-architect.prompt.md",
            (1.0, 1.4),
            "cross-cutting",
        )
        all_results["tests"].append(test12)

        # Calculate statistics
        print_header("STATISTICAL ANALYSIS")

        distances = []
        passed_tests = 0

        for test in all_results["tests"]:
            if test["results"]:
                distance = test["results"][0]["distance"]  # First result distance
                distances.append(distance)
                if test["pass"]:
                    passed_tests += 1

        # Calculate metrics
        if distances:
            distances_sorted = sorted(distances)
            mean_distance = mean(distances)
            std_distance = stdev(distances) if len(distances) > 1 else 0

            all_results["statistics"] = {
                "total_tests": len(all_results["tests"]),
                "passed_tests": passed_tests,
                "failed_tests": len(all_results["tests"]) - passed_tests,
                "pass_rate_percent": (passed_tests / len(all_results["tests"])) * 100,
                "distances": {
                    "mean": round(mean_distance, 4),
                    "std_dev": round(std_distance, 4),
                    "min": round(distances_sorted[0], 4),
                    "max": round(distances_sorted[-1], 4),
                    "percentile_25": round(distances_sorted[len(distances_sorted) // 4], 4),
                    "percentile_50": round(distances_sorted[len(distances_sorted) // 2], 4),
                    "percentile_75": round(distances_sorted[(3 * len(distances_sorted)) // 4], 4),
                },
                "confidence_level": (
                    "95%+" if passed_tests >= 11 else "85-95%" if passed_tests >= 10 else "< 85%"
                ),
            }

            stats = all_results["statistics"]
            print("📊 Test Results Summary:")
            print(
                f"   Tests Passed: {passed_tests}/{len(all_results['tests'])} ({stats['pass_rate_percent']:.1f}%)"
            )
            print(f"   Confidence Level: {stats['confidence_level']}")
            print("\n📈 Distance Statistics (New Thresholds):")
            print(f"   Mean Distance: {stats['distances']['mean']:.4f}")
            print(f"   Std Deviation: {stats['distances']['std_dev']:.4f}")
            print(f"   Min Distance: {stats['distances']['min']:.4f}")
            print(f"   Max Distance: {stats['distances']['max']:.4f}")
            print(f"   25th Percentile: {stats['distances']['percentile_25']:.4f}")
            print(f"   50th Percentile (Median): {stats['distances']['percentile_50']:.4f}")
            print(f"   75th Percentile: {stats['distances']['percentile_75']:.4f}")

        # Print summary
        print_header("EXECUTION SUMMARY")
        print("✅ All 12 tests completed successfully\n")
        print("📋 Test Breakdown:")
        for i, test in enumerate(all_results["tests"], 1):
            status = "✅ PASS" if test["pass"] else "⏳ REVIEW"
            print(f"   Test {i:2d}: {test['name']:<45s} {status}")

        print(
            "\n💡 Coverage: 6 agent types, 12 scenarios (multi-concept, ambiguous, cross-cutting)"
        )
        print(
            f"📊 Quality: {all_results['statistics'].get('confidence_level', 'N/A')} confidence\n"
        )

        # Save results to JSON
        results_file = Path(__file__).parent / "test_collection_results_extended.json"
        with open(results_file, "w") as f:
            json.dump(all_results, f, indent=2)

        print(f"💾 Results saved to: {results_file}\n")

        # Return success if pass rate > 85%
        success = all_results["statistics"].get("pass_rate_percent", 0) > 85
        return success

    except Exception as e:
        print(f"\n❌ Error during test execution: {e}\n")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
