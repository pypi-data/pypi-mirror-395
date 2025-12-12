# Basic Usage

Learn the fundamentals of chroma-ingestion.

## Command-Line Interface

### Ingesting Code

```bash
# Ingest code into a collection
chroma-ingest /path/to/code --collection my_collection
```

**Options:**
- `--collection` (optional) - Collection name (default: agents_context)
- `--chunk-size` (optional) - Tokens per chunk (default: 1000)
- `--chunk-overlap` (optional) - Token overlap (default: 200)

### Searching Code

```bash
# Search for relevant code
chroma-ingest search "how do we handle errors?" --collection my_collection
```

**Options:**
- `-n, --num-results` (optional) - Number of results to show (default: 5)
- `--collection` (optional) - Collection to search in (default: agents_context)

### Managing Collections

```bash
# List all collections
chroma-ingest list-collections

# Reset client connection (if configuration changed)
chroma-ingest reset-client
```

## Python API

### Import

```python
from chroma_ingestion import (
    CodeIngester,          # Ingest code files
    CodeRetriever,         # Search ingested code
    get_chroma_client,     # Access the Chroma client
)
```

### Basic Ingestion

```python
from chroma_ingestion import CodeIngester

# Create ingester
ingester = CodeIngester(
    target_folder="/path/to/code",
    collection_name="my_collection"
)

# Ingest files
files_processed, chunks_created = ingester.ingest_files()

print(f"✅ Processed {files_processed} files")
print(f"✅ Created {chunks_created} chunks")
```

### Basic Retrieval

```python
from chroma_ingestion import CodeRetriever

# Create retriever
retriever = CodeRetriever("my_collection")

# Search for relevant code
results = retriever.query(
    query_text="How do we handle authentication?",
    n_results=3
)

# Display results
for i, result in enumerate(results, 1):
    print(f"\n{i}. {result['metadata']['filename']}")
    print(f"   Relevance: {result['distance']:.3f}")
    print(f"   Preview: {result['document'][:200]}...")
```

## Understanding Results

Each search result contains:

```python
result = {
    'document': '...',  # The code chunk text
    'distance': 0.25,   # Relevance score (0=perfect, 2=poor)
    'metadata': {       # Source information
        'filename': 'auth.py',
        'source': '/path/to/code/auth.py',
        'chunk_index': 5,
        'folder': '/path/to/code',
        'file_type': '.py'
    }
}
```

**Distance Interpretation:**
- 0.0 - 0.3: Excellent match ⭐⭐⭐
- 0.3 - 0.5: Good match ⭐⭐
- 0.5 - 0.7: Acceptable match ⭐
- 0.7+: Poor match ❌

## Complete Example

```python
from chroma_ingestion import CodeIngester, CodeRetriever

# Step 1: Ingest code
print("📥 Ingesting code...")
ingester = CodeIngester(
    target_folder="./src",
    collection_name="my_project"
)
files, chunks = ingester.ingest_files()
print(f"✅ Ingested {files} files, {chunks} chunks")

# Step 2: Search ingested code
print("\n🔍 Searching code...")
retriever = CodeRetriever("my_project")

queries = [
    "how do we validate user input?",
    "what's the database schema?",
    "error handling patterns"
]

for query in queries:
    print(f"\nQuery: {query}")
    results = retriever.query(query, n_results=2)

    for result in results:
        filename = result['metadata']['filename']
        distance = result['distance']
        print(f"  • {filename} (relevance: {distance:.2f})")
```

## Common Workflows

### Workflow: Index and Search Organization Codebase

```python
from chroma_ingestion import CodeIngester, CodeRetriever

# Index main source code
ingester = CodeIngester("./src", collection_name="source_code")
ingester.ingest_files()

# Index tests separately
ingester = CodeIngester("./tests", collection_name="tests")
ingester.ingest_files()

# Search source code
retriever = CodeRetriever("source_code")
backend_handlers = retriever.query("request handlers", n_results=5)

# Search tests for patterns
test_retriever = CodeRetriever("tests")
auth_tests = test_retriever.query("authentication tests", n_results=5)
```

### Workflow: Find Similar Code

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")

# Find similar functions
similar = retriever.query(
    "def process_data(items):",
    n_results=10
)

print("Similar implementations:")
for result in similar:
    print(f"  • {result['metadata']['filename']}")
    print(f"    {result['document'][:100]}...")
```

## Next Steps

- 📖 [Ingestion Workflow](ingestion-workflow.md) - Detailed ingestion guide
- 🔍 [Retrieval Patterns](retrieval-patterns.md) - Advanced search
- 🔧 [Chunking Strategy](chunking-strategy.md) - Optimize chunk size
- 🔗 [Advanced Filtering](advanced-filtering.md) - Metadata filtering
