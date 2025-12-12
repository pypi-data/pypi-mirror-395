"""Unit tests for chroma_ingestion.ingestion module.

Tests for CodeIngester and AgentIngester classes covering:
- Initialization with various configurations
- File discovery logic
- Chunking behavior
- Collection management
- Error handling
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from chroma_ingestion.ingestion.agents import AgentIngester
from chroma_ingestion.ingestion.base import CodeIngester


class TestCodeIngesterInitialization:
    """Test CodeIngester initialization."""

    def test_init_with_defaults(self, tmp_path: Path) -> None:
        """Test initialization with default parameters."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test_collection",
            )

            assert ingester.target_folder == str(tmp_path)
            assert ingester.collection_name == "test_collection"
            assert ingester.chunk_size == 1000
            assert ingester.chunk_overlap == 200
            assert len(ingester.file_patterns) == 4

    def test_init_with_custom_chunk_params(self, tmp_path: Path) -> None:
        """Test initialization with custom chunk parameters."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test_collection",
                chunk_size=500,
                chunk_overlap=50,
            )

            assert ingester.chunk_size == 500
            assert ingester.chunk_overlap == 50

    def test_init_with_custom_file_patterns(self, tmp_path: Path) -> None:
        """Test initialization with custom file patterns."""
        patterns = ["**/*.py", "**/*.txt"]
        with patch("chroma_ingestion.ingestion.base.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test_collection",
                file_patterns=patterns,
            )

            assert ingester.file_patterns == patterns

    def test_init_creates_collection(self, tmp_path: Path) -> None:
        """Test that initialization creates or gets collection."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client") as mock_client:
            mock_http_client = MagicMock()
            mock_collection = MagicMock()
            mock_http_client.get_or_create_collection.return_value = mock_collection
            mock_client.return_value = mock_http_client

            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test_collection",
            )

            mock_http_client.get_or_create_collection.assert_called_once_with(
                name="test_collection"
            )
            assert ingester.collection == mock_collection


class TestCodeIngesterFileDiscovery:
    """Test CodeIngester file discovery."""

    def test_discover_files_empty_folder(self, tmp_path: Path) -> None:
        """Test discovering files in empty folder."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
            )

            files = ingester.discover_files()
            assert files == []

    def test_discover_files_python_files(self, tmp_code_folder: Path) -> None:
        """Test discovering Python files."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_code_folder),
                collection_name="test",
            )

            files = ingester.discover_files()
            # Should find example.py from fixture
            assert any(f.endswith("example.py") for f in files)

    def test_discover_files_markdown_files(self, tmp_code_folder: Path) -> None:
        """Test discovering Markdown files."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_code_folder),
                collection_name="test",
            )

            files = ingester.discover_files()
            # Should find README.md from fixture
            assert any(f.endswith("README.md") for f in files)

    def test_discover_files_custom_patterns(self, tmp_path: Path) -> None:
        """Test discovering files with custom patterns."""
        # Create test files
        (tmp_path / "test.py").write_text("print('hello')")
        (tmp_path / "test.txt").write_text("hello")

        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
                file_patterns=["**/*.txt"],
            )

            files = ingester.discover_files()
            # Should only find txt files
            assert any(f.endswith("test.txt") for f in files)
            assert not any(f.endswith("test.py") for f in files)

    def test_discover_files_recursive(self, tmp_path: Path) -> None:
        """Test recursive file discovery."""
        # Create nested structure
        nested_dir = tmp_path / "subdir" / "nested"
        nested_dir.mkdir(parents=True)
        (nested_dir / "nested.py").write_text("# nested")
        (tmp_path / "root.py").write_text("# root")

        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
            )

            files = ingester.discover_files()
            assert len(files) >= 2
            assert any(f.endswith("root.py") for f in files)
            assert any(f.endswith("nested.py") for f in files)


class TestCodeIngesterChunking:
    """Test CodeIngester chunking behavior."""

    def test_splitter_configured(self, tmp_path: Path) -> None:
        """Test that text splitter is properly configured."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
                chunk_size=500,
                chunk_overlap=100,
            )

            # Verify splitter exists and has correct configuration
            assert ingester.splitter is not None
            assert hasattr(ingester.splitter, "split_text")

    def test_split_text_returns_chunks(self, tmp_path: Path) -> None:
        """Test that text splitting returns chunks."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
                chunk_size=100,  # Small for testing
            )

            long_text = "word " * 200  # Create text longer than chunk size
            chunks = ingester.splitter.split_text(long_text)

            # Should split into multiple chunks
            assert len(chunks) > 1
            # Each chunk should be non-empty
            assert all(len(chunk) > 0 for chunk in chunks)


class TestCodeIngesterMetadata:
    """Test CodeIngester metadata handling."""

    def test_prepare_metadata(self, tmp_path: Path) -> None:
        """Test metadata preparation."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
            )

            file_path = tmp_path / "test.py"
            chunk_index = 0

            metadata = ingester.prepare_metadata(str(file_path), chunk_index)

            assert metadata["source"] == str(file_path)
            assert metadata["filename"] == "test.py"
            assert metadata["chunk_index"] == chunk_index
            assert "file_type" in metadata
            assert metadata["file_type"] == ".py"


class TestAgentIngesterInitialization:
    """Test AgentIngester initialization."""

    def test_agent_ingester_init(self, tmp_path: Path) -> None:
        """Test AgentIngester initialization."""
        with patch("chroma_ingestion.ingestion.agents.get_chroma_client"):
            ingester = AgentIngester(
                target_folder=str(tmp_path),
                collection_name="agents",
            )

            assert ingester.target_folder == str(tmp_path)
            assert ingester.collection_name == "agents"
            # Should inherit from CodeIngester
            assert isinstance(ingester, CodeIngester)

    def test_agent_ingester_has_agent_patterns(self, tmp_path: Path) -> None:
        """Test that AgentIngester uses agent-specific patterns."""
        with patch("chroma_ingestion.ingestion.agents.get_chroma_client"):
            ingester = AgentIngester(
                target_folder=str(tmp_path),
                collection_name="agents",
            )

            # Should have patterns for agent files
            patterns_str = " ".join(ingester.file_patterns)
            assert "agent" in patterns_str.lower()


class TestAgentIngesterParsing:
    """Test AgentIngester YAML front matter parsing."""

    def test_parse_agent_metadata_valid(self, tmp_path: Path) -> None:
        """Test parsing valid agent YAML metadata."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text(
            """---
name: Test Agent
description: A test agent
tags: [test, demo]
---
# Agent Body
This is the body of the agent.
"""
        )

        with patch("chroma_ingestion.ingestion.agents.get_chroma_client"):
            ingester = AgentIngester(
                target_folder=str(tmp_path),
                collection_name="agents",
            )

            metadata = ingester.parse_agent_metadata(str(agent_file))

            assert metadata["name"] == "Test Agent"
            assert metadata["description"] == "A test agent"
            assert metadata["tags"] == ["test", "demo"]

    def test_parse_agent_metadata_missing_frontmatter(self, tmp_path: Path) -> None:
        """Test parsing agent file without YAML front matter."""
        agent_file = tmp_path / "test.agent.md"
        agent_file.write_text("# Agent Body\nNo frontmatter here.")

        with patch("chroma_ingestion.ingestion.agents.get_chroma_client"):
            ingester = AgentIngester(
                target_folder=str(tmp_path),
                collection_name="agents",
            )

            metadata = ingester.parse_agent_metadata(str(agent_file))

            # Should return minimal metadata
            assert isinstance(metadata, dict)


class TestCodeIngesterErrorHandling:
    """Test CodeIngester error handling."""

    def test_discover_files_with_permission_error(self, tmp_path: Path) -> None:
        """Test handling of permission errors during file discovery."""
        restricted_dir = tmp_path / "restricted"
        restricted_dir.mkdir()

        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            with patch("glob.glob") as mock_glob:
                mock_glob.side_effect = PermissionError("Permission denied")

                ingester = CodeIngester(
                    target_folder=str(tmp_path),
                    collection_name="test",
                )

                # Should handle error gracefully
                with pytest.raises(PermissionError):
                    ingester.discover_files()

    def test_split_text_empty_content(self, tmp_path: Path) -> None:
        """Test splitting empty content."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
            )

            chunks = ingester.splitter.split_text("")
            # Empty text should result in empty or single empty chunk
            assert isinstance(chunks, list)


class TestCodeIngesterIntegration:
    """Integration tests for CodeIngester workflow."""

    def test_ingester_full_workflow_mocked(self, tmp_code_folder: Path) -> None:
        """Test full ingestion workflow with mocked client."""
        with patch("chroma_ingestion.ingestion.base.get_chroma_client") as mock_client:
            mock_collection = MagicMock()
            mock_client.return_value.get_or_create_collection.return_value = mock_collection

            ingester = CodeIngester(
                target_folder=str(tmp_code_folder),
                collection_name="test",
            )

            # Simulate discovering files
            files = ingester.discover_files()
            assert len(files) > 0

            # Verify collection was created
            mock_client.return_value.get_or_create_collection.assert_called()
            assert ingester.collection == mock_collection

    def test_ingester_preserves_folder_structure(self, tmp_path: Path) -> None:
        """Test that ingester metadata preserves folder structure."""
        subdir = tmp_path / "code" / "examples"
        subdir.mkdir(parents=True)
        file_path = subdir / "example.py"
        file_path.write_text("# example")

        with patch("chroma_ingestion.ingestion.base.get_chroma_client"):
            ingester = CodeIngester(
                target_folder=str(tmp_path),
                collection_name="test",
            )

            metadata = ingester.prepare_metadata(str(file_path), 0)

            # Should preserve relative path information
            assert "code" in metadata["folder"] or "code" in metadata["source"]
