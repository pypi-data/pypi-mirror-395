"""Unit tests for chroma_ingestion.retrieval module.

Tests for CodeRetriever and MultiCollectionSearcher classes covering:
- Query operations
- Result formatting
- Semantic search with thresholds
- Metadata filtering
- Collection management
- Error handling
"""

from unittest.mock import MagicMock, patch

from chroma_ingestion.retrieval.retriever import CodeRetriever, MultiCollectionSearcher


class TestCodeRetrieverInitialization:
    """Test CodeRetriever initialization."""

    def test_init_with_collection_name(self) -> None:
        """Test initialization with collection name."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")

            assert retriever.collection_name == "test_collection"
            mock_client.return_value.get_or_create_collection.assert_called_once_with(
                name="test_collection"
            )

    def test_init_creates_client(self) -> None:
        """Test that initialization creates Chroma client."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_http_client = MagicMock()
            mock_collection = MagicMock()
            mock_http_client.get_or_create_collection.return_value = mock_collection
            mock_client.return_value = mock_http_client

            retriever = CodeRetriever("test_collection")

            assert retriever.client == mock_http_client
            assert retriever.collection == mock_collection


class TestCodeRetrieverQuery:
    """Test CodeRetriever query operations."""

    def test_query_basic(self) -> None:
        """Test basic query operation."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [
                    [
                        "def hello():\n    return 'world'",
                        "class MyClass:\n    pass",
                    ]
                ],
                "metadatas": [
                    [
                        {"filename": "hello.py", "chunk_index": 0},
                        {"filename": "myclass.py", "chunk_index": 0},
                    ]
                ],
                "distances": [[0.1, 0.3]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query("hello function", n_results=2)

            assert len(results) == 2
            assert results[0]["document"] == "def hello():\n    return 'world'"
            assert results[0]["metadata"]["filename"] == "hello.py"
            assert results[0]["distance"] == 0.1

    def test_query_with_custom_n_results(self) -> None:
        """Test query with custom result count."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            retriever.query("test", n_results=10)

            # Verify n_results was passed to collection.query
            call_args = mock_collection.query.call_args
            assert call_args[1]["n_results"] == 10

    def test_query_empty_results(self) -> None:
        """Test query returning empty results."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query("nonexistent", n_results=5)

            assert results == []

    def test_query_error_handling(self) -> None:
        """Test query error handling."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.side_effect = Exception("Query failed")
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query("test")

            # Should return empty list on error
            assert results == []


class TestCodeRetrieverSemanticSearch:
    """Test CodeRetriever semantic search with thresholds."""

    def test_query_semantic_with_threshold(self) -> None:
        """Test semantic search with distance threshold."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [
                    [
                        "exact match",
                        "partial match",
                        "weak match",
                    ]
                ],
                "metadatas": [
                    [
                        {"filename": "f1.py"},
                        {"filename": "f2.py"},
                        {"filename": "f3.py"},
                    ]
                ],
                "distances": [[0.1, 0.4, 0.9]],  # varying quality
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query_semantic("test", n_results=5, distance_threshold=0.5)

            # Should filter out results with distance >= threshold
            assert len(results) == 2
            assert all(r["distance"] < 0.5 for r in results)

    def test_query_semantic_all_filtered(self) -> None:
        """Test semantic search when all results filtered by threshold."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [[0.9, 0.95]],  # All poor matches (as dummy structure)
                "documents": [["poor1", "poor2"]],
                "metadatas": [[{"filename": "f1"}, {"filename": "f2"}]],
                "distances": [[0.9, 0.95]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query_semantic("test", distance_threshold=0.5)

            # All should be filtered out
            assert len(results) == 0

    def test_query_semantic_confidence_levels(self) -> None:
        """Test semantic confidence level classification."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [["doc1", "doc2", "doc3"]],
                "metadatas": [[{"f": "f1"}, {"f": "f2"}, {"f": "f3"}]],
                "distances": [[0.2, 0.45, 0.65]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query_semantic("test", n_results=5, distance_threshold=1.0)

            # Verify confidence calculation (if implemented)
            assert len(results) == 3
            # Results ordered by confidence (lower distance = higher confidence)
            assert results[0]["distance"] <= results[1]["distance"]


class TestCodeRetrieverMetadataFiltering:
    """Test CodeRetriever metadata filtering."""

    def test_query_by_metadata(self) -> None:
        """Test querying with metadata filter."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.get.return_value = {
                "documents": ["doc1", "doc2"],
                "metadatas": [
                    {"filename": "test.py", "type": "code"},
                    {"filename": "test.md", "type": "doc"},
                ],
                "ids": ["id1", "id2"],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query_by_metadata(where={"type": "code"}, n_results=10)

            # Verify metadata filter was applied
            assert mock_collection.get.called

    def test_get_collection_info(self) -> None:
        """Test retrieving collection information."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.count.return_value = 42
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            info = retriever.get_collection_info()

            assert info["count"] == 42
            assert "name" in info


class TestCodeRetrieverResultFormatting:
    """Test CodeRetriever result formatting."""

    def test_result_structure(self) -> None:
        """Test that results have expected structure."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [["test_document"]],
                "metadatas": [
                    [
                        {
                            "filename": "test.py",
                            "chunk_index": 0,
                            "source": "/path/to/test.py",
                        }
                    ]
                ],
                "distances": [[0.25]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query("test")

            assert len(results) == 1
            result = results[0]

            # Check required fields
            assert "document" in result
            assert "metadata" in result
            assert "distance" in result

            # Check metadata content
            assert result["metadata"]["filename"] == "test.py"
            assert result["metadata"]["chunk_index"] == 0

    def test_result_formatting_with_multiple_results(self) -> None:
        """Test formatting multiple results."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [["doc1", "doc2", "doc3"]],
                "metadatas": [
                    [
                        {"filename": "f1.py"},
                        {"filename": "f2.py"},
                        {"filename": "f3.py"},
                    ]
                ],
                "distances": [[0.1, 0.2, 0.3]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query("test", n_results=3)

            # Results should be in distance order (closest first)
            assert len(results) == 3
            assert results[0]["distance"] == 0.1
            assert results[1]["distance"] == 0.2
            assert results[2]["distance"] == 0.3


class TestMultiCollectionSearcher:
    """Test MultiCollectionSearcher cross-collection search."""

    def test_init_with_collections(self) -> None:
        """Test initialization with collection names."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client"):
            searcher = MultiCollectionSearcher(collection_names=["col1", "col2", "col3"])

            assert searcher.collection_names == ["col1", "col2", "col3"]

    def test_search_multiple_collections(self) -> None:
        """Test searching across multiple collections."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_http_client = MagicMock()
            mock_col1 = MagicMock()
            mock_col2 = MagicMock()

            # Setup different results for each collection
            mock_col1.query.return_value = {
                "documents": [["doc_from_col1"]],
                "metadatas": [[{"source": "col1"}]],
                "distances": [[0.1]],
            }
            mock_col2.query.return_value = {
                "documents": [["doc_from_col2"]],
                "metadatas": [[{"source": "col2"}]],
                "distances": [[0.2]],
            }

            # Setup client to return different collections
            def get_or_create_side_effect(name):
                if name == "col1":
                    return mock_col1
                return mock_col2

            mock_http_client.get_or_create_collection.side_effect = get_or_create_side_effect
            mock_client.return_value = mock_http_client

            searcher = MultiCollectionSearcher(["col1", "col2"])
            results = searcher.search("query", n_results=1)

            # Should query both collections
            assert mock_col1.query.called
            assert mock_col2.query.called

    def test_search_results_ranked(self) -> None:
        """Test that multi-collection results are ranked by distance."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_http_client = MagicMock()
            mock_col1 = MagicMock()
            mock_col2 = MagicMock()

            mock_col1.query.return_value = {
                "documents": [["good_match"]],
                "metadatas": [[{"collection": "col1"}]],
                "distances": [[0.1]],  # Better match
            }
            mock_col2.query.return_value = {
                "documents": [["ok_match"]],
                "metadatas": [[{"collection": "col2"}]],
                "distances": [[0.3]],  # Worse match
            }

            def get_collection(name):
                return mock_col1 if name == "col1" else mock_col2

            mock_http_client.get_or_create_collection.side_effect = get_collection
            mock_client.return_value = mock_http_client

            searcher = MultiCollectionSearcher(["col1", "col2"])
            results = searcher.search("query")

            # Best result should come first
            if results:
                assert results[0]["distance"] <= 0.1


class TestCodeRetrieverEdgeCases:
    """Test CodeRetriever edge cases."""

    def test_query_none_collection(self) -> None:
        """Test query when collection is None."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_client.return_value.get_or_create_collection.return_value = None

            retriever = CodeRetriever("test_collection")

            # Should handle gracefully
            if retriever.collection is None:
                results = retriever.query("test")
                assert results == []

    def test_query_large_distance_threshold(self) -> None:
        """Test semantic search with very high threshold (accepts all)."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [["doc1", "doc2"]],
                "metadatas": [[{"f": "f1"}, {"f": "f2"}]],
                "distances": [[0.9, 0.95]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query_semantic("test", distance_threshold=1.0)

            # High threshold should accept all
            assert len(results) == 2

    def test_query_zero_distance_threshold(self) -> None:
        """Test semantic search with zero threshold (accepts none)."""
        with patch("chroma_ingestion.retrieval.retriever.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [["doc1", "doc2"]],
                "metadatas": [[{"f": "f1"}, {"f": "f2"}]],
                "distances": [[0.1, 0.2]],
            }
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            retriever = CodeRetriever("test_collection")
            results = retriever.query_semantic("test", distance_threshold=0.0)

            # Zero threshold should reject all
            assert len(results) == 0
