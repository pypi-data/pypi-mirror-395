# ChromaDB Integration Checklist for New Tools

**Step-by-step guide for adding ChromaDB to new projects in vibe-tools ecosystem**

## Phase 1: Setup & Configuration

### Step 1: Choose Your Data Sources
- [ ] Identify what content to ingest (code, docs, agent definitions)
- [ ] Estimate content volume (will inform chunk size)
- [ ] Plan collection name(s) based on content domain
- [ ] Document metadata schema for your domain

**Example:**
```
Collection: myproject_agents
Content: Agent definitions from my project
Chunk strategy: 1000 tokens with 200 overlap
Metadata: source, filename, agent_type, version
```

### Step 2: Environment Configuration
- [ ] Copy `.env.example` to `.env` (or ensure it's in `.env.local`)
- [ ] Verify or set these variables:
  ```
  CHROMA_HOST=localhost
  CHROMA_PORT=9500
  ```
- [ ] Test connection: `uv run python connect.py`
- [ ] Confirm no errors (message about OpenTelemetry is OK)

### Step 3: Choose Integration Pattern
- [ ] Decide on retrieval pattern (see INTEGRATION.md):
  - Single collection queries?
  - Multi-collection search?
  - Metadata-filtered queries?
  - Context injection into prompts?

---

## Phase 2: Ingestion Setup

### Step 4: Prepare Data
- [ ] Organize source files in a directory
- [ ] Supported formats: `.py`, `.md`, `.agent.md`, `.prompt.md`
- [ ] Validate files are UTF-8 encoded
- [ ] Create sample test file to verify ingestion works

**Directory structure:**
```
/my/data/
├── agent1.md
├── agent2.md
├── patterns/
│   └── pattern1.md
└── docs/
    └── readme.md
```

### Step 5: Initial Ingestion
- [ ] Run test ingestion on small subset:
  ```bash
  uv run python ingest.py \
    --folder /my/data \
    --collection myproject_test \
    --chunk-size 1000 \
    --chunk-overlap 200
  ```
- [ ] Verify no errors in output
- [ ] Check collection created: `uv run python connect.py`
- [ ] Run test query: `uv run python examples.py`

### Step 6: Verify Ingestion Quality
- [ ] Check chunk count is reasonable (not too few, not too many)
- [ ] Run 3-5 test queries to verify relevance
- [ ] Review metadata for each result
- [ ] Confirm source paths are correct

**Test queries to verify:**
```python
test_queries = [
    "main topic of your content",
    "specific feature or concept",
    "problem your content solves",
]
```

---

## Phase 3: Integration Implementation

### Step 7: Create Your Retriever Module
- [ ] Create `src/retrievers/myproject_retriever.py`
- [ ] Import CodeRetriever or MultiCollectionSearcher
- [ ] Implement custom query methods if needed
- [ ] Add domain-specific search logic

**Template:**
```python
from src.retrieval import CodeRetriever, MultiCollectionSearcher

class MyProjectRetriever:
    def __init__(self):
        self.retriever = CodeRetriever("myproject_agents")

    def get_agent_context(self, agent_name: str):
        """Get context for a specific agent"""
        return self.retriever.query_semantic(agent_name, n_results=2)
```

### Step 8: Integrate into Your Tool
- [ ] Import retriever in your main module
- [ ] Use `get_context()` for prompt injection
- [ ] Pass context through system prompt
- [ ] Test end-to-end with real queries

**Example usage:**
```python
from src.retrievers.myproject_retriever import MyProjectRetriever

retriever = MyProjectRetriever()
context = retriever.get_agent_context("backend architect")
prompt = build_system_prompt_with_context(context)
```

### Step 9: Add Error Handling
- [ ] Wrap retriever calls in try/except
- [ ] Handle "server not running" gracefully
- [ ] Handle "collection not found" with helpful message
- [ ] Provide fallback behavior if retrieval fails

```python
try:
    context = retriever.get_context(query)
except ConnectionError:
    print("ChromaDB server not running")
    context = "No context available"
except Exception as e:
    logger.error(f"Retrieval failed: {e}")
    context = ""
```

---

## Phase 4: Testing & Validation

### Step 10: Unit Tests
- [ ] Write test for basic query functionality
- [ ] Test metadata filtering works correctly
- [ ] Test semantic search with various queries
- [ ] Test multi-collection search if applicable

```python
def test_retriever_returns_results():
    retriever = MyProjectRetriever()
    results = retriever.get_agent_context("test")
    assert len(results) > 0
    assert all("document" in r for r in results)
```

### Step 11: Integration Tests
- [ ] Test retriever with actual system prompt injection
- [ ] Verify AI responses include cited sources
- [ ] Test with production-like queries
- [ ] Verify performance is acceptable

### Step 12: Quality Validation
- [ ] Run full verification: `uv run python verify_ingestion.py`
- [ ] Check average relevance scores
- [ ] Review sample queries and results
- [ ] Document any special cases or limitations

---

## Phase 5: Documentation & Deployment

### Step 13: Document Your Integration
- [ ] Create `RETRIEVAL.md` for your module
- [ ] Document available collections
- [ ] Provide example queries
- [ ] Document any custom metadata fields

**Content to include:**
- What collections are available
- Example queries that work well
- Performance characteristics
- Special features or limitations

### Step 14: Update Configuration
- [ ] Add your collection name to README
- [ ] Document chunk size/overlap choices
- [ ] List required environment variables
- [ ] Document fallback behavior

### Step 15: Deployment Checklist
- [ ] Ensure ChromaDB server runs on port 9500
- [ ] Verify `.env` configuration in deployment
- [ ] Test retrieval in staging before production
- [ ] Monitor retrieval latency in production
- [ ] Set up logging for failed queries

---

## Phase 6: Maintenance & Monitoring

### Step 16: Ongoing Maintenance
- [ ] Monitor collection size growth
- [ ] Periodically verify retrieval quality
- [ ] Update collections when source data changes
- [ ] Clean up old/unused collections

**Regular checks:**
```bash
# Monthly: Verify collection health
uv run python connect.py

# Quarterly: Run full verification
uv run python examples.py

# As needed: Re-ingest updated content
uv run python ingest.py --folder /my/data --collection myproject_agents
```

### Step 17: Performance Monitoring
- [ ] Track average query response time
- [ ] Monitor server connection health
- [ ] Check for error patterns in logs
- [ ] Adjust chunk size/overlap if needed

### Step 18: Feedback & Iteration
- [ ] Collect user feedback on result quality
- [ ] Note queries that don't return good results
- [ ] Adjust distance_threshold based on feedback
- [ ] Consider metadata filtering improvements

---

## Quick Reference: File Checklist

By end of Phase 3, your project should have:

- [ ] `.env` file with CHROMA_HOST and CHROMA_PORT
- [ ] `src/retrievers/myproject_retriever.py` - Custom retriever
- [ ] Tests for retriever functionality
- [ ] Integration points in your main tool
- [ ] Error handling for retrieval failures
- [ ] `RETRIEVAL.md` documentation

---

## Troubleshooting Checklist

| Problem | Solution |
|---------|----------|
| Connection refused | Verify ChromaDB server: `uv run chroma run --port 9500` |
| Collection not found | List available: `uv run python connect.py` |
| No results returned | Try different query or lower distance_threshold |
| Slow queries | Reduce n_results or use metadata filtering |
| Ingestion failed | Check file encoding is UTF-8 |
| Memory errors | Reduce batch_size in ingest.py |

---

## Example: Complete Integration (Backend Architect Tool)

**Scenario:** Adding agent retrieval to a backend architecture tool

### Files created:
1. `src/retrievers/architecture_retriever.py` - Agent lookup
2. `tests/test_architecture_retriever.py` - Unit tests
3. `ARCHITECTURE_RETRIEVAL.md` - Documentation

### Usage:
```python
from src.retrievers.architecture_retriever import ArchitectureRetriever

# Get relevant agent definitions for context
retriever = ArchitectureRetriever()
context = retriever.get_architecture_patterns(domain="microservices")

# Inject into system prompt
system_prompt = f"""You are a backend architect.
Reference these patterns:
{context}

Design the system..."""
```

### Collections used:
- `vibe_agents` - Agent definitions
- `ghc_agents` - GitHub Copilot specific patterns

---

## Success Criteria

Your integration is successful when:

✅ ChromaDB server runs reliably on port 9500
✅ Collections created and verified
✅ Retriever module works with your tool
✅ Tests pass with good relevance scores
✅ Error handling prevents tool failures
✅ Documentation is complete
✅ End-to-end integration tested
✅ Performance meets requirements

---

## Support & Resources

- **Integration Guide**: See `INTEGRATION.md`
- **Best Practices**: See `BEST_PRACTICES.md`
- **Code Examples**: See `agent_query.py`
- **Connection Test**: Run `python connect.py`
- **Verification**: Run `python examples.py`

---

**Next Steps:** After completing this checklist, your tool is ready to leverage ChromaDB for intelligent context retrieval!
