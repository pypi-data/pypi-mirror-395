"""Agent-specific ingestion with enhanced metadata extraction.

Extends CodeIngester with agent-aware features:
- YAML frontmatter parsing
- Tech stack keyword extraction
- Category classification
- Rich metadata for semantic analysis
"""

import glob
import os

import yaml

from chroma_ingestion.ingestion.base import CodeIngester


class AgentIngester(CodeIngester):
    """Specialized ingester for agent definition files.

    Extracts structured metadata from agent frontmatter and content:
    - Frontmatter parsing (YAML)
    - Tech stack keyword extraction
    - Category classification
    - Section-aware chunking
    """

    # Tech stack keywords to extract
    TECH_KEYWORDS = {
        "frontend": [
            "nextjs",
            "next.js",
            "react",
            "typescript",
            "tailwind",
            "css",
            "html",
            "ui",
            "ux",
        ],
        "backend": ["python", "fastapi", "api", "rest", "graphql", "websocket", "middleware"],
        "database": ["postgresql", "postgres", "sql", "neon", "prisma", "sqlalchemy", "database"],
        "testing": [
            "playwright",
            "vitest",
            "jest",
            "testing",
            "test",
            "e2e",
            "unit",
            "integration",
        ],
        "ai_ml": ["ai", "ml", "machine learning", "llm", "embeddings", "vector", "rag", "prompt"],
        "devops": ["docker", "deployment", "ci/cd", "kubernetes", "vercel", "railway", "cloud"],
        "security": ["security", "auth", "authentication", "jwt", "oauth", "vulnerability"],
    }

    # Category classification keywords
    CATEGORY_KEYWORDS = {
        "frontend": ["frontend", "react", "nextjs", "ui", "ux", "component"],
        "backend": ["backend", "api", "python", "fastapi", "server"],
        "architecture": ["architect", "system", "design", "infrastructure"],
        "testing": ["test", "qa", "quality", "playwright", "debug"],
        "ai_ml": ["ai", "ml", "data", "engineer", "scientist", "prompt"],
        "devops": ["devops", "deploy", "cloud", "incident", "performance"],
        "security": ["security", "audit", "vulnerability"],
        "quality": ["review", "refactor", "code quality", "best practice"],
        "database": ["database", "sql", "postgres", "neon", "graphql"],
        "planning": ["plan", "requirement", "pm", "product", "task"],
    }

    def __init__(
        self,
        source_folders: list[str],
        collection_name: str = "agents_analysis",
        chunk_size: int = 1500,  # Larger for agent files
        chunk_overlap: int = 300,
        exclusions: list[str] | None = None,
    ):
        """Initialize agent ingester with multiple source folders.

        Args:
            source_folders: List of absolute paths to agent folders
            collection_name: Name of Chroma collection
            chunk_size: Tokens per chunk (larger for agents)
            chunk_overlap: Token overlap between chunks
            exclusions: List of filenames to exclude
        """
        self.source_folders = source_folders
        self.exclusions = exclusions or []

        # Initialize parent with first folder (we'll override discovery)
        super().__init__(
            target_folder=source_folders[0] if source_folders else ".",
            collection_name=collection_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            file_patterns=["**/*.md", "**/*.agent.md", "**/*.prompt.md"],
        )

    def discover_files(self) -> list[str]:
        """Discover agent files across all source folders.

        Returns:
            Sorted list of unique absolute file paths
        """
        all_files = []
        for folder in self.source_folders:
            for pattern in self.file_patterns:
                full_pattern = os.path.join(folder, pattern)
                files = glob.glob(full_pattern, recursive=True)
                all_files.extend(files)

        # Filter exclusions and duplicates
        filtered = [
            f
            for f in all_files
            if (
                os.path.basename(f) not in self.exclusions
                and "__init__.py" not in f
                and "README.md" not in os.path.basename(f)
            )
        ]

        return sorted(list(set(filtered)))

    def parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """Parse YAML frontmatter from agent file.

        Args:
            content: Full file content

        Returns:
            Tuple of (frontmatter_dict, remaining_content)
        """
        frontmatter = {}
        body = content

        # Check for YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except yaml.YAMLError as e:
                    print(f"  ⚠️  YAML parse error: {e}")

        return frontmatter, body

    def extract_tech_stack(self, content: str) -> list[str]:
        """Extract tech stack keywords from content.

        Args:
            content: Full file content

        Returns:
            List of identified tech keywords
        """
        content_lower = content.lower()
        found_tech = set()

        for category, keywords in self.TECH_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    found_tech.add(keyword)

        return sorted(list(found_tech))

    def classify_category(self, filename: str, content: str) -> str:
        """Classify agent into a category.

        Args:
            filename: Agent filename
            content: Full file content

        Returns:
            Classified category name
        """
        text = (filename + " " + content).lower()

        category_scores = {}
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            category_scores[category] = score

        # Return highest scoring category
        return max(category_scores, key=category_scores.get, default="general")

    def extract_metadata(self, file_path: str, content: str) -> tuple[dict, str]:
        """Extract rich metadata from agent file.

        Args:
            file_path: Absolute file path
            content: Full file content

        Returns:
            Tuple of (metadata_dict, body_content)
        """
        frontmatter, body = self.parse_frontmatter(content)
        filename = os.path.basename(file_path)

        # Parse agent name from filename or title
        agent_name = frontmatter.get(
            "name",
            filename.replace(".md", "").replace(".agent", "").replace(".prompt", ""),
        )

        metadata = {
            "source": file_path,
            "filename": filename,
            "agent_name": agent_name,
            "description": frontmatter.get("description", "")[:500],  # Truncate
            "model": frontmatter.get("model", ""),
            "tools": ",".join(frontmatter.get("tools", [])) if frontmatter.get("tools") else "",
            "category": self.classify_category(filename, content),
            "tech_stack": ",".join(
                self.extract_tech_stack(content)
            ),  # Chroma requires string, not list
            "folder": os.path.dirname(file_path),
            "file_type": os.path.splitext(file_path)[1],
            "source_collection": self._get_source_collection(file_path),
        }

        return metadata, body

    def _get_source_collection(self, file_path: str) -> str:
        """Identify which source collection a file belongs to.

        Args:
            file_path: Absolute file path

        Returns:
            Source collection name
        """
        if ".github/agents" in file_path:
            return "github_agents"
        elif "ccs/.claude/agents" in file_path:
            return "ccs_claude"
        elif "ghc_tools/agents" in file_path:
            return "ghc_tools"
        elif "scf/src/superclaude" in file_path:
            return "superclaude"
        else:
            return "unknown"

    def ingest_agents(self, batch_size: int = 50, verbose: bool = True) -> tuple[int, int]:
        """Ingest agent files with enhanced metadata.

        Args:
            batch_size: Chunks per batch upsert
            verbose: Print progress messages

        Returns:
            Tuple of (files_processed, chunks_ingested)
        """
        agent_files = self.discover_files()

        if not agent_files:
            if verbose:
                print("❌ No agent files found")
            return 0, 0

        if verbose:
            print(
                f"📂 Found {len(agent_files)} agent files across {len(self.source_folders)} folders"
            )

        documents = []
        ids = []
        metadatas = []
        files_processed = 0
        files_failed = 0

        for file_path in agent_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                # Extract enhanced metadata
                base_metadata, body = self.extract_metadata(file_path, content)

                # Create semantic chunks
                chunks = self.splitter.create_documents([content])

                if chunks:
                    files_processed += 1
                    for i, chunk in enumerate(chunks):
                        doc_id = f"{base_metadata['agent_name']}:{i}"

                        # Add chunk-specific metadata
                        chunk_metadata = {
                            **base_metadata,
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                        }

                        documents.append(chunk.page_content)
                        ids.append(doc_id)
                        metadatas.append(chunk_metadata)

            except Exception as e:
                files_failed += 1
                if verbose:
                    print(f"  ⚠️  Could not process {os.path.basename(file_path)}: {e}")

        # Batch upsert
        if documents:
            if verbose:
                print(
                    f"🚀 Ingesting {len(documents)} chunks into collection '{self.collection_name}'..."
                )

            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i : i + batch_size]
                batch_ids = ids[i : i + batch_size]
                batch_metas = metadatas[i : i + batch_size]

                self.collection.upsert(
                    documents=batch_docs,
                    ids=batch_ids,
                    metadatas=batch_metas,
                )
                if verbose:
                    print(f"  ✓ Batch {i // batch_size + 1} ({len(batch_docs)} chunks)")

            if verbose:
                print(f"✅ Done! Ingested {len(documents)} chunks from {files_processed} agents")
                if files_failed > 0:
                    print(f"⚠️  {files_failed} files failed to process")

            return files_processed, len(documents)

        if verbose:
            print("❌ No documents created.")
        return files_processed, 0
