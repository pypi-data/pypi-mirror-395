"""Example usage of the Chroma retrieval system.

This script demonstrates how to:
1. Query ingested code/documents
2. Retrieve chunks by source
3. Analyze retrieval results
"""

from dotenv import load_dotenv

from chroma_ingestion.retrieval import CodeRetriever

# Load environment variables
load_dotenv()


def example_semantic_search():
    """Example: Semantic search for agent patterns."""
    print("\n" + "=" * 70)
    print("🔍 SEMANTIC SEARCH EXAMPLES")
    print("=" * 70)

    retriever = CodeRetriever("agents_context")

    queries = [
        "How do agents handle authentication and security?",
        "What are best practices for error handling?",
        "How do agents communicate with external services?",
        "What deployment strategies are recommended?",
    ]

    for query in queries:
        print(f"\n📌 Query: {query}")
        results = retriever.query(query, n_results=2)

        if results:
            for i, result in enumerate(results, 1):
                meta = result["metadata"]
                doc = result["document"]
                distance = result["distance"]

                print(f"\n  Result {i}:")
                print(f"    Source: {meta['filename']}")
                print(f"    Type: {meta['file_type']}")
                print(f"    Relevance (distance): {distance:.4f}")
                print("    Content preview:")

                # Pretty-print content with indentation
                lines = doc.split("\n")[:5]
                for line in lines:
                    print(f"      {line}")

                if len(doc.split("\n")) > 5:
                    print("      ...")
        else:
            print("  ❌ No results found")


def example_retrieve_by_source():
    """Example: Retrieve all chunks from a specific agent."""
    print("\n" + "=" * 70)
    print("📂 RETRIEVE BY SOURCE FILE")
    print("=" * 70)

    retriever = CodeRetriever("agents_context")

    # Get all chunks from a specific agent
    filename = "backend-architect.prompt.md"
    print(f"\n📄 Retrieving all chunks from: {filename}")

    chunks = retriever.get_by_source(filename)

    if chunks:
        print(f"✅ Found {len(chunks)} chunk(s)")
        for i, chunk in enumerate(chunks[:3], 1):  # Show first 3
            meta = chunk["metadata"]
            doc = chunk["document"]

            print(f"\n  Chunk {i}/{len(chunks)}:")
            print(f"    Index: {meta['chunk_index']}")
            print(f"    Preview: {doc[:150]}...")
    else:
        print(f"❌ No chunks found for {filename}")


def example_collection_stats():
    """Example: View collection statistics."""
    print("\n" + "=" * 70)
    print("📊 COLLECTION STATISTICS")
    print("=" * 70)

    retriever = CodeRetriever("agents_context")
    stats = retriever.get_collection_info()

    print(f"\nCollection: {stats['collection_name']}")
    print(f"Total chunks: {stats['total_chunks']}")

    if stats["total_chunks"] > 0:
        print(f"\nEstimated tokens: {stats['total_chunks'] * 800:,}")
        print("(assuming ~800 tokens per chunk)")


def example_specialized_queries():
    """Example: Domain-specific queries for agent patterns."""
    print("\n" + "=" * 70)
    print("🎯 DOMAIN-SPECIFIC QUERIES")
    print("=" * 70)

    retriever = CodeRetriever("agents_context")

    # Different types of queries for different use cases
    specialized_queries = {
        "Architecture": "microservices, API design, system architecture",
        "DevOps": "deployment, CI/CD, infrastructure as code, terraform",
        "Security": "authentication, authorization, encryption, compliance",
        "Performance": "optimization, caching, load balancing, scalability",
        "Testing": "unit tests, integration tests, test automation",
    }

    for category, keywords in specialized_queries.items():
        print(f"\n🔹 {category} ({keywords})")

        results = retriever.query(keywords, n_results=1)

        if results:
            result = results[0]
            meta = result["metadata"]
            doc = result["document"][:100]

            print(f"   Top match: {meta['filename']}")
            print(f"   Preview: {doc}...")
        else:
            print("   ❌ No results")


if __name__ == "__main__":
    print("🚀 Chroma Retrieval Examples\n")

    # Run all examples
    example_collection_stats()
    example_semantic_search()
    example_retrieve_by_source()
    example_specialized_queries()

    print("\n" + "=" * 70)
    print("✅ Examples complete!")
    print("=" * 70 + "\n")
