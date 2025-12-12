# ChromaDB Best Practices Guide

**Lessons learned from Chroma Cloud → Local Server migration**

## 1. Connection Architecture

### ✅ DO: Use Singleton Pattern

```python
# ✅ GOOD: Singleton ensures one connection throughout app
from src.clients.chroma_client import get_chroma_client

client = get_chroma_client()  # Reused globally
```

**Why:** Avoids connection pool exhaustion and maintains consistent state.

### ❌ DON'T: Create Multiple Clients

```python
# ❌ BAD: Creates new connection each time
def query_docs():
    client = chromadb.HttpClient(host='localhost', port=9500)
    return client.query(...)
```

### Configuration Best Practice

Store connection parameters in environment with sensible defaults:

```python
# src/config.py pattern
def get_chroma_config() -> dict:
    host = os.getenv("CHROMA_HOST", "localhost")
    port = int(os.getenv("CHROMA_PORT", "9500"))
    return {"host": host, "port": port}
```

**Benefits:**
- Works locally with defaults (no `.env` needed for dev)
- Production can override via environment variables
- Testable with different configurations

---

## 2. Ingestion Strategies

### ✅ DO: Use Semantic Chunking

```python
# ✅ GOOD: Respects code/document structure
splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size=1000,
    chunk_overlap=200,
)
```

**Why:** Preserves context across chunk boundaries and improves retrieval quality.

### ✅ DO: Batch Upserts

```python
# ✅ GOOD: Batch in groups of 100-500 to avoid memory issues
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    collection.upsert(documents=batch, ids=ids_batch, metadatas=meta_batch)
```

**Why:** Large single upserts can timeout or exceed memory limits.

### ✅ DO: Include Rich Metadata

```python
metadata = {
    "source": file_path,
    "filename": os.path.basename(file_path),
    "chunk_index": i,
    "folder": os.path.dirname(file_path),
    "file_type": os.path.splitext(file_path)[1],
}
```

**Why:** Enables filtering, source tracking, and debugging.

### ❌ DON'T: Reingest Without Deduplication

```python
# ❌ BAD: Causes "Expected IDs to be unique" errors
ingest.py --folder code --collection agents
ingest.py --folder code --collection agents  # Duplicate run = error
```

**Solution:** Use `upsert()` not `add()` - it handles duplicates automatically.

---

## 3. Query Strategies

### ✅ DO: Use Semantic Search for Discovery

```python
# ✅ GOOD: Natural language queries work well
results = retriever.query("how do I implement authentication?", n_results=3)
```

**Why:** Semantic search understands intent, not just keywords.

### ✅ DO: Filter for High Relevance

```python
# ✅ GOOD: Filter out weak matches
results = retriever.query_semantic(
    query_text="patterns",
    n_results=5,
    distance_threshold=0.5  # Only 50% match or better
)
```

**Relevance guide:**
- `distance` 0.0-0.3: Excellent match ⭐⭐⭐
- `distance` 0.3-0.5: Good match ⭐⭐
- `distance` 0.5-0.7: Weak match ⭐
- `distance` 0.7+: Poor match ❌

### ✅ DO: Search Multiple Collections

```python
# ✅ GOOD: Get comprehensive results
searcher = MultiCollectionSearcher(["vibe_agents", "ghc_agents"])
results = searcher.search_ranked(query, n_results=5)
```

**Why:** Avoids missing relevant content in other collections.

### ✅ DO: Combine Semantic + Metadata Filtering

```python
# ✅ GOOD: Two-level filtering for precision
results = retriever.query_semantic(query, n_results=10)
filtered = [r for r in results if r["metadata"]["file_type"] == ".md"]
```

**Why:** Reduces irrelevant results while preserving semantic understanding.

### ❌ DON'T: Rely on Keyword Matching

```python
# ❌ BAD: Misses variations and context
where_document={"$contains": "backend"}  # Literal string match only
```

**Better:** Use semantic search which understands synonyms and intent.

---

## 4. Prompt Injection Patterns

### ✅ DO: Format Context Clearly

```python
# ✅ GOOD: Clear source attribution
context = f"""
--- From {result['metadata']['source']} ---
{result['document']}

--- From {result['metadata']['source']} ---
{result['document']}
"""
```

**Why:** Helps AI understand and cite sources accurately.

### ✅ DO: Use get_context() Helper

```python
# ✅ GOOD: Built-in formatting
context = retriever.get_context("your query", n_results=3)
prompt = f"Consider this context:\n\n{context}\n\nNow answer..."
```

### ✅ DO: Include Source Headers

```python
# ✅ GOOD: Traceable injection
system_prompt = f"""You are a backend architect.
Reference these patterns:

{searcher.get_context_multiway(query)}

Now design the system..."""
```

### ❌ DON'T: Inject Without Attribution

```python
# ❌ BAD: AI might confabulate sources
prompt = f"Use this knowledge: {result['document']}"
```

---

## 5. Performance Optimization

### Connection Pooling

ChromaDB HttpClient handles connection pooling automatically. For high-volume use:

```python
# The singleton pattern handles this naturally
client = get_chroma_client()  # Reused across all requests
```

### Query Performance Tips

```python
# ✅ DO: Limit initial results
results = retriever.query(query, n_results=10)  # Get more, then filter

# ✅ DO: Use metadata filters first
results = retriever.query_by_metadata(where={"file_type": ".md"})
# Then semantic search on subset

# ❌ DON'T: Query with huge n_results
results = retriever.query(query, n_results=1000)  # Slow!
```

### Batch Processing

```python
# ✅ GOOD: Process large datasets in batches
queries = ["pattern1", "pattern2", "pattern3", ...]
for batch in [queries[i:i+10] for i in range(0, len(queries), 10)]:
    for q in batch:
        results = searcher.search_ranked(q, n_results=3)
        process(results)
```

---

## 6. Error Handling

### ✅ DO: Handle Connection Errors Gracefully

```python
try:
    client = get_chroma_client()
    results = retriever.query(query)
except ConnectionError as e:
    print("❌ ChromaDB server not running. Start with: uv run chroma run --port 9500")
    # Fallback or retry logic
except Exception as e:
    print(f"❌ Query failed: {e}")
    return []  # Graceful degradation
```

### ✅ DO: Validate Collection Exists

```python
try:
    collection = client.get_collection(name="my_collection")
except ValueError:
    print(f"Collection 'my_collection' not found")
    print(f"Available: {[c.name for c in client.list_collections()]}")
```

### ✅ DO: Check Results Quality

```python
results = retriever.query(query, n_results=5)

if not results:
    print("⚠️  No results found - try different query")
elif all(r["distance"] > 0.7 for r in results):
    print("⚠️  Results have low relevance - consider broader search")
```

---

## 7. Metadata Design

### Recommended Metadata Schema

```python
metadata = {
    "source": str,           # Full file path
    "filename": str,         # Basename for display
    "chunk_index": int,      # Position in file
    "folder": str,           # Directory path
    "file_type": str,        # .py, .md, etc.
    # Optional domain-specific:
    "category": str,         # "agent", "tool", "pattern"
    "agent_type": str,       # "frontend", "backend", etc.
    "version": str,          # For versioned content
}
```

### Query by Metadata Examples

```python
# By file type
results = retriever.query_by_metadata(where={"file_type": ".md"})

# By category (custom field)
results = retriever.query_by_metadata(where={"category": "agent"})

# By folder
results = retriever.query_by_metadata(where={"folder": {"$contains": "agents"}})

# Combine: file type AND agent type
results = retriever.query_by_metadata(
    where={
        "$and": [
            {"file_type": ".md"},
            {"agent_type": "backend"}
        ]
    }
)
```

---

## 8. Collection Management

### Naming Convention

```
vibe_agents              # Comprehensive agent library
ghc_agents               # GitHub Copilot specific agents
superclaude_agents       # SuperClaude framework agents
project_codebase         # Project-specific code
patterns_security        # Domain-specific patterns
```

### When to Create New Collections

✅ **DO create new collection when:**
- Content domain is distinct (agents vs. patterns vs. code)
- You need to version content separately
- Query patterns differ significantly

❌ **DON'T create new collection for:**
- Same content in different formats (use metadata instead)
- Minor organizational groupings (use folder metadata)

### Collection Cleanup

```python
# List all collections
collections = client.list_collections()
for c in collections:
    print(f"{c.name}: {c.count()} chunks")

# Delete unused collection
client.delete_collection(name="old_collection")

# Verify deletion
assert "old_collection" not in [c.name for c in client.list_collections()]
```

---

## 9. Testing & Validation

### Unit Test Pattern

```python
def test_query_returns_results():
    retriever = CodeRetriever("test_collection")
    results = retriever.query("test query", n_results=1)

    assert len(results) > 0, "Should return at least one result"
    assert "document" in results[0]
    assert "metadata" in results[0]
    assert "distance" in results[0]

def test_semantic_filters_by_distance():
    retriever = CodeRetriever("test_collection")
    results = retriever.query_semantic(
        "test",
        n_results=5,
        distance_threshold=0.5
    )

    assert all(r["distance"] <= 0.5 for r in results)
```

### Integration Test Pattern

```python
def test_multi_collection_search():
    searcher = MultiCollectionSearcher(["vibe_agents", "ghc_agents"])
    results = searcher.search_ranked("architect", n_results=3)

    assert len(results) > 0
    assert all("collection" in r for r in results)
    # Verify results are ranked by relevance
    distances = [r["distance"] for r in results]
    assert distances == sorted(distances)
```

---

## 10. Migration Checklist

When migrating from Chroma Cloud to local HttpClient:

- [ ] Update `.env` files with `CHROMA_HOST` and `CHROMA_PORT`
- [ ] Update `src/config.py` to load new variables
- [ ] Update `src/clients/chroma_client.py` to use `HttpClient`
- [ ] Start local ChromaDB server on port 9500
- [ ] Test connection with `python connect.py`
- [ ] Verify all collections migrated or re-ingested
- [ ] Run verification queries on each collection
- [ ] Update deployment documentation
- [ ] Test in staging environment first
- [ ] Update monitoring/logging for new connection type

---

## Key Takeaways

1. **Connection**: Use singleton + environment variables
2. **Ingestion**: Semantic chunks + batch upserts + rich metadata
3. **Querying**: Multi-level filtering (semantic + metadata)
4. **Injection**: Clear formatting with source attribution
5. **Performance**: Small result sets, filter early
6. **Reliability**: Graceful error handling + validation
7. **Organization**: Meaningful collection names + metadata schema
8. **Testing**: Unit + integration tests for retrieval quality

---

## References

- ChromaDB Documentation: https://docs.trychroma.com/
- LangChain Splitters: https://python.langchain.com/docs/modules/data_connection/text_splitters/
- Semantic Search: https://docs.trychroma.com/usage-guide#querying-a-collection
