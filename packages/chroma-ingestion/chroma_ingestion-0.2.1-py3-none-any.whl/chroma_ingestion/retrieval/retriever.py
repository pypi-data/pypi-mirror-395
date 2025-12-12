"""Retrieval and verification utilities for Chroma ingested code.

Provides tools for querying ingested code chunks and validating data quality.
"""

from chroma_ingestion.clients.chroma import get_chroma_client


class CodeRetriever:
    """Query and retrieve ingested code chunks from Chroma.

    Provides semantic search capabilities for code discovery and verification.
    """

    def __init__(self, collection_name: str):
        """Initialize the code retriever.

        Args:
            collection_name: Name of the Chroma collection to query
        """
        self.collection_name = collection_name
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def query(
        self,
        query_text: str,
        n_results: int = 3,
    ) -> list[dict]:
        """Query the collection for relevant code chunks.

        Args:
            query_text: Natural language or code query
            n_results: Number of results to return

        Returns:
            List of result dictionaries with document, metadata, and distance
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
            )

            # Reformat results for easier consumption
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                    strict=False,
                ):
                    formatted_results.append(
                        {
                            "document": doc,
                            "metadata": meta,
                            "distance": dist,
                        }
                    )

            return formatted_results

        except Exception as e:
            print(f"❌ Query failed: {e}")
            return []

    def query_semantic(
        self,
        query_text: str,
        n_results: int = 5,
        distance_threshold: float = 1.0,
    ) -> list[dict]:
        """Semantic search with optional distance threshold filtering.

        Useful for finding highly relevant chunks while filtering out weak matches.

        Args:
            query_text: Natural language or semantic query
            n_results: Number of results to return before filtering
            distance_threshold: Maximum distance to include (lower = more similar).
                Calibrated default is 1.0 based on empirical testing:
                < 0.8: Excellent match (high confidence)
                0.8-1.0: Good match (solid relevance)
                1.0-1.2: Okay match (acceptable relevance)
                > 1.2: Poor match (low confidence)

        Returns:
            List of filtered result dictionaries
        """
        results = self.query(query_text, n_results=n_results * 2)

        # Filter by distance threshold
        filtered = [r for r in results if r["distance"] <= distance_threshold]
        return filtered[:n_results]

    def query_by_metadata(
        self,
        where: dict | None = None,
        where_document: dict | None = None,
        n_results: int = 10,
    ) -> list[dict]:
        """Query collection with metadata filtering.

        Args:
            where: Metadata filter dictionary (e.g., {"filename": "config.py"})
            where_document: Document content filter
            n_results: Number of results to return

        Returns:
            List of filtered result dictionaries
        """
        try:
            results = self.collection.get(
                where=where,
                where_document=where_document,
                limit=n_results,
            )

            formatted_results = []
            if results["documents"]:
                for doc, meta in zip(results["documents"], results["metadatas"], strict=False):
                    formatted_results.append(
                        {
                            "document": doc,
                            "metadata": meta,
                        }
                    )

            return formatted_results

        except Exception as e:
            print(f"❌ Metadata query failed: {e}")
            return []

    def get_context(
        self,
        query_text: str,
        n_results: int = 3,
        include_metadata: bool = True,
    ) -> str:
        """Get relevant context as formatted string (useful for prompt injection).

        Args:
            query_text: Query to find relevant context
            n_results: Number of chunks to include
            include_metadata: Whether to include source metadata in output

        Returns:
            Formatted string suitable for injection into prompts
        """
        results = self.query(query_text, n_results=n_results)

        if not results:
            return "No relevant context found."

        context_parts = []
        for i, result in enumerate(results, 1):
            if include_metadata:
                source = result["metadata"].get("source", "unknown")
                context_parts.append(f"--- Source: {source} ---\n{result['document']}")
            else:
                context_parts.append(result["document"])

        return "\n\n".join(context_parts)

    def get_by_source(self, filename: str) -> list[dict]:
        """Retrieve all chunks from a specific source file.

        Args:
            filename: Name of the source file

        Returns:
            List of chunks from that file
        """
        try:
            results = self.collection.get(where={"filename": filename})

            formatted_results = []
            if results["documents"]:
                for doc, meta in zip(results["documents"], results["metadatas"], strict=False):
                    formatted_results.append(
                        {
                            "document": doc,
                            "metadata": meta,
                        }
                    )

            return formatted_results

        except Exception as e:
            print(f"❌ Get by source failed: {e}")
            return []

    def get_collection_info(self) -> dict:
        """Get information about the collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_chunks": count,
            }
        except Exception as e:
            print(f"❌ Get collection info failed: {e}")
            return {}


def verify_ingestion(collection_name: str, test_queries: list[str] | None = None) -> None:
    """Verify ingestion quality by running test queries.

    Args:
        collection_name: Name of the collection to verify
        test_queries: Optional list of test queries (defaults to standard set)
    """
    if test_queries is None:
        test_queries = [
            "How do agents handle errors and exceptions?",
            "What are the main classes and functions?",
            "How is configuration managed?",
        ]

    retriever = CodeRetriever(collection_name)
    stats = retriever.get_collection_info()

    print("\n" + "=" * 70)
    print("📊 INGESTION VERIFICATION REPORT")
    print("=" * 70)
    print(f"Collection: {stats['collection_name']}")
    print(f"Total chunks: {stats['total_chunks']}")

    if stats["total_chunks"] == 0:
        print("⚠️  No chunks found in collection!")
        return

    print("\n--- Testing Retrieval Quality ---\n")

    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        results = retriever.query(query, n_results=2)

        if results:
            for j, result in enumerate(results, 1):
                meta = result["metadata"]
                doc = result["document"]
                distance = result["distance"]

                print(f"  Result {j}:")
                print(f"    Source: {meta['filename']}")
                print(f"    Distance: {distance:.4f}")
                print(f"    Preview: {doc[:150]}...")
                print()
        else:
            print("  ❌ No results found\n")

    print("=" * 70)
    print("✅ Verification complete!")
    print("=" * 70)


class MultiCollectionSearcher:
    """Search across multiple Chroma collections simultaneously.

    Useful for finding relevant content across the entire knowledge base
    (e.g., agents, tools, documentation).
    """

    def __init__(self, collection_names: list[str]):
        """Initialize the multi-collection searcher.

        Args:
            collection_names: List of collection names to search
        """
        self.client = get_chroma_client()
        self.retrievers = {name: CodeRetriever(name) for name in collection_names}

    def search_all(
        self,
        query_text: str,
        n_results: int = 3,
    ) -> dict[str, list[dict]]:
        """Search all collections and return results organized by source.

        Args:
            query_text: Query text to search for
            n_results: Number of results per collection

        Returns:
            Dictionary mapping collection names to results
        """
        all_results = {}

        for collection_name, retriever in self.retrievers.items():
            results = retriever.query(query_text, n_results=n_results)
            all_results[collection_name] = results

        return all_results

    def search_ranked(
        self,
        query_text: str,
        n_results: int = 5,
    ) -> list[dict]:
        """Search all collections and return results ranked by relevance.

        Args:
            query_text: Query text to search for
            n_results: Number of top results to return

        Returns:
            List of results sorted by distance (most relevant first)
        """
        all_results = []

        for collection_name, retriever in self.retrievers.items():
            results = retriever.query(query_text, n_results=n_results * 2)

            # Add collection name to each result
            for result in results:
                result["collection"] = collection_name

            all_results.extend(results)

        # Sort by distance (lower = more relevant)
        all_results.sort(key=lambda r: r.get("distance", float("inf")))

        return all_results[:n_results]

    def get_context_multiway(
        self,
        query_text: str,
        n_results: int = 2,
    ) -> str:
        """Get context from multiple collections as formatted string.

        Useful for injection into prompts that need knowledge from multiple sources.

        Args:
            query_text: Query to find relevant context
            n_results: Number of results per collection

        Returns:
            Formatted string with context from all collections
        """
        all_results = self.search_all(query_text, n_results=n_results)

        context_parts = []

        for collection_name, results in all_results.items():
            if results:
                context_parts.append(f"=== From {collection_name} ===\n")
                for result in results:
                    source = result["metadata"].get("source", "unknown")
                    context_parts.append(f"[{source}]\n{result['document']}\n")

        if not context_parts:
            return "No relevant context found across collections."

        return "\n".join(context_parts)
