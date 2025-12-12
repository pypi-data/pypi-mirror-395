# Chroma Code Ingestion System - AI Coding Agent Instructions

## Project Overview

A semantic-aware code extraction and storage system that intelligently chunks code repositories and stores them in Chroma Cloud for AI agent retrieval and context generation. Designed to prepare large codebases for LLM-based agents to query and analyze patterns.

**Core Purpose:** Transform code/documentation into retrievable semantic chunks that AI agents can query with natural language.

**Tech Stack:**
- **Vector Database:** Chroma Cloud (distributed vector storage)
- **Text Splitting:** LangChain RecursiveCharacterTextSplitter (semantic-aware)
- **Configuration:** python-dotenv for environment management
- **Language Support:** Python, Markdown, Agent definitions, Prompts

---

## Critical Architecture Patterns

### 1. Singleton Client Pattern (MANDATORY)

The Chroma HttpClient must use a singleton pattern to avoid connection pool exhaustion:

```python
# ✅ CORRECT: Always use get_chroma_client()
from src.clients.chroma_client import get_chroma_client
client = get_chroma_client()  # Reused globally

# ❌ WRONG: Never create multiple clients
client = chromadb.HttpClient(host='localhost', port=9500)  # Creates new connection
```

**Why:** Maintains single connection, prevents resource leaks, consistent state.

**Key File:** `src/clients/chroma_client.py` (implements singleton with module-level `_client` variable)

### 2. Semantic Chunking Strategy

Always use **Markdown language splitter** for all file types (works for code, prose, documentation):

```python
splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size=1000,  # tokens, not characters
    chunk_overlap=200,  # preserves context across boundaries
)
```

**Why:** Respects document structure (headers, sections, code blocks) better than naive splitting.

**Key File:** `src/ingestion.py` (line 68-71)

### 3. Batch Upsert Pattern

Always batch ingestion to avoid timeout/memory errors:

```python
# Process in batches of 100-500 chunks
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    collection.upsert(documents=batch, ids=ids_batch, metadatas=meta_batch)
```

**Why:** Single large upsert can timeout or exceed memory limits. Chroma handles duplicates gracefully with `upsert()`.

**Key File:** `src/ingestion.py` (ingest_files method)

### 4. Rich Metadata Tracking

Every chunk must include metadata for filtering and source tracking:

```python
metadata = {
    "source": str(file_path),
    "filename": os.path.basename(file_path),
    "chunk_index": chunk_num,
    "folder": os.path.dirname(file_path),
    "file_type": os.path.splitext(file_path)[1],
}
```

**Why:** Enables source attribution, metadata-based filtering, debugging.

---

## Developer Workflows

### Ingestion Workflow

**Basic:** Ingest default folder (`vibe-tools/ghc_tools/agents`):
```bash
python ingest.py
```

**Custom folder:**
```bash
python ingest.py --folder /path/to/code --collection my_collection
```

**With verification:**
```bash
python ingest.py --verify  # Runs test queries post-ingestion
```

**Options:**
- `--chunk-size` (default 1000): Token size per chunk
- `--chunk-overlap` (default 200): Token overlap between chunks
- `--batch-size` (default 100): Chunks per batch upsert

**Key File:** `ingest.py` (command-line entry point)

### Retrieval Workflow

Query ingested chunks with semantic search:

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("agents_context")

# Basic semantic search
results = retriever.query("how do agents handle authentication?", n_results=3)

# High-confidence filtering
results = retriever.query_semantic(
    query_text="patterns",
    n_results=5,
    distance_threshold=0.5  # Only matches < 0.5 distance
)

# Metadata filtering
results = retriever.query_by_metadata(
    where={"file_type": ".md"},  # Filter by extension
    n_results=10
)
```

**Relevance Scale:**
- `distance` 0.0-0.3: Excellent match ⭐⭐⭐
- `distance` 0.3-0.5: Good match ⭐⭐
- `distance` 0.5-0.7: Weak match ⭐
- `distance` 0.7+: Poor match ❌

**Key Files:** `src/retrieval.py` (CodeRetriever class with query methods)

---

## Configuration & Environment

### Local Development (Defaults Work)

No `.env` needed for local development - uses hardcoded defaults:

```python
# src/config.py
CHROMA_HOST = "localhost"  # default
CHROMA_PORT = 9500         # default
```

### Production / Chroma Cloud

Set environment variables for cloud connection:

```bash
CHROMA_HOST=api.chroma.com
CHROMA_PORT=443
# Or use Chroma Cloud credentials if using HttpClient with auth
```

**Key File:** `src/config.py` (get_chroma_config function)

---

## Project Structure & File Roles

| File | Role |
|------|------|
| `src/clients/chroma_client.py` | Singleton HttpClient initialization & reset utility |
| `src/config.py` | Environment variable loading with sensible defaults |
| `src/ingestion.py` | CodeIngester: recursive file discovery, semantic splitting, batch upsert |
| `src/retrieval.py` | CodeRetriever: query, semantic search, metadata filtering |
| `ingest.py` | CLI entry point (argparse) for batch ingestion |
| `main.py` | Example usage (minimal) |
| `examples.py` | Reference queries and patterns for retrieval workflows |
| `BEST_PRACTICES.md` | Decision log: migration from Cloud to HttpClient, chunking strategy |

---

## Common Tasks & Patterns

### Task: Add Support for New File Type

1. **Update file patterns** in `CodeIngester.__init__`:
   ```python
   file_patterns = ["**/*.py", "**/*.md", "**/*.yaml"]  # Add .yaml
   ```

2. **Choose appropriate splitter:**
   - If semantic structure matters: Use `Language.MARKDOWN` (most general)
   - If language-specific: Use `Language.PYTHON`, `Language.YAML`, etc.

**Key File:** `src/ingestion.py` (lines 50-56)

### Task: Customize Chunk Size Strategy

Balance between:
- **Small chunks (500-800):** Higher precision, more retrieval calls needed
- **Medium chunks (1000-1500):** Sweet spot for most codebases
- **Large chunks (2000+):** Lower precision, fewer API calls

```python
ingester = CodeIngester(
    target_folder=".",
    collection_name="my_collection",
    chunk_size=1500,  # Adjust based on code density
    chunk_overlap=250,
)
```

### Task: Debug Ingestion Quality

Use `examples.py` pattern to test post-ingestion:

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("agents_context")

# Test domain-specific queries
test_queries = [
    "How do agents handle authentication?",
    "What are best practices for error handling?",
    "How do agents communicate with external services?",
]

for query in test_queries:
    results = retriever.query(query, n_results=3)
    print(f"Query: {query}")
    print(f"  Top match distance: {results[0]['distance'] if results else 'N/A'}")
```

---

## Known Gotchas & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| "Expected IDs to be unique" error | Running ingestion twice on same collection | Use `upsert()` not `add()` - handles duplicates |
| Large ingestion times out | Single large upsert exceeds timeout | Reduce batch_size (try 50 instead of 100) |
| Poor query relevance | Chunks too small or too large | Adjust chunk_size (1000-1500 typically optimal) |
| ConnectionError to localhost:9500 | Chroma server not running | Start server first: `chroma run` |
| Out of memory on large repos | Trying to process entire repo at once | Ingest by folder/collection (e.g., agents, schemas, services) |

---

## Integration Points & Dependencies

### External: Chroma Cloud
- **Purpose:** Vector storage and semantic search backend
- **Connection:** HttpClient (local or cloud)
- **Data Flow:** Chunks in → embeddings generated automatically → stored → searchable
- **Authentication:** Via environment variables or default localhost

### External: LangChain Text Splitters
- **Purpose:** Semantic-aware document chunking
- **Language Support:** Python, Markdown, YAML, JSON, HTML, LaTeX, Solidity, etc.
- **Configuration:** RecursiveCharacterTextSplitter.from_language()

### Cross-Module Communication
- `ingest.py` → `CodeIngester` (ingestion workflow)
- `CodeIngester` → `chroma_client.get_chroma_client()` (singleton initialization)
- Example code → `CodeRetriever` (query workflow)

---

## Testing & Verification

Built-in verification flag runs test queries post-ingestion:

```bash
python ingest.py --verify
```

This runs the queries defined in `examples.py` and reports semantic relevance scores. Look for:
- Distance scores < 0.5 for most matches (good quality)
- Consistent results across similar queries (semantic understanding)

---

## Performance Considerations

- **Ingestion Speed:** ~1000-2000 tokens/sec on typical hardware
- **Query Latency:** 200-500ms per query (network + embedding + search)
- **Storage:** ~1.5GB per 1M tokens in Chroma Cloud
- **Optimal Chunk Size:** 1000-1500 tokens for balanced precision/recall

---

## When to Use This System

✅ **Good For:**
- Building RAG (Retrieval-Augmented Generation) systems for agents
- Indexing large codebases for semantic discovery
- Creating searchable documentation/knowledge bases
- Agent pattern libraries (like vibe-tools/ghc_tools/agents)

❌ **Not For:**
- Real-time code changes (ingestion is batch-only)
- Full-text search (use PostgreSQL for that)
- Graph-based queries (Chroma is semantic-only)
