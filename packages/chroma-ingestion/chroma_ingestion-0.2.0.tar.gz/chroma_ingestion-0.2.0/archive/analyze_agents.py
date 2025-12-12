"""Agent analysis and consolidation planning.

Analyzes ingested agents to identify overlaps, duplicates, and consolidation
opportunities. Generates clustering and semantic similarity reports.
"""

from collections import defaultdict

from chroma_ingestion.retrieval import CodeRetriever


class AgentAnalyzer:
    """Analyze ingested agents for overlaps and consolidation opportunities."""

    def __init__(self, collection_name: str = "agents_analysis"):
        """Initialize agent analyzer.

        Args:
            collection_name: Name of the Chroma collection to query
        """
        self.retriever = CodeRetriever(collection_name)
        self.collection_name = collection_name

    def find_by_category(self, category: str, n_results: int = 50) -> list[dict]:
        """Find all agents in a specific category.

        Args:
            category: Category name (frontend, backend, testing, etc.)
            n_results: Maximum number of results

        Returns:
            List of matching document chunks with metadata
        """
        return self.retriever.query_by_metadata(
            where={"category": category},
            n_results=n_results,
        )

    def find_by_tech_stack(self, tech: str, n_results: int = 20) -> list[dict]:
        """Find agents mentioning a specific technology.

        Args:
            tech: Technology keyword (nextjs, python, playwright, etc.)
            n_results: Maximum number of results

        Returns:
            List of matching document chunks with metadata
        """
        return self.retriever.query_by_metadata(
            where_document={"$contains": tech},
            n_results=n_results,
        )

    def find_similar_agents(self, query: str, n_results: int = 10) -> list[dict]:
        """Semantic search for similar agents.

        Uses semantic distance to find topically similar agents.

        Args:
            query: Query text describing what you're looking for
            n_results: Number of results to return

        Returns:
            List of similar document chunks with distance scores
        """
        return self.retriever.query_semantic(
            query_text=query,
            n_results=n_results,
            distance_threshold=0.4,  # High similarity threshold
        )

    def get_unique_agents(self, results: list[dict]) -> list[str]:
        """Extract unique agent names from query results.

        Args:
            results: List of query results with metadata

        Returns:
            Sorted list of unique agent names
        """
        agents = set()
        for result in results:
            if "metadata" in result and "agent_name" in result["metadata"]:
                agents.add(result["metadata"]["agent_name"])
        return sorted(list(agents))

    def cluster_by_category(self) -> dict[str, list[str]]:
        """Group all agents by their classified category.

        Returns:
            Dictionary mapping category names to lists of agent names
        """
        categories = [
            "frontend",
            "backend",
            "architecture",
            "testing",
            "ai_ml",
            "devops",
            "security",
            "quality",
            "database",
            "planning",
        ]

        clusters = {}
        for category in categories:
            results = self.find_by_category(category)
            agents = self.get_unique_agents(results)
            if agents:
                clusters[category] = agents

        return clusters

    def get_category_distribution(self) -> dict[str, int]:
        """Get count of agents per category.

        Returns:
            Dictionary mapping category to agent count
        """
        clusters = self.cluster_by_category()
        return {cat: len(agents) for cat, agents in clusters.items()}

    def find_duplicates_by_expertise(self) -> dict[str, list[tuple]]:
        """Find agents with high semantic similarity (potential duplicates).

        Uses semantic queries to identify agents covering similar expertise.

        Returns:
            Dictionary mapping expertise area to lists of (agent_name, source_collection) tuples
        """
        duplicates = defaultdict(list)

        # Key queries to identify overlapping agents
        test_queries = [
            ("Next.js development App Router Server Components", "frontend"),
            ("Python FastAPI backend API development REST", "backend"),
            ("System architecture design patterns infrastructure", "architecture"),
            ("Automated testing Playwright E2E testing QA", "testing"),
            ("Machine learning AI engineering LLM embeddings", "ai_ml"),
            ("Deployment CI/CD DevOps Docker container", "devops"),
            ("Security vulnerabilities auth authentication", "security"),
            ("Code review refactoring best practices quality", "quality"),
            ("PostgreSQL database SQL optimization", "database"),
            ("Task planning requirements project management", "planning"),
        ]

        for query, expected_category in test_queries:
            results = self.find_similar_agents(query, n_results=10)
            if len(results) > 1:
                for result in results:
                    if "metadata" in result:
                        agent_name = result["metadata"].get("agent_name", "unknown")
                        source = result["metadata"].get("source_collection", "unknown")
                        distance = result.get("distance", 1.0)
                        duplicates[query].append((agent_name, source, distance))

        return duplicates

    def generate_consolidation_report(self) -> str:
        """Generate a comprehensive consolidation report.

        Includes category clustering, duplicate detection, and consolidation strategy.

        Returns:
            Formatted markdown report string
        """
        report = []
        report.append("# Agent Consolidation Analysis Report\n")
        report.append(f"Collection: `{self.collection_name}`\n")

        # Summary statistics
        clusters = self.cluster_by_category()
        total_agents = sum(len(agents) for agents in clusters.values())
        report.append("## Summary\n")
        report.append(f"- **Total unique agents**: {total_agents}")
        report.append(f"- **Categories identified**: {len(clusters)}")
        report.append("- **Target consolidated agents**: 10\n")
        report.append(
            f"- **Estimated reduction**: {total_agents} → 10 (~{100 * (1 - 10/total_agents):.0f}% reduction)\n\n"
        )

        # Category distribution
        report.append("## Agents by Category\n\n")
        distribution = self.get_category_distribution()

        category_order = [
            "frontend",
            "backend",
            "architecture",
            "testing",
            "ai_ml",
            "devops",
            "security",
            "quality",
            "database",
            "planning",
        ]

        for category in category_order:
            if category in clusters:
                agents = clusters[category]
                count = len(agents)
                report.append(f"### {category.title()} ({count} agents)")
                report.append("")
                for agent in agents[:10]:  # Show top 10
                    report.append(f"- {agent}")
                if len(agents) > 10:
                    report.append(f"- ... and {len(agents) - 10} more")
                report.append("")

        # Consolidation mapping
        report.append("\n## Recommended Consolidation Mapping\n\n")

        consolidation_map = {
            "frontend-expert": [
                "nextjs",
                "react",
                "frontend",
                "ui",
                "ux",
                "component",
            ],
            "backend-expert": ["backend", "python", "fastapi", "api", "server"],
            "architect-expert": [
                "architect",
                "system",
                "design",
                "infrastructure",
            ],
            "testing-expert": ["test", "playwright", "qa", "debug", "testing"],
            "ai-ml-expert": ["ai", "ml", "data", "engineer", "prompt", "llm"],
            "devops-expert": ["devops", "deploy", "cloud", "docker", "incident"],
            "security-expert": ["security", "auth", "audit", "vulnerability"],
            "quality-expert": ["review", "refactor", "code", "quality", "best"],
            "database-expert": ["database", "sql", "postgres", "neon", "graphql"],
            "planning-expert": ["plan", "requirement", "pm", "product", "task"],
        }

        for target, keywords in consolidation_map.items():
            report.append(f"### {target}")
            report.append(f"**Source agents** containing keywords: {', '.join(keywords)}")
            report.append("")

        # Similarity clusters
        report.append("\n## High-Similarity Agent Groups (Potential Duplicates)\n\n")

        duplicates = self.find_duplicates_by_expertise()
        for query, agents in list(duplicates.items())[:5]:  # Show top 5
            if agents:
                report.append(f"### Query: '{query}'\n")
                # Deduplicate agents
                unique_agents = {}
                for agent, source, distance in agents:
                    if agent not in unique_agents:
                        unique_agents[agent] = (source, distance)

                for agent, (source, distance) in sorted(
                    unique_agents.items(), key=lambda x: x[1][1]
                ):
                    report.append(f"- **{agent}** (source: {source}, distance: {distance:.3f})")
                report.append("")

        # Consolidation strategy
        report.append("\n## Consolidation Strategy\n\n")
        report.append(
            """
1. **Query each category** to identify all agents belonging to it
2. **Extract key expertise areas** from each agent's description and content
3. **Merge guidelines** from similar agents (resolve conflicts by priority)
4. **Combine expertise sections** and deduplicate
5. **Union tools lists** from all source agents
6. **Create consolidated agent file** with merged content
7. **Verify coverage** through semantic queries

Each consolidated agent will:
- Include the best expertise from 5-15 source agents
- Maintain references to source agents in metadata
- Cover all technologies relevant to that domain
- Provide comprehensive guidelines and best practices
"""
        )

        report.append("\n## Next Steps\n\n")
        report.append("1. Review this report for consolidation decisions")
        report.append("2. Run `generate_consolidated_agents.py` to create merged agents")
        report.append("3. Test consolidated agents with sample queries")
        report.append("4. Archive redundant source agents")

        return "\n".join(report)

    def print_summary(self):
        """Print a quick summary of analysis to console."""
        print("\n" + "=" * 70)
        print("AGENT ANALYSIS SUMMARY")
        print("=" * 70)

        # Category distribution
        distribution = self.get_category_distribution()
        print("\n📊 Agents by Category:")
        total = sum(distribution.values())
        for category in sorted(distribution.keys()):
            count = distribution[category]
            pct = 100 * count / total if total > 0 else 0
            bar = "█" * (count // 2)
            print(f"  {category:15s} {bar:20s} {count:3d} ({pct:5.1f}%)")

        print(f"\n  Total: {total} unique agents across {len(distribution)} categories")

        # Top duplicates
        print("\n🔍 Top Expertise Overlaps:")
        duplicates = self.find_duplicates_by_expertise()
        for i, (query, agents) in enumerate(list(duplicates.items())[:3]):
            unique_agents = set(a[0] for a in agents)
            print(f"\n  {i+1}. '{query}'")
            for agent in list(unique_agents)[:3]:
                print(f"     - {agent}")
            if len(unique_agents) > 3:
                print(f"     ... and {len(unique_agents) - 3} more")

        print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    analyzer = AgentAnalyzer()
    analyzer.print_summary()

    # Generate full report
    report = analyzer.generate_consolidation_report()
    with open("CONSOLIDATION_REPORT.md", "w") as f:
        f.write(report)

    print("✅ Full report saved to CONSOLIDATION_REPORT.md")
