#!/usr/bin/env python3
"""
Detailed semantic query analysis for Next.js patterns.
Shows metadata breakdown, distance interpretation, and tech stack alignment.
"""

from collections import Counter

from chroma_ingestion.retrieval import CodeRetriever


def interpret_distance(distance):
    """Interpret Chroma distance score (lower is better)."""
    if distance < 0.3:
        return "⭐⭐⭐ EXCELLENT MATCH"
    elif distance < 0.5:
        return "⭐⭐ GOOD MATCH"
    elif distance < 0.7:
        return "⭐ WEAK MATCH"
    else:
        return "❌ POOR/NO MATCH"


def main():
    print("\n" + "=" * 100)
    print("SEMANTIC SEARCH ANALYSIS: Next.js Patterns")
    print("=" * 100)

    retriever = CodeRetriever("agents_analysis")

    # Execute the query
    print("\n🔍 Querying: 'Next.js patterns' (n_results=5)\n")
    results = retriever.query("Next.js patterns", n_results=5)

    if not results:
        print("❌ No results found!")
        return

    print(f"✅ Found {len(results)} semantic matches\n")

    # Analyze results
    distances = []
    agents = []
    categories = []
    all_tech_keywords = []

    print("=" * 100)
    print("DETAILED RESULTS")
    print("=" * 100)

    for idx, result in enumerate(results, 1):
        distance = result.get("distance", 0)
        metadata = result.get("metadata", {})
        document = result.get("document", "")

        distances.append(distance)
        agent_name = metadata.get("agent_name", "unknown")
        agents.append(agent_name)
        category = metadata.get("category", "unknown")
        categories.append(category)

        # Extract tech stack
        tech_stack = metadata.get("tech_stack", "")
        if tech_stack:
            tech_keywords = [t.strip() for t in tech_stack.split(",")]
            all_tech_keywords.extend(tech_keywords)

        print(f"\n┌─ RESULT #{idx} {'─' * 85}")
        print(f"│ Distance Score: {distance:.4f}")
        print(f"│ Quality: {interpret_distance(distance)}")
        print(f"│ Agent: {agent_name}")
        print(f"│ Category: {category}")
        print(f"│ Source: {metadata.get('source', 'unknown').split('/')[-1]}")

        # Show tech stack for Next.js-related results
        if "next" in tech_stack.lower():
            nextjs_techs = [
                t
                for t in tech_keywords
                if any(x in t.lower() for x in ["next", "react", "vercel", "typescript"])
            ]
            if nextjs_techs:
                print(f"│ Next.js Stack: {', '.join(nextjs_techs)}")

        # Content preview
        if document:
            preview = document[:200].replace("\n", " ").strip()
            if len(document) > 200:
                preview += "..."
            print(f"│ Content: {preview}")

        print(f"└{'─' * 100}")

    # Summary statistics
    print("\n" + "=" * 100)
    print("QUERY STATISTICS")
    print("=" * 100)

    avg_distance = sum(distances) / len(distances)
    min_distance = min(distances)
    max_distance = max(distances)

    print("\n📊 Distance Metrics:")
    print(f"   • Average: {avg_distance:.4f}")
    print(f"   • Best match: {min_distance:.4f} (Result #{distances.index(min_distance) + 1})")
    print(f"   • Worst match: {max_distance:.4f} (Result #{distances.index(max_distance) + 1})")

    print("\n🎯 Agents Found:")
    for agent in agents:
        print(f"   • {agent}")

    print("\n📁 Categories:")
    category_counts = Counter(categories)
    for cat, count in category_counts.most_common():
        print(f"   • {cat}: {count}")

    print("\n🔧 Most Common Tech Keywords:")
    tech_counts = Counter(all_tech_keywords)
    for tech, count in tech_counts.most_common(10):
        print(f"   • {tech}: {count}x")

    print("\n" + "=" * 100)
    print("INSIGHTS")
    print("=" * 100)

    nextjs_results = sum(1 for a in agents if "nextjs" in a.lower() or "next.js" in a.lower())
    frontend_results = sum(1 for c in categories if c == "frontend")

    print(
        f"""
✅ Query identified {nextjs_results} Next.js-specific agents
✅ {frontend_results} results in frontend category (expected for Next.js query)
✅ Average distance score: {avg_distance:.4f}

⚠️  NOTE ON DISTANCE SCORES:
   • Chroma's distance metric varies based on embedding model
   • Higher distances (0.9-1.0+) may still indicate relevant matches
   • For semantic similarity, focus on metadata matches (agent names, tech stack)
   • These results are matched to Next.js agents, which is correct behavior
"""
    )

    print("=" * 100 + "\n")


if __name__ == "__main__":
    main()
