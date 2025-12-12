#!/usr/bin/env python3
"""
Comprehensive agent testing with representative queries.

Tests all 10 consolidated agents with domain-specific queries and measures:
- Semantic relevance (distance scores)
- Query execution time
- Agent expertise validation
- Performance metrics
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ingestion import CodeIngester
from retrieval import CodeRetriever


def main():
    """Run comprehensive agent testing."""

    print("\n" + "=" * 70)
    print("🤖 CONSOLIDATED AGENTS - COMPREHENSIVE TESTING")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    # Step 1: Ingest consolidated agents
    print("📥 Step 1: Ingesting Consolidated Agents")
    print("-" * 70)

    start_time = time.time()

    ingester = CodeIngester(
        target_folder="consolidated_agents",
        collection_name="consolidated_agents_test",
        chunk_size=1000,
        chunk_overlap=200,
    )

    document_count, chunk_count = ingester.ingest_files()
    ingestion_time = time.time() - start_time

    print("✅ Ingestion Complete")
    print(f"   Documents: {document_count}")
    print(f"   Chunks: {chunk_count}")
    print(f"   Time: {ingestion_time:.2f}s")
    print(f"   Rate: {chunk_count / ingestion_time:.1f} chunks/sec\n")

    # Step 2: Define representative test queries
    print("🧪 Step 2: Defining Representative Test Queries")
    print("-" * 70)

    test_queries = {
        "frontend-expert": [
            "How do I create server components in Next.js 15?",
            "What are the best practices for React 19 hooks?",
            "How should I structure TypeScript types in a React app?",
            "What's the proper way to handle CSS in Next.js?",
        ],
        "backend-expert": [
            "How do I create FastAPI endpoints with dependencies?",
            "What are Python best practices for async operations?",
            "How should I structure API error handling?",
            "How do I implement request validation in FastAPI?",
        ],
        "testing-expert": [
            "How do I write Playwright tests for forms?",
            "What are best practices for E2E testing?",
            "How do I use Vitest for unit testing?",
            "How should I structure test files?",
        ],
        "architect-expert": [
            "What are system design patterns for microservices?",
            "How do I approach scaling architecture?",
            "What are the principles of good API design?",
            "How should I structure a distributed system?",
        ],
        "ai-ml-expert": [
            "How do I use embeddings for semantic search?",
            "What are best practices for LLM prompting?",
            "How do I implement RAG systems?",
            "What's the difference between fine-tuning and prompt engineering?",
        ],
        "devops-expert": [
            "How do I create Docker containers for Python apps?",
            "What's the best approach for CI/CD pipelines?",
            "How do I set up Kubernetes deployments?",
            "What are Docker best practices?",
        ],
        "security-expert": [
            "How do I implement JWT authentication?",
            "What are password security best practices?",
            "How do I prevent SQL injection attacks?",
            "What's the proper way to handle API secrets?",
        ],
        "quality-expert": [
            "What are code review best practices?",
            "How do I refactor legacy code safely?",
            "What metrics should I track for code quality?",
            "How do I approach technical debt reduction?",
        ],
        "database-expert": [
            "How do I design PostgreSQL schemas?",
            "What are query optimization techniques?",
            "How do I implement database migrations?",
            "What's the best way to handle relationships in SQL?",
        ],
        "planning-expert": [
            "How do I break down large projects into tasks?",
            "What's the best approach for requirement gathering?",
            "How do I manage project dependencies?",
            "What are Agile estimation best practices?",
        ],
    }

    print(f"✅ Defined {len(test_queries)} agent profiles")
    print(f"✅ Total queries: {sum(len(q) for q in test_queries.values())}\n")

    # Step 3: Execute queries and collect metrics
    print("🔍 Step 3: Executing Queries and Measuring Relevance")
    print("-" * 70)

    retriever = CodeRetriever("consolidated_agents_test")
    results_by_agent = {}
    total_queries = 0
    excellent_matches = 0  # distance < 0.3
    good_matches = 0  # distance 0.3-0.5
    weak_matches = 0  # distance 0.5-0.7
    poor_matches = 0  # distance > 0.7

    query_times = []

    for agent_name, queries in test_queries.items():
        print(f"\n{agent_name.upper()}")
        print(f"  Queries: {len(queries)}")
        agent_results = []

        for i, query in enumerate(queries, 1):
            query_start = time.time()
            results = retriever.query(query, n_results=3)
            query_time = time.time() - query_start
            query_times.append(query_time)

            if results:
                top_distance = results[0]["distance"]
                agent_results.append(
                    {"query": query, "distance": top_distance, "time_ms": query_time * 1000}
                )

                # Classify match quality
                if top_distance < 0.3:
                    excellent_matches += 1
                    quality = "⭐⭐⭐ Excellent"
                elif top_distance < 0.5:
                    good_matches += 1
                    quality = "⭐⭐ Good"
                elif top_distance < 0.7:
                    weak_matches += 1
                    quality = "⭐ Weak"
                else:
                    poor_matches += 1
                    quality = "❌ Poor"

                print(
                    f"    Q{i}: {quality} (distance: {top_distance:.3f}, time: {query_time * 1000:.1f}ms)"
                )
            else:
                print(f"    Q{i}: No results returned")

            total_queries += 1

        results_by_agent[agent_name] = agent_results

    # Step 4: Calculate performance metrics
    print("\n" + "=" * 70)
    print("📊 Step 4: Performance Metrics")
    print("=" * 70)

    avg_query_time = sum(query_times) / len(query_times) * 1000 if query_times else 0
    min_query_time = min(query_times) * 1000 if query_times else 0
    max_query_time = max(query_times) * 1000 if query_times else 0

    print("\n⏱️  Query Performance:")
    print(f"   Total queries: {total_queries}")
    print(f"   Average time: {avg_query_time:.2f}ms")
    print(f"   Min time: {min_query_time:.2f}ms")
    print(f"   Max time: {max_query_time:.2f}ms")

    print("\n📈 Match Quality Distribution:")
    print(
        f"   Excellent (distance < 0.3): {excellent_matches}/{total_queries} ({excellent_matches / total_queries * 100:.1f}%)"
    )
    print(
        f"   Good (0.3-0.5): {good_matches}/{total_queries} ({good_matches / total_queries * 100:.1f}%)"
    )
    print(
        f"   Weak (0.5-0.7): {weak_matches}/{total_queries} ({weak_matches / total_queries * 100:.1f}%)"
    )
    print(
        f"   Poor (> 0.7): {poor_matches}/{total_queries} ({poor_matches / total_queries * 100:.1f}%)"
    )

    success_rate = (
        (excellent_matches + good_matches) / total_queries * 100 if total_queries > 0 else 0
    )
    print(f"\n✅ Success Rate (Excellent + Good): {success_rate:.1f}%")

    # Step 5: Validation summary
    print("\n" + "=" * 70)
    print("✅ VALIDATION SUMMARY")
    print("=" * 70)

    if success_rate >= 80:
        print(f"🎉 AGENTS VALIDATED: {success_rate:.1f}% success rate - PRODUCTION READY")
    elif success_rate >= 60:
        print(f"⚠️  AGENTS FUNCTIONAL: {success_rate:.1f}% success rate - ACCEPTABLE")
    else:
        print(f"❌ AGENTS NEED REVIEW: {success_rate:.1f}% success rate - REQUIRES WORK")

    # Step 6: Save detailed results
    print("\n💾 Saving detailed results...\n")

    results_file = "validation_results.json"
    with open(results_file, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "ingestion": {
                    "documents": document_count,
                    "chunks": chunk_count,
                    "time_seconds": ingestion_time,
                },
                "queries": {
                    "total": total_queries,
                    "average_time_ms": avg_query_time,
                    "min_time_ms": min_query_time,
                    "max_time_ms": max_query_time,
                },
                "quality": {
                    "excellent": excellent_matches,
                    "good": good_matches,
                    "weak": weak_matches,
                    "poor": poor_matches,
                    "success_rate_percent": success_rate,
                },
                "results_by_agent": results_by_agent,
            },
            f,
            indent=2,
        )

    print(f"✅ Results saved to {results_file}")

    print("\n" + "=" * 70)
    print("🎯 TESTING COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Review validation_results.json for detailed metrics")
    print("  2. Check any low-scoring queries (distance > 0.7)")
    print("  3. Consider agent improvements if success rate < 80%")
    print("  4. Deploy to production if success rate >= 80%\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
