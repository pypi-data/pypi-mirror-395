#!/usr/bin/env python3
"""
Query the agents_analysis Chroma collection for Next.js patterns.
Execute with: uv run query_nextjs_patterns.py
"""

from chroma_ingestion.retrieval import CodeRetriever


def main():
    print("=" * 80)
    print("QUERYING CHROMA COLLECTION FOR NEXT.JS PATTERNS")
    print("=" * 80)
    print()

    # Initialize the retriever for the agents_analysis collection
    print("📊 Initializing CodeRetriever for 'agents_analysis' collection...")
    retriever = CodeRetriever("agents_analysis")

    # Execute the semantic query
    print("🔍 Executing query: 'Next.js patterns' (n_results=5)...")
    print()

    try:
        results = retriever.query("Next.js patterns", n_results=5)

        if not results:
            print("❌ No results found")
            return

        print(f"✅ Found {len(results)} results\n")
        print("-" * 80)

        for idx, result in enumerate(results, 1):
            print(f"\n🎯 RESULT #{idx}")
            print("-" * 80)

            # Display result metadata
            if isinstance(result, dict):
                distance = result.get("distance", "N/A")
                document = result.get("document", "")
                metadata = result.get("metadata", {})

                print(f"📏 Distance Score: {distance:.4f}")
                if distance < 0.3:
                    relevance = "⭐⭐⭐ EXCELLENT"
                elif distance < 0.5:
                    relevance = "⭐⭐ GOOD"
                elif distance < 0.7:
                    relevance = "⭐ WEAK"
                else:
                    relevance = "❌ POOR"
                print(f"   Relevance: {relevance}")

                # Display metadata
                if metadata:
                    print("\n📋 Metadata:")
                    for key, value in metadata.items():
                        if key in ["agent_name", "category", "tech_stack", "source"]:
                            print(f"   • {key}: {value}")

                # Display document content (first 300 chars)
                if document:
                    preview = document[:300].replace("\n", " ")
                    if len(document) > 300:
                        preview += "..."
                    print("\n📝 Content Preview:")
                    print(f"   {preview}")

        print("\n" + "=" * 80)
        print("✅ QUERY COMPLETE")
        print("=" * 80)

    except Exception as e:
        print(f"❌ Error executing query: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
