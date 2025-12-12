# Chroma Code Ingestion System - Architecture & Patterns

## Project Purpose
Semantic-aware code extraction and storage system that chunks repositories and stores them in Chroma Cloud for AI agent retrieval and context generation. Built on LangChain RecursiveCharacterTextSplitter and Chroma vector database.

## Core Components

### Singleton Client Pattern (CRITICAL)
- **Location:** `src/clients/chroma_client.py`
- **Pattern:** Global `_client` variable with `get_chroma_client()` function
- **Reason:** Prevents connection pool exhaustion, maintains single connection across app
- **Usage:** Always import and use `get_chroma_client()`, never create new HttpClient instances

### Semantic Chunking Strategy
- **Location:** `src/ingestion.py` lines 68-71
- **Tool:** `RecursiveCharacterTextSplitter.from_language(Language.MARKDOWN, chunk_size=1000, chunk_overlap=200)`
- **Why Markdown:** Respects document structure (headers, sections, code blocks) - more general than language-specific splitters
- **Optimal Range:** 1000-1500 tokens for balanced precision/recall

### Batch Upsert Pattern
- **Location:** `src/ingestion.py` (ingest_files method)
- **Pattern:** Process in batches of 100-500 chunks to avoid memory/timeout errors
- **Key Benefit:** Chroma's `upsert()` handles duplicates automatically (safe for reingestion)
- **Failure Mode:** Single large upsert can timeout; reduce batch_size to 50 if issues occur

### Rich Metadata Tracking
- **Fields:** source (filepath), filename, chunk_index, folder, file_type
- **Purpose:** Source attribution, filtering, debugging
- **Enables:** Metadata-based queries via `query_by_metadata(where={"file_type": ".md"})`

## File Roles
- `src/config.py` - Environment loading with sensible defaults (localhost:9500)
- `src/ingestion.py` - CodeIngester class: discovery, splitting, batch upsert
- `src/retrieval.py` - CodeRetriever class: semantic search, metadata filtering, distance thresholds
- `ingest.py` - CLI entry point with argparse
- `examples.py` - Reference patterns and test queries
- `BEST_PRACTICES.md` - Lessons from Cloud→HttpClient migration

## Developer Workflows

### Ingestion
```bash
python ingest.py [--folder PATH] [--collection NAME] [--chunk-size 1000] [--chunk-overlap 200] [--batch-size 100] [--verify]
```
Default folder: `vibe-tools/ghc_tools/agents`

### Retrieval
Three query methods in CodeRetriever:
1. `query(text, n_results)` - Basic semantic search
2. `query_semantic(text, n_results, distance_threshold)` - Filter weak matches
3. `query_by_metadata(where, where_document, n_results)` - Metadata filtering

**Relevance Scale:**
- 0.0-0.3: Excellent (⭐⭐⭐)
- 0.3-0.5: Good (⭐⭐)
- 0.5-0.7: Weak (⭐)
- 0.7+: Poor (❌)

## Common Patterns & Gotchas

### Pattern: Adding New File Type
1. Update `file_patterns` list in CodeIngester.__init__
2. Choose splitter: MARKDOWN for structure-aware, language-specific for details
3. Test with `ingest.py --verify`

### Pattern: Debug Ingestion Quality
Use examples.py pattern - test with domain-specific queries post-ingestion, verify distance < 0.5

### Gotcha: "Expected IDs to be unique"
- Cause: Running ingestion twice on same collection without upsert
- Fix: Already fixed - code uses upsert() which handles duplicates

### Gotcha: Timeout/Memory on Large Repos
- Reduce batch_size from 100 to 50
- Or split ingestion by folder/collection (agents, schemas, services separately)

### Gotcha: Poor Query Relevance
- Chunk size too small/large? Adjust from 1000 (default) - typically 1000-1500 optimal
- Test with `ingest.py --verify` to see test query distances

## Configuration
- **Local Dev:** No .env needed (defaults: localhost:9500)
- **Production:** Set CHROMA_HOST, CHROMA_PORT, or Chroma Cloud credentials
- **Testing:** Use reset_client() in chroma_client.py

## Performance Baselines
- Ingestion: ~1000-2000 tokens/sec
- Query latency: 200-500ms per query
- Storage: ~1.5GB per 1M tokens
- Supported formats: .py, .md, .agent.md, .prompt.md

## Use Cases
✅ RAG systems for agents
✅ Large codebase semantic indexing
✅ Searchable documentation
✅ Agent pattern libraries
❌ Real-time code changes
❌ Full-text search (use PostgreSQL)
❌ Graph queries (use graph DB)
