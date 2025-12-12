# Chroma Code Ingestion System

[![PyPI version](https://img.shields.io/pypi/v/chroma-ingestion?color=blue)](https://pypi.org/project/chroma-ingestion/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/chroma-core/chroma-ingestion/workflows/CI/badge.svg)](https://github.com/chroma-core/chroma-ingestion/actions)

Intelligently extract, chunk, and store code/documents in Chroma Cloud using semantic-aware text splitting. This system is designed to prepare code repositories for AI agent retrieval and context generation.

**📚 [Full Documentation](https://github.com/chroma-core/chroma-ingestion/wiki)** | **🚀 [Quick Start](#quick-start)** | **📖 [API Reference](#api-reference)** | **🤝 [Contributing](CONTRIBUTING.md)**

## Features

✅ **Code-Aware Splitting**: Uses RecursiveCharacterTextSplitter to preserve semantic structure (classes, functions, sections)
✅ **Multi-Format Support**: Python files, Markdown, Agent definitions, Prompts
✅ **Batch Processing**: Efficiently handles large codebases with intelligent batching
✅ **Metadata Tracking**: Maintains source file info, chunk indices, and file types
✅ **Chroma Cloud Integration**: Directly stores chunks in Chroma Cloud for semantic search
✅ **Verification Tools**: Built-in query testing and data quality validation

## Quick Start

### Installation

Install from PyPI:

```bash
pip install chroma-ingestion
```

Or install from source with development dependencies:

```bash
git clone https://github.com/chroma-core/chroma-ingestion.git
cd chroma-ingestion
pip install -e ".[dev]"
```

### Basic Usage

#### Command-Line Interface

```bash
# Ingest code files into ChromaDB
chroma-ingest /path/to/code --collection my_collection

# Search ingested code
chroma-ingest search "authentication patterns" --collection my_collection

# List available collections
chroma-ingest list-collections
```

#### Python API

```python
from chroma_ingestion import CodeIngester, CodeRetriever

# Ingest code files
ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="my_collection"
)
ingester.ingest_files()

# Query ingested code
retriever = CodeRetriever("my_collection")
results = retriever.query("How do we handle errors?", n_results=3)

for result in results:
    print(f"Source: {result['metadata']['filename']}")
    print(f"Content: {result['document']}")
```

## Project Structure

```
chroma/
├── src/
│   └── chroma_ingestion/
│       ├── __init__.py         # Public API exports
│       ├── cli.py              # Command-line interface
│       ├── config.py           # Configuration management
│       ├── ingestion/          # Ingestion module
│       ├── retrieval/          # Retrieval module
│       └── clients/            # Client management
├── tests/                      # Comprehensive test suite
├── examples/                   # Example scripts
├── docs/                       # Documentation
├── pyproject.toml             # Project configuration
├── CHANGELOG.md               # Release notes
└── README.md                  # This file
```

## Installation & Configuration

### From PyPI

```bash
pip install chroma-ingestion
```

### From Source

```bash
git clone https://github.com/chroma-core/chroma-ingestion.git
cd chroma-ingestion
pip install -e ".[dev]"
```

### Dependencies

All dependencies are automatically installed:
- `chromadb>=1.3.5` - Vector database
- `langchain-text-splitters>=1.0.0` - Semantic text splitting
- `python-dotenv>=1.0.0` - Environment variable management
- `pyyaml>=6.0` - Configuration
- `click>=8.0` - CLI framework

### Configuration

For Chroma Cloud:

```bash
export CHROMA_HOST=api.chroma.com
export CHROMA_PORT=443
# Or set credentials in .env file
```

For local development:

```bash
# No configuration needed - uses localhost:9500 by default
chroma run
```

## Configuration

## Usage

### Command-Line Interface (New!)

```bash
# Ingest code files
chroma-ingest /path/to/code --collection my_collection

# Ingest with custom chunk size
chroma-ingest /path/to/code --collection my_collection --chunk-size 1500

# Search ingested code
chroma-ingest search "authentication patterns" -n 5 --collection my_collection

# List available collections
chroma-ingest list-collections

# Reset client connection
chroma-ingest reset-client
```

### Python API

#### Basic Ingestion

```python
from chroma_ingestion import CodeIngester

ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="my_collection",
    chunk_size=1000,
    chunk_overlap=200
)

files_processed, chunks_ingested = ingester.ingest_files()
print(f"Processed {files_processed} files, created {chunks_ingested} chunks")
```

#### Searching Ingested Code

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")

# Semantic search
results = retriever.query("How do we handle errors?", n_results=3)

for result in results:
    print(f"File: {result['metadata']['filename']}")
    print(f"Relevance: {result['distance']:.3f}")
    print(f"Content: {result['document'][:200]}...")
```

### Basic Ingestion (Deprecated - Use CLI Instead)

The old `python ingest.py` approach is deprecated. Use the new CLI:

```bash
chroma-ingest /path/to/your/folder --collection my_collection
```

#### Custom Folder

Ingest a different folder:

```bash
chroma-ingest /path/to/your/folder --collection my_collection
```

#### With Verification

Run ingestion and automatically verify data quality:

```bash
chroma-ingest /path/to/your/folder --verify
```

#### Advanced Options

```bash
chroma-ingest /path/to/code \
  --collection agents_context \
  --chunk-size 1500 \
  --chunk-overlap 300
```

**Options:**
- `--collection`: Chroma collection name (default: agents_context)
- `--chunk-size`: Tokens per chunk (default: 1000)
- `--chunk-overlap`: Token overlap between chunks (default: 200)

## Ingestion Workflow

### Step 1: File Discovery
Scans target folder recursively for matching files:
- `*.py` (Python files)
- `*.md` (Markdown)
- `*.agent.md` (Agent definitions)
- `*.prompt.md` (Prompt templates)

### Step 2: Semantic Chunking
Uses RecursiveCharacterTextSplitter to create chunks:
- Preserves semantic structure (sections, code blocks, definitions)
- Maintains configurable overlap for context preservation
- Intelligent splitting at logical boundaries

### Step 3: Metadata Enhancement
Each chunk stores:
- `source` - Full file path
- `filename` - Base filename
- `chunk_index` - Position in file
- `folder` - Parent directory
- `file_type` - Extension (.py, .md, .agent.md, etc.)

### Step 4: Batch Upload
Uploads to Chroma Cloud in batches:
- Default batch size: 100 chunks
- Prevents memory limits
- Shows progress for large ingestions

## Example: Query Ingested Data

After ingestion, query the data:

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("agents_context")

# Search for error handling patterns
results = retriever.query("How do agents handle errors?", n_results=3)

for result in results:
    print(f"Source: {result['metadata']['filename']}")
    print(f"Distance: {result['distance']:.4f}")
    print(f"Preview: {result['document'][:200]}...")
    print()
```

## Data Quality Verification

The system includes built-in verification:

```bash
python ingest.py --verify
```

This runs test queries to ensure:
- ✅ Chunks are properly stored in Chroma
- ✅ Semantic search retrieves relevant results
- ✅ Metadata is correctly preserved
- ✅ Distance scores indicate relevance (< 0.8 excellent, 0.8-1.2 acceptable)

**Example verification output:**
```
Collection: agents_context
Total chunks: 311

Query 1: How do agents handle errors and exceptions?
  Result 1: adr-generator.agent.md (distance: 0.95) ✅ Good
  Result 2: WinFormsExpert.agent.md (distance: 1.08) ✅ Okay

Query 2: What are the main classes and functions?
  Result 1: security-engineer.prompt.md (distance: 1.15) ✅ Okay
  ...
```

## Advanced Usage

### Custom File Patterns

Ingest specific file types:

```python
from src.ingestion import CodeIngester

# Only Python files
ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="python_only",
    file_patterns=["**/*.py"]
)

# Agent definitions only
ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="agents_only",
    file_patterns=["**/*.agent.md"]
)
```

### Chunking Strategy Tuning

Adjust chunk size based on your use case:

```bash
# Large, detailed chunks (fewer, longer contexts)
python ingest.py --chunk-size 2000 --chunk-overlap 400

# Small, focused chunks (more granular retrieval)
python ingest.py --chunk-size 500 --chunk-overlap 100
```

**Guidelines:**
- **chunk_size**: ~250 tokens = brief context, ~1000 = full function, ~2000+ = multi-function
- **chunk_overlap**: 10-20% of chunk_size prevents cutting logic mid-statement

### Filter by Source

Retrieve chunks from specific files:

```python
from src.retrieval import CodeRetriever

retriever = CodeRetriever("agents_context")

# Get all chunks from one agent
backend_chunks = retriever.get_by_source("backend-architect.prompt.md")

for chunk in backend_chunks:
    print(chunk["document"])
```

## Performance Characteristics

### Ingestion Performance

For the default vibe-tools/ghc_tools/agents folder (23 files, 311 chunks):
- **Time**: ~3-5 seconds
- **Throughput**: ~100 chunks per batch
- **Storage**: ~1-2MB in Chroma Cloud (after embedding)

### Query Performance

Semantic search in Chroma Cloud:
- **Latency**: ~200-500ms per query (actual: ~78ms in testing)
- **Accuracy**: Improves with detailed queries
- **Distance Threshold**: 0-2.0 range, calibrated expectations:
  - < 0.8: Excellent match
  - 0.8-1.0: Good match
  - 1.0-1.2: Acceptable match
  - > 1.2: Poor match

## Troubleshooting

### No files found
```
❌ No matching files found in: /path/to/folder
```
**Solution**: Check folder path and file patterns. Verify files exist:
```bash
ls /path/to/folder/**/*.md
```

### Chroma Cloud authentication error
```
❌ Could not authenticate with Chroma Cloud
```
**Solution**: Verify credentials in `.env`:
```bash
grep CHROMA .env
```

### Memory errors during large ingestions
**Solution**: Reduce batch size or chunk size:
```bash
python ingest.py --chunk-size 500
```

### Poor retrieval quality
**Solution**:
1. Check distance scores (< 0.8 excellent, < 1.0 good, < 1.2 acceptable, > 1.2 poor)
2. Adjust chunk size (too small loses context, too large loses precision)
3. Use more specific queries (simplify multi-concept queries)

## Next Steps

1. **Monitor collection health** with automated validation:
   ```bash
   python validate_thresholds.py --report
   ```

2. **Ingest your own codebase**:
   ```bash
   python ingest.py --folder /path/to/your/code --collection my_codebase
   ```

3. **Build retrieval pipelines** using CodeRetriever for AI agents

4. **Integrate with LLM applications** for code-aware context generation

5. **Set up CI/CD health checks** to catch threshold drift early

## Monitoring & Maintenance

### Threshold Validation

Automatically validate that distance thresholds remain calibrated:

```bash
# Basic validation
python validate_thresholds.py

# With markdown report
python validate_thresholds.py --report

# Strict mode (fail on drift)
python validate_thresholds.py --strict
```

**What it checks:**
- Frontend queries return frontend agents (distance 1.0-1.3)
- DevOps queries return devops/quality agents (distance 1.0-1.3)
- Backend queries return backend agents (distance 0.7-0.9)
- Security queries return security agents (distance 0.9-1.2)

**Output:**
- JSON results: `threshold_validation_results.json`
- Markdown report: `validation_report.md` (with --report flag)
- Exit codes: 0 = all pass, 1 = drift detected, 2 = tests failed

### CI/CD Integration

Add threshold validation to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Validate Collection Thresholds
  run: |
    cd chroma
    python validate_thresholds.py --strict
    if [ $? -eq 1 ]; then
      echo "⚠️ Threshold drift detected"
      exit 1
    fi
```

### When to Re-validate

**Weekly:** Run validation to ensure stability
```bash
python validate_thresholds.py --report
```

**After changes:**
- Updating ingestion configuration
- Adding new agents to collection
- Changing chunking strategy
- Upgrading Chroma or embedding models

**Signs of drift to watch for:**
- Distances consistently 20-30% higher/lower than expected
- Different agents appearing for familiar queries
- Distance ranges spreading wider than expected

## Architecture Decision: CloudClient vs PersistentClient

This project uses **Chroma CloudClient** because:
- ✅ Persistent storage (data survives restarts)
- ✅ Remote backup and redundancy
- ✅ Multi-user access and sharing
- ✅ Easy scaling as codebase grows
- ✅ API-compatible with local Chroma

For local development, you can switch to PersistentClient:
```python
# In src/clients/chroma_client.py
_client = chromadb.PersistentClient(path="./chroma_db")
```

## References

- [Chroma Documentation](https://docs.trychroma.com/)
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_loaders/splitting/)
- [Semantic Search Best Practices](https://www.pinecone.io/learn/semantic-search/)
