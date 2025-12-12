# ChromaDB HttpClient Integration Guide

**For connecting to local ChromaDB server on port 9500**

## Quick Start

### 1. Ensure ChromaDB Server is Running

```bash
# In one terminal
uv run chroma run --port 9500
```

Wait for: `OpenTelemetry... (notice, not an error)`

### 2. Copy Connection Pattern

Use this in any Python script that needs to connect to ChromaDB:

```python
import chromadb

# Simple connection to local ChromaDB server
client = chromadb.HttpClient(host='localhost', port=9500)

# Get or create a collection
collection = client.get_or_create_collection(name="my_collection")

# You now have a fully functional ChromaDB client!
```

## Integration Patterns

### Pattern 1: Single Collection Query

```python
from src.clients.chroma_client import get_chroma_client
from src.retrieval import CodeRetriever

# Get authenticated client (reused singleton)
client = get_chroma_client()

# Initialize retriever for your collection
retriever = CodeRetriever("my_collection")

# Query for relevant context
results = retriever.query("how do I implement X?", n_results=3)

for result in results:
    print(f"Source: {result['metadata']['source']}")
    print(f"Content: {result['document']}")
```

### Pattern 2: Multi-Collection Search

```python
from src.retrieval import MultiCollectionSearcher

# Search across multiple collections at once
searcher = MultiCollectionSearcher([
    "vibe_agents",
    "ghc_agents",
    "superclaude_agents"
])

# Get ranked results across all collections
results = searcher.search_ranked("backend architecture", n_results=5)

for result in results:
    print(f"Collection: {result['collection']}")
    print(f"Relevance: {(1 - result['distance']):.1%}")
```

### Pattern 3: Context Injection into Prompts

```python
from src.retrieval import MultiCollectionSearcher

searcher = MultiCollectionSearcher(["vibe_agents", "ghc_agents"])

# Get formatted context ready for prompt injection
context = searcher.get_context_multiway(
    "error handling patterns",
    n_results=2
)

# Build your system prompt with context
system_prompt = f"""You are a code expert.
Reference the following patterns:

{context}

Now help the user..."""
```

### Pattern 4: Semantic Search with Filtering

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("vibe_agents")

# Only return highly relevant results (distance < 0.5)
results = retriever.query_semantic(
    "security best practices",
    n_results=5,
    distance_threshold=0.5  # Stricter filtering
)

# Results are pre-filtered for high relevance
for result in results:
    relevance_pct = (1 - result['distance']) * 100
    print(f"✓ {relevance_pct:.0f}% match: {result['metadata']['source']}")
```

### Pattern 5: Metadata-Based Filtering

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("vibe_agents")

# Get all chunks from a specific file
results = retriever.query_by_metadata(
    where={"filename": "backend-architect.md"}
)

# Or get chunks by file type
results = retriever.query_by_metadata(
    where={"file_type": ".md"}
)
```

## Configuration

### Environment Variables (Optional)

If you need a non-standard server location, create/update `.env`:

```bash
CHROMA_HOST=localhost      # Default: localhost
CHROMA_PORT=9500           # Default: 9500
```

The configuration loads from `src/config.py`:

```python
def get_chroma_config() -> dict:
    """Returns host and port from env vars (with defaults)"""
    host = os.getenv("CHROMA_HOST", "localhost")
    port = int(os.getenv("CHROMA_PORT", "9500"))
    return {"host": host, "port": port}
```

## Available Collections

Collections already ingested and ready to query:

| Collection | Contents | Chunks |
|-----------|----------|--------|
| `vibe_agents` | Comprehensive agent definitions (131 files) | 1,387 |
| `ghc_agents` | GitHub Copilot tools agents (23 files) | 311 |
| `superclaude_agents` | SuperClaude framework agents (21 files) | 137 |

**Total indexed:** ~1,835 chunks

## Ingesting Your Own Code

```bash
cd /home/ob/Development/Tools/chroma

# Ingest Python files, Markdown, and agent definitions
uv run python ingest.py \
    --folder /path/to/your/code \
    --collection my_project \
    --chunk-size 1000 \
    --chunk-overlap 200
```

## Troubleshooting

### "Connection refused" error

```
❌ Connection failed: [Errno 111] Connection refused
```

**Solution:** Make sure ChromaDB server is running:

```bash
uv run chroma run --port 9500
```

### "Collection not found" error

```
❌ Query failed: Collection my_collection not found
```

**Solution:** Check available collections:

```python
from src.clients.chroma_client import get_chroma_client
client = get_chroma_client()
collections = client.list_collections()
print([c.name for c in collections])
```

### No results returned

Possible causes:

1. **Empty collection** - Check with `collection.count()`
2. **Poor query match** - Try different keywords or use `query_semantic()` with lower threshold
3. **Large distance threshold** - Lower the `distance_threshold` parameter

## Advanced Usage

### Streaming Results

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("vibe_agents")

# Get many results and process in batches
all_results = retriever.query("patterns", n_results=20)

for batch in [all_results[i:i+5] for i in range(0, len(all_results), 5)]:
    process_batch(batch)
```

### Custom Distance Weighting

```python
# Scores range 0-1 where 0 = perfect match, 1 = no match
results = retriever.query("my query", n_results=10)

# Rank by relevance percentage instead of raw distance
ranked = sorted(results, key=lambda r: r["distance"])
for result in ranked[:3]:
    relevance = (1 - result["distance"]) * 100
    print(f"{relevance:.0f}% match")
```

## API Reference

### CodeRetriever

```python
class CodeRetriever:
    query(query_text, n_results=3)              # Basic semantic search
    query_semantic(query_text, n_results=5,
                   distance_threshold=0.5)      # Semantic + filtering
    query_by_metadata(where=None,
                      where_document=None)      # Metadata filtering
    get_context(query_text, n_results=3,
                include_metadata=True)          # For prompt injection
    get_by_source(filename)                     # Get all chunks from file
    get_collection_info()                       # Collection statistics
```

### MultiCollectionSearcher

```python
class MultiCollectionSearcher:
    search_all(query_text, n_results=3)         # Search all collections
    search_ranked(query_text, n_results=5)      # Ranked results
    get_context_multiway(query_text,
                         n_results=2)           # Multi-source context
```

## Examples

See these scripts for working examples:

- **`agent_query.py`** - Query agent definitions and inject into prompts
- **`examples.py`** - Verify ingestion quality
- **`connect.py`** - Test server connectivity

## Next Steps

1. ✅ Start ChromaDB server: `uv run chroma run --port 9500`
2. ✅ Test connection: `uv run python connect.py`
3. ✅ Query agents: `uv run python agent_query.py "your query"`
4. ✅ Integrate into your project using patterns above

## Support

For issues or questions:
- Check `.env` configuration
- Verify ChromaDB server is running and accessible
- Review error messages for specific collection/query issues
- See `src/retrieval.py` for complete implementation details
