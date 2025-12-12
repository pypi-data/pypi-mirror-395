#!/usr/bin/env python3
"""
Re-ingest original agents from vibe-tools with full technical depth.

This script indexes the original agent files from vibe-tools/ghc_tools/agents/
instead of the consolidated versions. These contain the full technical knowledge
and will produce much better semantic search results.

Original agents: 23 agents, ~256KB total
- Each 8-26 KB with detailed technical guidance
- Real examples, patterns, and implementation details
- Not just role descriptors but actual knowledge bases
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
    """Re-ingest original agents and test with comprehensive queries."""

    print("\n" + "=" * 80)
    print("🔄 RE-INGESTING ORIGINAL AGENTS FROM VIBE-TOOLS")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    # Step 1: Ingest original agents
    print("📥 Step 1: Ingesting Original Agents from vibe-tools")
    print("-" * 80)

    original_agents_path = Path("/home/ob/Development/Tools/vibe-tools/ghc_tools/agents")

    if not original_agents_path.exists():
        print(f"❌ Error: Path not found: {original_agents_path}")
        sys.exit(1)

    # Count files first
    agent_files = (
        list(original_agents_path.glob("*.md"))
        + list(original_agents_path.glob("*.prompt.md"))
        + list(original_agents_path.glob("*.agent.md"))
    )
    print(f"📂 Found {len(agent_files)} agent files")

    # Show sample file sizes
    print("📊 Sample agent file sizes:")
    for f in sorted(agent_files)[:5]:
        size_kb = f.stat().st_size / 1024
        print(f"   {f.name}: {size_kb:.1f} KB")
    print(f"   ... and {len(agent_files) - 5} more\n")

    start_time = time.time()

    # Use fresh collection for original agents
    ingester = CodeIngester(
        target_folder=str(original_agents_path),
        collection_name="original_agents",
        chunk_size=1000,
        chunk_overlap=200,
    )

    document_count, chunk_count = ingester.ingest_files()
    ingestion_time = time.time() - start_time

    print("✅ Ingestion Complete")
    print(f"   Documents: {document_count}")
    print(f"   Chunks: {chunk_count}")
    print(f"   Time: {ingestion_time:.2f}s")
    print(f"   Rate: {chunk_count/ingestion_time:.1f} chunks/sec\n")

    # Step 2: Define test queries
    print("🧪 Step 2: Defining Representative Test Queries")
    print("-" * 80)

    test_queries = {
        "Backend Architecture": [
            "How do I design a reliable backend system with fault tolerance?",
            "What are best practices for API design and error handling?",
            "How should I implement database optimization and scaling?",
            "What's the proper way to handle security in backend systems?",
        ],
        "Frontend Architecture": [
            "How do I structure a modern React application?",
            "What are performance optimization patterns for web apps?",
            "How should I handle state management in complex UIs?",
            "What are accessibility best practices?",
        ],
        "DevOps & Architecture": [
            "How do I design scalable infrastructure?",
            "What are CI/CD pipeline best practices?",
            "How should I approach containerization and orchestration?",
            "What's the proper way to handle monitoring and observability?",
        ],
        "Python Development": [
            "What are Python best practices for backend development?",
            "How should I structure Python projects?",
            "What are async programming patterns in Python?",
            "How do I write efficient, maintainable Python code?",
        ],
        "Security": [
            "How do I implement secure authentication and authorization?",
            "What are OWASP best practices?",
            "How should I handle encryption and secrets management?",
            "What are security testing approaches?",
        ],
        "Testing & Quality": [
            "How do I write effective unit tests?",
            "What are E2E testing best practices?",
            "How should I approach test automation?",
            "What are quality assurance strategies?",
        ],
        "Database & Data": [
            "How do I design database schemas?",
            "What are query optimization techniques?",
            "How should I approach data modeling?",
            "What are ACID compliance patterns?",
        ],
        "Performance": [
            "How do I profile and optimize performance?",
            "What are caching strategies?",
            "How should I approach load testing?",
            "What are latency optimization techniques?",
        ],
    }

    total_queries = sum(len(q) for q in test_queries.values())
    print(f"✅ Defined {len(test_queries)} query categories")
    print(f"✅ Total queries: {total_queries}\n")

    # Step 3: Execute queries
    print("🔍 Step 3: Executing Queries and Measuring Relevance")
    print("-" * 80)

    retriever = CodeRetriever("original_agents")

    results_by_category = {}
    all_results = []

    for category, queries in test_queries.items():
        print(f"\n{category.upper()}")
        results_by_category[category] = {"queries": [], "stats": {}}

        for i, query in enumerate(queries, 1):
            start_q = time.time()
            results = retriever.query(query, n_results=3)
            query_time = (time.time() - start_q) * 1000  # ms

            if results:
                best_distance = results[0]["distance"]
                best_source = results[0]["metadata"].get("filename", "unknown")

                # Classify quality
                if best_distance < 0.3:
                    quality = "✅ Excellent"
                elif best_distance < 0.5:
                    quality = "✅ Good"
                elif best_distance < 0.7:
                    quality = "⚠️  Weak"
                else:
                    quality = "❌ Poor"

                print(
                    f"  Q{i}: {quality} (distance: {best_distance:.3f}, time: {query_time:.1f}ms)"
                )
                print(f"       → {best_source}")

                results_by_category[category]["queries"].append(
                    {
                        "query": query,
                        "distance": best_distance,
                        "time_ms": query_time,
                        "quality": quality,
                        "source": best_source,
                        "results": results,
                    }
                )

                all_results.append(
                    {
                        "category": category,
                        "query": query,
                        "distance": best_distance,
                        "time_ms": query_time,
                    }
                )
            else:
                print(f"  Q{i}: ❌ No results")
                results_by_category[category]["queries"].append(
                    {
                        "query": query,
                        "distance": None,
                        "time_ms": query_time,
                        "quality": "❌ Error",
                        "source": "N/A",
                    }
                )

    # Step 4: Calculate metrics
    print("\n" + "=" * 80)
    print("📊 Step 4: Performance Metrics")
    print("=" * 80)

    if all_results:
        distances = [r["distance"] for r in all_results if r["distance"] is not None]
        times = [r["time_ms"] for r in all_results]

        excellent = len([d for d in distances if d < 0.3])
        good = len([d for d in distances if 0.3 <= d < 0.5])
        weak = len([d for d in distances if 0.5 <= d < 0.7])
        poor = len([d for d in distances if d >= 0.7])

        print("\n⏱️  Query Performance:")
        print(f"   Total queries: {len(all_results)}")
        print(f"   Average time: {sum(times)/len(times):.2f}ms")
        print(f"   Min time: {min(times):.2f}ms")
        print(f"   Max time: {max(times):.2f}ms")

        print("\n📈 Match Quality Distribution:")
        print(
            f"   Excellent (distance < 0.3): {excellent}/{len(distances)} ({100*excellent/len(distances):.1f}%)"
        )
        print(f"   Good (0.3-0.5): {good}/{len(distances)} ({100*good/len(distances):.1f}%)")
        print(f"   Weak (0.5-0.7): {weak}/{len(distances)} ({100*weak/len(distances):.1f}%)")
        print(f"   Poor (> 0.7): {poor}/{len(distances)} ({100*poor/len(distances):.1f}%)")

        success_rate = (excellent + good) / len(distances) * 100
        print(f"\n✅ Success Rate (Excellent + Good): {success_rate:.1f}%")

        # Save results to JSON
        output_file = "reingest_results.json"
        with open(output_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "ingestion": {
                        "source": "vibe-tools/ghc_tools/agents",
                        "documents": document_count,
                        "chunks": chunk_count,
                        "time_seconds": ingestion_time,
                        "rate_chunks_per_sec": chunk_count / ingestion_time,
                    },
                    "testing": {
                        "total_queries": len(all_results),
                        "quality": {
                            "excellent": excellent,
                            "good": good,
                            "weak": weak,
                            "poor": poor,
                            "success_rate_percent": success_rate,
                        },
                        "performance": {
                            "avg_time_ms": sum(times) / len(times),
                            "min_time_ms": min(times),
                            "max_time_ms": max(times),
                        },
                    },
                    "results_by_category": results_by_category,
                },
                f,
                indent=2,
            )

        print(f"\n💾 Results saved to {output_file}")

    print("\n" + "=" * 80)
    print("🎯 RE-INGESTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
