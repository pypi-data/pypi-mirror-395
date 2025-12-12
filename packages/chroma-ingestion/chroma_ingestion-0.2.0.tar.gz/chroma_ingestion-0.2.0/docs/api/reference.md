# API Reference

Complete reference for all public APIs in chroma-ingestion.

## Core Classes

### CodeIngester

The main class for ingesting code and documentation.

#### Constructor

```python
CodeIngester(
    target_folder: str,
    collection_name: str = "code_collection",
    file_patterns: list[str] | None = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
)
```

**Parameters:**

- `target_folder` (str, required) - Root directory to ingest files from
- `collection_name` (str, default="code_collection") - Name of Chroma collection
- `file_patterns` (list[str], optional) - Glob patterns for files to include. Defaults to common patterns
- `chunk_size` (int, default=1000) - Target tokens per chunk
- `chunk_overlap` (int, default=200) - Token overlap between chunks

**Example:**

```python
from chroma_ingestion import CodeIngester

ingester = CodeIngester(
    target_folder="/home/user/project",
    collection_name="myproject",
    chunk_size=1200,
    chunk_overlap=300
)
```

#### discover_files()

Find all files matching the configured patterns.

```python
files = ingester.discover_files() -> list[str]
```

**Returns:** List of absolute file paths

**Example:**

```python
files = ingester.discover_files()
print(f"Found {len(files)} files")
for f in files[:5]:
    print(f"  - {f}")
```

#### ingest_files()

Chunk and upload all files to Chroma.

```python
files, chunks = ingester.ingest_files(
    batch_size: int = 100
) -> tuple[int, int]
```

**Parameters:**

- `batch_size` (int, default=100) - Chunks per batch upload

**Returns:** Tuple of (files_processed, chunks_created)

**Example:**

```python
files, chunks = ingester.ingest_files(batch_size=50)
print(f"Processed {files} files, created {chunks} chunks")
```

**Raises:**

- `ConnectionError` - Cannot connect to Chroma server
- `ValueError` - No files found or invalid configuration

---

### AgentIngester

Specialized ingester for AI agent definitions.

#### Constructor

```python
AgentIngester(
    target_folder: str,
    collection_name: str = "agents",
    chunk_size: int = 1500,  # Larger default for agent files
    chunk_overlap: int = 300
)
```

**Parameters:** Same as CodeIngester, with larger defaults for agent documentation

**Example:**

```python
from chroma_ingestion import AgentIngester

agent_ingester = AgentIngester(
    target_folder="/path/to/agents",
    collection_name="agent_definitions"
)
```

#### ingest_files()

Same signature as CodeIngester.ingest_files()

---

### CodeRetriever

Query and retrieve chunks from a collection.

#### Constructor

```python
CodeRetriever(collection_name: str)
```

**Parameters:**

- `collection_name` (str, required) - Name of Chroma collection to query

**Example:**

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("myproject")
```

#### query()

Semantic search with optional distance threshold.

```python
results = retriever.query(
    query_text: str,
    n_results: int = 5,
    distance_threshold: float | None = None
) -> list[dict]
```

**Parameters:**

- `query_text` (str, required) - Search query
- `n_results` (int, default=5) - Number of results to return
- `distance_threshold` (float, optional) - Only return results with distance < threshold

**Returns:** List of result dicts with keys: `document`, `distance`, `metadata`

**Example:**

```python
results = retriever.query(
    "authentication flow",
    n_results=3,
    distance_threshold=0.4
)

for result in results:
    print(f"Distance: {result['distance']:.2f}")
    print(f"File: {result['metadata']['filename']}")
    print(f"Content: {result['document'][:100]}...")
```

#### query_semantic()

Alias for query() with emphasis on distance threshold.

```python
results = retriever.query_semantic(
    query_text: str,
    n_results: int = 5,
    distance_threshold: float = 0.5
) -> list[dict]
```

**Example:**

```python
# Only high-confidence matches
results = retriever.query_semantic(
    "JWT token validation",
    distance_threshold=0.3
)
```

#### query_by_metadata()

Query with metadata filtering.

```python
results = retriever.query_by_metadata(
    query_text: str,
    where: dict | None = None,
    n_results: int = 5
) -> list[dict]
```

**Parameters:**

- `query_text` (str, required) - Search query
- `where` (dict, optional) - Metadata filter conditions
- `n_results` (int, default=5) - Number of results

**Example:**

```python
# Only Python files
results = retriever.query_by_metadata(
    query_text="error handling",
    where={"file_type": ".py"},
    n_results=10
)

# Python or TypeScript files in api folder
results = retriever.query_by_metadata(
    query_text="routing",
    where={
        "file_type": {"$in": [".py", ".ts"]},
        "folder": "/app/api"
    },
    n_results=10
)
```

#### get_by_source()

Get all chunks from a specific file.

```python
results = retriever.get_by_source(
    filename: str
) -> list[dict]
```

**Parameters:**

- `filename` (str, required) - Filename to retrieve (e.g., "auth.py")

**Example:**

```python
auth_chunks = retriever.get_by_source("auth.py")
print(f"Found {len(auth_chunks)} chunks from auth.py")
```

#### get_collection_info()

Get metadata about the collection.

```python
info = retriever.get_collection_info() -> dict
```

**Returns:** Dict with keys: `name`, `count`, `metadata`

**Example:**

```python
info = retriever.get_collection_info()
print(f"Collection: {info['name']}")
print(f"Total chunks: {info['count']}")
```

---

### MultiCollectionSearcher

Search across multiple collections simultaneously.

#### Constructor

```python
MultiCollectionSearcher(collection_names: list[str])
```

**Parameters:**

- `collection_names` (list[str], required) - Names of collections to search

**Example:**

```python
from chroma_ingestion import MultiCollectionSearcher

searcher = MultiCollectionSearcher([
    "backend_code",
    "frontend_code",
    "documentation"
])
```

#### search()

Search across all collections.

```python
results = searcher.search(
    query_text: str,
    n_results: int = 5
) -> list[dict]
```

**Parameters:**

- `query_text` (str, required) - Search query
- `n_results` (int, default=5) - Results per collection

**Returns:** List of result dicts with additional `collection_name` field

**Example:**

```python
results = searcher.search("authentication", n_results=3)

for result in results:
    print(f"[{result['collection_name']}] {result['metadata']['filename']}")
```

#### search_with_weights()

Search with custom relevance weights per collection.

```python
results = searcher.search_with_weights(
    query_text: str,
    weights: dict[str, float] | None = None,
    n_results: int = 5
) -> list[dict]
```

**Parameters:**

- `query_text` (str, required) - Search query
- `weights` (dict, optional) - Collection name → weight mapping. Defaults to equal weights
- `n_results` (int, default=5) - Results per collection

**Example:**

```python
# Prioritize backend code over frontend
results = searcher.search_with_weights(
    "API authentication",
    weights={
        "backend_code": 0.6,
        "frontend_code": 0.3,
        "documentation": 0.1
    },
    n_results=5
)
```

---

## Module Functions

### get_chroma_client()

Get or create the singleton Chroma client.

```python
from chroma_ingestion import get_chroma_client

client = get_chroma_client() -> chromadb.HttpClient
```

**Returns:** Singleton HttpClient instance

**Example:**

```python
client = get_chroma_client()
collections = client.list_collections()
```

**Note:** Always use this instead of creating new HttpClient instances.

### list_collections()

List all available collections.

```python
from chroma_ingestion import list_collections

collections = list_collections() -> list[dict]
```

**Returns:** List of collection dicts with keys: `name`, `count`

**Example:**

```python
collections = list_collections()
for coll in collections:
    print(f"- {coll['name']} ({coll['count']} chunks)")
```

### delete_collection()

Delete a collection.

```python
from chroma_ingestion import delete_collection

delete_collection(collection_name: str) -> bool
```

**Parameters:**

- `collection_name` (str, required) - Name of collection to delete

**Returns:** True if successful

**Example:**

```python
if delete_collection("old_collection"):
    print("Collection deleted")
```

### reset_client()

Reset the singleton client (useful for testing).

```python
from chroma_ingestion import reset_client

reset_client() -> None
```

**Example:**

```python
reset_client()  # Forces new client on next get_chroma_client() call
```

---

## CLI Commands

The package provides CLI commands via Click:

```bash
# Ingest code
chroma-ingest --folder /path/to/code --collection myproject

# Search for chunks
chroma-search --collection myproject "authentication"

# Reset singleton client
chroma-reset-client

# List collections
chroma-list-collections
```

## Result Format

All query methods return results in this format:

```python
[
    {
        'document': str,           # Chunk text content
        'distance': float,         # Semantic distance (0=perfect match)
        'metadata': {
            'source': str,         # Full file path
            'filename': str,       # Base filename
            'chunk_index': int,    # Position in file
            'folder': str,         # Parent directory
            'file_type': str       # File extension
        },
        'collection_name': str     # Only in MultiCollectionSearcher
    },
    ...
]
```

## Error Handling

Common exceptions:

```python
try:
    ingester = CodeIngester("/nonexistent/path")
    ingester.ingest_files()
except ConnectionError:
    print("Cannot connect to Chroma server")
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Performance Notes

- **Query latency:** 200-500ms per query
- **Ingestion rate:** 1000-2000 tokens/sec
- **Batch size recommendation:** 50-200 chunks per batch
- **Memory per collection:** ~1.5GB per 1M tokens

## Type Hints

All APIs use complete type hints for IDE autocompletion:

```python
from chroma_ingestion import CodeIngester, CodeRetriever
from typing import Optional, Dict, List

# Full type support
results: List[Dict] = retriever.query("test", n_results=5)
info: Dict = retriever.get_collection_info()
```

## Next Steps

- 📝 [Basic Usage](../getting-started/basic-usage.md) - Get started
- 🔧 [Configuration](../getting-started/configuration.md) - Environment setup
- 📚 [Guides](../guides/ingestion-workflow.md) - Detailed walkthroughs
