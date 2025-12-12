# Ingestion Workflow

Complete guide to the code ingestion process from start to finish.

## Overview

The ingestion workflow consists of 4 main stages:

1. **Discovery** - Recursively find matching files
2. **Chunking** - Split files semantically while preserving context
3. **Enhancement** - Add metadata for filtering and traceability
4. **Upload** - Batch upload to Chroma for semantic indexing

## Stage 1: File Discovery

### Finding Files

```python
from chroma_ingestion import CodeIngester

ingester = CodeIngester(
    target_folder="/path/to/code",
    file_patterns=["**/*.py", "**/*.md"]  # Glob patterns
)

files = ingester.discover_files()
print(f"Found {len(files)} files")
```

### Default Patterns

By default, chroma-ingestion looks for:
- `**/*.py` - Python source files
- `**/*.md` - Markdown documentation
- `**/*.agent.md` - AI agent definitions
- `**/*.prompt.md` - Prompt templates

### Custom Patterns

```python
# Only TypeScript
ingester = CodeIngester(
    target_folder="./src",
    file_patterns=["**/*.ts", "**/*.tsx"]
)

# Multiple specific types
ingester = CodeIngester(
    target_folder="./project",
    file_patterns=[
        "**/*.py",
        "**/*.js",
        "**/*.yaml",
        "README.md"
    ]
)
```

## Stage 2: Semantic Chunking

### How Chunking Works

Chunks are created using `RecursiveCharacterTextSplitter` which:

1. **Respects structure** - Splits at logical boundaries (\n\n, \n, spaces)
2. **Preserves context** - Overlaps chunks to maintain surrounding context
3. **Sizes consistently** - Creates chunks of target token size
4. **Maintains semantics** - Doesn't split in middle of code or sentences

### Chunk Configuration

```python
ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="my_collection",
    chunk_size=1000,      # Tokens per chunk
    chunk_overlap=200     # Overlap between chunks
)
```

### Chunk Size Guidelines

| Size | Use Case | Pros | Cons |
|------|----------|------|------|
| 500 | Individual functions | High precision | Loses context |
| 1000 | **Default/balanced** | Good precision & context | **Recommended** |
| 1500 | Classes/modules | More context | Less precise |
| 2000+ | Multi-entity | Full context | Too broad |

### Overlap Configuration

```python
# Tight overlap - less redundancy
chunk_size=1000, chunk_overlap=100  # 10% overlap

# Generous overlap - better context preservation
chunk_size=1000, chunk_overlap=300  # 30% overlap
```

## Stage 3: Metadata Enhancement

Each chunk includes rich metadata for filtering and traceability:

```python
metadata = {
    'source': '/full/path/to/file.py',  # Full file path
    'filename': 'file.py',              # Base filename
    'chunk_index': 5,                   # Chunk position in file
    'folder': '/full/path/to',          # Parent directory
    'file_type': '.py'                  # File extension
}
```

### Using Metadata for Filtering

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")

# Get chunks from specific file
auth_chunks = retriever.get_by_source("auth.py")

# Filter by file type
python_chunks = retriever.query_by_metadata(
    where={"file_type": ".py"},
    n_results=10
)

# Filter by folder
utils_chunks = retriever.query_by_metadata(
    where={"folder": "/path/to/utils"},
    n_results=5
)
```

## Stage 4: Batch Upload

### Upload Process

```python
ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="my_collection",
    chunk_size=1000,
    chunk_overlap=200
)

# Ingest with default batch size (100)
files, chunks = ingester.ingest_files()

# Ingest with custom batch size
files, chunks = ingester.ingest_files(batch_size=50)

print(f"Processed {files} files")
print(f"Created {chunks} chunks")
```

### Batch Size Tuning

- **Large batches (500+)** - Faster but uses more memory
- **Default (100)** - Balanced for most cases
- **Small batches (10-50)** - Slower but minimal memory

Use smaller batches if you see out-of-memory errors.

## Complete Example Workflow

```python
from chroma_ingestion import CodeIngester, CodeRetriever

# Step 1: Discover files
print("📂 Discovering files...")
ingester = CodeIngester(
    target_folder="./src",
    file_patterns=["**/*.py", "**/*.md"],
    chunk_size=1200,
    chunk_overlap=300
)

files = ingester.discover_files()
print(f"   Found {len(files)} files")

# Step 2: Chunk and upload
print("\n🔄 Ingesting code...")
files_processed, chunks_created = ingester.ingest_files(batch_size=50)
print(f"   Processed {files_processed} files")
print(f"   Created {chunks_created} chunks")

# Step 3: Verify ingestion
print("\n✅ Verifying...")
retriever = CodeRetriever("my_collection")
info = retriever.get_collection_info()
print(f"   Collection has {info['count']} chunks")

# Step 4: Test with queries
print("\n🔍 Testing retrieval...")
test_queries = [
    "How do we handle errors?",
    "What are the main classes?",
    "Authentication patterns"
]

for query in test_queries:
    results = retriever.query(query, n_results=1)
    if results:
        score = results[0]['distance']
        file = results[0]['metadata']['filename']
        print(f"   '{query}' → {file} (score: {score:.2f})")
```

## Best Practices

✅ **Do:**
- Start with default chunk_size (1000) and tune based on results
- Use generous overlap (20-30%) for code files
- Monitor distance scores to ensure quality
- Test with different chunk sizes on a sample
- Archive ingestion results for reproducibility

❌ **Don't:**
- Use very small chunks (< 300 tokens) - loses context
- Use very large chunks (> 3000 tokens) - too broad
- Ignore batch size errors - reduce batch size
- Mix different chunk sizes in same collection
- Re-ingest without clearing old chunks first

## Troubleshooting

### "Collection already has similar chunks"

```python
# Use upsert (default) to replace existing chunks
ingester.ingest_files()  # Replaces duplicates automatically
```

### "Memory error during ingestion"

```python
# Reduce batch size
ingester.ingest_files(batch_size=25)  # Was 100
```

### "Poor retrieval quality"

```python
# Try different chunk size
ingester = CodeIngester(
    target_folder="./code",
    chunk_size=800,      # Smaller
    chunk_overlap=200
)
```

## Next Steps

- 🔍 [Retrieval Patterns](retrieval-patterns.md) - Learn advanced queries
- 🔧 [Chunking Strategy](chunking-strategy.md) - Optimize chunk sizes
- 🎯 [Advanced Filtering](advanced-filtering.md) - Use metadata filtering
