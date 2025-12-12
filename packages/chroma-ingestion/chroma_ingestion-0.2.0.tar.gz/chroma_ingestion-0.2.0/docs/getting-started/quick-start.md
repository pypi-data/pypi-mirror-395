# Quick Start

Get up and running with chroma-ingestion in 5 minutes.

## Installation

```bash
pip install chroma-ingestion
```

## Basic Usage

### 1. Ingest Your Code

```bash
chroma-ingest /path/to/your/code --collection my_collection
```

That's it! Your code is now indexed in Chroma.

### 2. Search Your Code

```bash
chroma-ingest search "how do we handle errors?" --collection my_collection
```

Result:
```
1. src/errors.py (distance: 0.25)
   class ErrorHandler:
       def handle(self, error: Exception) -> None:
           ...
```

### 3. Use in Python

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")
results = retriever.query("authentication flow", n_results=3)

for result in results:
    print(f"📄 {result['metadata']['filename']}")
    print(f"📍 Match quality: {result['distance']:.2f}")
    print(result['document'])
    print()
```

## Advanced: Python API

### Ingestion with Custom Configuration

```python
from chroma_ingestion import CodeIngester

ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="my_collection",
    chunk_size=1500,        # Larger chunks for more context
    chunk_overlap=300,      # More overlap for detailed code
    file_patterns=["**/*.py", "**/*.md"]  # Custom file types
)

files, chunks = ingester.ingest_files()
print(f"✅ Processed {files} files, created {chunks} chunks")
```

### Retrieval with Metadata Filtering

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")

# Search with metadata filtering
results = retriever.query_by_metadata(
    where={"file_type": ".py"},  # Only Python files
    n_results=5
)

# Get all chunks from specific file
file_chunks = retriever.get_by_source("auth.py")
```

## Common Tasks

### Task: Index Multiple Folders

```bash
# Index main source code
chroma-ingest ./src --collection main_source

# Index tests separately
chroma-ingest ./tests --collection test_source

# Search across both
chroma-ingest search "test utilities" --collection test_source
```

### Task: Tune Chunk Size

For detailed code contexts (functions, classes):
```bash
chroma-ingest ./code --chunk-size 2000 --chunk-overlap 400
```

For focused, small chunks:
```bash
chroma-ingest ./code --chunk-size 500 --chunk-overlap 100
```

### Task: Verify Ingestion Quality

```bash
chroma-ingest search "main class" --collection my_collection -n 10
```

Look for:
- ✅ Results are relevant (distance < 0.5)
- ✅ Multiple results found
- ✅ Metadata looks correct

## Next Steps

- 📖 [Full Installation Guide](installation.md) - Detailed setup
- 🔧 [Configuration](configuration.md) - Environment variables
- 📚 [User Guides](../guides/basic-usage.md) - Learn more
- 🔍 [API Reference](../api/overview.md) - Full API docs
