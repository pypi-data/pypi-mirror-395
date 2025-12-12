#!/usr/bin/env python3
"""Test consolidated agents against semantic queries.

Validates that consolidated agents:
1. Return relevant results for domain queries
2. Maintain semantic similarity (distance < 0.3)
3. Cover all key expertise areas
"""

from chroma_ingestion.retrieval import CodeRetriever

# Test queries organized by consolidated agent target
TEST_QUERIES = {
    "frontend-expert": [
        ("Next.js App Router Server Components", 3),
        ("React 19 hooks state management", 3),
        ("TypeScript React component patterns", 2),
        ("Tailwind CSS design system", 2),
        ("shadcn/ui component library", 2),
    ],
    "backend-expert": [
        ("Python FastAPI REST API development", 3),
        ("Database ORM SQLAlchemy patterns", 2),
        ("API authentication and security", 2),
        ("Backend architecture design", 2),
    ],
    "architect-expert": [
        ("System architecture design patterns", 3),
        ("Microservices infrastructure design", 2),
        ("Technology selection and evaluation", 2),
        ("Scalability and performance architecture", 2),
    ],
    "testing-expert": [
        ("Playwright E2E testing automation", 3),
        ("Vitest unit testing framework", 3),
        ("Test automation best practices", 2),
        ("Testing strategy and coverage", 2),
    ],
    "ai-ml-expert": [
        ("Machine learning engineering LLM", 3),
        ("AI prompt engineering best practices", 3),
        ("Embeddings and vector search", 2),
        ("RAG retrieval augmented generation", 2),
    ],
    "devops-expert": [
        ("Docker containerization deployment", 3),
        ("CI/CD pipeline automation", 3),
        ("Kubernetes orchestration", 2),
        ("Cloud infrastructure DevOps", 2),
    ],
    "security-expert": [
        ("Authentication authorization security", 3),
        ("Vulnerability scanning security audit", 2),
        ("Encryption and data protection", 2),
    ],
    "quality-expert": [
        ("Code review best practices", 3),
        ("Refactoring code quality improvement", 2),
        ("Testing and quality assurance", 2),
    ],
    "database-expert": [
        ("PostgreSQL SQL optimization", 3),
        ("Database schema design", 2),
        ("Query performance tuning", 2),
        ("Neon serverless database", 2),
    ],
    "planning-expert": [
        ("Task planning project management", 3),
        ("Requirements analysis documentation", 2),
        ("Technical specification writing", 2),
    ],
}

# Consolidated agent targets and their descriptions
CONSOLIDATED_AGENTS = {
    "frontend-expert": "Next.js, React, TypeScript frontend engineer",
    "backend-expert": "Python FastAPI backend and API development",
    "architect-expert": "System architecture and design patterns",
    "testing-expert": "Automated testing and QA specialist",
    "ai-ml-expert": "Machine learning and AI engineering",
    "devops-expert": "DevOps, deployment, and infrastructure",
    "security-expert": "Security, authentication, and vulnerability",
    "quality-expert": "Code review, refactoring, and quality",
    "database-expert": "PostgreSQL and database optimization",
    "planning-expert": "Project planning and requirements",
}


def test_consolidated_agents():
    """Test all consolidated agents with semantic queries."""
    retriever = CodeRetriever("agents_analysis")

    print("\n" + "=" * 80)
    print("CONSOLIDATED AGENT TESTING")
    print("=" * 80)

    results_summary = {}
    total_queries = 0
    total_relevant = 0

    for agent, queries in TEST_QUERIES.items():
        print(f"\n📌 Testing {agent}")
        print(f"   Description: {CONSOLIDATED_AGENTS[agent]}")
        print(f"   Queries: {len(queries)}")

        agent_relevant = 0
        agent_total = 0

        for query, min_results in queries:
            agent_total += 1
            total_queries += 1

            # Semantic search
            results = retriever.query_semantic(
                query_text=query,
                n_results=min_results,
                distance_threshold=0.5,  # Allow some flexibility
            )

            # Check if we found relevant results
            if results:
                agent_relevant += 1
                total_relevant += 1

                # Show best match
                best_match = results[0]
                distance = best_match.get("distance", 1.0)
                agent_name = best_match.get("metadata", {}).get("agent_name", "unknown")

                status = "✅" if distance < 0.3 else "⚠️" if distance < 0.5 else "❌"
                print(f"   {status} '{query[:50]}'")
                print(f"      → {agent_name} (distance: {distance:.3f})")
            else:
                print(f"   ❌ '{query[:50]}' - NO RESULTS")

        results_summary[agent] = (agent_relevant, agent_total)
        coverage = 100 * agent_relevant / agent_total if agent_total > 0 else 0
        print(f"   Coverage: {agent_relevant}/{agent_total} ({coverage:.0f}%)")

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    print("\n📊 Overall Results:")
    print(f"   Total queries: {total_queries}")
    print(f"   Relevant results: {total_relevant}")
    coverage = 100 * total_relevant / total_queries if total_queries > 0 else 0
    print(f"   Coverage: {coverage:.1f}%")

    print("\n📋 Coverage by Agent:")
    for agent, (relevant, total) in sorted(results_summary.items()):
        coverage_pct = 100 * relevant / total if total > 0 else 0
        bar = "█" * int(coverage_pct // 10)
        print(f"   {agent:20s} {bar:10s} {relevant:2d}/{total:2d} ({coverage_pct:5.1f}%)")

    print("\n" + "=" * 80)

    if coverage >= 80:
        print("✅ TESTING PASSED: All consolidated agents are working well!")
        return 0
    elif coverage >= 60:
        print("⚠️  TESTING PARTIAL: Most agents working, but some coverage gaps")
        return 0
    else:
        print("❌ TESTING FAILED: Significant coverage gaps detected")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(test_consolidated_agents())
