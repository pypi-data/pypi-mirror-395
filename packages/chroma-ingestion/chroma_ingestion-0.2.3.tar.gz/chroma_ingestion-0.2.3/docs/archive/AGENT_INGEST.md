# Agent Ingestion & Consolidation Plan

## Executive Summary

Ingest 80+ agent definitions from 5 source folders into Chroma for semantic analysis, identify overlapping/duplicate agents, and consolidate into ~10 focused agents tailored to our tech stack (Next.js, React, Python, FastAPI, PostgreSQL, Playwright).

---

## Phase 1: Discovery & Inventory

### Source Folders

| Folder | Files | Description |
|--------|-------|-------------|
| `.github/agents` | 9 | Core debugging, planning, testing agents |
| `ccs/.claude/agents` | ~50 | Comprehensive agent library with subfolders |
| `ghc_tools/agents` | 23 | Enterprise tools and specialized agents |
| `scf/src/superclaude/agents` | 20 | SuperClaude framework agents |
| `SuperClaude_Framework/src/superclaude/agents` | 20 | **Skip** - duplicate of scf |

### Exclusion List (Irrelevant to Our Stack)

```python
EXCLUSIONS = [
    # Language-specific (not in our stack)
    "CSharpExpert.agent.md",
    "WinFormsExpert.agent.md",
    "swift-macos-expert.md",
    "golang-pro.md",
    "electron-pro.md",
    "mobile-developer.md",
    "c-pro.md",
    "cpp-pro.md",

    # Framework-specific (Svelte not in stack)
    "svelte-development.md",
    "svelte-storybook.md",
    "svelte-testing.md",

    # Enterprise tools (not in stack)
    "azure-devops-specialist.md",
    "octopus-deploy-release-notes-mcp.agent.md",
    "dynatrace-expert.agent.md",
    "amplitude-experiment-implementation.agent.md",
    "arm-migration.agent.md",
    "jfrog-sec.agent.md",
    "launchdarkly-flag-cleanup.agent.md",
    "pagerduty-incident-responder.agent.md",
    "stackhawk-security-onboarding.agent.md",
    "terraform.agent.md",
]
```

### Inclusion Categories

| Category | Example Files | Count |
|----------|---------------|-------|
| Frontend | nextjs-pro.md, react-pro.md, frontend-*.md | ~8 |
| Backend | python-*.md, backend-architect.md, fastapi | ~6 |
| Architecture | system-architect.md, project-architect.md | ~5 |
| Testing | playwright-tester.md, test-*.md, qa-expert.md | ~8 |
| AI/ML | ai-engineer.md, ml-engineer.md, prompt-engineer.md | ~5 |
| DevOps | devops-*.md, deployment-engineer.md, cloud-architect.md | ~6 |
| Security | security-*.md, code-auditor.md | ~3 |
| Quality | code-reviewer.md, refactoring-expert.md | ~5 |
| Database | postgresql-*.md, database-optimizer.md, neon-*.md | ~4 |
| Planning | task-planner.md, requirements-analyst.md, pm-agent.md | ~5 |

**Estimated Total After Filtering: ~55 agents**

---

## Phase 2: Enhanced Ingestion Pipeline

### 2.1 Create AgentIngester Class

Extend the existing `CodeIngester` with agent-specific features:

```python
# src/agent_ingestion.py

import re
import yaml
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from src.ingestion import CodeIngester


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
        "frontend": ["nextjs", "next.js", "react", "typescript", "tailwind", "css", "html", "ui", "ux"],
        "backend": ["python", "fastapi", "api", "rest", "graphql", "websocket", "middleware"],
        "database": ["postgresql", "postgres", "sql", "neon", "prisma", "sqlalchemy", "database"],
        "testing": ["playwright", "vitest", "jest", "testing", "test", "e2e", "unit", "integration"],
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
        source_folders: List[str],
        collection_name: str = "agents_analysis",
        chunk_size: int = 1500,  # Larger for agent files
        chunk_overlap: int = 300,
        exclusions: Optional[List[str]] = None,
    ):
        """Initialize agent ingester with multiple source folders."""
        self.source_folders = source_folders
        self.exclusions = exclusions or []

        # Initialize parent with first folder (we'll override discovery)
        super().__init__(
            target_folder=source_folders[0],
            collection_name=collection_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            file_patterns=["**/*.md", "**/*.agent.md", "**/*.prompt.md"],
        )

    def discover_files(self) -> List[str]:
        """Discover agent files across all source folders."""
        import glob
        import os

        all_files = []
        for folder in self.source_folders:
            for pattern in self.file_patterns:
                full_pattern = os.path.join(folder, pattern)
                files = glob.glob(full_pattern, recursive=True)
                all_files.extend(files)

        # Filter exclusions
        filtered = [
            f for f in all_files
            if os.path.basename(f) not in self.exclusions
            and "__init__.py" not in f
            and "README.md" not in os.path.basename(f)
        ]

        return sorted(list(set(filtered)))

    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter from agent file.

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
                except yaml.YAMLError:
                    pass

        return frontmatter, body

    def extract_tech_stack(self, content: str) -> List[str]:
        """Extract tech stack keywords from content."""
        content_lower = content.lower()
        found_tech = set()

        for category, keywords in self.TECH_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    found_tech.add(keyword)

        return list(found_tech)

    def classify_category(self, filename: str, content: str) -> str:
        """Classify agent into a category."""
        text = (filename + " " + content).lower()

        category_scores = {}
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            category_scores[category] = score

        # Return highest scoring category
        return max(category_scores, key=category_scores.get, default="general")

    def extract_metadata(self, file_path: str, content: str) -> Dict:
        """Extract rich metadata from agent file."""
        import os

        frontmatter, body = self.parse_frontmatter(content)
        filename = os.path.basename(file_path)

        # Parse agent name from filename or title
        agent_name = frontmatter.get("name", filename.replace(".md", "").replace(".agent", "").replace(".prompt", ""))

        metadata = {
            "source": file_path,
            "filename": filename,
            "agent_name": agent_name,
            "description": frontmatter.get("description", "")[:500],  # Truncate long descriptions
            "model": frontmatter.get("model", ""),
            "tools": ",".join(frontmatter.get("tools", [])) if frontmatter.get("tools") else "",
            "category": self.classify_category(filename, content),
            "tech_stack": ",".join(self.extract_tech_stack(content)),
            "folder": os.path.dirname(file_path),
            "file_type": os.path.splitext(file_path)[1],
            "source_collection": self._get_source_collection(file_path),
        }

        return metadata, body

    def _get_source_collection(self, file_path: str) -> str:
        """Identify which source collection a file belongs to."""
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

    def ingest_agents(self, batch_size: int = 50) -> Tuple[int, int]:
        """Ingest agent files with enhanced metadata.

        Returns:
            Tuple of (files_processed, chunks_ingested)
        """
        agent_files = self.discover_files()

        if not agent_files:
            print(f"❌ No agent files found")
            return 0, 0

        print(f"📂 Found {len(agent_files)} agent files across {len(self.source_folders)} folders")

        documents = []
        ids = []
        metadatas = []
        files_processed = 0

        for file_path in agent_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract enhanced metadata
                base_metadata, body = self.extract_metadata(file_path, content)

                # Create semantic chunks
                chunks = self.splitter.create_documents([content])  # Use full content for context

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
                print(f"⚠️  Could not process {file_path}: {e}")

        # Batch upsert
        if documents:
            print(f"🚀 Ingesting {len(documents)} chunks into collection '{self.collection_name}'...")

            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]
                batch_metas = metadatas[i:i + batch_size]

                self.collection.upsert(
                    documents=batch_docs,
                    ids=batch_ids,
                    metadatas=batch_metas,
                )
                print(f"  ✓ Batch {i // batch_size + 1} ({len(batch_docs)} chunks)")

            print(f"✅ Done! Ingested {len(documents)} chunks from {files_processed} agents")
            return files_processed, len(documents)

        return files_processed, 0
```

### 2.2 Enhanced Metadata Schema

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Full file path |
| `filename` | string | File name only |
| `agent_name` | string | Parsed agent name |
| `description` | string | From frontmatter (truncated) |
| `model` | string | Preferred model |
| `tools` | string | Comma-separated tools list |
| `category` | string | Classified category |
| `tech_stack` | string | Comma-separated tech keywords |
| `folder` | string | Parent folder |
| `file_type` | string | File extension |
| `source_collection` | string | Which source folder |
| `chunk_index` | int | Position in document |
| `total_chunks` | int | Total chunks for this agent |

---

## Phase 3: Ingestion Execution

### 3.1 Run Script

```python
# ingest_agents.py

from src.agent_ingestion import AgentIngester

# Source folders (relative to vibe-tools root)
SOURCE_FOLDERS = [
    "/home/ob/Development/Tools/vibe-tools/.github/agents",
    "/home/ob/Development/Tools/vibe-tools/ccs/.claude/agents",
    "/home/ob/Development/Tools/vibe-tools/ghc_tools/agents",
    "/home/ob/Development/Tools/vibe-tools/scf/src/superclaude/agents",
]

# Exclusions (not relevant to our stack)
EXCLUSIONS = [
    "CSharpExpert.agent.md",
    "WinFormsExpert.agent.md",
    "swift-macos-expert.md",
    "golang-pro.md",
    "electron-pro.md",
    "mobile-developer.md",
    "svelte-development.md",
    "svelte-storybook.md",
    "svelte-testing.md",
    "azure-devops-specialist.md",
    "octopus-deploy-release-notes-mcp.agent.md",
    "dynatrace-expert.agent.md",
    "amplitude-experiment-implementation.agent.md",
    "arm-migration.agent.md",
    "jfrog-sec.agent.md",
    "launchdarkly-flag-cleanup.agent.md",
    "pagerduty-incident-responder.agent.md",
    "stackhawk-security-onboarding.agent.md",
    "terraform.agent.md",
]

if __name__ == "__main__":
    ingester = AgentIngester(
        source_folders=SOURCE_FOLDERS,
        collection_name="agents_analysis",
        chunk_size=1500,
        chunk_overlap=300,
        exclusions=EXCLUSIONS,
    )

    files, chunks = ingester.ingest_agents(batch_size=50)
    print(f"\n📊 Summary: {files} files → {chunks} chunks")

    # Print stats
    stats = ingester.get_collection_stats()
    print(f"📦 Collection '{stats['collection_name']}' now has {stats['total_chunks']} total chunks")
```

### 3.2 Expected Output

```
📂 Found 55 agent files across 4 folders
🚀 Ingesting 220 chunks into collection 'agents_analysis'...
  ✓ Batch 1 (50 chunks)
  ✓ Batch 2 (50 chunks)
  ✓ Batch 3 (50 chunks)
  ✓ Batch 4 (50 chunks)
  ✓ Batch 5 (20 chunks)
✅ Done! Ingested 220 chunks from 55 agents

📊 Summary: 55 files → 220 chunks
📦 Collection 'agents_analysis' now has 220 total chunks
```

---

## Phase 4: Semantic Analysis

### 4.1 Analysis Queries

Create an analysis script to find overlaps and clusters:

```python
# analyze_agents.py

from src.retrieval import CodeRetriever
from collections import defaultdict

class AgentAnalyzer:
    """Analyze ingested agents for overlaps and consolidation opportunities."""

    def __init__(self, collection_name: str = "agents_analysis"):
        self.retriever = CodeRetriever(collection_name)

    def find_by_category(self, category: str, n_results: int = 20) -> list:
        """Find all agents in a category."""
        return self.retriever.query_by_metadata(
            where={"category": category},
            n_results=n_results
        )

    def find_by_tech_stack(self, tech: str, n_results: int = 20) -> list:
        """Find agents mentioning a specific technology."""
        return self.retriever.query_by_metadata(
            where_document={"$contains": tech},
            n_results=n_results
        )

    def find_similar_agents(self, query: str, n_results: int = 10) -> list:
        """Semantic search for similar agents."""
        return self.retriever.query_semantic(
            query_text=query,
            n_results=n_results,
            distance_threshold=0.4  # High similarity
        )

    def cluster_by_category(self) -> dict:
        """Group all agents by their classified category."""
        categories = ["frontend", "backend", "architecture", "testing",
                      "ai_ml", "devops", "security", "quality", "database", "planning"]

        clusters = {}
        for category in categories:
            results = self.find_by_category(category)
            # Extract unique agent names
            agents = list(set(r["metadata"]["agent_name"] for r in results))
            clusters[category] = agents

        return clusters

    def find_duplicates(self) -> dict:
        """Find agents with high semantic similarity (potential duplicates)."""
        duplicates = defaultdict(list)

        # Key queries to identify overlapping agents
        test_queries = [
            ("Next.js development best practices", "frontend"),
            ("Python backend API development", "backend"),
            ("System architecture design patterns", "architecture"),
            ("Automated testing with Playwright", "testing"),
            ("Machine learning engineering", "ai_ml"),
        ]

        for query, expected_category in test_queries:
            results = self.find_similar_agents(query, n_results=5)
            if len(results) > 1:
                agents = [r["metadata"]["agent_name"] for r in results]
                sources = [r["metadata"]["source_collection"] for r in results]
                duplicates[query] = list(zip(agents, sources))

        return duplicates

    def generate_consolidation_report(self) -> str:
        """Generate a report for consolidation decisions."""
        report = []
        report.append("# Agent Consolidation Report\n")

        # Category clusters
        clusters = self.cluster_by_category()
        report.append("## Agents by Category\n")
        for category, agents in clusters.items():
            if agents:
                report.append(f"### {category.title()} ({len(agents)} agents)")
                for agent in agents:
                    report.append(f"- {agent}")
                report.append("")

        # Duplicates
        duplicates = self.find_duplicates()
        report.append("\n## Potential Duplicates/Overlaps\n")
        for query, agents in duplicates.items():
            report.append(f"### Query: '{query}'")
            for agent, source in agents:
                report.append(f"- {agent} (from {source})")
            report.append("")

        return "\n".join(report)


if __name__ == "__main__":
    analyzer = AgentAnalyzer()

    print("=" * 60)
    print("AGENT ANALYSIS REPORT")
    print("=" * 60)

    # Print clusters
    clusters = analyzer.cluster_by_category()
    for category, agents in clusters.items():
        print(f"\n{category.upper()} ({len(agents)} agents):")
        for agent in agents[:5]:  # Show top 5
            print(f"  - {agent}")
        if len(agents) > 5:
            print(f"  ... and {len(agents) - 5} more")

    # Print duplicates
    print("\n" + "=" * 60)
    print("POTENTIAL DUPLICATES")
    print("=" * 60)
    duplicates = analyzer.find_duplicates()
    for query, agents in duplicates.items():
        print(f"\n{query}:")
        for agent, source in agents:
            print(f"  - {agent} ({source})")

    # Save full report
    report = analyzer.generate_consolidation_report()
    with open("CONSOLIDATION_REPORT.md", "w") as f:
        f.write(report)
    print("\n✅ Full report saved to CONSOLIDATION_REPORT.md")
```

### 4.2 Sample Analysis Queries

| Query | Purpose | Expected Findings |
|-------|---------|-------------------|
| "Next.js App Router Server Components" | Find frontend experts | nextjs-pro, expert-nextjs-developer, frontend-architect |
| "Python FastAPI backend development" | Find backend experts | python-pro, python-expert, backend-architect |
| "Playwright E2E testing" | Find testing experts | playwright-tester, test-engineer, qa-expert |
| "System architecture design" | Find architects | system-architect, project-architect, architecture-auditor |
| "AI ML engineering prompts" | Find AI experts | ai-engineer, ml-engineer, prompt-engineer |

---

## Phase 5: Consolidation Strategy

### 5.1 Target Agent Roles

Based on analysis, consolidate into these 10 focused agents:

| Target Agent | Source Agents | Focus Area |
|--------------|---------------|------------|
| **frontend-expert** | nextjs-pro, react-pro, expert-nextjs-developer, frontend-architect, frontend-developer, ui-designer | Next.js, React, TypeScript, UI/UX, Components |
| **backend-expert** | python-pro, python-expert, backend-architect, full-stack-developer | Python, FastAPI, APIs, Server logic |
| **architect-expert** | system-architect, project-architect, architecture-auditor, architecture-blueprint-generator | System design, Architecture decisions, Technical planning |
| **testing-expert** | playwright-tester, test-engineer, qa-expert, test-automator, debugger | Playwright, Vitest, E2E, Unit testing, Debugging |
| **ai-ml-expert** | ai-engineer, ml-engineer, data-scientist, prompt-engineer, python-ml-agent | AI/ML, LLMs, RAG, Embeddings, Prompts |
| **devops-expert** | devops-architect, deployment-engineer, cloud-architect, performance-engineer | Docker, Deployment, CI/CD, Performance |
| **security-expert** | security-engineer, security-auditor, code-auditor | Security auditing, Auth, Vulnerability scanning |
| **quality-expert** | code-reviewer, refactoring-expert, quality-engineer, self-review | Code review, Best practices, Refactoring |
| **database-expert** | postgresql-dba, database-optimizer, neon-migration-specialist, graphql-architect | PostgreSQL, SQL, Neon, Database optimization |
| **planning-expert** | task-planner, pm-agent, requirements-analyst, task-orchestrator, technical-writer | Planning, Requirements, Documentation, Tasks |

### 5.2 Consolidation Process

1. **Query agents by category** → Get all chunks for each target role
2. **Extract key sections** → Expertise, Guidelines, Scenarios from each source
3. **Merge intelligently**:
   - Combine expertise lists (deduplicate)
   - Merge guidelines (resolve conflicts)
   - Union common scenarios
   - Keep best tools lists
4. **Generate new agent file** with consolidated content
5. **Verify coverage** → Query new agent should match original queries

### 5.3 Consolidated Agent Template

```markdown
---
name: {target-agent-name}
description: {merged description from source agents}
model: sonnet
tools: [{union of all relevant tools}]
sources: [{list of source agents merged}]
---

# {Target Agent Name}

**Role**: {Comprehensive role description merged from sources}

**Expertise**: {Deduplicated expertise list}

## Core Competencies

{Merged from all source agents, organized by sub-topic}

## Guidelines

{Merged guidelines, conflicts resolved}

## Common Scenarios

{Union of all scenarios from source agents}

## MCP Integration

{Relevant MCP tools for this role}

## Response Style

{Merged response style guidelines}
```

---

## Execution Timeline

| Phase | Duration | Output |
|-------|----------|--------|
| Phase 1: Discovery | 30 min | Agent inventory, exclusion list finalized |
| Phase 2: Pipeline | 2 hours | `agent_ingestion.py` with enhanced metadata |
| Phase 3: Execution | 15 min | 55 agents → ~220 chunks in Chroma |
| Phase 4: Analysis | 1 hour | `CONSOLIDATION_REPORT.md` with clusters/duplicates |
| Phase 5: Consolidation | 3 hours | 10 consolidated agent files |

**Total: ~7 hours**

---

## Success Metrics

1. **Coverage**: All relevant technologies represented in consolidated agents
2. **Reduction**: 55+ agents → 10 focused agents (~80% reduction)
3. **Query Quality**: Semantic queries return relevant consolidated agent with distance < 0.3
4. **No Gaps**: Every source agent mapped to at least one target agent
5. **No Duplicates**: Single source of truth for each expertise area

---

## Next Steps

1. [ ] Create `src/agent_ingestion.py` with `AgentIngester` class
2. [ ] Create `ingest_agents.py` CLI script
3. [ ] Run ingestion and verify collection stats
4. [ ] Create `analyze_agents.py` for semantic analysis
5. [ ] Generate `CONSOLIDATION_REPORT.md`
6. [ ] Review report and finalize consolidation mapping
7. [ ] Generate 10 consolidated agent files
8. [ ] Test consolidated agents against sample queries
9. [ ] Archive or delete redundant source agents

---

## Files to Create

| File | Purpose |
|------|---------|
| `src/agent_ingestion.py` | AgentIngester class |
| `ingest_agents.py` | CLI for agent ingestion |
| `analyze_agents.py` | Semantic analysis and reporting |
| `CONSOLIDATION_REPORT.md` | Analysis output |
| `consolidated_agents/` | Folder for 10 new agents |
