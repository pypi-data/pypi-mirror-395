# Retrieval Patterns

Common patterns and best practices for querying ingested code.

## Basic Retrieval

### Simple Semantic Search

```python
from chroma_ingestion import CodeRetriever

retriever = CodeRetriever("my_collection")

# Basic query
results = retriever.query(
    "authentication flow",
    n_results=5
)

for result in results:
    print(f"File: {result['metadata']['filename']}")
    print(f"Distance: {result['distance']}")
    print(f"Content: {result['document'][:200]}...")
```

### Understanding Distance Scores

Lower distance = better match

| Distance | Quality | Use |
|----------|---------|-----|
| 0.0-0.3 | Excellent ⭐⭐⭐ | Trust the result |
| 0.3-0.5 | Good ⭐⭐ | Probably relevant |
| 0.5-0.7 | Weak ⭐ | May be false positive |
| 0.7+ | Poor ❌ | Ignore or refine query |

## Advanced Patterns

### Filtering by File Type

```python
retriever = CodeRetriever("my_collection")

# Get only Python files
python_chunks = retriever.query_by_metadata(
    query_text="error handling",
    where={"file_type": ".py"},
    n_results=10
)
```

### Filtering by Folder

```python
# Get chunks from specific folder
auth_chunks = retriever.query_by_metadata(
    query_text="token validation",
    where={"folder": "/path/to/auth"},
    n_results=5
)
```

### Filtering by Source File

```python
# Get all chunks from a specific file
file_chunks = retriever.get_by_source("authentication.py")

# Get chunks from multiple files
files = ["auth.py", "users.py"]
multi_file_chunks = retriever.query_by_metadata(
    where={"filename": {"$in": files}},
    n_results=20
)
```

### High-Confidence Results

```python
# Only get very relevant matches
results = retriever.query_semantic(
    query_text="JWT token handling",
    n_results=10,
    distance_threshold=0.3  # Only < 0.3 distance
)

# Useful for strict requirements
if not results:
    print("No high-confidence matches found")
else:
    print(f"Found {len(results)} highly relevant chunks")
```

## Query Optimization

### Specific Queries

❌ **Too broad:**
```python
results = retriever.query("code")  # 90% of chunks match
```

✅ **Specific:**
```python
results = retriever.query("JWT token validation in FastAPI")
```

### Domain-Specific Language

Use your domain's terminology:

```python
# Data science context
retriever.query("scikit-learn pipeline cross-validation")

# Web context
retriever.query("React useEffect cleanup function")

# DevOps context
retriever.query("Kubernetes pod initialization probes")
```

### Multi-Part Queries

```python
# Complex query
results = retriever.query(
    "How do we handle async operations with error recovery "
    "and logging in the authentication module?"
)

# Often returns better results than simple keywords
```

## Collection Management

### Get Collection Info

```python
info = retriever.get_collection_info()

print(f"Total chunks: {info['count']}")
print(f"Collection name: {info['name']}")
print(f"Metadata: {info.get('metadata', {})}")
```

### List All Collections

```python
from chroma_ingestion import list_collections

collections = list_collections()

for coll in collections:
    print(f"- {coll['name']} ({coll['count']} chunks)")
```

### Delete Collection

```python
from chroma_ingestion import delete_collection

delete_collection("old_collection")
```

## Real-World Examples

### Example 1: Finding Error Handling Patterns

```python
retriever = CodeRetriever("backend_code")

# Query for error handling
error_patterns = retriever.query(
    "error handling and exception catching",
    n_results=5
)

print("Error handling patterns:")
for result in error_patterns:
    if result['distance'] < 0.4:  # Only good matches
        print(f"\n{result['metadata']['filename']}:")
        print(result['document'][:300])
```

### Example 2: Finding API Endpoints

```python
retriever = CodeRetriever("fastapi_code")

# Find all endpoint definitions
endpoints = retriever.query(
    "FastAPI route decorator GET POST endpoint",
    n_results=15
)

# Filter by file
api_routes = [
    r for r in endpoints
    if r['metadata']['file_type'] == '.py'
    and '/api/' in r['metadata']['folder']
]

print(f"Found {len(api_routes)} API endpoint chunks")
```

### Example 3: Finding Configuration Examples

```python
retriever = CodeRetriever("configs")

# Find configuration patterns
configs = retriever.query(
    "environment variable configuration setup",
    n_results=5,
    distance_threshold=0.4
)

if configs:
    for config in configs:
        print(f"Config in {config['metadata']['filename']}:")
        print(config['document'])
```

### Example 4: Cross-File Pattern Analysis

```python
retriever = CodeRetriever("project_code")

# Find where database connections are used
db_usage = retriever.query(
    "database connection string cursor query execute",
    n_results=10
)

# Group by file
by_file = {}
for result in db_usage:
    filename = result['metadata']['filename']
    if filename not in by_file:
        by_file[filename] = []
    by_file[filename].append(result)

print(f"Database usage in {len(by_file)} files:")
for filename, chunks in by_file.items():
    print(f"  - {filename} ({len(chunks)} references)")
```

## Performance Tips

### Batch Queries

```python
# Instead of many individual queries
queries = [
    "authentication",
    "authorization",
    "token validation",
    "user management"
]

results_map = {}
for query in queries:
    results_map[query] = retriever.query(query, n_results=3)
    print(f"✓ Processed '{query}'")
```

### Caching Results

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_auth_patterns():
    retriever = CodeRetriever("my_collection")
    return retriever.query("authentication patterns", n_results=5)

# Second call uses cached result
patterns = get_auth_patterns()
```

### Batch Metadata Filtering

```python
# Efficient filtering
file_types = [".py", ".ts"]
results = retriever.query_by_metadata(
    query_text="imports and dependencies",
    where={"file_type": {"$in": file_types}},
    n_results=20
)
```

## Common Use Cases

### Finding Import Patterns

```python
retriever.query(
    "module imports dependencies from package",
    n_results=10
)
```

### Finding Test Examples

```python
retriever.query(
    "unit test fixture pytest assert",
    n_results=5
)
```

### Finding Documentation

```python
retriever.query(
    "docstring documentation parameter returns",
    n_results=5
)
```

### Finding Security-Related Code

```python
retriever.query(
    "authentication authorization security token validation",
    n_results=10
)
```

## Troubleshooting

### "No relevant results"

```python
# Try broader query
results = retriever.query("authentication")  # vs "JWT RS256 symmetric"

# Or increase results
results = retriever.query(query, n_results=20)  # vs 5

# Or lower threshold
results = retriever.query_semantic(query, distance_threshold=0.6)
```

### "Too many irrelevant results"

```python
# Make query more specific
results = retriever.query("FastAPI dependency injection Depends")

# Or increase threshold
results = retriever.query_semantic(query, distance_threshold=0.2)

# Or filter by metadata
results = retriever.query_by_metadata(
    query,
    where={"file_type": ".py"},
    n_results=5
)
```

### "Collection empty"

```python
info = retriever.get_collection_info()
print(f"Collection has {info['count']} chunks")

if info['count'] == 0:
    print("Run ingestion first: CodeIngester(...).ingest_files()")
```

## Next Steps

- 📝 [Basic Usage](basic-usage.md) - Get started with code examples
- 🔧 [Chunking Strategy](chunking-strategy.md) - Understand how chunks are created
- 🎯 [Advanced Filtering](advanced-filtering.md) - Deep dive into filtering
