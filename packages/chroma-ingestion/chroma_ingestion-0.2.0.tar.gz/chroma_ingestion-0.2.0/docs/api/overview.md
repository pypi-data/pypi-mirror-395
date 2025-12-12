# API Reference

Complete reference for chroma-ingestion public APIs.

## Module Overview

```python
from chroma_ingestion import (
    CodeIngester,              # Main ingestion class
    AgentIngester,             # Specialized for AI agents
    CodeRetriever,             # Search and retrieval
    MultiCollectionSearcher,   # Cross-collection search
    get_chroma_client,         # Access singleton client
)
```

## CodeIngester

**Purpose:** Recursively discover files, chunk them semantically, and upload to Chroma.

### Usage

```python
from chroma_ingestion import CodeIngester

ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="my_collection",
    chunk_size=1000,           # Tokens per chunk
    chunk_overlap=200,         # Token overlap
    file_patterns=["**/*.py", "**/*.md"]  # File types to ingest
)

files, chunks = ingester.ingest_files(batch_size=100)
```

### Methods

- `discover_files()` - Find all matching files recursively
- `ingest_files(batch_size=100)` - Process and upload to Chroma
- `get_collection_stats()` - View collection metadata

## CodeRetriever

**Purpose:** Query and retrieve chunks from ingested code.

### Usage

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")

# Semantic search
results = retriever.query("authentication patterns", n_results=5)

# Get chunks from specific file
chunks = retriever.get_by_source("auth.py")

# Collection info
info = retriever.get_collection_info()
```

### Methods

- `query(query_text, n_results=3)` - Semantic search
- `get_by_source(filename)` - Get all chunks from file
- `get_collection_info()` - View collection statistics

## MultiCollectionSearcher

**Purpose:** Search across multiple collections simultaneously.

### Usage

```python
from chroma_ingestion import MultiCollectionSearcher

searcher = MultiCollectionSearcher(
    collection_names=["backend", "frontend", "utils"]
)

results = searcher.search("error handling", n_results=3)
```

### Methods

- `search(query_text, n_results=3)` - Search all collections
- `search_with_context(query_text, n_results=3)` - Include collection context

## AgentIngester

**Purpose:** Specialized for ingesting AI agent definitions and prompt templates.

### Usage

```python
from chroma_ingestion import AgentIngester

ingester = AgentIngester(
    target_folder="/path/to/agents",
    collection_name="agents"
)

files, chunks = ingester.ingest_files()
```

Inherits from `CodeIngester` with optimized defaults for agent files.

## get_chroma_client()

**Purpose:** Access the singleton Chroma client.

### Usage

```python
from chroma_ingestion import get_chroma_client

client = get_chroma_client()

# Use client directly
collection = client.get_collection("my_collection")
```

## Result Format

All retrieval methods return results in this format:

```python
result = {
    'document': str,          # Code chunk text
    'distance': float,        # Relevance score (0=perfect, 2=poor)
    'metadata': {             # Source information
        'filename': str,      # Base filename
        'source': str,        # Full path
        'chunk_index': int,   # Position in file
        'folder': str,        # Parent directory
        'file_type': str      # File extension (.py, .md, etc)
    }
}
```

## Configuration

See [Configuration Guide](../getting-started/configuration.md) for environment variable setup.

## Next Steps

- 📖 [Basic Usage](../guides/basic-usage.md) - Learn by example
- 🔍 [Retrieval Patterns](../guides/retrieval-patterns.md) - Advanced search
- ⚙️ [Configuration](../getting-started/configuration.md) - Setup
