"""Code extraction and ingestion module for Chroma.

This module provides intelligent code-aware chunking and storage of text and code
into Chroma Cloud. It uses RecursiveCharacterTextSplitter to preserve semantic
structure and maintains metadata for source tracking.

Supports:
- Python files (.py)
- Markdown files (.md, .agent.md, .prompt.md)
- Agent definitions and prompts
"""

import glob
import os

from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

from chroma_ingestion.clients.chroma import get_chroma_client


class CodeIngester:
    """Intelligent code/document ingestion for Chroma with semantic splitting.

    This class handles:
    - Recursive file discovery (Python, Markdown, Agent files)
    - Code-aware or markdown-aware chunking
    - Batch upsert to Chroma Cloud
    - Metadata tracking (file path, chunk index, file type)
    """

    def __init__(
        self,
        target_folder: str,
        collection_name: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        file_patterns: list[str] | None = None,
    ):
        """Initialize the code ingester.

        Args:
            target_folder: Root folder to recursively scan for files
            collection_name: Name of Chroma collection to store chunks
            chunk_size: Approximate tokens per chunk (default: 1000)
            chunk_overlap: Token overlap between chunks (default: 200)
            file_patterns: File patterns to ingest (default: *.py, *.md, *.agent.md, *.prompt.md)
        """
        self.target_folder = target_folder
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.file_patterns = file_patterns or [
            "**/*.py",
            "**/*.md",
            "**/*.agent.md",
            "**/*.prompt.md",
        ]

        # Initialize Chroma client and collection
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(name=collection_name)

        # Configure splitter - use markdown for all files (more general)
        self.splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def discover_files(self) -> list[str]:
        """Discover files in target folder recursively.

        Returns:
            List of absolute paths to matching files
        """
        all_files = []
        for pattern in self.file_patterns:
            full_pattern = os.path.join(self.target_folder, pattern)
            files = glob.glob(full_pattern, recursive=True)
            all_files.extend(files)

        return sorted(list(set(all_files)))  # Remove duplicates and sort

    def ingest_files(self, batch_size: int = 100) -> tuple[int, int]:
        """Ingest files from target folder into Chroma.

        Uses semantic splitting to preserve document structure.
        Batch upserts to avoid memory limits.

        Args:
            batch_size: Number of chunks to upsert per batch

        Returns:
            Tuple of (total_files_processed, total_chunks_ingested)
        """
        py_files = self.discover_files()

        if not py_files:
            print(f"❌ No matching files found in: {self.target_folder}")
            return 0, 0

        print(f"📂 Scanning: {self.target_folder}")
        print(f"📦 Found {len(py_files)} file(s)")

        documents: list[str] = []
        ids: list[str] = []
        metadatas: list[dict] = []
        files_processed = 0

        # Process each file
        for file_path in py_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                # Create semantic chunks
                chunks = self.splitter.create_documents([content])

                if chunks:
                    files_processed += 1
                    for i, chunk in enumerate(chunks):
                        # Unique ID: filename + chunk index
                        doc_id = f"{os.path.basename(file_path)}:{i}"

                        documents.append(chunk.page_content)
                        ids.append(doc_id)
                        metadatas.append(
                            {
                                "source": file_path,
                                "filename": os.path.basename(file_path),
                                "chunk_index": i,
                                "folder": os.path.dirname(file_path),
                                "file_type": os.path.splitext(file_path)[1],
                            }
                        )

            except Exception as e:
                print(f"⚠️  Could not read {file_path}: {e}")

        # Batch upsert to Chroma Cloud
        if documents:
            print(f"🚀 Ingesting {len(documents)} chunks into Chroma Cloud...")

            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i : i + batch_size]
                batch_ids = ids[i : i + batch_size]
                batch_metas = metadatas[i : i + batch_size]

                self.collection.upsert(
                    documents=batch_docs,
                    ids=batch_ids,
                    metadatas=batch_metas,
                )
                print(f"  ✓ Batch {i // batch_size + 1} complete ({len(batch_docs)} chunks)")

            print(f"✅ Done! Ingested {len(documents)} chunks from {files_processed} file(s)")
            return files_processed, len(documents)
        else:
            print("❌ No documents created.")
            return files_processed, 0

    def get_collection_stats(self) -> dict:
        """Get statistics about the ingested collection.

        Returns:
            Dictionary with collection metadata
        """
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "total_chunks": count,
            "target_folder": self.target_folder,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
        }
