# ChromaDB Integration Patterns & Learnings

## Date: December 2, 2025

### Core Integration Patterns

**Pattern 1: Basic Single Collection Query**
```python
from src.retrieval import CodeRetriever
retriever = CodeRetriever("collection_name")
results = retriever.query("search query", n_results=3)
```

**Pattern 2: Multi-Collection Ranked Search**
```python
from src.retrieval import MultiCollectionSearcher
searcher = MultiCollectionSearcher(["vibe_agents", "ghc_agents"])
results = searcher.search_ranked("query", n_results=5)
```

**Pattern 3: Context Injection for Prompts**
```python
context = searcher.get_context_multiway("query", n_results=2)
system_prompt = f"Reference this context:\n\n{context}\n\nNow..."
```

**Pattern 4: High-Precision Filtering**
```python
results = retriever.query_semantic(
    "query",
    n_results=5,
    distance_threshold=0.5  # Only excellent/good matches
)
```

**Pattern 5: Metadata-Based Filtering**
```python
results = retriever.query_by_metadata(
    where={"filename": "backend-architect.md"}
)
```

### Key Design Decisions

1. **Singleton Pattern for Client**
   - Avoids connection pool exhaustion
   - Maintains consistent state throughout app
   - Implemented in `get_chroma_client()`

2. **Environment Configuration**
   - Host and port from env vars with sensible defaults
   - Works locally without .env (uses localhost:9500)
   - Overridable for production deployments

3. **Semantic Chunking Strategy**
   - 1000 token chunks with 200 token overlap
   - Preserves document/code structure
   - Improves cross-chunk context retrieval

4. **Metadata Schema**
   - source, filename, chunk_index, folder, file_type
   - Enables filtering and source attribution
   - Essential for production quality

5. **Multi-Collection Architecture**
   - vibe_agents: Comprehensive agent library (868 chunks)
   - ghc_agents: GitHub Copilot specific (311 chunks)
   - superclaude_agents: SuperClaude patterns (137 chunks)
   - Total: ~1,800 chunks across focused domains

### Distance Threshold Guidance

- **0.0-0.3**: Excellent match (use as-is)
- **0.3-0.5**: Good match (recommended threshold)
- **0.5-0.7**: Weak match (filter with caution)
- **0.7+**: Poor match (generally exclude)

All test collections averaged ~1.0 distance on semantic queries.

### Error Handling Essentials

```python
try:
    results = retriever.query(query)
except ConnectionError:
    # ChromaDB server not running
    return fallback_context()
except ValueError:
    # Collection not found
    return list_available_collections()
except Exception as e:
    logger.error(f"Retrieval failed: {e}")
    return graceful_degradation()
```

### Integration Workflow

1. **Setup** (5 min)
   - Start ChromaDB: `uv run chroma run --port 9500`
   - Test connection: `uv run python connect.py`
   - Verify .env configuration

2. **Ingest** (10-30 min)
   - Run: `uv run python ingest.py --folder /data --collection name`
   - Verify chunks created
   - Test sample queries

3. **Integrate** (1-2 hours)
   - Create retriever module
   - Integrate into tool's query pipeline
   - Add error handling
   - Test end-to-end

4. **Validate** (30 min)
   - Run test queries
   - Verify relevance scores
   - Check source attribution
   - Performance baseline

5. **Document** (30 min)
   - Update README with collection info
   - Document query examples
   - Add troubleshooting guide
   - Note any special cases

### Scaling Considerations

- **Up to 10K chunks**: Single machine, no optimization needed
- **10K-100K chunks**: Consider batch query optimization
- **100K+ chunks**: May need clustering by domain
- **Real-time updates**: Re-ingest changed files regularly

### Migration Lessons (Cloud → Local)

- ✅ HttpClient simpler than CloudClient setup
- ✅ Local server provides better latency
- ✅ Connection pooling handled automatically
- ✅ All downstream code works without changes
- ✅ No credential management needed
- ⚠️ Server must be running before queries
- ⚠️ Port 9500 must be available

### Tools & Commands Reference

```bash
# Start ChromaDB server
uv run chroma run --port 9500

# Test connection
uv run python connect.py

# Ingest data
uv run python ingest.py --folder /data --collection name

# Query agents
uv run python agent_query.py "your query"

# Verify ingestion
uv run python examples.py
```

### Documentation Artifacts Created

1. **INTEGRATION.md** - Complete integration guide with patterns
2. **BEST_PRACTICES.md** - 10 best practice categories
3. **INTEGRATION_CHECKLIST.md** - Step-by-step implementation guide
4. **agent_query.py** - Working example of context injection

### Testing Results Summary

**vibe_agents (868 chunks)**
- Distance range: 0.89-1.17 (excellent)
- Coverage: Comprehensive agent definitions
- Quality: ⭐⭐⭐ Excellent

**ghc_agents (311 chunks)**
- Distance range: 0.98-1.34 (good)
- Coverage: GitHub Copilot specific
- Quality: ⭐⭐⭐ Excellent

**superclaude_agents (137 chunks)**
- Distance range: 0.98-1.31 (good)
- Coverage: Framework patterns
- Quality: ⭐⭐ Good

### Recommended Next Steps

1. Integrate into specific vibe-tools projects
2. Create domain-specific retrievers
3. Add monitoring/metrics for retrieval quality
4. Consider caching for frequent queries
5. Expand collections with project-specific knowledge
